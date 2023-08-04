import os
import pioneer_api_download_upload as dl
from pathlib import Path
#to initiate an empty model access via pioneer.Api() --> api, create a new data base, export it, then download as .zip from Account Activity.
#db_new = api.database_create(name='my_DB_Via_API',desc="PostGres Database created via pioneer Api")
#api.database_export(DB_Name,group='tables')

# Specify the folder path where your .csv files are located
folder_path = "data\SuSCO_Model_main"

# List all files in the folder
file_list = os.listdir(folder_path)

#create folders
input_modeler_directory = os.path.join(folder_path, 'input_modeler')
outputs_directory = os.path.join(folder_path, 'outputs')
special_tables_directory = os.path.join(folder_path, 'special_tables')
Path(input_modeler_directory).mkdir(parents=True, exist_ok=True)
Path(outputs_directory).mkdir(parents=True, exist_ok=True)
Path(special_tables_directory).mkdir(parents=True, exist_ok=True)


# Iterate through the files and rename .csv files
for filename in file_list:
    if filename.endswith(".csv"):
        new_filename = filename[10:]  # Remove anura_2_6
        print(new_filename)
        if new_filename.startswith('optimization') or new_filename.startswith('simulation'):
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(outputs_directory, new_filename)
            os.rename(old_path, new_path)            
        elif new_filename in ['maps.csv', 'scg_conversion_log.csv', 'analytics.csv', 'histograms.csv', 'modelinfo.csv']:
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(special_tables_directory, new_filename)
            os.rename(old_path, new_path)
            #os.remove(old_path)
        else:
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(input_modeler_directory, new_filename)
            os.rename(old_path, new_path)
            #os.remove(old_path)   
        #print(f"Renamed: {filename} -> {new_filename}")

