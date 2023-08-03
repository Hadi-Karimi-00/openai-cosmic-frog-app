# Python Download Sample Template
# Code can be run on a local machine to download files directly from Atlas to local machine
# Users must modify details in lines 24 - 28 (#UserToDo)

import os
import datetime as dt
import subprocess
import sys
import importlib.util


start = dt.datetime.now()
print('Start: %s' %start)

package_name = 'optilogic'
spec = importlib.util.find_spec(package_name)
if spec is None:
    print(package_name + " is not installed")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "optilogic"])

from optilogic.pioneer import Api

# ENTER USER DETAILS HERE for each item located in between the single quotes

API_Key = 'api key here' #UserToDo from home page --> account --> app key management
local_directory = r'' #UserToDo enter your local folder directory ex. C:\Users\jane\OneDrive - Optilogic, Inc\Documents\01_Projects
#the r prefix before a string literal denotes a raw string. A raw string treats backslashes (\) as literal characters rather than escape characters.
user_workspace_selection = 'Studio' #UserToDo enter your workspace name here ex. 'Studio'
ATLAS_directory_path_selection = 'Atlas directory path here' #UserToDo replace with your Atlas path ex. My Models/TrainingModel
ob = Api(appkey=API_Key, un='user name here', auth_legacy=False) #UserToDo add email address, ex. jane.user@optilogic.com

# END Section for template user changes

def ignore_this_file(file_name: str) -> bool:
    ignore_files = ['.ci.sh', '.git']
    return file_name in ignore_files \
           or file_name.endswith('.tsv')


def download_files_in_directory(from_directory: str, to_directory: str) -> None:
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


download_files_in_directory(ATLAS_directory_path_selection, local_directory)

end = dt.datetime.now()
print('End: %s' %end)

print("It took: %s" %(end - start))