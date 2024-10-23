from abc import ABC, abstractmethod


class ComputeTbPrevNumeratorUseCase(ABC):

    THREE_MONTHS = 3

    @abstractmethod
    def compute(self, patients_enrolled, start_period, end_period):
        pass