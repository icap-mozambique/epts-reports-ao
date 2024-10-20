import pandas as pd

from src.infrastructure.forms import PatientDemographicForm
from src.infrastructure.forms import PatientOutcomeForm
from src.infrastructure.forms import CARE_AND_TREATMENT
from src.infrastructure.adapters import ConsultationAdapter
from src.infrastructure.adapters import LaboratoryAdapter
from src.infrastructure.adapters import PharmacyAdapter
from src.infrastructure.adapters import TxMlIndicatorMetadataAdapter
from src.infrastructure.adapters import TxPvlsDenominatorIndicatorMetadataAdapter
from src.infrastructure.adapters import TxPvlsDenominatorPregBreastIndicatorMetadataAdapter
from src.infrastructure.adapters import TxPvlsNumeratorIndicatorMetadataAdapter
from src.infrastructure.adapters import TxPvlsNumeratorPregBreastIndicatorMetadataAdapter
from src.infrastructure.adapters import TxRttIndicatorMetadataAdapter
from src.infrastructure.adapters import TxRttIttIndicatorMetadataAdapter
from src.infrastructure.forms import PatientConsultationForm
from src.infrastructure.forms import PatientLaboratoryForm
from src.infrastructure.forms import PatientPharmacyForm
from src.main.application.service import ComputeTxCurrDisaggregationService
from src.main.application.service import ComputeTxMlDisaggregationService
from src.main.application.service import ComputeTxMlService
from src.main.application.service import ComputeTxNewDisaggregationService
from src.main.application.service import ComputeTxPvlsDenominatorDisaggregationService
from src.main.application.service import ComputeTxPvlsDenominatorService
from src.main.application.service import ComputeTxPvlsNumeratorDisaggregationService
from src.main.application.service import ComputeTxPvlsNumeratorService
from src.main.application.service import ComputeTxRttDisaggregationService
from src.main.application.service import ComputeTxRttService
from src.infrastructure.adapters import ArvDispenseIndicatorMetadataAdapter
from src.infrastructure.adapters import TxNewIndicatorMetadataAdapter
from src.infrastructure.adapters import TxCurrIndicatorMetadataAdapter
from src.main.application.service import ComputeTxNewService
from src.main.application.service import ComputeTxCurrService

