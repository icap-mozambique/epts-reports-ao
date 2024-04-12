

from abc import ABC, abstractmethod

class ComputeTxPvlsNumeratorUseCase(ABC):

    @abstractmethod
    def compute(self, patients):
        pass