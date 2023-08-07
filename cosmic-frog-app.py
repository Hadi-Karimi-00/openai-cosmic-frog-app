
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
import pioneer_api_download_upload as dl

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

# Set locations of model data files ['input_modeler', 'output', 'special_tables']
directories = dl.Directories(local_directory, DB_Name)

""" 0- initiate an empty model and download anura templates"""
#db_new = api.database_create(name='my_DB_Via_API',desc="PostGres Database created via pioneer Api")
#api.database_export(DB_Name,group='tables')

""" 1- downloading the data model"""
# Via SQLalchemy engine
#constr = dl.get_connection_string(User_Name,API_Key,DB_Name)
#engine = sal.create_engine(constr, pool_timeout=300, max_overflow=-1, pool_size=100, pool_pre_ping=True, pool_recycle=3600, echo=True)
#conn = engine.connect()

main_db_nm = 'SuSCO_Model_main'
api.database_export(main_db_nm,group='tables')

""" 2- make changes to data tables"""
# copied SuSCO_Model_main directory into susco_model_1 (folders: input_modeler, output, special_tables)

""" 3- upload modified data"""
fromdir = local_directory + "\\" + DB_Name
todir = ATLAS_directory_path_selection

dl.copy_files_in_folder(api, fromdir, todir, user_workspace_selection)

""" 4- executing the model run script in Atlas (SDK>>05_Solver and Model Runner>>run_model.py)"""
# At the moment giving CVS files path results in error (maybe becuase .frog database is not updated?)
# Giving database name results in successful run but I cannot find the scenrio output folders. Maybe the .frog database is updated? Yes the .frog database is updated
# but no csv folder created.

end = dt.datetime.now()
print('End: %s' %end)

print("It took: %s" %(end - start))