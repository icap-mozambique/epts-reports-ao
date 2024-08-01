from abc import ABC, abstractmethod


class ComputeTxCurrDisaggregationUseCase(ABC):
    GENDERS = ['Female', 'Male']
      
    LESS_THAN_ONE_YEAR = '<1'
    
    SIXTY_FIVE_MORE = '65+'

    LESS_THAN_FIFTEEN = '<15'

    FIFTEEN_MORE = '15+'

    ARV_DISPENSE_QUANTITIES = ['Less than 3 months', '3 to 5 months', '6 or more months']

    @abstractmethod
    def compute(self, patients, end_period):
        pass