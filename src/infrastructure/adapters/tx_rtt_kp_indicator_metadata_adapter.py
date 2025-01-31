from dhis2 import Api
from src.main.application.out.indicator_metadata_port import IndicatorMetadataPort


class TxRttKpIndicatorMetadataAdapter(IndicatorMetadataPort):
    
    METADATA_ID = 'pxxcjUHZ0ao'

    AGE_BANDS = []

    def __init__(self, api: Api) -> None:
       self.api = api

    def find_indicator_metadata(self):
       indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
       indicators_metadata = indicators_metadata.json()['dataElementOperands']
       
       for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER_', '')
            name = name.split('TX_RTT (N, TA, KeyPop/HIVStatus): Restarted ARV ')[1]

            # KP. eg: PWID
            indicator_key = name.split(', ')[1]
            indicator_metadata['indicator_key'] = indicator_key
            
       return indicators_metadata

    def age_bands(self):
       return self.AGE_BANDS
