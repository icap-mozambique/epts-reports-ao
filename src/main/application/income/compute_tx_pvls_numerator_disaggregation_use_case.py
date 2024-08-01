from abc import ABC, abstractmethod

class ComputeTxPlvsNumeratorDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']
    
    LESS_THAN_ONE_YEAR = '<1'
    
    SIXTY_FIVE_MORE = '65+'

    @abstractmethod
    def compute(self, tx_pvls_patients, end_period):
        pass