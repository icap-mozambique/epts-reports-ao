from logging import Logger

import pandas as pd
from src.main.application.income import ComputePmtctStatDenominatorDisaggregationUseCase
from src.main.application.out import IndicatorMetadataPort

class ComputePmtctStatDenominatorDisaggregationService(ComputePmtctStatDenominatorDisaggregationUseCase):

    def __init__(self, logger: Logger, pmtct_stat_denominator_indicator_metadata_port: IndicatorMetadataPort) -> None:
       self.logger = logger
       self.pmtct_stat_denominator_indicator_metadata_port = pmtct_stat_denominator_indicator_metadata_port

    def compute(self, pmtct_stat_patients, end_period):
        
        indicators = {}

        indicators_metadata = self.pmtct_stat_denominator_indicator_metadata_port.find_indicator_metadata()

        for patient in pmtct_stat_patients:

            for gender in self.GENDERS:
                
                if not self.match_gender(patient, gender):
                    continue

                for age_band in self.pmtct_stat_denominator_indicator_metadata_port.age_bands():

                    if not self.match_age_band(patient, age_band, end_period):
                        continue

                    indicator_key = age_band +'_'+gender[0]
                    metadatas = [indicator_metadata for indicator_metadata in indicators_metadata if indicator_key == indicator_metadata['indicator_key']]

                    # assure facility disaggregation
                    indicator_key = indicator_key + '_' + patient['orgUnit']

                    if indicator_key not in indicators:
                        indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}
                        metadata = metadatas[0]
                    
                        indicators[indicator_key]['dataElement'] = metadata['id'].split('.')[0]
                        indicators[indicator_key]['categoryOptionCombo'] = metadata['id'].split('.')[1]
                        indicators[indicator_key]['attributeOptionCombo'] = ''
                        indicators[indicator_key]['orgUnit'] = patient['orgUnit']

                    else:
                        indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
                
                break
        
        indicators = list(indicators.values())

        return indicators

    def match_gender(self,patient, gender):
        if patient['patientSex'][0] == gender[0]:
            return True
        
        return False
    
    def match_age_band(self, patient, age_band, end_period):
        end_period = pd.to_datetime(end_period)
        
        date_of_birth = pd.to_datetime(patient['patientAge'])
        
        years_between = end_period.year - date_of_birth.year

        if age_band == self.LESS_THAN_TEN_YEARS and years_between < 10:
            return True
        
        if age_band == self.FIFTY_MORE and years_between >= 50:
            return True
        
        if age_band != self.LESS_THAN_TEN_YEARS and age_band != self.FIFTY_MORE:
            start_range = int(age_band.split('-')[0])
            end_range = int(age_band.split('-')[1])

            if (years_between >= start_range and years_between <= end_range):
                return True
            
        return False
