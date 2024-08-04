from dhis2 import Api
from src.main.application.out import IndicatorMetadataPort

class PmtctEidIndicatorMedatadaAdapter(IndicatorMetadataPort):

    METADATA_ID = 'ihz1VxsfpMK'

    AGE_BANDS = ['<= 2 months', '2 - 12 months']

    def __init__(self, api: Api) -> None:
        self.api = api

    def find_indicator_metadata(self):
        indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
        indicators_metadata = indicators_metadata.json()['dataElementOperands']

        for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER_', '')
            name = name.split('PMTCT_EID (N, TA, Age/EID): Infant Testing ')[1]

            # Age, gender. eg: <= 2 months_EID First Test
            indicator_key = name.split(', ')[0] + '_' + name.split(', ')[1]
            indicator_metadata['indicator_key'] = indicator_key

        return indicators_metadata

    def age_bands(self):
        return self.AGE_BANDS