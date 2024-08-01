from abc import ABC, abstractmethod

class ComputeTxRttUseCase(ABC):

    DAYS_EXPECTED = 27

    MINIMUM_ART_DAYS = 58

    @abstractmethod
    def compute(self, enrolled_patients, start_period, end_period):
        pass