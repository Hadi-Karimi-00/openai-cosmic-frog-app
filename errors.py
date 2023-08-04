
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
sr = pd.DataFrame.from_dict(e)['queryResults']
df =pd.DataFrame(sr.tolist())
df.drop('id', axis=1, inplace=True)
print(df)


"""error here. Not able to establish connection to PostGRES host using sqlalchemy. Used pioneer.Api.sql_query() instead."""
constr = dl.get_connection_string(User_Name,API_Key,DB_Name)
# SQL alchemy engine
engine = sal.create_engine(constr, pool_timeout=300, max_overflow=-1, pool_size=100, pool_pre_ping=True, pool_recycle=3600, echo=True)
# Get schema table names
inspector = sal.inspect(engine)
print(inspector.get_schema_names())
if SCHEMA == '':
    SCHEMA = inspector.default_schema_name
    print(f'Schema not provided. Using default schema: {SCHEMA}.')
table_names = inspector.get_table_names(schema=SCHEMA)

print(table_names)

""" info 
While running `inspector=sal.inspect(engine)` (where `engine=sal.create_engine(connection_string)`) you may get a connection error using personal PC, see errors.py for more info. that is because of firewall and the port being blocked. Should consult IT to allow that port, or update the pg.hba.conf, or turn off EZ Scaler firewall temporarily. `create_engine()` call itself does **not** establish any actual DBAPI connections directly. The object instance will
request a connection from the underlying [_pool.Pool] once _engine.Engine.connect is called, or a method which depends on it
such [as _engine]. Engine.execute is invoked. The [_pool.Pool] in turn will establish the first actual DBAPI connection when this request
is received. <br>
https://serverfault.com/questions/697187/postgresql-connection-timed-out <br>
"""
print(engine.echo)
print(engine.driver)
print(engine.pool)
print(engine.clear_compiled_cache())

c = engine.connect()
engine.raw_connection()

conn = engine.begin()
query = sal.text(f"SELECT * FROM anura_2_6.analytics")
table = pd.read_sql_query(query, con=conn)


""" resolved: if we get the SQLAlchemy connection string instead of Postgres string we can run and conneect using engine = sal.create_engine() and con = engine.connect()"""
# this is what we get from that string:
# "engine = sqlalchemy.create_engine('postgresql://042a92a6-7b12-42f6-8cc4-895c8fe8da46_768c341fe803:/TJC4v89EFARQ~^p@optilogic.postgres.database.azure.com:6432/042a92a6-7b12-42f6-8cc4-895c8fe8da46-a1ab0214e304?sslmode=require&fallback_application_name=optilogic_sqlalchemy')"

engine = sal.create_engine('postgresql://042a92a6-7b12-42f6-8cc4-895c8fe8da46_768c341fe803:/TJC4v89EFARQ~^p@optilogic.postgres.database.azure.com:6432/042a92a6-7b12-42f6-8cc4-895c8fe8da46-a1ab0214e304?sslmode=require&fallback_application_name=optilogic_sqlalchemy')

conn = engine.connect()