from abc import ABC, abstractmethod

class ComputeHtsIndexCaseOfferedDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']

    LESS_THAN_ONE_YEAR = '<1'

    FIXTY_MORE = '50+'

    @abstractmethod
    def compute(self, offered_patients, end_period):
        pass
