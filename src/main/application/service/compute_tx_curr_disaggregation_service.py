from logging import Logger
import pandas as pd
from src.main.application.out.indicator_metadata_port import IndicatorMetadataPort
from src.main.application.income import ComputeTxCurrDisaggregationUseCase

class ComputeTxCurrDisaggregationService(ComputeTxCurrDisaggregationUseCase):

    def __init__(self, tx_curr_indicator_metadata_port: IndicatorMetadataPort, arv_dispense_indicator_metadata_port: IndicatorMetadataPort, logger: Logger) -> None:
        self.tx_curr_indicator_metadata_port = tx_curr_indicator_metadata_port
        self.arv_dispense_indicator_metadata_port = arv_dispense_indicator_metadata_port
        self.logger = logger
    
    def compute(self, patients, end_period):
        indicators = {}

        tx_curr_indicators_metadata = self.tx_curr_indicator_metadata_port.find_indicator_metadata()
        arv_dispense_indicators_metadata = self.arv_dispense_indicator_metadata_port.find_indicator_metadata()

        for patient in patients:
            for gender in self.GENDERS:
                if not self.gender_match(patient, gender):
                    continue

                # ARV dipense quantities
                for arv_age_band in self.arv_dispense_indicator_metadata_port.age_bands():
                    if not self.arv_age_band_match(patient, arv_age_band, end_period):
                        continue

                    for arv_dispense_quantity in self.ARV_DISPENSE_QUANTITIES:
                        if not self.arv_dispense_quntity_match(patient, arv_dispense_quantity):
                            continue

                        arv_indicator_key = arv_age_band + '_' + gender[0] + '_' + arv_dispense_quantity
                        arv_dispense_metadatas = [metadata_id for metadata_id in arv_dispense_indicators_metadata if arv_indicator_key == metadata_id['indicator_key']]

                        # assure facility data 
                        arv_indicator_key = arv_indicator_key + '_' + patient['orgUnit']

                        if arv_indicator_key not in indicators:
                            indicators[arv_indicator_key] = {'indicator_key': arv_indicator_key, 'value':1}
                            arv_dispense_metadata_indicator_id = arv_dispense_metadatas[0]
                        
                            indicators[arv_indicator_key]['dataElement'] = arv_dispense_metadata_indicator_id['id'].split('.')[0]
                            indicators[arv_indicator_key]['categoryOptionCombo'] = arv_dispense_metadata_indicator_id['id'].split('.')[1]
                            indicators[arv_indicator_key]['attributeOptionCombo'] = ''
                            indicators[arv_indicator_key]['orgUnit'] = patient['orgUnit']
                        else:
                            indicators[arv_indicator_key]['value'] = indicators[arv_indicator_key]['value'] + 1
                            
                # TX_CURR
                for age_band in self.tx_curr_indicator_metadata_port.age_bands():
                    if not self.age_band_match(patient, age_band, end_period):
                        continue

                    indicator_key = age_band+'_'+gender[0]
                    tx_curr_metadatas = [metadata_id for metadata_id in tx_curr_indicators_metadata if indicator_key == metadata_id['indicator_key']]

                    # assure facility data 
                    indicator_key = indicator_key + '_' + patient['orgUnit']
                    
                    if indicator_key not in indicators:
                        indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}
                        tx_curr_metadata_indicator_id = tx_curr_metadatas[0]
                    
                        indicators[indicator_key]['dataElement'] = tx_curr_metadata_indicator_id['id'].split('.')[0]
                        indicators[indicator_key]['categoryOptionCombo'] = tx_curr_metadata_indicator_id['id'].split('.')[1]
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
    
    def gender_match(self, patient, gender):
        
        if patient['patientSex'][0] == gender[0]:
            return True
        
        return False
    

    def arv_age_band_match(self, patient, age_band, end_period):
        
        end_period = pd.to_datetime(end_period)
        
        try:
            date_of_birth = pd.to_datetime(patient['patientAge'])
        except pd.errors.OutOfBoundsDatetime:
            self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid age: {patient['patientAge']}")
            return False
        
        years_between = end_period.year - date_of_birth.year

        if age_band == self.LESS_THAN_FIFTEEN and years_between < 15:
            return True
        
        if age_band == self.FIFTEEN_MORE and years_between >= 15:
            return True
        
        return False
    
    def arv_dispense_quntity_match(self, patient, arv_dispense_quantity):
        quantity = int(patient['pickupQuantity'])

        if arv_dispense_quantity == 'Less than 3 months' and quantity < 90:
            return True
        
        if arv_dispense_quantity == '3 to 5 months' and (quantity >= 90 and quantity <= 150):
            return True
        
        if arv_dispense_quantity == '6 or more months' and quantity >= 180:
            return True
        
        return False



