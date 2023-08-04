*# openai-cosmic-frog-app
### Web application on sustainability and supply chain optimization that deploys OpenAI and OptiLogic 

CF model implementation: 

1. Initiate and download [empty] model (.frog data model) <br>
    a. Create a folder in Atlas under My Files for your model. <br>
    b. Inside the above folder, create a folder named "input_modeler". Contains the tables where model data will resides. <br>
    c. In order to create empty tables for input_modeler:  
            - Go to CF or Lightning Editor, click right on the model forlder above and follow [Create Cosmic Frog Model]. <br>
            - Options to get the empty tables for the .frog model: <br>
                i. Open the .frog model in CF, select the required tables (use Ctrl for multiple selection) and Export CSV from File tab. Better yet, go to 
                SQL Editor, select the model, right click on Anura_2_6 and Export CSV. <br>
                ii. Go to SDK folder in Atlas >> 4_Cosmic Frog Data Model and Templates >> Cosmic Frog Blank Tables >> Inputs/Outputs. <br>
                Download CSV files either manually from Atlas or via Python using function `download_files_in_directory()` <br>
                iii. Get the connection string for the model in CF (right click on .frog). Use sqlalchemy to connect to postgres url and retive data[^1]. <br>
                iiii. Initiate a `pioneer.Api()` instance. Get list of tables with `api.database_tables(DB_NAME)`. Retrieve data table using `api.sql_query(DB_NAME, query)`.
                We can also use `api.database_export(DB_Name, group='all')`. Run this function then go to CF Downloads page to retrieve it. 

3. Update data (according to Anura data scheme) <br>
4. Upload [new] data model <br>
5. Execute the model run <br>
6. Track the job queue <br>
7. Download output (populated data model) <br>

[1^] While running `inspector=sal.inspect(engine)` (where `engine=sal.create_engine(connection_string)`) you may get a connection error using personal PC, see errors.py for more info. 


CF: Cosmic Frog <br> 
SuSCO: Sustainable Supply Chain Optimization <br>
SDK: Supply Chain Design Kit <br>
