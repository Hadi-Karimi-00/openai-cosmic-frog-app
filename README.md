# openai-cosmic-frog-app
### Web application on sustainability and supply chain optimization that deploys OpenAI and OptiLogic 

CF model implementation: 

1. Initiate and download [empty] model (.frog data model) 
    a. Create a folder in Atlas under My Files for your model. 
    b. Inside the above folder, create a folder named "input_modeler". Contains the tables where model data will resides.
    c. In order to create empty tables for input_modeler: 
       _ Go to CF or Lightning Editor, click right on the model forlder above and follow [Create Cosmic Frog Model]. 
         Options to get the empty tables for the .frog model: 
            i. Open the .frog model in CF, select the required tables (use Ctrl for multiple selection) and Export CSV from File tab.
            ii. Go to SDK folder in Atlas >> 4_Cosmic Frog Data Model and Templates >> Cosmic Frog Blank Tables >> Inputs/Outputs. 
            Download CSV files either manually from Atlas or via Python using function `download_files_in_directory()`
            iii. Get the connection string for the model in CF (right click on .frog). Use pioneer API download template*. 

2. Update data (according to Anura data scheme)
3. Upload [new] data model
4. Execute the model run 
5. Track the job queue 
6. Download output (populated data model) 

Note*: While running `inspector=sal.inspect(engine)` (where `engine=sal.create_engine(connection_string)`) you may get a connection error using personal PC, that is because of firewall and the port being blocked. Should consult IT to allow that port, or update the pg.hba.conf, or turn off EZ Scaler firewall temporarily.
OperationalError: Is the server running on that host and accepting TCP/IP connections?
https://serverfault.com/questions/697187/postgresql-connection-timed-out

`create_engine()` call itself does **not** establish any actual DBAPI connections directly. The object instance will
request a connection from the underlying [_pool.Pool] once _engine.Engine.connect is called, or a method which depends on it
such [as _engine]. Engine.execute is invoked. The [_pool.Pool] in turn will establish the first actual DBAPI connection when this request
is received.


CF: Cosmic Frog 
SuSCO: Sustainable Supply Chain Optimization 
SDK: Supply Chain Design Kit 
