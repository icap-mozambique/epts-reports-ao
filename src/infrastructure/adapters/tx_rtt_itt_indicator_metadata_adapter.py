from dhis2 import Api
from src.main.application.out import IndicatorMetadataPort

class TxRttIttIndicatorMetadataAdapter(IndicatorMetadataPort):
    
    METADATA_ID = 'euQty0yYWEk'

    AGE_BANDS = []

    def __init__(self, api: Api) -> None:
        self.api = api

    def find_indicator_metadata(self):
        indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
        indicators_metadata = indicators_metadata.json()['dataElementOperands']

        for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER25_', '')
            name = name.replace('MER_', '')
            name = name.split('TX_RTT (N, TA, ARTNoContactReasonIIT/HIVStatus): Restarted ARV No Contact Outcome - ')[1]

            # Age, gender. eg: Interruption in Treatment (3-5 Months Treatment)
            indicator_key = name.split(', ')[0]
            indicator_metadata['indicator_key'] = indicator_key

        return indicators_metadata
    
    def age_bands(self):
        return self.AGE_BANDS


