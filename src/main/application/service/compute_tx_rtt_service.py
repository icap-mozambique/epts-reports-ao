from logging import Logger
import pandas as pd
from src.main.application.income import ComputeTxCurrUseCase
from src.main.application.out import PharmacyPort
from src.main.application.income import ComputeTxRttUseCase

class ComputeTxRttService(ComputeTxRttUseCase):

    def __init__(self, logger: Logger, pharmacy_port: PharmacyPort, tx_curr_use_case: ComputeTxCurrUseCase) -> None:
        self.logger = logger
        self.pharmacy_port = pharmacy_port
        self.tx_curr_use_case = tx_curr_use_case

    def compute(self, enrolled_patients, start_period, end_period):
        
        patients = []
        
        for enrolled_patient in enrolled_patients:

            if str(enrolled_patient['patientAge']) == 'nan' or str(enrolled_patient['artStartDate']) == 'nan' or str(enrolled_patient['nextPickupDate']) == 'nan':
                continue

            try:
               pd.to_datetime(enrolled_patient['artStartDate'])
            except pd.errors.OutOfBoundsDatetime:
               self.logger.warning(f"The patient: {enrolled_patient['trackedEntity']} - {enrolled_patient['patientIdentifier']} - {enrolled_patient['patientName']} - {enrolled_patient['patientSex']} of facility {enrolled_patient['orgUnit']} was not processed due to invalid next ART start date: {enrolled_patient['artStartDate']}")
               continue

            try:
                 pd.to_datetime(enrolled_patient['patientAge'])
            except pd.errors.OutOfBoundsDatetime:
                self.logger.warning(f"The patient: {enrolled_patient['trackedEntity']} - {enrolled_patient['patientIdentifier']} - {enrolled_patient['patientName']} - {enrolled_patient['patientSex']} of facility {enrolled_patient['orgUnit']} was not processed due to invalid birthdate: {enrolled_patient['patientAge']}")
                continue

            if self.patient_left_prior_reporting_period(enrolled_patient, start_period) and self.tx_curr_use_case.is_currently_on_art(enrolled_patient, end_period):
                prior_last_art_date = pd.to_datetime(enrolled_patient['priorNextPickupDate']) + pd.Timedelta(days=self.DAYS_EXPECTED)
                enrolled_patient['priorLastArtDate'] = prior_last_art_date
                patients.append(enrolled_patient)
                continue
            
            if self.patient_left_within_reporting_period(enrolled_patient, end_period) and self.tx_curr_use_case.is_currently_on_art(enrolled_patient, end_period):
                last_art_date = pd.to_datetime(enrolled_patient['nextPickupDate']) + pd.Timedelta(days=self.DAYS_EXPECTED)
                enrolled_patient['lastArtDate'] = last_art_date
                patients.append(enrolled_patient)
        
        return patients
    
    def patient_left_prior_reporting_period(self, patient, period):

        if (pd.to_datetime(period) - pd.to_datetime(patient['artStartDate'])).days < self.MINIMUM_ART_DAYS:
            return False

        self.pharmacy_port.find_last_pickup_of_the_period(patient, period)

        if 'priorNextPickupDate' not in patient:
            return False
        
        try:
            prior_last_art_date = pd.to_datetime(patient['priorNextPickupDate']) + pd.Timedelta(days=self.DAYS_EXPECTED)
        except pd.errors.OutOfBoundsDatetime:
            self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid prior next ART pickup date: {patient['priorNextPickupDate']}")
            return False

        if prior_last_art_date >= pd.to_datetime(period):
            return False
        
        return True
    
    def patient_left_within_reporting_period(self, patient, period):
        if (pd.to_datetime(period) - pd.to_datetime(patient['artStartDate'])).days < self.MINIMUM_ART_DAYS:
            return False
        
        try:
            last_art_date = pd.to_datetime(patient['nextPickupDate']) + pd.Timedelta(days=self.DAYS_EXPECTED)
        except pd.errors.OutOfBoundsDatetime:
            self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed due to invalid prior next ART pickup date: {patient['priorNextPickupDate']}")
            return False

        if last_art_date >= pd.to_datetime(period):
            return False
        
        return True

