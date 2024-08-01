from abc import ABC, abstractmethod

class ComputePmtctArtNumeratorUseCase(ABC):

    @abstractmethod
    def compute(self, enrolled_patients):
        pass