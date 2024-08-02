from abc import ABC, abstractmethod

class ComputeTbStatNumeratorUseCase(ABC):

    @abstractmethod
    def compute(self, tb_stat_patients):
        pass
