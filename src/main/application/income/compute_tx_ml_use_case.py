from abc import ABC, abstractmethod
import pandas as pd

class ComputeTxMlUseCase(ABC):

    QUARTERLY_DAYS_EXPECTED = 27

    MONTHLY_DAYS_EXPECTED = 7

    @abstractmethod
    def compute(self, enrolled_patients, start_date, end_date, days):
            pass