from logging import Logger
import pandas as pd
from src.main.application.out import IndicatorMetadataPort
from src.main.application.income import ComputePmtctEidDisaggregationUseCase

class ComputePmtctEidDisaggregationService(ComputePmtctEidDisaggregationUseCase):

    def __init__(self, logger:Logger, pmtct_eid_indicators_metadata_port: IndicatorMetadataPort) -> None:
       self.logger = logger
       self.pmtct_eid_indicators_metadata_port = pmtct_eid_indicators_metadata_port

    def compute(self, pmtct_eid_patients, end_period):
        
        indicators = {}

        indicators_metadata = self.pmtct_eid_indicators_metadata_port.find_indicator_metadata()

        for patient in pmtct_eid_patients:

            for test_number in self.TESTS_NUMBER:

                if not self.match_test_number(patient, test_number):
                    continue

                for age_band in self.pmtct_eid_indicators_metadata_port.age_bands():

                    if not self.match_age_band(patient, age_band, end_period):
                        continue

                    indicator_key  = age_band + '_' + test_number
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
    
    def match_test_number(self, patient, test_number):
        if str(patient['pcrNumber']) == 'nan':
            return False
        
        if patient['pcrNumber'] == 'PRIMEIRO_TESTE' and test_number == 'EID First Test':
            return True
        
        if patient['pcrNumber'] == 'SEGUNDO_TESTE_OU_MAIS' and test_number == 'EID Second Test or more':
            return True
        
        return False
    

    def match_age_band(self, patient, age_band, end_period):
        end_period = pd.to_datetime(end_period)

        try:
            date_of_birth = pd.to_datetime(patient['patientAge'])
        except pd.errors.OutOfBoundsDatetime:
            self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid age: {patient['patientAge']}")
            return False
        
        months_between = end_period.month - date_of_birth.month

        if age_band == self.LESS_THAN_OR_EQUAL_TWO_MONTHS and months_between <= 2:
            return True
        
        if age_band == self.LESS_THAN_OR_EQUAL_TWELVE_MONTHS and months_between > 2 and months_between <= 12:
            return True
            
        return False

