from abc import ABC, abstractmethod

class ComputeHtsDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']
    
    RESULTS = ['Positive', 'Negative']

    LESS_THAN_ONE_YEAR = '<1'

    LESS_THAN_TEN_YEARS = '<10'
    
    FIXTY_MORE = '50+'

    @abstractmethod
    def compute(self, patients, end_period):
        pass