from abc import ABC, abstractmethod

class ComputeTxTbNumeratorUseCase(ABC):

    @abstractmethod
    def compute(self, enrolled_patients):
        pass