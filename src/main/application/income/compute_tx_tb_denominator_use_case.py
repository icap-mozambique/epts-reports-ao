from abc import ABC, abstractmethod

class ComputeTxTbDenominatorUseCase(ABC):

    @abstractmethod
    def compute(self, enrolled_patients):
        pass