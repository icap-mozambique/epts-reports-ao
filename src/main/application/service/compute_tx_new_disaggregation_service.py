import pandas as pd
from src.main.application.income.compute_tx_new_disaggretation_use_case import ComputeTxNewDisaggregationUseCase

class ComputeTxNewDisaggregationService(ComputeTxNewDisaggregationUseCase):

    def compute(self, patients: list, end_period):
        indicators = {}
        for patient in patients:
            if 'txNew' in patient:
                for gender in self.GENDERS:
                    if self.gender_match(patient, gender):
                        for cd4 in self.CD4S:
                            if(self.cd4_match(patient, cd4)):
                                for age_band in self.AGE_BANDS:
                                    if self.age_band_match(patient, age_band, end_period):
                                        indicator_key = age_band+'_'+gender+'_'+cd4
                                        if indicator_key not in indicators:
                                            indicators[indicator_key] = {'indicator_key': indicator_key, 'value':1}
                                        else:
                                            indicators[indicator_key]['value'] = indicators[indicator_key]['value'] + 1
                                        break
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
    
    def cd4_match(self, patient, cd4):
        if 'lastCD4' not in patient:
            return 'CD4 Unknown' == cd4
        
        if int(patient['lastCD4']) < self.CD4_MINIMUM_VALUE:
            return '<200' == cd4
        
        if int(patient['lastCD4']) >= self.CD4_MINIMUM_VALUE:
            return '>=200' == cd4
            



        

