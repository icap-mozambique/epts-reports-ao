from dhis2 import Api
from src.main.application.out import IndicatorMetadataPort

class PmtctArtNumeratorIndicatorMetadataAdapter(IndicatorMetadataPort):
    
    METADATA_ID = 'NLETU6RpNFz'

    AGE_BANDS = ['<10', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65+']

    def __init__(self, api: Api) -> None:
        self.api = api

    def find_indicator_metadata(self):
        indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
        indicators_metadata = indicators_metadata.json()['dataElementOperands']

        for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER25_', '')
            name = name.replace('MER_', '')
            name = name.split('PMTCT_ART (N, TA, Age/NewExistingArt/Sex/HIVStatus): ART ')[1]

            # Age, gender. eg: <10_F_New
            indicator_key = name.split(', ')[0] + '_' + name.split(', ')[3][0] +'_'+ name.split(', ')[2]
            indicator_metadata['indicator_key'] = indicator_key

        return indicators_metadata

    def age_bands(self):
        return self.AGE_BANDS