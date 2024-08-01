from abc import ABC, abstractmethod

class ComputeTxRttDisaggregationUseCase(ABC):
    
    GENDERS = ['Female', 'Male']
     
    CD4S = ['<200 CD4', '>=200 CD4', 'CD4 Unknown', 'CD4 Not Eligible']

    LESS_THAN_ONE_YEAR = '<1'

    SIXTY_FIVE_MORE = '65+'

    CD4_MINIMUM_VALUE = 200

    THREE_MONTHS = 90

    FIVE_MONTHS = 150

    SIX_MONTHS = 180

    @abstractmethod
    def compute(self, rtt_patients, end_period):
        pass