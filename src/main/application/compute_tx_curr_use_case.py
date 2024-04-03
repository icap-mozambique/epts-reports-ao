import pandas as pd

DAYS_EXPECTED = 27 

class ComputeTxCurrUseCase:
        def compute(self, patients: list, period: pd.Timestamp):
               for patient in patients:
                      
                      if 'nextPickupDate' in patient:
                        last_art_date = pd.to_datetime(patient['nextPickupDate']) + pd.Timedelta(days=DAYS_EXPECTED)

                        if last_art_date >= pd.to_datetime(period) and ('transferedOut' or 'dead' not in patient):
                                patient['txCurr'] = True
                             
                      