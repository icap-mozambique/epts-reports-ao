from abc import ABC, abstractmethod

class ComputeTbStatNumeratorDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']

    RESULTS = ['Known at Entry Positive', 'Newly Identified Positive', 'Newly Identified Negative']
    
    LESS_THAN_ONE_YEAR = '<1'
    
    FIFTY_MORE = '50+'

    @abstractmethod
    def compute(self, tb_stat_patients, end_period):
        pass