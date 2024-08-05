from src.main.application.out import IndicatorMetadataPort


class IndexCaseContactsNumberIndicatorMetadataAdapter(IndicatorMetadataPort):
    
    METADATA_ID = 'wJSHzXjl3ev'

    AGE_BANDS = ['<15', '15+']

    def __init__(self, api):
        self.api = api
    
    def find_indicator_metadata(self):
        indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
        indicators_metadata = indicators_metadata.json()['dataElementOperands']

        for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER_', '')
            name = name.split('HTS_INDEX (N, TA, Index/Age Aggregated/Sex/Contacts): Number of contacts ')[1]

            # age and gender. eg: <15_F
            indicator_key = name.split(', ')[0] + '_' + name.split(', ')[1][0]
            indicator_metadata['indicator_key'] = indicator_key

        return indicators_metadata
    
    def age_bands(self):
        return self.AGE_BANDS