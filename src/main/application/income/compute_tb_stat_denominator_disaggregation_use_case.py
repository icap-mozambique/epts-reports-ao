from abc import ABC, abstractmethod

class ComputeTbStatDenominatorDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']
    
    LESS_THAN_ONE_YEAR = '<1'
    
    FIFTY_MORE = '50+'

    @abstractmethod
    def compute(self, tb_stat_patients, end_period):
        pass