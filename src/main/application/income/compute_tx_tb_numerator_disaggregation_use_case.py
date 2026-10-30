from abc import ABC, abstractmethod

class ComputeTxTbNumeratorDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']

    TB_TYPES = ['New', 'Already']

    LESS_THAN_ONE_YEAR = '<1'
        
    SIXTY_FIVE_MORE = '65+'

    @abstractmethod
    def compute(self, patients):
        pass