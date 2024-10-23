import pandas as pd

from src.main.application.income import ComputeTbPrevNumeratorUseCase

class ComputeTbPrevNumeratorService(ComputeTbPrevNumeratorUseCase):

    def __init__(self, logger):
        self.logger = logger

    def compute(self, patients_enrolled, start_period, end_period):
        patients = []

        for patient in patients_enrolled:
            
            if str(patient['inhEndDate']) == 'nan':
                continue

            try:
                pd.to_datetime(patient['inhEndDate'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid next INH end date: {patient['inhEndDate']}")
                continue

            start_period_less_three_months = (pd.to_datetime(start_period) - pd.DateOffset(months=self.THREE_MONTHS))
            end_period = pd.to_datetime(end_period)

            if pd.to_datetime(patient['inhEndDate']) >= start_period_less_three_months and pd.to_datetime(patient['inhEndDate']) <= end_period :
                patients.append(patient)
        
        return patients

