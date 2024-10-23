from abc import ABC, abstractmethod


class ComputeTbPrevDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']

    ART_START = ['New', 'Already']

    LESS_THAN_FIFTEEN = '<15'

    FIFTEEN_MORE = '15+'

    @abstractmethod
    def compute(self, patients, end_period):
        pass