import pandas as pd

from src.main.application.income import ComputeTbPrevDenominatorUseCase

class ComputeTbPrevDenominatorService(ComputeTbPrevDenominatorUseCase):

    def __init__(self, logger):
        self.logger = logger

    def compute(self, enrolled_patients):

        patients = []

        for patient in enrolled_patients:

            if str(patient['artStartDate']) == 'nan':
                continue
            
            if str(patient['inhStartDate']) == 'nan':
                continue
            
            try:
                pd.to_datetime(patient['artStartDate'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid next ART start date: {patient['artStartDate']}")
                continue

            try:
                pd.to_datetime(patient['inhStartDate'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid next INH start date: {patient['inhStartDate']}")
                continue

            if pd.to_datetime(patient['inhStartDate']) < pd.to_datetime(patient['artStartDate']):
                continue

            patient['artStart'] = 'Already'

            if self.NEWLY_ENROLLED_DAYS >= (pd.to_datetime(patient['inhStartDate']) - pd.to_datetime(patient['artStartDate'])).days:
                patient['artStart'] = 'New'
            
            patients.append(patient)
        
        return patients
            


