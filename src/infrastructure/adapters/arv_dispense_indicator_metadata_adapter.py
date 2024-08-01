from dhis2 import Api
from src.main.application.out.indicator_metadata_port import IndicatorMetadataPort

class ArvDispenseIndicatorMetadataAdapter(IndicatorMetadataPort):

    METADATA_ID = 'Lz3yNLFlNx4'

    AGE_BANDS = ['<15', '15+']
    
    def __init__(self, api:Api) -> None:
        self.api = api

    def find_indicator_metadata(self):
        indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
        indicators_metadata = indicators_metadata.json()['dataElementOperands']

        for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER_', '')
            name = name.split('TX_CURR (N, TA, Age/Sex/ARVDispense/HIVStatus): Receiving ART ')[1]

            #  Age, gender and quantity. eg: <15_F_Less than 3 months
            indicator_key = name.split(', ')[0] + '_' + name.split(', ')[1][0] + '_' + name.split(', ')[2].split(' - ')[1]
            indicator_metadata['indicator_key'] = indicator_key

        return indicators_metadata

    def age_bands(self):
        return self.AGE_BANDS

    
    