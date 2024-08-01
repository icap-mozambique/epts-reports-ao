from abc import ABC, abstractmethod

class ComputePmtctArtNumeratorDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']

    ARTS = ['New', 'Already']
    
    LESS_THAN_TEN_YEARS = '<10'
    
    SIXTY_FIVE_MORE = '65+'

    @abstractmethod
    def compute(self, pmtct_art_patients, end_period):
        pass