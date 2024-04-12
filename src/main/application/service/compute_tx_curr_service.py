import pandas as pd

from src.main.application.income import ComputeTxCurrUseCase

class ComputeTxCurrService(ComputeTxCurrUseCase):

    def compute(self, patients: list, end_period: pd.Timestamp):
                for patient in patients:
                        if self.is_currently_on_art(patient, end_period):
                                patient['txCurr'] = True
                                
    def is_currently_on_art(self, patient, end_period) -> bool:
            if 'nextPickupDate' in patient:
                    if 'artStartDate' in patient:
                        last_art_date = pd.to_datetime(patient['nextPickupDate']) + pd.Timedelta(days=self.DAYS_EXPECTED)
            
                        if last_art_date >= pd.to_datetime(end_period) and 'dead' not in patient:
                                return True