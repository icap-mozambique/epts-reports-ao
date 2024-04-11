from abc import ABC, abstractmethod
import pandas as pd

class ComputeTxMlUseCase(ABC):

    DAYS_EXPECTED = 27

    @abstractmethod
    def compute(self, patients, start_date, end_date):
            pass