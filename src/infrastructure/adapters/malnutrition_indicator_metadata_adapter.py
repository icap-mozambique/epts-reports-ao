from src.main.application.out import IndicatorMetadataPort


class MalnutritionIndicatorMetadataAdapter(IndicatorMetadataPort):

    METADATA_ID = 'ghoSZ0XbWn3'

    AGE_BANDS = ['<1', '1-4']

    def __init__(self, api):
        self.api = api
            
    def find_indicator_metadata(self):
        indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
        indicators_metadata = indicators_metadata.json()['dataElementOperands']

        for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER_', '')
            name = name.split('HTS_TST (N, TA, Malnutrition/Age/Sex/Result): HTS received results ')[1]

            indicator_key = name.split(', ')[0] + '_' + name.split(', ')[1][0] + '_' + name.split(', ')[2][0]
            indicator_metadata['indicator_key'] = indicator_key

        return indicators_metadata

    def age_bands(self):
        return self.AGE_BANDS

