from logging import Logger
import pandas as pd

from src.main.application.out import ConsultationPort
from src.main.application.out import LaboratoryPort
from src.main.application.income import ComputeTxPvlsDenominatorUseCase
from src.main.application.income import ComputeTxCurrUseCase

class ComputeTxPvlsDenominatorService(ComputeTxPvlsDenominatorUseCase):

    def __init__(self, logger: Logger, tx_curr_use_case: ComputeTxCurrUseCase, laboratory_port: LaboratoryPort, consultation_port: ConsultationPort) -> None:
        self.logger = logger
        self.tx_curr_use_case = tx_curr_use_case
        self.laboratory_port = laboratory_port
        self.consultation_port = consultation_port

    def compute(self, art_patients, end_period):
        patients = []
        
        for patient in art_patients:
            
            try:
                pd.to_datetime(patient['patientAge'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid age: {patient['patientAge']}")
                continue

            if self.tx_curr_use_case.is_currently_on_art(patient, end_period):
                
                self.laboratory_port.add_last_viral_load_result_date_of_the_period(patient, end_period)

                if str(patient['viralLoadResultDate']) == 'nan':
                    continue
                
                art_start_date = pd.to_datetime(patient['artStartDate'])

                try:
                    last_vl_date = pd.to_datetime(patient['viralLoadResultDate'])
                except pd.errors.OutOfBoundsDatetime:
                    self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid viral load reult date: {patient['viralLoadResultDate']}")
                    continue

                days_between = (last_vl_date - art_start_date).days

                if days_between >= self.DAYS_IN_ART:
                    self.consultation_port.add_patient_pregnant_or_breastfeeding_status(patient, end_period)
                    patients.append(patient)
                    
        return patients