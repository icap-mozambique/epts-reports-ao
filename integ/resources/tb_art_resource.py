import pandas as pd

from src.infrastructure.adapters import TbArtIndicatorMetadataAdapter
from src.main.application.service import ComputeTbArtDisaggregationService
from src.main.application.service import ComputeTbArtNumeratorService
from src.infrastructure.forms import TB
from src.infrastructure.forms import PatientEventForm
from src.infrastructure.forms import PatientDemographicForm


class TbArtResource:

    def __init__(self, api, logger, start_period, end_period, period, org_units):
        self.api = api
        self.logger = logger
        self.start_period = start_period
        self.end_period = end_period
        self.period = period
        self.org_units = org_units

    def extract_tb_enrollements(self):
        
        enrollments = pd.DataFrame(columns=['enrollment', 'trackedEntity', 'program', 'status', 'orgUnit', 'enrolledAt', 'patientIdentifier', 'patientAge', 'patientSex','patientName', 'enrollmentDate', 'hivTestDate', 'testResult', 'artStartDate', 'artStatus'])
        enrollments.to_csv('TB_ART_ENROLLMENTS.csv', index=False)
        patient_demographics = PatientDemographicForm(self.api)
        patient_events = PatientEventForm(self.api)

        # Rewind to cover 1 year enrollments
        NINE_MONTHS = 9
        start_period_less_nine_months = (pd.to_datetime(self.start_period) - pd.DateOffset(months=NINE_MONTHS)).strftime('%Y-%m-%d')

        for org_unit in self.org_units:

            org_unit = org_unit['id']

            #get all patient enrollments
            patients_enrolled = self.api.get('tracker/enrollments', params={'orgUnit':org_unit, 'skipPaging':'true', 'program': TB, 'fields':'{,enrollment, enrolledAt, orgUnit, trackedEntity, program, status,}', 'enrolledAfter':f'{start_period_less_nine_months}', 'enrolledBefore':f'{self.end_period}', 'order':'enrolledAt:asc'})
            patients_enrolled = patients_enrolled.json()['instances']

            self.logger.info(f"Processing the facility: {org_unit}, a total of {len(patients_enrolled)} enrolled patient(s)")
            
            counter = 1

            for patient_enrolled in patients_enrolled:

                patient_demographics.add_demographics(patient_enrolled)
                patient_events.add_patient_last_tb_event(patient_enrolled)

                self.logger.info(f"From {len (patients_enrolled)} patietnts enrolled, {counter} (is) are ready to be processed.")
                counter = counter + 1 

            if patients_enrolled:
                patients_enrolled = pd.json_normalize(patients_enrolled)
                
                enrollments = pd.read_csv('TB_ART_ENROLLMENTS.csv')
                enrollments = pd.concat([enrollments, patients_enrolled])
                enrollments.to_csv('TB_ART_ENROLLMENTS.csv', index=False, encoding='utf-8')
    
    def process_tb_art_indicators(self):
        enrollments = pd.read_csv('TB_ART_ENROLLMENTS.csv')
        enrollments = enrollments.to_dict(orient='records')

        tb_art_numerator_use_case = ComputeTbArtNumeratorService()
        tb_art_patients = tb_art_numerator_use_case.compute(enrollments)

        tb_art_metadata_indicator_port = TbArtIndicatorMetadataAdapter(self.api)
        tb_art_numerator_disaggregation_use_case = ComputeTbArtDisaggregationService(self.logger, tb_art_metadata_indicator_port)
        tb_art_patients_disaggreation = tb_art_numerator_disaggregation_use_case.compute(tb_art_patients, self.end_period)

        combination = tb_art_patients_disaggreation

        if combination:
            # extract data
            indicators = pd.json_normalize(combination)
            indicators['period'] = self.period
            indicators = indicators[['dataElement','period','orgUnit', 'categoryOptionCombo','attributeOptionCombo', 'value']]
            indicators = indicators.sort_values(['orgUnit', 'dataElement', 'period'])
            indicators.to_csv('TB_ART_DATA.csv', index=False)

    def run(self):
        # self.extract_tb_enrollements()
        self.logger.info('The TB_ART_ENROLLMENTS.csv is completed.')

        self.process_tb_art_indicators()
        self.logger.info('The TB_ART_DATA.csv is completed.')