from abc import ABC, abstractmethod

class ComputePmtctStatNumeratorDisaggregationUseCase(ABC):

    GENDERS = ['Female']

    RESULTS = ['Known at Entry Positive', 'Newly Identified Positive', 'Newly Identified Negative', 'Recent Negative']
    
    LESS_THAN_TEN_YEARS = '<10'
    
    FIFTY_MORE = '50+'

    @abstractmethod
    def compute(self, pmtct_stat_patients, end_period):
        pass