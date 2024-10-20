import uvicorn
from fastapi import FastAPI
from dhis2 import Api

from integ.resources import TxResource
from src.main.common import LoggingConfig
from src.main.common import FileUtil

app =  FastAPI()

# server data details
credentials = FileUtil.load_credentias()
username = credentials['username']
password = credentials['password']        
url = 'https://dhis-ao.icap.columbia.edu'

# period of analysis
start_period = '2024-07-01'
end_period = '2024-09-30'
period = '2024Q3'

@app.get('/')
async def root():
    return {'message':'The server is runnig...'}

@app.get('/tx-data')
async def root():
    
    api = Api(url, username, password)
    config = FileUtil.load_logging_config()
    logging_config = LoggingConfig(config)
    logger = logging_config.logging_setup()
    
    tx_resource = TxResource(api, logger, start_period, end_period, period)
    return tx_resource.run()
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)