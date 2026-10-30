from abc import ABC, abstractmethod

class ComputeTxTbDenominatorDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']

    RESULTS = ['Positive', 'Negative']

    TB_TYPES = ['New', 'Already']

    LESS_THAN_ONE_YEAR = '<1'
        
    SIXTY_FIVE_MORE = '65+'

    @abstractmethod
    def compute(self, patients):
        pass