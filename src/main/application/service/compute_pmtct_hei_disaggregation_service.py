import pandas as pd
from src.main.application.out import IndicatorMetadataPort
from src.main.application.income import ComputePmtctHeiDisaggregationUseCase

class ComputePmtctHeiDisaggregationService(ComputePmtctHeiDisaggregationUseCase):

    def __init__(self, logger, pmtct_hei_indicators_metadata_port: IndicatorMetadataPort, pmtct_hei_pos_indicators_metadata_port: IndicatorMetadataPort) -> None:
        self.logger = logger
        self.pmtct_hei_indicators_metadata_port = pmtct_hei_indicators_metadata_port
        self.pmtct_hei_pos_indicators_metadata_port = pmtct_hei_pos_indicators_metadata_port

    def compute(self, pmtct_hei_patients, end_period):
        indicators = {}
        hei_indicators_metadata = self.pmtct_hei_indicators_metadata_port.find_indicator_metadata()
        hei_pos_indicators_metadata = self.pmtct_hei_pos_indicators_metadata_port.find_indicator_metadata()

        for patient in pmtct_hei_patients:

            for result in self.RESULTS:

                if not self.match_result(patient, result):
                    continue

                for age_band in self.pmtct_hei_indicators_metadata_port.age_bands():

                    if not self.match_age_band(patient, age_band, end_period):
                        continue

                    indicator_key = age_band + '_' + result[0]
                    hei_metadata = [metadata for metadata in hei_indicators_metadata if indicator_key == metadata['indicator_key']][0]
                    indicator_key = indicator_key + '_' + patient['orgUnit']

                    self.update_indicator_value(patient, indicators, hei_metadata, indicator_key)

                    if not self.positive_and_art_initiated(patient):
                        continue

                    pos_indicator_key = age_band
                    hei_pos_metadata = [metadata for metadata in hei_pos_indicators_metadata if pos_indicator_key == metadata['indicator_key']][0]
                    pos_indicator_key = pos_indicator_key + '_' + patient['orgUnit']

                    self.update_indicator_value(patient, indicators, hei_pos_metadata, pos_indicator_key)
                    
                    break
        
        indicators = list(indicators.values())

        return indicators
    
    def match_result(self, patient, result):
        if patient['testResult'][0] == result[0]:
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
    
    def update_indicator_value(self, patient, indicators, metadata, indicator_key):
        if indicator_key not in indicators:
            indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}
        
            indicators[indicator_key]['dataElement'] = metadata['id'].split('.')[0]
            indicators[indicator_key]['categoryOptionCombo'] = metadata['id'].split('.')[1]
            indicators[indicator_key]['attributeOptionCombo'] = ''
            indicators[indicator_key]['orgUnit'] = patient['orgUnit']

        else:
            indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
    
    def positive_and_art_initiated(self, patient):
        if patient['testResult'] == 'POSITIVO' and str(patient['artStartDate']) != 'nan':
            return True
        
        return False




