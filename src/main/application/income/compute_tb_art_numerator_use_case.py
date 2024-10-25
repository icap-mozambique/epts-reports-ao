from abc import ABC, abstractmethod

class ComputeTbArtNumeratorUseCase(ABC):

    @abstractmethod
    def compute(self, patients_enrolled):
        pass