from logging import Logger

import pandas as pd
from src.main.application.out import IndicatorMetadataPort
from src.main.application.income import ComputePmtctArtNumeratorDisaggregationUseCase

class ComputePmtctArtNumeratorDisaggregationService(ComputePmtctArtNumeratorDisaggregationUseCase):

    def __init__(self, logger: Logger, pmtct_art_numerator_indicator_metadata_port: IndicatorMetadataPort) -> None:
       self.logger = logger
       self.pmtct_art_numerator_indicator_metadata_port = pmtct_art_numerator_indicator_metadata_port

    def compute(self, pmtct_art_patients, end_period):
        
        indicators = {}

        indicators_metadata = self.pmtct_art_numerator_indicator_metadata_port.find_indicator_metadata()

        for patient in pmtct_art_patients:

            for gender in self.GENDERS:
                
                if not self.match_gender(patient, gender):
                    continue

                for art in self.ARTS:

                    if not self.match_art(patient, art):
                        continue

                    for age_band in self.pmtct_art_numerator_indicator_metadata_port.age_bands():

                        if not self.match_age_band(patient, age_band, end_period):
                            continue

                        indicator_key = age_band +'_'+gender[0] + '_' + art
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
        
        try:
            date_of_birth = pd.to_datetime(patient['patientAge'])
        except pd.errors.OutOfBoundsDatetime:
            self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid age: {patient['patientAge']}")
            return False
        
        years_between = end_period.year - date_of_birth.year

        if age_band == self.LESS_THAN_TEN_YEARS and years_between < 10:
            return True
        
        if age_band == self.SIXTY_FIVE_MORE and years_between >= 65:
            return True
        
        if age_band != self.LESS_THAN_TEN_YEARS and age_band != self.SIXTY_FIVE_MORE:
            start_range = int(age_band.split('-')[0])
            end_range = int(age_band.split('-')[1])

            if (years_between >= start_range and years_between <= end_range):
                return True
            
        return False
    
    def match_art(self, patient, art):
        if str(patient['artStatus']) == 'nan':
            return False
        
        if str(patient['artStatus']) == 'NOVO' and art == 'New':
            return True
        
        if str(patient['artStatus']) == 'ANTIGO' and art == 'Already':
            return True
        
        return False
