import pandas as pd

from src.infrastructure.adapters import TbStatDenominatorIndicatorMetadataAdapter
from src.infrastructure.adapters import TbStatNumeratorIndicatorMetadataAdapter
from src.infrastructure.forms import PatientEventForm
from src.main.application.service import ComputeTbStatDenominatorDisaggregationService
from src.main.application.service import ComputeTbStatNumeratorDisaggregationService
from src.main.application.service import ComputeTbStatNumeratorService
from src.infrastructure.forms import TB
from src.infrastructure.forms import PatientDemographicForm

class TbResource:

    def __init__(self, api, logger, start_period, end_period, period, org_units):
        self.api = api
        self.logger = logger
        self.start_period = start_period
        self.end_period = end_period
        self.period = period
        self.org_units = org_units
    
    def extract_tb_enrollments(self):
        enrollments = pd.DataFrame(columns=['enrollment', 'trackedEntity', 'program', 'status', 'orgUnit', 'enrolledAt', 'patientIdentifier', 'patientAge', 'patientSex','patientName', 'enrollmentDate', 'hivTestDate', 'testResult', 'artStartDate', 'artStatus'])
        enrollments.to_csv('TB_ENROLLMENTS.csv', index=False)
        patient_demographics = PatientDemographicForm(self.api)
        patient_events = PatientEventForm(self.api)

        for org_unit in self.org_units:

            org_unit = org_unit['id']

            #get all patient enrollments
            patients_enrolled = self.api.get('tracker/enrollments', params={'orgUnit':org_unit, 'skipPaging':'true', 'program': TB, 'fields':'{,enrollment, enrolledAt, orgUnit, trackedEntity, program, status,}', 'enrolledAfter':f'{self.start_period}', 'enrolledBefore':f'{self.end_period}', 'order':'enrolledAt:asc'})
            patients_enrolled = patients_enrolled.json()['instances']

            self.logger.info(f"Processing the facility: {org_unit}, a total of {len(patients_enrolled)} enrolled patient(s)")
            
            counter = 1

            for patient_enrolled in patients_enrolled:

                patient_demographics.add_demographics(patient_enrolled)
                patient_events.add_patient_first_tb_event(patient_enrolled)

                self.logger.info(f"From {len (patients_enrolled)} patietnts enrolled, {counter} (is) are ready to be processed.")
                counter = counter + 1 

            if patients_enrolled:
                patients_enrolled = pd.json_normalize(patients_enrolled)
                
                enrollments = pd.read_csv('TB_ENROLLMENTS.csv')
                enrollments = pd.concat([enrollments, patients_enrolled])
                enrollments.to_csv('TB_ENROLLMENTS.csv', index=False, encoding='utf-8')
    
    def process_tb_indicators(self):
        enrollments = pd.read_csv('TB_ENROLLMENTS.csv')
        enrollments = enrollments.to_dict(orient='records')

        tb_stat_denominator_indicator_metadata_port = TbStatDenominatorIndicatorMetadataAdapter(self.api)
        tb_stat_denominator_disaggregation_service = ComputeTbStatDenominatorDisaggregationService(self.logger, tb_stat_denominator_indicator_metadata_port)
        tb_stat_denominator_patients_disaggregation = tb_stat_denominator_disaggregation_service.compute(enrollments, self.end_period)

        tb_stat_numerator_service = ComputeTbStatNumeratorService()
        tb_stat_numerator_patients = tb_stat_numerator_service.compute(enrollments)

        tb_stat_numerator_indicator_metadata_port = TbStatNumeratorIndicatorMetadataAdapter(self.api)
        tb_stat_numerator_disaggregation_service = ComputeTbStatNumeratorDisaggregationService(self.logger, tb_stat_numerator_indicator_metadata_port)
        tb_stat_numerator_patients_disaggregation = tb_stat_numerator_disaggregation_service.compute(tb_stat_numerator_patients, self.end_period)

        combination = tb_stat_denominator_patients_disaggregation + tb_stat_numerator_patients_disaggregation

        if combination:
            # extract data
            indicators = pd.json_normalize(combination)
            indicators['period'] = self.period
            indicators = indicators[['dataElement','period','orgUnit', 'categoryOptionCombo','attributeOptionCombo', 'value']]
            indicators = indicators.sort_values(['orgUnit', 'dataElement', 'period'])
            indicators.to_csv('TB_DATA.csv', index=False)

    def run(self):
        self.extract_tb_enrollments()
        self.logger.info('The TB_ENROLLMENTS.csv file is completed.')

        self.process_tb_indicators(self)
        self.logger.info('The TB_DATA.csv is completed.')