class TxResource:

    def __init__(self, api, logger, start_period, end_period, period):
        self.logger = logger
        self.api = api
        self.org_units = self.api.get('organisationUnitGroups/gH2DlwAo1ja', params={'fields':'organisationUnits[id, name]'}).json()['organisationUnits']
        self.start_period = start_period
        self.end_period = end_period
        self.period = period
    
    def prepare_tx_indicators(self):

        self.tx_curr_service = ComputeTxCurrService(self.logger)
        self.tx_new_service = ComputeTxNewService(self.tx_curr_service, self.logger)

        tx_curr_indicator_metadata_port = TxCurrIndicatorMetadataAdapter(self.api)
        arv_dispense_indicator_metadata_port = ArvDispenseIndicatorMetadataAdapter(self.api)
        tx_new_indicator_metadata_port = TxNewIndicatorMetadataAdapter(self.api)

        self.tx_curr_disaggregation_service = ComputeTxCurrDisaggregationService(tx_curr_indicator_metadata_port, arv_dispense_indicator_metadata_port, self.logger)
        self.tx_new_disaggretation_service = ComputeTxNewDisaggregationService(tx_new_indicator_metadata_port, self.logger)

        tx_ml_indicator_metadata_port = TxMlIndicatorMetadataAdapter(self.api)
        self.tx_ml_service = ComputeTxMlService(self.logger)
        self.tx_ml_disaggregation_service = ComputeTxMlDisaggregationService(tx_ml_indicator_metadata_port)

        patient_consultation_form = PatientConsultationForm(self.api)
        consultation_port = ConsultationAdapter(patient_consultation_form)
        patient_laboratoty_form = PatientLaboratoryForm(self.logger,self.api)
        laboratory_port = LaboratoryAdapter(patient_laboratoty_form)

        self.tx_pvls_denominator_service = ComputeTxPvlsDenominatorService(self.logger, self.tx_curr_service, laboratory_port, consultation_port)
        self.tx_pvls_numerator_service = ComputeTxPvlsNumeratorService()

        tx_pvls_denominator_indicator_metadata_port = TxPvlsDenominatorIndicatorMetadataAdapter(self.api)
        tx_pvls_denominator_pred_breast_indicator_metadata_port = TxPvlsDenominatorPregBreastIndicatorMetadataAdapter(self.api)
        self.tx_pvls_denominator_disaggregation_service = ComputeTxPvlsDenominatorDisaggregationService(tx_pvls_denominator_indicator_metadata_port, tx_pvls_denominator_pred_breast_indicator_metadata_port)

        tx_pvls_numerator_indicator_metadata_port = TxPvlsNumeratorIndicatorMetadataAdapter(self.api)
        tx_pvls_numerator_pred_breast_indicator_metadata_port = TxPvlsNumeratorPregBreastIndicatorMetadataAdapter(self.api)
        self.tx_pvls_numerator_disaggregation_service = ComputeTxPvlsNumeratorDisaggregationService(tx_pvls_numerator_indicator_metadata_port, tx_pvls_numerator_pred_breast_indicator_metadata_port)

        pharmacy_form = PatientPharmacyForm(self.logger, self.api)
        pharmacy_port = PharmacyAdapter(pharmacy_form)
        tx_rtt_indicator_metadata_port = TxRttIndicatorMetadataAdapter(self.api)
        tx_rtt_itt_indicator_metadata_port = TxRttIttIndicatorMetadataAdapter(self.api)
        self.tx_rtt_service = ComputeTxRttService(self.logger, pharmacy_port, self.tx_curr_service)
        self.tx_rtt_disaggregation_service = ComputeTxRttDisaggregationService(self.logger, tx_rtt_indicator_metadata_port, tx_rtt_itt_indicator_metadata_port)


    def extract_tx_enrollments(self):
        enrollments = pd.DataFrame(columns=['enrollment', 'trackedEntity', 'program', 'status', 'orgUnit', 'enrolledAt', 'patientIdentifier', 'patientAge', 'patientSex','patientName', 
                                    'artStartDate', 'firstConsultationDate','pickupQuantity', 'lastPickupDate', 'nextPickupDate', 'lastCD4', 'viralLoadResultDate', 
                                    'viralLoadResultValue', 'transferedOut', 'dateOfTransfer','dead', 'dateOfDeath'])
        
        enrollments.to_csv('TX_ENROLLMENTS.csv', index=False)

        patient_demographics = PatientDemographicForm(self.api)
        patient_consultation= PatientConsultationForm(self.api)
        patient_pharmacy_form = PatientPharmacyForm(self.logger, self.api)
        patient_laboratory_from = PatientLaboratoryForm(self.logger,self.api)
        patient_outcome_form = PatientOutcomeForm(self.api)

        # Load patients enrolled
        for org_unit in self.org_units:

            org_unit = org_unit['id']

            #get all patient enrollments
            patients_enrolled = self.api.get('tracker/enrollments', params={'orgUnit':org_unit, 'skipPaging':'true', 'program': CARE_AND_TREATMENT, 'fields':'{,enrollment, enrolledAt, orgUnit, trackedEntity, program, status,}'})
            patients_enrolled = patients_enrolled.json()['instances']

            self.logger.info(f"Processing the facility: {org_unit}, a total of {len(patients_enrolled)} enrolled patient(s)")
            
            counter = 1

            for patient_enrolled in patients_enrolled:
                patient_id = patient_enrolled['trackedEntity']

                patient_demographics.add_demographics(patient_enrolled)

                patient_consultation.add_first_consultation(patient_enrolled)

                patient_pharmacy_form.add_last_pharmacy(patient_enrolled, self.end_period)

                patient_laboratory_from.add_laboratory(patient_enrolled)

                patient_outcome_form.add_final_outcome(patient_enrolled)

                self.logger.info(f"From {len (patients_enrolled)} patients enrolled, {counter} (is) are ready to be processed.")
                counter = counter + 1 

            if patients_enrolled:
                patients_enrolled = pd.json_normalize(patients_enrolled)
                
                enrollments = pd.read_csv('TX_ENROLLMENTS.csv')
                enrollments = pd.concat([enrollments, patients_enrolled])
                enrollments.to_csv('TX_ENROLLMENTS.csv', index=False, encoding='utf-8')
    
    def process_tx_indicators(self, start_period, end_period):
        enrollments = pd.read_csv('TX_ENROLLMENTS.csv')
        enrollments = enrollments.to_dict(orient='records')

        tx_curr_patients = self.tx_curr_service.compute(enrollments, end_period)
        tx_curr_patients_disaggregation = self.tx_curr_disaggregation_service.compute(tx_curr_patients, end_period)

        tx_new_patients = self.tx_new_service.compute(tx_curr_patients, start_period, end_period)
        tx_new_patients_disaggregation = self.tx_new_disaggretation_service.compute(tx_new_patients, end_period)

        tx_ml_patients = self.tx_ml_service.compute(enrollments, start_period, end_period, ComputeTxMlService.QUARTERLY_DAYS_EXPECTED)
        tx_ml_patients_disaggregation = self.tx_ml_disaggregation_service.compute(tx_ml_patients, end_period)

        tx_pvls_denominator_patients = self.tx_pvls_denominator_service.compute(tx_curr_patients, end_period)
        tx_pvls_denominator_patients_disaggregation = self.tx_pvls_denominator_disaggregation_service.compute(tx_pvls_denominator_patients, end_period)

        tx_pvls_numerator_patients = self.tx_pvls_numerator_service.compute(tx_pvls_denominator_patients)
        tx_pvls_numerator_patients_disaggregation = self.tx_pvls_numerator_disaggregation_service.compute(tx_pvls_numerator_patients, end_period)

        tx_rtt_patients = self.tx_rtt_service.compute(enrollments, start_period, end_period)
        tx_rtt_patients_disaggregation = self.tx_rtt_disaggregation_service.compute(tx_rtt_patients, end_period)

        combination = tx_curr_patients_disaggregation + tx_new_patients_disaggregation + tx_ml_patients_disaggregation + tx_pvls_denominator_patients_disaggregation + tx_pvls_numerator_patients_disaggregation + tx_rtt_patients_disaggregation

        if combination:
            # extract data
            indicators = pd.json_normalize(combination)
            indicators['period'] = self.period
            indicators = indicators[['dataElement','period','orgUnit', 'categoryOptionCombo','attributeOptionCombo', 'value']]
            indicators = indicators.sort_values(['orgUnit', 'dataElement', 'period'])
            indicators.to_csv('TX_DATA.csv', index=False)

    def run(self):
        self.prepare_tx_indicators()
        
        self.extract_tx_enrollments()
        self.logger.info("The TX_ENROLLMENTS.csv file is completed.")
        
        self.process_tx_indicators(self.start_period, self.end_period)
        self.logger.info("The TX_DATA.csv file is completed.")
        
        return {'message':'Data was successfully processed.'}