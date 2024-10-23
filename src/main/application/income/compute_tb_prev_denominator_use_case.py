

from abc import ABC, abstractmethod

class ComputeTbPrevDenominatorUseCase(ABC):

    NEWLY_ENROLLED_DAYS = 180

    @abstractmethod
    def compute(self, enrolled_patients):
        pass