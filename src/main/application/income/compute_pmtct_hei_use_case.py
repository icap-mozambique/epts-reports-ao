from abc import ABC, abstractmethod

class ComputePmtctHeiUseCase(ABC):

    @abstractmethod
    def compute(self, patients_enrolled):
        pass