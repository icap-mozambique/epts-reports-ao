import pandas as pd

from src.infrastructure.adapters import IndexCaseAcceptedIndicatorMetadataAdapter
from src.infrastructure.adapters import IndexCaseContactsNumberIndicatorMetadataAdapter
from src.infrastructure.adapters import IndexCaseIndicatorMetadataAdapter
from src.infrastructure.adapters import IndexCaseOfferedIndicatorMetadataAdapter
from src.infrastructure.forms import INDEX_CONTACTS_STAGE
from src.main.application.income import ComputeHtsIndexCaseAcceptedDisaggregationUseCase
from src.main.application.income import ComputeHtsIndexCaseContactsNumberDisaggregationUseCase
from src.main.application.income import ComputeHtsIndexCaseDisaggregationUseCase
from src.main.application.income import ComputeHtsIndexCaseOfferedDisaggregationUseCase
from src.main.application.income import ComputeHtsIndexCaseUseCase
from src.main.application.out import IndicatorMetadataPort
from src.main.application.service import ComputeHtsIndexCaseAcceptedDisaggregationService
from src.main.application.service import ComputeHtsIndexCaseAcceptedService
from src.main.application.service import ComputeHtsIndexCaseContactsNumberDisaggregationService
from src.main.application.service import ComputeHtsIndexCaseDisaggregationService
from src.main.application.service import ComputeHtsIndexCaseOfferedDisaggregationService
from src.main.application.service import ComputeHtsIndexCaseService
from src.infrastructure.forms import PatientDemographicForm
from src.infrastructure.forms import PatientEventForm
from src.infrastructure.forms import INDEX, INDEX_DETAILS_STAGE

