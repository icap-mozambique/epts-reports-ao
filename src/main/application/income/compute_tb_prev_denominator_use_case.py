

from abc import ABC, abstractmethod

class ComputeTbPrevDenominatorUseCase(ABC):

    @abstractmethod
    def compute(self, enrolled_patients):
        pass