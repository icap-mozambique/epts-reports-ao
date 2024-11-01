from abc import ABC, abstractmethod

class ComputeTxPvlsDenominatorUseCase(ABC):

    DAYS_IN_ART = 90
    
    SIX_MONTH_IN_ART = 180

    NINE_MONTHS = 9
    
    @abstractmethod
    def compute(self, patients, end_period):
        pass