class HtsIndexResource:

    def __init__(self, api, logger, start_period, end_period, period, org_units):
        self.api = api
        self.logger = logger
        self.start_period = start_period
        self.end_period = end_period
        self.period = period
        self.org_units = org_units

    
    def extract_index_enrollments(self):
        index_enrollments = pd.DataFrame(columns=['trackedEntity', 'program', 'status', 'orgUnit', 'patientIdentifier', 'patientAge', 'patientSex','patientName', 'childrenLessThan15Years', 'testPartner', 'numberOfContacts'])
        index_enrollments.to_csv('INDEX_ENROLLMENTS.csv', index=False)

        # Load patients envents
        patient_demographics = PatientDemographicForm(self.api)

        for org_unit in self.org_units:

            org_unit = org_unit['id']

            #get all patient events
            patients_enrolled = self.api.get('tracker/enrollments', params={'orgUnit':org_unit, 'skipPaging':'true', 'program': INDEX, 'fields':'{,enrollment, enrolledAt, orgUnit, trackedEntity, program, status,}', 'enrolledAfter':f'{self.start_period}', 'enrolledBefore':f'{self.end_period}', 'order':'enrolledAt:asc'})
            patients_enrolled = patients_enrolled.json()['instances']

            self.logger.info(f"Processing the facility: {org_unit}, a total of {len(patients_enrolled)} enrolled patient(s)")
            
            counter = 1

            for patient_enrolled in patients_enrolled:
                patient_demographics.add_demographics(patient_enrolled)

                self.logger.info(f"From {len (patients_enrolled)} patietnts enrolled, {counter} (is) are ready to be processed.")
                counter = counter + 1 

            if patients_enrolled:
                patients_enrolled = pd.json_normalize(patients_enrolled)
                
                enrollments = pd.read_csv('INDEX_ENROLLMENTS.csv')
                enrollments = pd.concat([enrollments, patients_enrolled])
                enrollments.to_csv('INDEX_ENROLLMENTS.csv', index=False, encoding='utf-8')
            
        
    def extract_contacts_enrollments(self):
        # index case contacts
        index_enrollments = pd.DataFrame(columns=['trackedEntity', 'program', 'status', 'orgUnit', 'patientAge', 'patientSex', 'ic_new_case', 'result', 'ic_date'])
        index_enrollments.to_csv('CONTACTS_INDEX_ENROLLMENTS.csv', index=False)

        # Load patients envents
        patient_events_port = PatientEventForm(self.api)

        for org_unit in self.org_units:

            org_unit = org_unit['id']

            #get all patient events
            patients_events = patient_events_port.find_index_contacts_by_unit_and_period(org_unit, self.start_period, self.end_period)

            self.logger.info(f"Processing the facility: {org_unit}, a total of {len(patients_events)} enrolled patient(s)")

            if patients_events:
                patients_events = pd.json_normalize(patients_events)
                
                enrollments = pd.read_csv('CONTACTS_INDEX_ENROLLMENTS.csv')
                enrollments = pd.concat([enrollments, patients_events])
                enrollments.to_csv('CONTACTS_INDEX_ENROLLMENTS.csv', index=False, encoding='utf-8')
    

    def process_hts_index_indicators(self):
        index_enrollments = pd.read_csv('INDEX_ENROLLMENTS.csv')
        index_enrollments = index_enrollments.to_dict(orient='records')

        # index
        index_case_offered_indicators_metadata_port = IndexCaseOfferedIndicatorMetadataAdapter(self.api)
        index_case_offered_use_case: ComputeHtsIndexCaseOfferedDisaggregationUseCase = ComputeHtsIndexCaseOfferedDisaggregationService(self.logger, index_case_offered_indicators_metadata_port)
        index_case_offered_patients_disaggregations =  index_case_offered_use_case.compute(index_enrollments, self.end_period)

        index_case_accepted_use_case = ComputeHtsIndexCaseAcceptedService()
        index_case_accepted_patients = index_case_accepted_use_case.compute(index_enrollments)

        index_case_accepted_indicators_metadata_port : IndicatorMetadataPort = IndexCaseAcceptedIndicatorMetadataAdapter(self.api)
        index_case_accepted_disaggregation_use_case: ComputeHtsIndexCaseAcceptedDisaggregationUseCase = ComputeHtsIndexCaseAcceptedDisaggregationService(self.logger, index_case_accepted_indicators_metadata_port)
        index_case_accepted_patients_disaggregation = index_case_accepted_disaggregation_use_case.compute(index_case_accepted_patients, self.end_period)

        # contacts
        index_contacts_enrollments = pd.read_csv('CONTACTS_INDEX_ENROLLMENTS.csv')
        index_contacts_enrollments = index_contacts_enrollments.to_dict(orient='records')

        index_case_contacts_number_indicators_metadata_port: IndicatorMetadataPort = IndexCaseContactsNumberIndicatorMetadataAdapter(self.api)
        index_case_contacts_number_disaggregation_use_case: ComputeHtsIndexCaseContactsNumberDisaggregationUseCase = ComputeHtsIndexCaseContactsNumberDisaggregationService(self.logger, index_case_contacts_number_indicators_metadata_port)
        index_case_contacts_number_patients_disaggregation = index_case_contacts_number_disaggregation_use_case.compute(index_contacts_enrollments, self.end_period)

        index_case_use_case: ComputeHtsIndexCaseUseCase = ComputeHtsIndexCaseService()
        index_case_patients = index_case_use_case.compute(index_contacts_enrollments)

        index_case_indicators_metadata_port :IndicatorMetadataPort = IndexCaseIndicatorMetadataAdapter(self.api)
        index_case_disaggregation_use_case: ComputeHtsIndexCaseDisaggregationUseCase = ComputeHtsIndexCaseDisaggregationService(self.logger,index_case_indicators_metadata_port)
        index_case_patients_disaggregations = index_case_disaggregation_use_case.compute(index_case_patients, self.end_period)

        combination = index_case_offered_patients_disaggregations + index_case_accepted_patients_disaggregation + index_case_contacts_number_patients_disaggregation + index_case_patients_disaggregations

        if combination:
            # extract data
            indicators = pd.json_normalize(combination)
            indicators['period'] = self.period
            indicators = indicators[['dataElement','period','orgUnit', 'categoryOptionCombo','attributeOptionCombo', 'value']]
            indicators = indicators.sort_values(['orgUnit', 'dataElement', 'period'])
            indicators.to_csv('INDEX_DATA.csv', index=False)

    def run(self):
        self.extract_index_enrollments()
        self.logger.info('The INDEX_ENROLLMENTS.csv file is completed.')

        self.extract_contacts_enrollments()
        self.logger.info('The CONTACTS_INDEX_ENROLLMENTS.csv file is completed.')

        self.process_hts_index_indicators()
        self.logger.info('The INDEX_DATA.csv file is completed.')


    