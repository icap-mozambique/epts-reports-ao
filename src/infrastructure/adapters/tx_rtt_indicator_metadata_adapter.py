from dhis2 import Api
from src.main.application.out import IndicatorMetadataPort

class TxRttIndicatorMetadataAdapter(IndicatorMetadataPort):
    
    METADATA_ID = 'EXHtjo00lEh'

    AGE_BANDS = ['<1', '1-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65+']

    def __init__(self, api: Api) -> None:
        self.api = api

    def find_indicator_metadata(self):
        indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
        indicators_metadata = indicators_metadata.json()['dataElementOperands']

        for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER25_', '')
            name = name.replace('MER_', '')
            name = name.split('TX_RTT (N, TA, Age/Sex/CD4/HIVStatus): Restarted ARV ')[1]

            # Age, gender. eg: <15_F_<200 CD4
            indicator_key = name.split(', ')[3] + '_' + name.split(', ')[0][0] + '_' + name.split(', ')[1]
            indicator_metadata['indicator_key'] = indicator_key

        return indicators_metadata
    
    def age_bands(self):
        return self.AGE_BANDS


