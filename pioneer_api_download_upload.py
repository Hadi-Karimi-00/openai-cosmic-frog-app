
import os
import sys
import datetime as dt
import subprocess
import sys
import importlib.util
import sqlalchemy as sal
import pandas as pd
from typing import Tuple
from pathlib import Path
from tqdm import tqdm

package_name = 'optilogic'
spec = importlib.util.find_spec(package_name)
if spec is None:
    print(package_name + " is not installed")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "optilogic"])

from optilogic import pioneer

class Directories:
    
    def __init__(self, root_directory: str, database_name: str):
        
        model_directory = os.path.join(root_directory, database_name)
        input_modeler_directory = os.path.join(model_directory, 'input_modeler')
        outputs_directory = os.path.join(model_directory, 'outputs')
        special_tables_directory = os.path.join(model_directory, 'special_tables')
        
        self.model_directory = model_directory
        self.input_modeler_directory = input_modeler_directory
        self.outputs_directory = outputs_directory
        self.special_tables_directory = special_tables_directory
        
        Path(self.input_modeler_directory).mkdir(parents=True, exist_ok=True)
        Path(self.outputs_directory).mkdir(parents=True, exist_ok=True)
        Path(self.special_tables_directory).mkdir(parents=True, exist_ok=True)


def ignore_this_file(file_name: str) -> bool:
    ignore_files = ['.ci.sh', '.git']
    return file_name in ignore_files \
           or file_name.endswith('.tsv')


def download_files_in_directory(from_directory: str, to_directory: str, ob: pioneer.Api, user_workspace_selection: str) -> None:
    for i in range(len(ob.wksp_files(user_workspace_selection, filter=from_directory)["files"])):
        file_path = ob.wksp_files(user_workspace_selection,
                                  filter=from_directory)["files"][i]["filePath"]

        file_name = file_path.split("/")[-1]
        path_len = len(file_path) - len(file_name) - 1
        path_name = file_path[1:path_len]

        if path_name != from_directory and len(path_name) > len(from_directory):
            new_from_dir = from_directory + "/" + path_name.split("/")[-1]
            new_to_dir = to_directory + "\\" + path_name.split("/")[-1]
            if not os.path.exists(new_to_dir):
                os.makedirs(new_to_dir)
            download_files_in_directory(new_from_dir, new_to_dir)
        elif not ignore_this_file(file_name):
            output = ob.wksp_file_download(user_workspace_selection, file_path)
            output = [i for i in output.split("\n")]
            print(file_path.split("/")[-1])
            try:
                f = open(os.path.join(to_directory, file_name), 'w')
                for line in output:
                    f.write(line)
                    f.write('\n')
            finally:
                f.close()


def download_database_as_csvs() -> None:
    
    timestamp_start = dt.datetime.now()

    # Get user input from environment variables
    user_name, app_key, database_name, schema = get_user_input()

    # Connect to database
    connection_string = get_connection_string(user_name, app_key, database_name)
    
    # Download tables from database
    get_tables_from_postgres_sqlalchemy(connection_string, schema, database_name)

    timestamp_end = dt.datetime.now()
    total_seconds = (timestamp_end - timestamp_start).total_seconds()
    print(f'It took {total_seconds} seconds to download the model.')


def get_user_input(USER_NAME, APP_KEY, DATABASE_NAME, SCHEMA) -> Tuple[str, str, str, str]:
    
    print('Getting user input...')

    user_name = USER_NAME
    app_key = APP_KEY
    database_name = DATABASE_NAME
    schema = SCHEMA
    
    
    if not user_name:
        sys.exit('Provide USER_NAME.')
        
    if not app_key:
        sys.exit('Provide APP_KEY.')
        
    if not database_name:
        sys.exit('Provide DATABASE_NAME.')
    
    return user_name, app_key, database_name, schema

