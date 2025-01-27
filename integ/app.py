import os
import uvicorn
from fastapi import FastAPI, HTTPException
from dhis2 import Api
from fastapi.responses import FileResponse

from integ.resources import TbPrevResource
from integ.resources import HtsIndexResource
from integ.resources import HtsResource
from integ.resources import PmtctResource
from integ.resources import TbResource
from integ.resources import TxResource
from integ.resources import TbArtResource

from src.main.common import LoggingConfig
from src.main.common import FileUtil

app =  FastAPI()

# server data details
credentials = FileUtil.load_credentias()
username = credentials['username']
password = credentials['password']        
url = 'https://dhis-ao.icap.columbia.edu'

# period of analysis
start_period = '2024-10-01'
end_period = '2024-12-31'
period = '2024Q4'
units_group = 'gH2DlwAo1ja'
semi_annual_period = '2024AprilS1'
annual_period = '2023Oct'

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

@app.get('/tb-prev-data')
async def tb_prev_data():
    api = api = Api(url, username, password)
    org_units = api.get(f'organisationUnitGroups/{units_group}', params={'fields':'organisationUnits[id, name]'}).json()['organisationUnits']
    
    config = FileUtil.load_logging_config()
    logging_config = LoggingConfig(config)
    logger = logging_config.logging_setup()

    tb_prev_resource = TbPrevResource(api, logger, start_period, end_period, semi_annual_period, org_units)
    return tb_prev_resource.run()

@app.get('/tb-art-data')
async def tb_prev_data():
    api = api = Api(url, username, password)
    org_units = api.get(f'organisationUnitGroups/{units_group}', params={'fields':'organisationUnits[id, name]'}).json()['organisationUnits']
    
    config = FileUtil.load_logging_config()
    logging_config = LoggingConfig(config)
    logger = logging_config.logging_setup()

    tb_art_resource = TbArtResource(api, logger, start_period, end_period, annual_period, org_units)
    return tb_art_resource.run()

@app.get('/download/{code}')
def download(code: str):
    if code == 'TX':
        if not os.path.exists('TX_DATA.csv'):
            raise HTTPException(status_code=404, detail="File not available yet. Try again later.")
        else:
            return FileResponse(path="TX_DATA.csv",filename="TX_DATA.csv", media_type="text/csv")
        
    if code == 'TB':
        if not os.path.exists('TB_DATA.csv'):
            raise HTTPException(status_code=404, detail="File not available yet. Try again later.")
        else:
            return FileResponse(path="TB_DATA.csv",filename="TB_DATA.csv", media_type="text/csv")
        
    if code == 'TB_PREV':
        if not os.path.exists('TB_PREV_DATA.csv'):
            raise HTTPException(status_code=404, detail="File not available yet. Try again later.")
        else:
            return FileResponse(path="TB_PREV_DATA.csv",filename="TB_PREV_DATA.csv", media_type="text/csv")
        
    if code == 'TB_ART':
        if not os.path.exists('TB_ART_DATA.csv'):
            raise HTTPException(status_code=404, detail="File not available yet. Try again later.")
        else:
            return FileResponse(path="TB_ART_DATA.csv",filename="TB_ART_DATA.csv", media_type="text/csv")
    
    if code == 'PMTCT':
        if not os.path.exists('PMTCT_DATA.csv'):
             raise HTTPException(status_code=404, detail="File not available yet. Try again later.")
        else:
            return FileResponse(path="PMTCT_DATA.csv",filename="PMTCT_DATA.csv", media_type="text/csv")
    
    if code == 'HTS':
        if not os.path.exists('HTS_DATA.csv'):
            raise HTTPException(status_code=404, detail="File not available yet. Try again later.")
        else:
            return FileResponse(path="HTS_DATA.csv",filename="HTS_DATA.csv", media_type="text/csv")
    
    if code == 'INDEX':
        if not os.path.exists('INDEX_DATA.csv'):
            raise HTTPException(status_code=404, detail="File not available yet. Try again later.")
        else:
            return FileResponse(path="INDEX_DATA.csv",filename="INDEX_DATA.csv", media_type="text/csv")
    
    raise HTTPException(status_code=404, detail="File code is invalid.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)