from logging import Logger
import pandas as pd

from src.main.application.out import ConsultationPort
from src.main.application.out import LaboratoryPort
from src.main.application.income import ComputeTxPvlsDenominatorUseCase
from src.main.application.income import ComputeTxCurrUseCase

class ComputeTxPvlsDenominatorService(ComputeTxPvlsDenominatorUseCase):

    def __init__(self, logger: Logger, laboratory_port: LaboratoryPort, consultation_port: ConsultationPort) -> None:
        self.logger = logger
        self.laboratory_port = laboratory_port
        self.consultation_port = consultation_port

    def compute(self, art_patients, start_period, end_period):
        patients = []
        
        for patient in art_patients:

            if str(patient['dead']) != 'nan':
                 continue
            
            if str(patient['transferedOut']) != 'nan':
                continue
            
            try:
                pd.to_datetime(patient['patientAge'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid age: {patient['patientAge']}")
                continue
                
            self.laboratory_port.add_last_viral_load_result_date_of_the_period(patient, end_period)

            if str(patient['viralLoadRequestDate']) == 'nan':
                continue

            if str(patient['viralLoadResultValue']) == 'nan':
                continue

            try:
                last_viral_load_request_date = pd.to_datetime(patient['viralLoadRequestDate'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid viral load reult date: {patient['viralLoadResultDate']}")
                continue

            start_date_nine_months_before = pd.to_datetime(start_period) - pd.DateOffset(months=self.NINE_MONTHS)

            if start_date_nine_months_before < last_viral_load_request_date or last_viral_load_request_date > pd.to_datetime(end_period):
                continue
            
            art_start_date = pd.to_datetime(patient['artStartDate'])

            days_between = (last_viral_load_request_date - art_start_date).days

            self.consultation_port.add_patient_pregnant_or_breastfeeding_status(patient, end_period)

            if (('pregnant' in patient and patient['pregnant'] == True) or ('breastfeeding' in patient and patient['breastfeeding']== True)) and days_between >= self.DAYS_IN_ART:
                patients.append(patient)
                continue

            if ('pregnant' not in patient or 'breastfeeding' not in patient) and days_between >= self.SIX_MONTH_IN_ART:
                patients.append(patient)
                    
        return patients