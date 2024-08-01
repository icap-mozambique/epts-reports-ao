import pandas as pd
from src.main.application.out import IndicatorMetadataPort
from src.main.application.income import ComputeTxRttDisaggregationUseCase

class ComputeTxRttDisaggregationService(ComputeTxRttDisaggregationUseCase):

    def __init__(self, logger, tx_rtt_indicator_metadata_port: IndicatorMetadataPort, tx_rtt_itt_indicator_metadata_port: IndicatorMetadataPort) -> None:
        self.logger = logger
        self.tx_rtt_indicator_metadata_port = tx_rtt_indicator_metadata_port
        self.tx_rtt_itt_indicator_metadata_port = tx_rtt_itt_indicator_metadata_port

    def compute(self, rtt_patients, end_period):

        tx_rtt_indicators_metadata = self.tx_rtt_indicator_metadata_port.find_indicator_metadata()
        tx_rtt_iit_indicators_metadata = self.tx_rtt_itt_indicator_metadata_port.find_indicator_metadata()

        indicators = {}

        for patient in rtt_patients:

            for gender in self.GENDERS:
                if not self.match_gender(patient, gender):
                    continue

                for cd4 in self.CD4S:
                    
                    if not self.match_cd4(patient, cd4):
                        continue

                    for age_band in self.tx_rtt_indicator_metadata_port.age_bands():

                        if not self.match_age_band(patient, age_band, end_period):
                            continue

                        if cd4 == '<200 CD4' and (age_band == '<1' or age_band == '1-4'):
                            continue

                        if cd4 == '>=200 CD4' and (age_band == '<1' or age_band == '1-4'):
                            continue

                        # the indicator pattern e.g: 5-9_F_>=200 CD4
                        indicator_key = age_band + '_' + gender[0] + '_' + cd4
                        self.update_indicator_value(patient, indicators, tx_rtt_indicators_metadata, indicator_key)

                        if 'priorLastArtDate' in patient:
                            number_of_itt_days = (pd.to_datetime(patient['lastPickupDate']) - pd.to_datetime(patient['priorLastArtDate'])).days
                        else:
                           number_of_itt_days = (pd.to_datetime(patient['lastPickupDate']) - pd.to_datetime(patient['lastArtDate'])).days 

                        # ITT less than 3 months
                        if number_of_itt_days < self.THREE_MONTHS:
                            indicator_key = 'Lost to Follow-Up (<3 Months Treatment)'
                            self.update_indicator_value(patient, indicators, tx_rtt_iit_indicators_metadata, indicator_key)
                            break

                        # ITT between 3 to 5 months
                        if number_of_itt_days >= self.THREE_MONTHS and number_of_itt_days <= self.FIVE_MONTHS:
                            indicator_key = 'Interruption in Treatment (3-5 Months Treatment)'
                            self.update_indicator_value(patient, indicators, tx_rtt_iit_indicators_metadata, indicator_key)
                            break
                        
                        # ITT between 3 to 5 months
                        if number_of_itt_days >= self.SIX_MONTHS:
                            indicator_key = 'Interruption In Treatment (6+ Months Treatment)'
                            self.update_indicator_value(patient, indicators, tx_rtt_iit_indicators_metadata, indicator_key)
                            break
        
        indicators = list(indicators.values())

        return indicators

    def match_gender(self, patient, gender):

        if patient['patientSex'][0] == gender[0]:
            return True
        
        return False

    def match_cd4(self, patient, cd4):

        if 'priorLastArtDate' in patient:
            eligibility_days = (pd.to_datetime(patient['lastPickupDate']) - pd.to_datetime(patient['priorLastArtDate'])).days
        else:
            eligibility_days = (pd.to_datetime(patient['lastPickupDate']) - pd.to_datetime(patient['lastArtDate'])).days

        if str(patient['lastCD4']) == 'nan' and 'CD4 Not Eligible' == cd4 and eligibility_days < self.SIX_MONTHS:
            return True
        
        if str(patient['lastCD4']) == 'nan' and 'CD4 Unknown' == cd4 and eligibility_days >= self.SIX_MONTHS:
            return True
        
        if str(patient['lastCD4']) != 'nan' and int(patient['lastCD4']) < self.CD4_MINIMUM_VALUE and '<200 CD4' == cd4:
            return True
        
        if str(patient['lastCD4']) != 'nan' and int(patient['lastCD4']) >= self.CD4_MINIMUM_VALUE and '>=200 CD4' == cd4:
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
    
    def update_indicator_value(self, patient, indicators, indicators_metadata, indicator_key ):

        metadatas = [indicator_metadata for indicator_metadata in indicators_metadata if indicator_key == indicator_metadata['indicator_key']]
                        
        if indicator_key not in indicators:
            indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}
            metadata = metadatas[0]
        
            indicators[indicator_key]['dataElement'] = metadata['id'].split('.')[0]
            indicators[indicator_key]['categoryOptionCombo'] = metadata['id'].split('.')[1]
            indicators[indicator_key]['attributeOptionCombo'] = ''
            indicators[indicator_key]['orgUnit'] = patient['orgUnit']

        else:
            indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1