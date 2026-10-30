from logging import Logger

import pandas as pd

from src.main.application.out import IndicatorMetadataPort
from src.main.application.income import ComputeTxTbDenominatorDisaggregationUseCase

class ComputeTxTbDenominatorDisaggregationService(ComputeTxTbDenominatorDisaggregationUseCase):

    def __init__(self, tx_tb_denominator_metadata_port: IndicatorMetadataPort, logger: Logger):
        self.tx_tb_denominator_metadata_port = tx_tb_denominator_metadata_port
        self.logger = logger
        
    def compute(self, patients, end_period):
        indicators = {}

        tx_tb_denominator_metadata = self.tx_tb_denominator_metadata_port.find_indicator_metadata()

        for patient in patients:
            for tb_type in self.TB_TYPES:
                if not self.match_tb_type(patient, tb_type):
                    continue

                for result in self.RESULTS:
                    if not self.match_result(patient, result):
                        continue

                    for gender in self.GENDERS:
                        if not self.gender_match(patient, gender):
                            continue

                        for age_band in self.tx_tb_denominator_metadata_port.age_bands():
                            if not self.age_band_match(patient,age_band, end_period):
                                continue

                            # Age, Gender, Result and Status eg. <1_F_P_New
                            indicator_key = age_band+'_'+gender[0]+'_'+result[0]+'_'+tb_type
                            metadata = [metadata_id for metadata_id in tx_tb_denominator_metadata if indicator_key == metadata_id['indicator_key']]
        
                            # assure facility data 
                            indicator_key = indicator_key + '_' + patient['orgUnit']
                            
                            if indicator_key not in indicators:
                                indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}
                                metadata_indicator_id = metadata[0]
                            
                                indicators[indicator_key]['dataElement'] = metadata_indicator_id['id'].split('.')[0]
                                indicators[indicator_key]['categoryOptionCombo'] = metadata_indicator_id['id'].split('.')[1]
                                indicators[indicator_key]['attributeOptionCombo'] = ''
                                indicators[indicator_key]['orgUnit'] = patient['orgUnit']
        
                            else:
                                indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
                            
                            break
                
        indicators = list(indicators.values())
                        
        return indicators            


    def match_result(self, patient, result):
        if patient['tb_status'] == 'Rastreado e sem sinais' and result == 'Negative':
            return True
        
        if patient['tb_status'] != 'Rastreado e sem sinais' and result == 'Positive':
            return True

        return False
        

    def match_tb_type(self, patient, type):
        if patient['tb_entry_type'] == 'CASO_NOVO' and type == 'New':
            return True
        
        if patient['tb_entry_type'] == 'ROTINA' and type == 'Already':
            return True

        return False
        

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
        if str(patient['patientSex']) == 'nan':
            return False
        if patient['patientSex'][0] == gender[0]:
            return True
            
        return False 



