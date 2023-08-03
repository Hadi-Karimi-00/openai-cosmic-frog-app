import sys
import os

import datetime as dt
import sqlalchemy as sal
import pandas as pd

from typing import Tuple
from pathlib import Path
from tqdm import tqdm
from optilogic import pioneer


# COSMIC FROG USER INPUT
USER_NAME = "" # YOUR ACCOUNT USERNAME (IT CAN BE EMAIL OR USERNAME)
APP_KEY = "" # YOUR APPLICATION KEY
DATABASE_NAME = "" # MODEL NAME
SCHEMA = "" # IF YOU LEAVE EMPTY STRING, IT WILL BE THE LATEST VERSION OF THE SCHEMA

class Directories:
    
    def __init__(self, database_name: str, schema: str):
        
        model_directory = os.path.join('downloaded_csv_files', database_name, schema)
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

def download_database_as_csvs() -> None:
    
    timestamp_start = dt.datetime.now()

    # Get user input from environment variables
    user_name, app_key, database_name, schema = get_user_input()

    # Connect to database
    connection_string = get_connection_string(user_name, app_key, database_name)
    
    # Download tables from database
    get_tables_from_postgres(connection_string, schema, database_name)

    timestamp_end = dt.datetime.now()
    total_seconds = (timestamp_end - timestamp_start).total_seconds()
    print(f'It took {total_seconds} seconds to download the model.')


def get_user_input() -> Tuple[str, str, str, str]:
    
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
                
def get_tables_from_postgres(connection_string: str, schema: str, database_name: str) -> None:
    
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

if __name__ == '__main__':
    download_database_as_csvs()
    
    
    
    
    
    
    
    
    