*# openai-cosmic-frog-app
### Web application on sustainability and supply chain optimization that deploys OpenAI and OptiLogic 

CF model implementation: 

1. Initiate and download [empty] model (.frog data model) <br>
    a. Create a folder in Atlas under My Files for your model. <br>
    b. Inside the above folder, create a folder named "input_modeler". Contains the tables where model data will resides. <br>
    c. In order to create empty tables for input_modeler: <br>
            - Go to CF or Lightning Editor, click right on the model forlder above and follow [Create Cosmic Frog Model]. 
            - Options to get the empty tables for the .frog model: <br>
                i. Open the .frog model in CF, select the required tables (use Ctrl for multiple selection) and Export CSV from File tab. <br>
                ii. Go to SDK folder in Atlas >> 4_Cosmic Frog Data Model and Templates >> Cosmic Frog Blank Tables >> Inputs/Outputs. <br>
                Download CSV files either manually from Atlas or via Python using function `download_files_in_directory()` <br>
                iii. Get the connection string for the model in CF (right click on .frog). Use pioneer API download template [1^]. <br>
3. Update data (according to Anura data scheme) <br>
4. Upload [new] data model <br>
5. Execute the model run <br>
6. Track the job queue <br>
7. Download output (populated data model) <br>

[1^] While running `inspector=sal.inspect(engine)` (where `engine=sal.create_engine(connection_string)`) you may get a connection error using personal PC, that is because of firewall and the port being blocked. Should consult IT to allow that port, or update the pg.hba.conf, or turn off EZ Scaler firewall temporarily.
OperationalError: Is the server running on that host and accepting TCP/IP connections?
https://serverfault.com/questions/697187/postgresql-connection-timed-out <br>
`create_engine()` call itself does **not** establish any actual DBAPI connections directly. The object instance will
request a connection from the underlying [_pool.Pool] once _engine.Engine.connect is called, or a method which depends on it
such [as _engine]. Engine.execute is invoked. The [_pool.Pool] in turn will establish the first actual DBAPI connection when this request
is received.

CF: Cosmic Frog <br> 
SuSCO: Sustainable Supply Chain Optimization <br>
SDK: Supply Chain Design Kit <br>
