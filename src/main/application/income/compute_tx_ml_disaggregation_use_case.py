from abc import ABC, abstractmethod


class ComputeTxMlDisaggregationUseCase(ABC):
    GENDERS = ['Female', 'Male']
    
    LESS_THAN_ONE_YEAR = '<1'
    
    SIXTY_FIVE_MORE = '65+'

    OUTCOMES = ['Died','Lost to Follow-Up (<3 Months Treatment)', 'Lost to Follow-Up (3-5 Months Treatment)', 'Lost to Follow-Up (6+ Months Treatment)', 'Transferred Out', 'Refused (Stopped) Treatment'] 

    @abstractmethod
    def compute(self, patients, end_period):
        pass