from abc import ABC, abstractmethod

class ComputeHtsIndexCaseAcceptedDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']

    LESS_THAN_ONE_YEAR = '<1'

    FIXTY_MORE = '50+'

    @abstractmethod
    def compute(self, index_case_acceptec_patients, end_period):
        pass