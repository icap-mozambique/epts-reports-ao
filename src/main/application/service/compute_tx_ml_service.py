import pandas as pd
from src.main.application.income import ComputeTxMlUseCase

class ComputeTxMlService(ComputeTxMlUseCase):

    def compute(self, patients, start_date, end_date):
            for patient in patients:
                if 'nextPickupDate' in patient:
                    last_art_date = pd.to_datetime(patient['nextPickupDate']) + pd.Timedelta(days=self.DAYS_EXPECTED)

                    start_date = pd.to_datetime(start_date)
                    end_date = pd.to_datetime(end_date)

                    if last_art_date >= start_date and last_art_date <= end_date:
                        patient['txML'] = True