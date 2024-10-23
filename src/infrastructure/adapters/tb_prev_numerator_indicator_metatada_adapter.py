from src.main.application.out import IndicatorMetadataPort


class TbPrevNumeratorIndicatorMetadataAdapter(IndicatorMetadataPort):

    METADATA_ID = 'N6fw6CjSHSc'

    AGE_BANDS = ['<15', '15+']

    def __init__(self, api):
        self.api = api

    def find_indicator_metadata(self):
        indicators_metadata = self.api.get('dataElementOperands', params={'paging':False, 'fields':'id,name', 'filter':f'dataElement.id:eq:{self.METADATA_ID}'})
        indicators_metadata = indicators_metadata.json()['dataElementOperands']

        for indicator_metadata in indicators_metadata:
            name = indicator_metadata['name']
            name = name.replace('MER_', '')
            name = name.split('TB_PREV (N, TA, Age/Sex/NewExistingArt/HIVStatus): IPT ')[1]

            # Age, gender. eg: <15_F_New
            indicator_key = name.split(', ')[0] + '_' + name.split(', ')[1][0] + '_' + name.split(', ')[3]
            indicator_metadata['indicator_key'] = indicator_key

        return indicators_metadata

    def age_bands(self):
        return self.AGE_BANDS