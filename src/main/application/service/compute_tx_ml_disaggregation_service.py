import math
import pandas as pd
from src.main.application.income import ComputeTxMlDisaggregationUseCase
from src.main.application.out.indicator_metadata_port import IndicatorMetadataPort

class ComputeTxMlDisaggregationService(ComputeTxMlDisaggregationUseCase):

    def __init__(self, tx_ml_indicator_metadata_port: IndicatorMetadataPort) -> None:
        self.tx_ml_indicator_metadata_port = tx_ml_indicator_metadata_port
    
    def compute(self, enrolled_patients, end_period):
        indicators = {}

        indicators_metadata = self.tx_ml_indicator_metadata_port.find_indicator_metadata()

        for patient in enrolled_patients:

            for gender in self.GENDERS:

                if not self.gender_match(patient, gender):
                    continue

                for age_band in self.tx_ml_indicator_metadata_port.age_bands():
                    if not self.age_band_match(patient, age_band, end_period):
                        continue

                    if self.is_patient_dead(patient):
                        indicator_key = age_band+'_'+gender[0] +'_Died'

                        metadatas = [metadata_id for metadata_id in indicators_metadata if indicator_key == metadata_id['indicator_key']]
                        indicator_key = indicator_key + '_' + patient['orgUnit']

                        self.update_indicator_value(patient, indicators, metadatas, indicator_key)
                        continue

                    if self.patient_was_transferred_out(patient):
                        indicator_key = age_band+'_'+gender[0] +'_Transferred Out'

                        metadatas = [metadata_id for metadata_id in indicators_metadata if indicator_key == metadata_id['indicator_key']]
                        indicator_key = indicator_key + '_' + patient['orgUnit']

                        self.update_indicator_value(patient, indicators, metadatas, indicator_key)
                        continue
                    
                    if self.patient_in_treatment_less_than_3_months(patient):
                        indicator_key = age_band+'_'+gender[0] +'_Interruption in Treatment (<3 Months Treatment)'

                        metadatas = [metadata_id for metadata_id in indicators_metadata if indicator_key == metadata_id['indicator_key']]
                        indicator_key = indicator_key + '_' + patient['orgUnit']

                        self.update_indicator_value(patient, indicators, metadatas, indicator_key)
                        continue

                    if self.patient_in_treatment_between_3_to_5_months(patient):
                        indicator_key = age_band+'_'+gender[0] +'_Interruption in Treatment (3-5 Months Treatment)'

                        metadatas = [metadata_id for metadata_id in indicators_metadata if indicator_key == metadata_id['indicator_key']]
                        indicator_key = indicator_key + '_' + patient['orgUnit']

                        self.update_indicator_value(patient, indicators, metadatas, indicator_key)
                        continue

                    if self.patient_in_treatment_for_more_than_6_months(patient):
                        indicator_key = age_band+'_'+gender[0] +'_Interruption In Treatment (6+ Months Treatment)'

                        metadatas = [metadata_id for metadata_id in indicators_metadata if indicator_key == metadata_id['indicator_key']]
                        indicator_key = indicator_key + '_' + patient['orgUnit']

                        self.update_indicator_value(patient, indicators, metadatas, indicator_key)
                        continue

        indicators = list(indicators.values())

        return indicators
    
    def age_band_match(self, patient, age_band, end_period):
        
        end_period = pd.to_datetime(end_period)
        date_of_birth = pd.to_datetime(patient['patientAge'])
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
    
    def is_patient_dead(self, patient):
        if str(patient['dead']) == 'nan':
            return False
        
        if patient['dead'] == True:
            return True
        
        return False
    
    def update_indicator_value(self, patient, indicators, metadatas, indicator_key):       
        metadata_indicator_id = metadatas[0]

        if indicator_key not in indicators:
            indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}

            indicators[indicator_key]['dataElement'] = metadata_indicator_id['id'].split('.')[0]
            indicators[indicator_key]['categoryOptionCombo'] = metadata_indicator_id['id'].split('.')[1]
            indicators[indicator_key]['attributeOptionCombo'] = ''
            indicators[indicator_key]['orgUnit'] = patient['orgUnit']
        else:
            indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
    
    def patient_in_treatment_less_than_3_months(self, patient):
        if str(patient['nextPickupDate']) == 'nan':
            return False
        
        art_start_date = pd.to_datetime(patient['artStartDate'])
        next_pick_up_date = pd.to_datetime(patient['nextPickupDate'])

        days = (next_pick_up_date - art_start_date).days

        return days < 90
    
    def patient_in_treatment_between_3_to_5_months(self, patient):
        if str(patient['nextPickupDate']) == 'nan':
            return False
        
        art_start_date = pd.to_datetime(patient['artStartDate'])
        next_pick_up_date = pd.to_datetime(patient['nextPickupDate'])

        days = (next_pick_up_date - art_start_date).days

        return days >= 90 and days <= 150
    
    def patient_in_treatment_for_more_than_6_months(self, patient):
        if str(patient['nextPickupDate']) == 'nan':
            return False
        
        art_start_date = pd.to_datetime(patient['artStartDate'])
        next_pick_up_date = pd.to_datetime(patient['nextPickupDate'])

        days = (next_pick_up_date - art_start_date).days

        return days >= 180
    
    def patient_was_transferred_out(self, patient):
        if str(patient['transferedOut']) == 'nan':
            return False
        
        if patient['transferedOut'] == True:
            return True
        
        return False

      




