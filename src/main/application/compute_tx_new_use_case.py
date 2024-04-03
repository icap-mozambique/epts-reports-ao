import pandas as pd

DAYS_EXPECTED = 27

class ComputeTxNewUseCase:

    def compute(self, patients, start_period, end_period):
        for patient in patients:
            if 'artStartDate' in patient:
                art_start_date = pd.to_datetime(patient['artStartDate'])
                start_period = pd.to_datetime(start_period)
                end_period = pd.to_datetime(end_period)

                if art_start_date >= start_period and art_start_date <= end_period:
                    
                    if 'nextPickupDate' in patient:
                        last_art_date = pd.to_datetime(patient['nextPickupDate']) + pd.Timedelta(days=DAYS_EXPECTED)
                        
                        if last_art_date >= end_period and ('transferedOut' or 'dead' not in patient):
                            patient['txNew'] = True