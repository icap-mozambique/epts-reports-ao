from abc import ABC, abstractmethod

class ComputePmtctEidUseCase(ABC):

    @abstractmethod
    def compute(self, patients_enrolled):
        pass