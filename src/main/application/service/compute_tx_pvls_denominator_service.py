from logging import Logger
import pandas as pd

from src.main.application.out import ConsultationPort
from src.main.application.out import LaboratoryPort
from src.main.application.income import ComputeTxPvlsDenominatorUseCase
from src.main.application.income import ComputeTxCurrUseCase

class ComputeTxPvlsDenominatorService(ComputeTxPvlsDenominatorUseCase):

    def __init__(self, logger: Logger, laboratory_port: LaboratoryPort, consultation_port: ConsultationPort, tx_curr_service: ComputeTxCurrUseCase) -> None:
        self.logger = logger
        self.laboratory_port = laboratory_port
        self.consultation_port = consultation_port
        self.tx_curr_service = tx_curr_service

    def compute(self, art_patients, start_period, end_period):
        patients = []
        
        for patient in art_patients:

            if not self.tx_curr_service.is_currently_on_art(patient, end_period):
                continue

            if str(patient['dead']) != 'nan':
                 continue
            
            if str(patient['transferedOut']) != 'nan':
                continue
            
            try:
                pd.to_datetime(patient['patientAge'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid age: {patient['patientAge']}")
                continue

            if str(patient['viralLoadResultValue']) == 'nan':
                continue

            if str(patient['viralLoadRequestDate']) == 'nan':
                continue

            try:
                last_viral_load_request_date = pd.to_datetime(patient['viralLoadRequestDate'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid viral load reult date: {patient['viralLoadResultDate']}")
                continue

            start_date_nine_months_before = pd.to_datetime(start_period) - pd.DateOffset(months=self.NINE_MONTHS)

            if not (last_viral_load_request_date >= start_date_nine_months_before and last_viral_load_request_date <= pd.to_datetime(end_period)):
                continue

            try:
                art_start_date = pd.to_datetime(patient['artStartDate'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid ART start Date: {patient['artStartDate']}")
                continue

            days_between = (last_viral_load_request_date - art_start_date).days

            if (patient['pregnant'] == True or patient['breastfeeding']== True) and days_between >= self.DAYS_IN_ART:
                patients.append(patient)
                continue

            if patient['pregnant'] and patient['breastfeeding'] and days_between >= self.SIX_MONTH_IN_ART:
                patients.append(patient)
                    
        return patients