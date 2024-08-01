from logging import Logger
import pandas as pd

from src.main.application.income import ComputeTxCurrUseCase

class ComputeTxCurrService(ComputeTxCurrUseCase):
    
    def __init__(self, logger: Logger) -> None:
           self.logger = logger

    def compute(self, patients_enrolled: list, end_period: pd.Timestamp):
        patients = []
        
        for patient_enrolled in patients_enrolled:
                if self.is_currently_on_art(patient_enrolled, end_period):
                       patients.append(patient_enrolled)
                       
        return patients
                                
    def is_currently_on_art(self, patient, end_period) -> bool:
        if str(patient['nextPickupDate']) == 'nan':
                return False
                
        if str(patient['artStartDate']) == 'nan':
                return False
        
        try:
               pd.to_datetime(patient['artStartDate'])
        except pd.errors.OutOfBoundsDatetime:
               self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid next ART start date: {patient['artStartDate']}")
               return False
        
        try:
               last_art_date = pd.to_datetime(patient['nextPickupDate']) + pd.Timedelta(days=self.DAYS_EXPECTED)
        except pd.errors.OutOfBoundsDatetime:
               self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid next ART pickup date: {patient['nextPickupDate']}")
               return False
            
        if last_art_date >= pd.to_datetime(end_period) and str(patient['dead']) == 'nan':
                return True
        
        return False