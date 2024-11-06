import pandas as pd
from src.main.application.out import IndicatorMetadataPort
from src.main.application.income import ComputeTxPlvsDenominatorDisaggregationUseCase

class ComputeTxPvlsDenominatorDisaggregationService(ComputeTxPlvsDenominatorDisaggregationUseCase):

    def __init__(self, tx_pvls_denominator_indicator_metadata_port: IndicatorMetadataPort, tx_pvls_denominator_preg_breast_indicator_metadata_port: IndicatorMetadataPort) -> None:
        self.tx_pvls_denominator_indicator_metadata_port = tx_pvls_denominator_indicator_metadata_port
        self.tx_pvls_denominator_preg_breast_indicator_metadata_port = tx_pvls_denominator_preg_breast_indicator_metadata_port

    def compute(self, tx_pvls_patients, end_period):

        tx_pvls_denominator_indicator_metadata = self.tx_pvls_denominator_indicator_metadata_port.find_indicator_metadata()
        tx_pvls_denominator_preg_breast_inidcator_metadata = self.tx_pvls_denominator_preg_breast_indicator_metadata_port.find_indicator_metadata()

        indicators = {}

        for patient in tx_pvls_patients:

            for gender in self.GENDERS:

                if not self.match_gender(patient, gender):
                    continue

                for age_band in self.tx_pvls_denominator_indicator_metadata_port.age_bands():
                    
                    if not self.match_age_band(patient, age_band, end_period):
                        continue

                    indicator_key = age_band+'_'+gender[0]
                    
                    metadatas = [metadata_id for metadata_id in tx_pvls_denominator_indicator_metadata if indicator_key == metadata_id['indicator_key']]
                    indicator_key = indicator_key + '_' + patient['orgUnit']

                    self.update_indicator_value(patient, indicators, metadatas, indicator_key)

                    if self.pregnant(patient):
                        indicator_key = 'Pregnant'

                        metadatas = [metadata_id for metadata_id in tx_pvls_denominator_preg_breast_inidcator_metadata if indicator_key == metadata_id['indicator_key']]
                        indicator_key = indicator_key + '_' + patient['orgUnit']

                        self.update_indicator_value(patient, indicators, metadatas, indicator_key)

                    if self.breastfeeding(patient):
                        indicator_key = 'Breastfeeding'
                        metadatas = [metadata_id for metadata_id in tx_pvls_denominator_preg_breast_inidcator_metadata if indicator_key == metadata_id['indicator_key']]
                        indicator_key = indicator_key + '_' + patient['orgUnit']

                        self.update_indicator_value(patient, indicators, metadatas, indicator_key)
                    
                    break
        
        indicators = list(indicators.values())

        return indicators

    def match_gender(self,patient, gender):
        if str(patient['patientSex']) == 'nan':
            return False
        
        if patient['patientSex'][0] == gender[0]:
            return True
        
        return False
    
    def match_age_band(self, patient, age_band, end_period):
        end_period = pd.to_datetime(end_period)
        
        date_of_birth = pd.to_datetime(patient['patientAge'])
        
        years_between = end_period.year - date_of_birth.year

        if age_band == self.LESS_THAN_ONE_YEAR and years_between == 0:
            return True
        
        if age_band == self.SIXTY_FIVE_MORE and years_between >= 65:
            return True
        
        if age_band != self.LESS_THAN_ONE_YEAR and age_band != self.SIXTY_FIVE_MORE:
            start_range = int(age_band.split('-')[0])
            end_range = int(age_band.split('-')[1])

            if (years_between >= start_range and years_between <= end_range):
                return True
            
        return False
    

    def update_indicator_value(self, patient, indicators, metadatas, indicator_key):
        metadata_indicator_id = metadatas[0]

        if indicator_key not in indicators:
            indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}

            indicators[indicator_key]['dataElement'] = metadata_indicator_id['id'].split('.')[0]
            indicators[indicator_key]['categoryOptionCombo'] = metadata_indicator_id['id'].split('.')[1]
            indicators[indicator_key]['attributeOptionCombo'] = ''
            indicators[indicator_key]['orgUnit'] = patient['orgUnit']
        else:
            indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
    
    def pregnant(self, patient):
        if 'pregnant' not in patient:
            return False
        
        return patient['pregnant'] == True
    
    def breastfeeding(self, patient):
        if 'breastfeeding' not in patient:
            return False
        
        return patient['breastfeeding'] == True




