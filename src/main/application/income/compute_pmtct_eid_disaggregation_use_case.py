from abc import ABC, abstractmethod


class ComputePmtctEidDisaggregationUseCase(ABC):

    TESTS_NUMBER = ['EID First Test','EID Second Test or more']

    LESS_THAN_OR_EQUAL_TWO_MONTHS = '<= 2 months'
    
    LESS_THAN_OR_EQUAL_TWELVE_MONTHS = '2 - 12 months'

    @abstractmethod
    def compute(self, pmtct_eid_patients, end_period):
        pass