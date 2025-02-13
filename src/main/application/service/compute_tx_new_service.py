
from logging import Logger
import pandas as pd

from src.main.application.income import ComputeTxNewUseCase

class ComputeTxNewService(ComputeTxNewUseCase):

    def __init__(self, logger: Logger):
        self.logger = logger
    
    def compute(self, patients, start_period, end_period):
        tx_new_patients = []

        for patient in patients:
             
             if patient['entryType'] == 'TRANSFERIDO':
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
    