from abc import ABC, abstractmethod

class ComputePmtctStatNumeratorUseCase(ABC):

    @abstractmethod
    def compute(self, enrolled_patients):
        pass