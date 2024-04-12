
import pandas as pd
from src.main.application.income import ComputeTxCurrUseCase
from src.main.application.income import ComputeTxNewUseCase

class ComputeTxNewService(ComputeTxNewUseCase):

    def __init__(self, compute_tx_curr_use_case: ComputeTxCurrUseCase):
        self.compute_tx_curr_use_case = compute_tx_curr_use_case
    
    def compute(self, patients, start_period, end_period):

        for patient in patients:

            if self.compute_tx_curr_use_case.is_currently_on_art(patient, end_period):
                       
                    art_start_date = pd.to_datetime(patient['artStartDate'])
                    start_period = pd.to_datetime(start_period)
                    end_period = pd.to_datetime(end_period)

                    if art_start_date >= start_period and art_start_date <= end_period:
                        patient['txNew'] = True
    