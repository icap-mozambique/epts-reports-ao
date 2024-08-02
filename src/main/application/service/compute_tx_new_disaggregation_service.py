from logging import Logger
import pandas as pd
from src.main.application.out.indicator_metadata_port import IndicatorMetadataPort
from src.main.application.income.compute_tx_new_disaggretation_use_case import ComputeTxNewDisaggregationUseCase

class ComputeTxNewDisaggregationService(ComputeTxNewDisaggregationUseCase):

    def __init__(self, tx_new_indicator_metadata_port: IndicatorMetadataPort, logger: Logger) -> None:
        self.tx_new_indicator_metadata_port = tx_new_indicator_metadata_port
        self.logger = logger

    def compute(self, patients: list, end_period):
        
        indicators = {}

        indicators_metadata = self.tx_new_indicator_metadata_port.find_indicator_metadata()

        for patient in patients:
            for gender in self.GENDERS:
                if not self.gender_match(patient, gender):
                    continue

                for cd4 in self.CD4S:
                    if not self.cd4_match(patient, cd4):
                        continue

                    for age_band in self.tx_new_indicator_metadata_port.age_bands():
                        if not self.age_band_match(patient, age_band, end_period):
                            continue

                        # indicator_key pattern AGE_GENDER_cd4, e.i: 20-25_F_<200
                        indicator_key = age_band+'_'+gender[0]+'_'+cd4
                        metadatas = [metadata_id for metadata_id in indicators_metadata if indicator_key == metadata_id['indicator_key']]

                        # assure facility data 
                        indicator_key = indicator_key + '_' + patient['orgUnit']
                        
                        if indicator_key not in indicators:
                            indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}
                            
                            metadata_indicator_id = metadatas[0]
                    
                            indicators[indicator_key]['dataElement'] = metadata_indicator_id['id'].split('.')[0]
                            indicators[indicator_key]['categoryOptionCombo'] = metadata_indicator_id['id'].split('.')[1]
                            indicators[indicator_key]['attributeOptionCombo'] = ''
                            indicators[indicator_key]['orgUnit'] = patient['orgUnit']
                        else:
                            indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
                        
                        break
                    
        indicators = list(indicators.values())

        return indicators
    
    def age_band_match(self, patient, age_band, end_period):

        end_period = pd.to_datetime(end_period)
        
        try:
            date_of_birth = pd.to_datetime(patient['patientAge'])
        except pd.errors.OutOfBoundsDatetime:
            self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid age: {patient['patientAge']}")
            return False
 
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

    def gender_match(self, patient, gender):

        if patient['patientSex'][0] == gender[0]:
            return True
        
        return False
    
    def cd4_match(self, patient, cd4):
        if str(patient['lastCD4']) == 'nan':
            return 'CD4 Unknown' == cd4
        
        if str(patient['lastCD4']) != 'nan' and int(patient['lastCD4']) < self.CD4_MINIMUM_VALUE:
            return '<200 CD4' == cd4
        
        if str(patient['lastCD4']) != 'nan' and int(patient['lastCD4']) >= self.CD4_MINIMUM_VALUE:
            return '>=200 CD4' == cd4
            



        

