from abc import ABC, abstractmethod

class ComputePmtctStatDenominatorDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']
    
    LESS_THAN_TEN_YEARS = '<10'
    
    FIFTY_MORE = '50+'

    @abstractmethod
    def compute(self, pmtct_stat_patients, end_period):
        pass