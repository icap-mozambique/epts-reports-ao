import pandas as pd
import logging

from src.main.application.out import IndicatorMetadataPort
from src.main.application.income import ComputeHtsDisaggregationUseCase


class ComputeHtsDisaggregationService(ComputeHtsDisaggregationUseCase):

    logging.basicConfig(level=logging.WARNING,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename="../data/external/logs.log",
                        )
    
    def __init__(self, indicator_metadata_port: IndicatorMetadataPort) -> None:
        self.indicator_metadata_port = indicator_metadata_port
    
    def compute(self, patients, end_period):
        indicators = {}
        indicators_metadata = self.indicator_metadata_port.find_indicator_metadata()

        for patient in patients:

            for gender in self.GENDERS:
                if not self.gender_match(patient, gender):
                    continue
                
                for result in self.RESULTS:
                    if not self.result_match(patient, result):
                        continue
                
                    for age_band in self.indicator_metadata_port.age_bands():
                        if not self.age_band_match(patient, age_band, end_period):
                            continue

                        # indicator_key pattern AGE_GENDER_RESULT, e.i: 20-25_F_P
                        indicator_key = age_band +'_'+ gender[0] +'_'+ result[0]
                        
                        metadatas = [metadata_id for metadata_id in indicators_metadata if indicator_key == metadata_id['indicator_key']]

                        if not metadatas:
                            logging.warning(f"{patient['trackedEntity']} - {patient['patientName']} - {patient['patientSex']} with key: {indicator_key} was ignored")
                            continue

                        if indicator_key in indicators:
                            indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
                        else:
                            indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}                        
                            
                            metadata_indicator_id = metadatas[0]
                            
                            indicators[indicator_key]['dataElement'] = metadata_indicator_id['id'].split('.')[0]
                            indicators[indicator_key]['categoryOptionCombo'] = metadata_indicator_id['id'].split('.')[1]
                            indicators[indicator_key]['attributeOptionCombo'] = ''
                            indicators[indicator_key]['orgUnit'] = patient['orgUnit']

                        break
        
        indicators = list(indicators.values())

        return indicators
    
    def gender_match(self, patient, gender):
        return patient['patientSex'][0] == gender[0]

    def result_match(self, patient, result):
        return patient['result'][0] == result[0]
    
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
        
        if age_band == self.LESS_THAN_TEN_YEARS and years_between < 10:
            return True
        
        if age_band == self.FIXTY_MORE and years_between >= 50:
            return True
        
        if age_band != self.LESS_THAN_ONE_YEAR and age_band != self.LESS_THAN_TEN_YEARS and age_band != self.FIXTY_MORE:
            start_range = int(age_band.split('-')[0])
            end_range = int(age_band.split('-')[1])

            if (years_between >= start_range and years_between <= end_range):
                return True
            
        return False
    

