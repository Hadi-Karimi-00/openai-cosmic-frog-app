
"""
Cosmic Frog optimization-simulation UI

Created on Tue Aug  1 15:32:29 2023
@author: HK 62866
"""

import os
import datetime as dt
import subprocess
import sys
import importlib.util
from optilogic import pioneer
import sqlalchemy as sal
import pandas as pd
from typing import Tuple
from pathlib import Path
from tqdm import tqdm
import PythonAPI_Download_postgres as dl

start = dt.datetime.now()
print('Start: %s' %start)

#Frog Model Config
API_Key = os.environ.get('cf_app_key')
User_Name = os.environ.get('my_user_name')
local_directory = r'C:\Users\62866\OneDrive - Bain\OpenAI\Code\openai-cosmic-frog-app\data' 
user_workspace_selection = 'Studio' 
ATLAS_directory_path_selection = '/My Files/My SuSCO Model' # should begin with ‘My Models/…’ not ‘projects/My Models
DB_Name = "susco_model_1" #model database name as it appears in Cloud Storage
SCHEMA = "" # IF YOU LEAVE EMPTY STRING, IT WILL BE THE LATEST VERSION OF THE SCHEMA

#activate an API object
api = pioneer.Api(appkey=API_Key, un=User_Name, auth_legacy=False)

""" downloading the data model"""
api.database_schemas()
db_info = api.database_tables(DB_Name)
print(db_info['tables'][0])
tables_list = [i.get('name') for i in db_info['tables']]
tables_list[1]
api.database_export(DB_Name, named=tables_list)
query1 = f"SELECT * FROM anura_2_6.analytics"
query2 = f"SELECT * FROM anura_2_6.customers"
e = api.sql_query('My SuSCO Model 1', query2)
df = pd.DataFrame.from_dict(e)

aa = api.wksp_files(user_workspace_selection, ATLAS_directory_path_selection)
#files = ob.wksp_files(user_workspace_selection, filter=ATLAS_directory_path_selection)
#connection_string = api.sql_connection_info(DB_Name)
#print(connection_string)
constr = dl.get_connection_string(User_Name,API_Key,DB_Name)

conn_str = "postgresql+psycopg2://7c9482f2-4d3f-4e60-8595-fa7d85139d3c_1bb463251b10:<yPP9-LbReY5sTL<@optilogic.postgres.database.azure.com:6432/7c9482f2-4d3f-4e60-8595-fa7d85139d3c-029e283e954d?sslmode=require&fallback_application_name=optilogic_postgresql"
# SQL alchemy engine
engine = sal.create_engine(constr, pool_timeout=300, max_overflow=-1, pool_size=100, pool_pre_ping=True, pool_recycle=3600, echo=True)



print(engine.echo)
print(engine.driver)
print(engine.pool)
print(engine.clear_compiled_cache())

c = engine.connect()
engine.raw_connection()

conn = engine.begin()
query = sal.text(f"SELECT * FROM anura_2_6.analytics")
table = pd.read_sql_query(query, con=conn)


# Get schema table names
inspector = sal.inspect(engine)
print(inspector.get_schema_names())
if SCHEMA == '':
    SCHEMA = inspector.default_schema_name
    print(f'Schema not provided. Using default schema: {SCHEMA}.')
table_names = inspector.get_table_names(schema=SCHEMA)

print(table_names)