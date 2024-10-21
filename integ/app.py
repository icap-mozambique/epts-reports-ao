import uvicorn
from fastapi import FastAPI
from dhis2 import Api

from integ.resources import HtsIndexResource
from integ.resources import HtsResource
from integ.resources import PmtctResource
from integ.resources import TbResource
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
units_group = 'gH2DlwAo1ja'

@app.get('/')
async def root():
    return {'message':'The server is runnig...'}

@app.get('/tx-data')
async def tx_data():
    api = api = Api(url, username, password)
    org_units = api.get(f'organisationUnitGroups/{units_group}', params={'fields':'organisationUnits[id, name]'}).json()['organisationUnits']
    
    config = FileUtil.load_logging_config()
    logging_config = LoggingConfig(config)
    logger = logging_config.logging_setup()

    tx_resource = TxResource(api, logger, start_period, end_period, period, org_units)
    return tx_resource.run()

@app.get('/tb-data')
async def tb_data():
    api = api = Api(url, username, password)
    org_units = api.get(f'organisationUnitGroups/{units_group}', params={'fields':'organisationUnits[id, name]'}).json()['organisationUnits']
    
    config = FileUtil.load_logging_config()
    logging_config = LoggingConfig(config)
    logger = logging_config.logging_setup()

    tb_resource = TbResource(api, logger, start_period, end_period, period, org_units)
    return tb_resource.run()

@app.get('/pmtct-data')
async def pmtct_data():
    api = api = Api(url, username, password)
    org_units = api.get(f'organisationUnitGroups/{units_group}', params={'fields':'organisationUnits[id, name]'}).json()['organisationUnits']
    
    config = FileUtil.load_logging_config()
    logging_config = LoggingConfig(config)
    logger = logging_config.logging_setup()

    pmtct_resource = PmtctResource(api, logger, start_period, end_period, period, org_units)
    return pmtct_resource.run()

@app.get('/hts-data')
async def hts_data():
    api = api = Api(url, username, password)
    org_units = api.get(f'organisationUnitGroups/{units_group}', params={'fields':'organisationUnits[id, name]'}).json()['organisationUnits']
    
    config = FileUtil.load_logging_config()
    logging_config = LoggingConfig(config)
    logger = logging_config.logging_setup()

    hts_resource = HtsResource(api, logger, start_period, end_period, period, org_units)
    return hts_resource.run()

@app.get('/hts-index-data')
async def hts_data():
    api = api = Api(url, username, password)
    org_units = api.get(f'organisationUnitGroups/{units_group}', params={'fields':'organisationUnits[id, name]'}).json()['organisationUnits']
    
    config = FileUtil.load_logging_config()
    logging_config = LoggingConfig(config)
    logger = logging_config.logging_setup()

    hts_index_resource = HtsIndexResource(api, logger, start_period, end_period, period, org_units)
    return hts_index_resource.run()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)