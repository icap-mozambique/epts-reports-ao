from logging import Logger
import pandas as pd

from src.main.application.income import ComputeHtsIndexCaseDisaggregationUseCase
from src.main.application.out import IndicatorMetadataPort

class ComputeHtsIndexCaseDisaggregationService(ComputeHtsIndexCaseDisaggregationUseCase):

    def __init__(self,logger: Logger, indicator_metadata_port: IndicatorMetadataPort) -> None:
        self.logger = logger
        self.indicator_metadata_port = indicator_metadata_port
    
    def compute(self, patients, end_period):

        indicators = {}
        
        indicators_metadata = self.indicator_metadata_port.find_indicator_metadata()

        for patient in patients:

            for gender in self.GENDERS:
                if not self.match_gender(patient, gender):
                    continue
                
                for result in self.RESULTS:
                    if not self.match_result(patient, result):
                        continue
                
                    for age_band in self.indicator_metadata_port.age_bands():
                        
                        if not self.match_age_band(patient, age_band, end_period):
                            continue

                        if self.match_documented_negatives(patient, result, age_band):
                            self.update_indicator_value(patient, indicators, indicators_metadata, age_band, gender, result)
                            break
                        
                        self.update_indicator_value(patient, indicators, indicators_metadata, age_band, gender, result)
                        break
        
        indicators = list(indicators.values())

        return indicators
    
    def match_gender(self, patient, gender):
        return patient['patientSex'][0] == gender[0]

    def match_result(self, patient, result):

        if patient['result'] == 'POSITIVO_CONHECIDO' and result == 'Known at Entry Positive':
            return True
        
        if patient['result'] == 'POSITIVO' and result == 'Newly Identified Positive':
            return True
        
        if patient['result'] == 'NEGATIVO' and result == 'Newly Identified Negative':
            return True
        
        if patient['result'] == 'NEGATIVO_CONHECIDO' and result == 'Documented Negative':
            return True
       
        return False
    
    def match_age_band(self, patient, age_band, end_period):

        end_period = pd.to_datetime(end_period)
        date_of_birth = pd.to_datetime(patient['patientAge'])
        years_between = end_period.year - date_of_birth.year

        if age_band == self.LESS_THAN_ONE_YEAR and years_between == 0:
            return True
        
        if age_band == self.FIXTY_MORE and years_between >= 50:
            return True
        
        if age_band != self.LESS_THAN_ONE_YEAR and age_band != self.FIXTY_MORE:
            start_range = int(age_band.split('-')[0])
            end_range = int(age_band.split('-')[1])

            if (years_between >= start_range and years_between <= end_range):
                return True
            
        return False
    
    def match_documented_negatives(self, patient, result, age_band):
        if patient['result'] == 'NEGATIVO_CONHECIDO' and result == 'Documented Negative' and age_band in self.DOCUMENTED_NEGATIVE_BANDS:
            return True
        
        return False
    
    def update_indicator_value(self, patient, indicators, indicators_metadata, age_band, gender, result):
        # indicator_key pattern AGE_GENDER_RESULT, e.i: 20-25_F_Newly Identified Positive
        indicator_key = age_band +'_'+ gender[0] +'_'+ result
    
        metadata = [metadata_id for metadata_id in indicators_metadata if indicator_key == metadata_id['indicator_key']][0]

        indicator_key = indicator_key + '_' + patient['orgUnit']

        if indicator_key in indicators:
            indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
        else:
            indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}                        
            indicators[indicator_key]['dataElement'] = metadata['id'].split('.')[0]
            indicators[indicator_key]['categoryOptionCombo'] = metadata['id'].split('.')[1]
            indicators[indicator_key]['attributeOptionCombo'] = ''
            indicators[indicator_key]['orgUnit'] = patient['orgUnit']

    

