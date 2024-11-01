

from abc import ABC, abstractmethod

class ComputeTxPvlsNumeratorUseCase(ABC):

    MAX_VIRAL_LOAD_SUPPPRESSED_VALUE = 1000

    @abstractmethod
    def compute(self, patients):
        pass