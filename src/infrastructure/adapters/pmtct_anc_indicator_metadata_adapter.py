from src.main.application.out import IndicatorMetadataPort

class PmtctIndicatorMetadataAdapter(IndicatorMetadataPort):

    METADATA_ID = 'bII4eG3osk5'

    AGE_BANDS = ['<10', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50+']

    def __init__(self, api):
        self.api = api

    def find_indicator_metadata(self):
        indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
        indicators_metadata = indicators_metadata.json()['dataElementOperands']
        indicators_metadata = [key for key in indicators_metadata if 'MER_Known at Entry' not in key['name']]
        indicators_metadata = [key for key in indicators_metadata if 'MER_Recent' not in key['name']]

        for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER_', '')
            name = name.replace('Newly Identified ', '')
            name = name.split('PMTCT_STAT (N, TA, Age/Sex/KnownNewResult): Known Results ')[1]

            indicator_key = name.split(', ')[0] + '_' + name.split(', ')[1][0] + '_' + name.split(', ')[2][0]
            indicator_metadata['indicator_key'] = indicator_key

        return indicators_metadata

    def age_bands(self):
        return self.AGE_BANDS


