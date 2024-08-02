from abc import ABC, abstractmethod

class ComputePmtctStatDenominatorUseCase(ABC):

    @abstractmethod
    def compute(self, enrolled_patients):
        pass