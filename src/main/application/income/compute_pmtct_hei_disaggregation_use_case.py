from abc import ABC, abstractmethod


class ComputePmtctHeiDisaggregationUseCase(ABC):

    RESULTS = ['Positive', 'Negative']

    LESS_THAN_OR_EQUAL_TWO_MONTHS = '<= 2 months'
    
    LESS_THAN_OR_EQUAL_TWELVE_MONTHS = '2 - 12 months'

    @abstractmethod
    def compute(self, pmtct_hei_patients, end_period):
        pass