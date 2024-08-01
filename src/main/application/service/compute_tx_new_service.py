
from logging import Logger
import pandas as pd
from src.main.application.income import ComputeTxCurrUseCase
from src.main.application.income import ComputeTxNewUseCase

class ComputeTxNewService(ComputeTxNewUseCase):

    def __init__(self, compute_tx_curr_use_case: ComputeTxCurrUseCase, logger: Logger):
        self.compute_tx_curr_use_case = compute_tx_curr_use_case
        self.logger = logger
    
    def compute(self, patients, start_period, end_period):
        tx_new_patients = []

        for patient in patients:
             
             if not self.compute_tx_curr_use_case.is_currently_on_art(patient, end_period):
                 continue
             
             try:
                 art_start_date = pd.to_datetime(patient['artStartDate'])
             except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid ART start date: {patient['artStartDate']}")
                continue
             
             start_period = pd.to_datetime(start_period)
             end_period = pd.to_datetime(end_period)
             
             if art_start_date >= start_period and art_start_date <= end_period:
                 tx_new_patients.append(patient)
        
        return tx_new_patients
    