def get_connection_string(user_name: str, 
                          app_key: str, 
                          database_name: str
                          ) -> str:
    
    print('Getting connection string...')
    
    api = pioneer.Api(auth_legacy=False, un=user_name, appkey=app_key)
    connection_string = api.sql_connection_info(database_name)
    user = connection_string['raw']['user']
    password = connection_string['raw']['password']
    host = connection_string['raw']['host']
    port = connection_string['raw']['port']
    db_name = connection_string['raw']['dbname']
    final_connection_string = f'postgresql://{user}:{password}@{host}:{port}/{db_name}?sslmode=require'
    
    return final_connection_string
    
def is_output_table(table_name: str) -> bool:
    if table_name.startswith('optimization') or table_name.startswith('simulation'):
        return True
    else:
        return False

def is_special_table(table_name: str) -> bool:
    if table_name in ['maps', 'scg_conversion_log', 'analytics', 'histograms', 'modelinfo']:
        return True
    else:
        return False
                
def get_tables_from_postgres_sqlalchemy(connection_string: str, schema: str, database_name: str) -> None:
    """function need further adjustment DO NOT USE AS IS"""
    print(f'Setting up SQL Alchemy engine...')
    # SQL alchemy engine
    engine = sal.create_engine(connection_string, pool_timeout=300, max_overflow=-1, pool_size=100) 
    
    # Get schema table names
    inspector = sal.inspect(engine)
    print(inspector.get_schema_names())
    if schema == '':
        schema = inspector.default_schema_name
        print(f'Schema not provided. Using default schema: {schema}.')
    table_names = inspector.get_table_names(schema=schema)
    
    # Set location of downloaded files
    directories = Directories(database_name, schema)
    
    print(f'Reading tables from {schema} schema in {database_name} database...')
    for table_name in tqdm(table_names):
        with engine.begin() as connection:
            query = sal.text(f"SELECT * FROM {schema}.{table_name}")
            table = pd.read_sql_query(query, con=connection)
            del table['id']
        if not table.empty:
            file_name = f'{table_name}.csv'
            if is_output_table(table_name):
                file_path = os.path.join(directories.outputs_directory, file_name) 
            elif is_special_table(table_name):
                file_path = os.path.join(directories.special_tables_directory, file_name) 
            else:
                file_path = os.path.join(directories.input_modeler_directory, file_name)
            table.to_csv(file_path, index=False)
    connection.close()

def get_tables_from_postgres_api(api: pioneer.Api, schema: str, database_name: str, dirs: Directories) -> None:
    
    print(f'Getting table names and schema')
    sc_all=api.database_schemas()['schemas']['anura']
    sc_stable = [s.get('schemaName') for s in sc_all if s.get('status')=='stable']
    if schema == '':
        schema = sc_stable[-1]
        print(f'Schema not provided. Using stable schema: {schema}.')

    db_info = api.database_tables(database_name)
    tables_list = [i.get('name') for i in db_info['tables']]
       
    print(f'Retrieving tables from {schema} schema in {database_name} database...')
    for table_name in tqdm(tables_list):
        query = f"SELECT * FROM {schema}.{table_name}"
        e = api.sql_query(database_name, query)
        sr = pd.DataFrame.from_dict(e)['queryResults']
        table =pd.DataFrame(sr.tolist())
        if not table.empty:
            table.drop('id', axis=1, inplace=True)
            file_name = f'{table_name}.csv'
            if is_output_table(table_name):
                file_path = os.path.join(dirs.outputs_directory, file_name) 
            elif is_special_table(table_name):
                file_path = os.path.join(dirs.special_tables_directory, file_name) 
            else:
                file_path = os.path.join(dirs.input_modeler_directory, file_name)
            table.to_csv(file_path, index=False)
    

def copy_files_in_folder(api: pioneer.Api, from_directory: str, to_directory: str, user_workspace_selection: str) -> None:
    for file_name in os.listdir(from_directory):
        full_path = os.path.join(from_directory, file_name)
        if os.path.isdir(full_path):
            new_sub_dir = to_directory + '/' + file_name
            copy_files_in_folder(api, full_path, new_sub_dir, user_workspace_selection)
        else:
            print(file_name)
            api.wksp_file_upload(user_workspace_selection,
                                to_directory + '/' + file_name,
                                full_path, True)
