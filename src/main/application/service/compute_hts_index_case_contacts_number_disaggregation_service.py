from logging import Logger

import pandas as pd
from src.main.application.out import IndicatorMetadataPort
from src.main.application.income import ComputeHtsIndexCaseContactsNumberDisaggregationUseCase

class ComputeHtsIndexCaseContactsNumberDisaggregationService(ComputeHtsIndexCaseContactsNumberDisaggregationUseCase):

    def __init__(self, logger: Logger, index_case_contacts_number_indicators_metadata_port: IndicatorMetadataPort) -> None:
        self.logger = logger
        self.index_case_contacts_number_indicators_metadata_port = index_case_contacts_number_indicators_metadata_port
        super().__init__()

    def compute(self, index_case_contacts, end_period):
       
       indicators = {}

       indicators_metadata = self.index_case_contacts_number_indicators_metadata_port.find_indicator_metadata()
       
       for patient in index_case_contacts:
            
             for gender in self.GENDERS:

                 if not self.match_gender(patient, gender):
                     continue

                 for age_band in self.index_case_contacts_number_indicators_metadata_port.age_bands():

                     if not self.match_age_band(patient, age_band, end_period):
                         continue
                    
                     indicator_key =  age_band +'_'+ gender[0]
                     metadata = [metadata for metadata in indicators_metadata if indicator_key == metadata['indicator_key']][0]
                    
                     indicator_key = indicator_key + '_' + patient['orgUnit']
                    
                     if indicator_key not in indicators:
                         indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}
                    
                         indicators[indicator_key]['dataElement'] = metadata['id'].split('.')[0]
                         indicators[indicator_key]['categoryOptionCombo'] = metadata['id'].split('.')[1]
                         indicators[indicator_key]['attributeOptionCombo'] = ''
                         indicators[indicator_key]['orgUnit'] = patient['orgUnit']

                     else:
                         indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
                
                     break
       
       indicators = list(indicators.values())
       
       return indicators
    
    def match_gender(self, patient, gender):
        if str(patient['patientSex']) == 'nan':
            return False
        
        return patient['patientSex'][0] == gender[0]

    def match_age_band(self, patient, age_band, end_period):
        if str(patient['patientAge']) == 'nan':
            return False
        
        end_period = pd.to_datetime(end_period)
        
        try:
            date_of_birth = pd.to_datetime(patient['patientAge'])
        except pd.errors.OutOfBoundsDatetime:
            self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid age: {patient['patientAge']}")
            return False
        
        years_between = end_period.year - date_of_birth.year
       
        if age_band == self.LESS_THAN_FIFTEEN_YEARS and years_between < 15:
            return True
       
        if age_band == self.GREATER_THAN_FIFTEEN_MORE and years_between >= 15:
            return True
        
        return False



