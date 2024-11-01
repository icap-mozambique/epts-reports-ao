from abc import ABC, abstractmethod

class ComputePmtctStatNumeratorUseCase(ABC):

    @abstractmethod
    def compute(self, enrolled_patients, start_period):
        pass