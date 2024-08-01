from logging import Logger
import pandas as pd
from src.main.application.income import ComputeTxMlUseCase

class ComputeTxMlService(ComputeTxMlUseCase):

    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def compute(self, enrolled_patients, start_date, end_date, days):
            patients = []

            for patient in enrolled_patients:
                if str(patient['patientAge']) == 'nan' or str(patient['artStartDate']) == 'nan' or str(patient['nextPickupDate']) == 'nan':
                     continue
                
                try:
                     pd.to_datetime(patient['patientAge'])
                except pd.errors.OutOfBoundsDatetime:
                    self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid birthdate: {patient['patientAge']}")
                    continue

                try:
                     last_art_date = pd.to_datetime(patient['nextPickupDate']) + pd.Timedelta(days=days)
                except pd.errors.OutOfBoundsDatetime:
                    self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid next ART pickup date: {patient['nextPickupDate']}")
                    continue

                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)

                if last_art_date >= start_date and last_art_date <= end_date:
                     patients.append(patient)

            return patients