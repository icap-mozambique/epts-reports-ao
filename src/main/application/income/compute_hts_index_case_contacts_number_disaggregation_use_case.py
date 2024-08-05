from abc import ABC, abstractmethod


class ComputeHtsIndexCaseContactsNumberDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']

    LESS_THAN_FIFTEEN_YEARS = '<15'

    GREATER_THAN_FIFTEEN_MORE = '15+'

    @abstractmethod
    def compute(self, index_case_contacts, end_period):
        pass