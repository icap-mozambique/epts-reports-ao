from abc import ABC, abstractmethod

class ComputeTxPvlsDenominatorUseCase(ABC):

    DAYS_IN_ART = 90
    
    @abstractmethod
    def compute(self, patients, end_period):
        pass