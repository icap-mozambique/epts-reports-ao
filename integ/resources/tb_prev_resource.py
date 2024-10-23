import pandas as pd

from src.infrastructure.adapters import TbPrevNumeratorIndicatorMetadataAdapter
from src.infrastructure.adapters import TbPrevDenominatorIndicatorMetadataAdapter
from src.main.application.service import ComputeTbPrevDisaggregationService
from src.main.application.service import ComputeTbPrevNumeratorService
from src.main.application.service import ComputeTbPrevDenominatorService
from src.infrastructure.forms import PatientConsultationForm
from src.infrastructure.forms import PatientDemographicForm
from src.infrastructure.forms import PatientOutcomeForm
from src.infrastructure.forms import PatientPharmacyForm
from src.infrastructure.forms import CARE_AND_TREATMENT

class TbPrevResource:

    def __init__(self, api, logger, start_period, end_period, period, org_units):
        self.api = api
        self.logger = logger
        self.start_period = start_period
        self.end_period = end_period
        self.period = period
        self.org_units = org_units

    def extract_tb_prev_enrollments(self):
        enrollments = pd.DataFrame(columns=['enrollment', 'trackedEntity', 'program', 'status', 'orgUnit', 'enrolledAt', 'patientIdentifier', 'patientAge', 'patientSex','patientName', 
                                    'artStartDate', 'firstConsultationDate', 'inhStartDate', 'inhEndDate', 'transferedOut', 'dateOfTransfer','dead', 'dateOfDeath'])
        
        enrollments.to_csv('TB_PREV_ENROLLMENTS.csv', index=False)

        patient_demographics = PatientDemographicForm(self.api)
        patient_consultation= PatientConsultationForm(self.api)
        patient_pharmacy_form = PatientPharmacyForm(self.logger, self.api)
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

                patient_demographics.add_demographics(patient_enrolled)

                patient_consultation.add_first_consultation(patient_enrolled)

                patient_pharmacy_form.add_inh_start_date(patient_enrolled, self.start_period, self.end_period)
                patient_pharmacy_form.add_inh_end_date(patient_enrolled, self.start_period, self.end_period)

                patient_outcome_form.add_final_outcome(patient_enrolled)

                self.logger.info(f"From {len (patients_enrolled)} patients enrolled, {counter} (is) are ready to be processed.")
                counter = counter + 1 

            if patients_enrolled:
                patients_enrolled = pd.json_normalize(patients_enrolled)
                
                enrollments = pd.read_csv('TB_PREV_ENROLLMENTS.csv')
                enrollments = pd.concat([enrollments, patients_enrolled])
                enrollments.to_csv('TB_PREV_ENROLLMENTS.csv', index=False, encoding='utf-8')
    
    def process_tb_prev_indicators(self):
        enrollments = pd.read_csv('TB_PREV_ENROLLMENTS.csv')
        enrollments = enrollments.to_dict(orient='records')

        tb_prev_denominator_use_case = ComputeTbPrevDenominatorService(self.logger)
        patients_denominator = tb_prev_denominator_use_case.compute(enrollments)

        tb_prev_numerator_use_case = ComputeTbPrevNumeratorService(self.logger)
        patients_numerator = tb_prev_numerator_use_case.compute(patients_denominator, self.start_period, self.end_period)

        tb_prev_denominator_indicator_metadata_port = TbPrevDenominatorIndicatorMetadataAdapter(self.api)
        tb_prev_denominator_disaggregation_use_case = ComputeTbPrevDisaggregationService(tb_prev_denominator_indicator_metadata_port, self.logger)
        tb_prev_denominator_patients_disaggregation = tb_prev_denominator_disaggregation_use_case.compute(patients_denominator, self.end_period)

        tb_prev_numerator_indicator_metadata_port = TbPrevNumeratorIndicatorMetadataAdapter(self.api)
        tb_prev_numerator_disaggregation_use_case = ComputeTbPrevDisaggregationService(tb_prev_numerator_indicator_metadata_port, self.logger)
        tb_prev_numerator_patients_disaggregation = tb_prev_numerator_disaggregation_use_case.compute(patients_numerator, self.end_period)

        combination = tb_prev_denominator_patients_disaggregation + tb_prev_numerator_patients_disaggregation

        if combination:
            # extract data
            indicators = pd.json_normalize(combination)
            indicators['period'] = self.period
            indicators = indicators[['dataElement','period','orgUnit', 'categoryOptionCombo','attributeOptionCombo', 'value']]
            indicators = indicators.sort_values(['orgUnit', 'dataElement', 'period'])
            indicators.to_csv('TB_PREV_DATA.csv', index=False)
    
    def run(self):
        self.extract_tb_prev_enrollments()
        self.logger.info('The TB_PREV_ENROLLMENTS.csv is completed.')

        self.process_tb_prev_indicators()
        self.logger.info('The TB_PREV_DATA.csv is completed.')