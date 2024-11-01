import pandas as pd

from src.main.application.out import IndicatorMetadataPort
from src.main.application.income import ComputeTbArtDisaggregationUseCase

class ComputeTbArtDisaggregationService(ComputeTbArtDisaggregationUseCase):

    def __init__(self, logger, indicator_metadata_port: IndicatorMetadataPort):
        self.logger = logger
        self.indicator_metadata_port = indicator_metadata_port

    def compute(self, patients, end_period):
                
        indicators = {}

        indicators_metadata = self.indicator_metadata_port.find_indicator_metadata()

        for patient in patients:
            for gender in self.GENDERS:
                if not self.gender_match(patient, gender):
                    continue

                for art_status in self.ART_STATUS:
                    if not self.art_status_match(patient, art_status):
                        continue

                    for age_band in self.indicator_metadata_port.age_bands():
                        if not self.age_band_match(patient, age_band, end_period):
                            continue

                        # indicator_key pattern AGE_GENDER_ART_STATUS, e.i: 20-25_F_New
                        indicator_key = age_band+'_'+gender[0]+'_'+art_status
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
    
    def art_status_match(self, patient, art_status):
        if patient['artStatus'] == 'NOVO' and art_status == 'New':
           return True

        if (patient['artStatus'] == 'ANTIGO' or patient['artStatus'] == 'TARV_NOUTRA_US') and art_status == 'Already':
            return True

        return False
    
    def gender_match(self, patient, gender):

        if str(patient['patientSex']) == 'nan':
            return False
        
        if patient['patientSex'][0] == gender[0]:
            return True
        
        return False


