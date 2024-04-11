from abc import ABC, abstractmethod
import pandas as pd

class ComputeTxCurrUseCase(ABC):
        
        DAYS_EXPECTED = 27

        @abstractmethod
        def compute(self, patients: list, end_period: pd.Timestamp):
                pass

        @abstractmethod
        def is_currently_on_art(self, patient, end_period) -> bool:
                pass