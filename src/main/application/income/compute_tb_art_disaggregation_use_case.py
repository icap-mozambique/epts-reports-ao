from abc import ABC, abstractmethod

class ComputeTbArtDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']

    ART_STATUS = ['New', 'Already']

    LESS_THAN_ONE_YEAR = '<1'
    
    SIXTY_FIVE_MORE = '65+'

    @abstractmethod
    def compute(self, patients, end_period):
        pass