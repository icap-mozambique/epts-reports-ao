import pandas as pd

from src.infrastructure.adapters import PmtctArtNumeratorIndicatorMetadataAdapter
from src.infrastructure.adapters import PmtctEidIndicatorMedatadaAdapter
from src.infrastructure.adapters import PmtctHeiIndicatorsMetadataAdapter
from src.infrastructure.adapters import PmtctHeiPosIndicatorsMetadataAdapter
from src.infrastructure.adapters import PmtctStatDenominatorIndicatorMetadataAdapter
from src.infrastructure.adapters import PmtctStatNumeratorIndicatorMetadataAdapter
from src.infrastructure.forms import DPI
from src.main.application.income import ComputePmtctEidDisaggregationUseCase
from src.main.application.income import ComputePmtctEidUseCase
from src.main.application.income import ComputePmtctHeiDisaggregationUseCase
from src.main.application.income import ComputePmtctHeiUseCase
from src.main.application.out import IndicatorMetadataPort
from src.main.application.service import ComputePmtctArtNumeratorDisaggregationService
from src.main.application.service import ComputePmtctArtNumeratorService
from src.main.application.service import ComputePmtctEidDisaggregationService
from src.main.application.service import ComputePmtctEidService
from src.main.application.service import ComputePmtctHeiDisaggregationService
from src.main.application.service import ComputePmtctHeiService
from src.main.application.service import ComputePmtctStatDenominatorDisaggregationService
from src.main.application.service import ComputePmtctStatDenominatorService
from src.main.application.service import ComputePmtctStatNumeratorDisaggregationService
from src.main.application.service import ComputePmtctStatNumeratorService
from src.infrastructure.forms import PatientDemographicForm
from src.infrastructure.forms import PatientEventForm
from src.infrastructure.forms import PTV

class PmtctResource:

    def __init__(self, api, logger, start_period, end_period, period, org_units):
        self.api = api
        self.logger = logger
        self.start_period = start_period
        self.end_period = end_period
        self.period = period
        self.org_units = org_units
    
    def extract_pmtct_enrollments(self):
        enrollments = pd.DataFrame(columns=['enrollment', 'trackedEntity', 'program', 'status', 'orgUnit', 'enrolledAt', 'patientIdentifier', 'patientAge', 'patientSex','patientName', 'ancType', 'testResult', 'artStartDate', 'artStatus', 'onArt'])
        enrollments.to_csv('PMTCT_ENROLLMENTS.csv', index=False)

        # Load patients enrolled
        patient_demographics = PatientDemographicForm(self.api)
        patient_events = PatientEventForm(self.api)

        for org_unit in self.org_units:

            org_unit = org_unit['id']

            #get all patient enrollments
            patients_enrolled = self.api.get('tracker/enrollments', params={'orgUnit':org_unit, 'skipPaging':'true', 'program': PTV, 'fields':'{,enrollment, enrolledAt, orgUnit, trackedEntity, program, status,}', 'enrolledAfter':f'{self.start_period}', 'enrolledBefore':f'{self.end_period}', 'order':'enrolledAt:desc'})
            patients_enrolled = patients_enrolled.json()['instances']

            self.logger.info(f"Processing the facility: {org_unit}, a total of {len(patients_enrolled)} enrolled patient(s)")
            
            counter = 1

            for patient_enrolled in patients_enrolled:

                patient_demographics.add_demographics(patient_enrolled)
                patient_events.add_patient_first_anc_event(patient_enrolled)

                self.logger.info(f"From {len (patients_enrolled)} patients enrolled, {counter} (is) are ready to be processed.")
                counter = counter + 1 

            if patients_enrolled:
                patients_enrolled = pd.json_normalize(patients_enrolled)
                
                enrollments = pd.read_csv('PMTCT_ENROLLMENTS.csv')
                enrollments = pd.concat([enrollments, patients_enrolled])
                enrollments.to_csv('PMTCT_ENROLLMENTS.csv', index=False, encoding='utf-8')
    
    def extract_pmtct_dpi_enrollments(self):
        dpi_enrollments = pd.DataFrame(columns=['enrollment', 'trackedEntity', 'program', 'status', 'orgUnit', 'enrolledAt', 'patientIdentifier', 'patientAge', 'patientSex','patientName', 'exposed', 'pcrNumber', 'testResult', 'artStartDate'])
        dpi_enrollments.to_csv('DPI_ENROLLMENTS.csv', index=False)

        # Load patients enrolled
        patient_demographics = PatientDemographicForm(self.api)
        patient_events = PatientEventForm(self.api)

        for org_unit in self.org_units:

            org_unit = org_unit['id']

            #get all patient enrollments
            patients_enrolled = self.api.get('tracker/enrollments', params={'orgUnit':org_unit, 'skipPaging':'true', 'program': DPI, 'fields':'{,enrollment, enrolledAt, orgUnit, trackedEntity, program, status,}', 'enrolledAfter':f'{self.start_period}', 'enrolledBefore':f'{self.end_period}', 'order':'enrolledAt:asc'})
            patients_enrolled = patients_enrolled.json()['instances']

            self.logger.info(f"Processing the facility: {org_unit}, a total of {len(patients_enrolled)} enrolled patient(s)")
            
            counter = 1

            for patient_enrolled in patients_enrolled:

                patient_demographics.add_demographics(patient_enrolled)
                patient_events.add_patient_last_dpi_event(patient_enrolled)

                self.logger.info(f"From {len (patients_enrolled)} patients enrolled, {counter} (is) are ready to be processed.")
                counter = counter + 1 

            if patients_enrolled:
                patients_enrolled = pd.json_normalize(patients_enrolled)
                
                enrollments = pd.read_csv('DPI_ENROLLMENTS.csv')
                enrollments = pd.concat([enrollments, patients_enrolled])
                enrollments.to_csv('DPI_ENROLLMENTS.csv', index=False, encoding='utf-8')
    

    def process_pmtct_indicators(self):
        enrollments = pd.read_csv('PMTCT_ENROLLMENTS.csv')
        enrollments = enrollments.to_dict(orient='records')

        pmtct_art_numerator_service = ComputePmtctArtNumeratorService()
        pmtct_art_numerator_patients = pmtct_art_numerator_service.compute(enrollments)
        pmtct_art_numerator_indicator_metadata_port = PmtctArtNumeratorIndicatorMetadataAdapter(self.api)
        pmtct_art_numerator_disaggegation_service = ComputePmtctArtNumeratorDisaggregationService(self.logger, pmtct_art_numerator_indicator_metadata_port)
        pmtct_art_numerator_patients_disaggregation = pmtct_art_numerator_disaggegation_service.compute(pmtct_art_numerator_patients, self.end_period)
        self.logger.info('PMTCT_ART completed!')

        pmtct_stat_denominator_service = ComputePmtctStatDenominatorService()
        pmtct_stat_denominator_patients = pmtct_stat_denominator_service.compute(enrollments)
        pmtct_stat_denominator_indicator_metadata_port = PmtctStatDenominatorIndicatorMetadataAdapter(self.api)
        pmtct_stat_denominator_disaggregation_service = ComputePmtctStatDenominatorDisaggregationService(self.logger, pmtct_stat_denominator_indicator_metadata_port)
        pmtct_stat_denominator_patients_disaggregation = pmtct_stat_denominator_disaggregation_service.compute(pmtct_stat_denominator_patients, self.end_period)
        self.logger.info('PMTCT_STAT_DENOMINATOR completed!')

        pmtct_stat_numerator_service = ComputePmtctStatNumeratorService()
        pmtct_stat_numerator_patients = pmtct_stat_numerator_service.compute(enrollments)
        pmtct_stat_numerator_indicator_metadata_port = PmtctStatNumeratorIndicatorMetadataAdapter(self.api)
        pmtct_stat_numerator_disaggregation_service = ComputePmtctStatNumeratorDisaggregationService(self.logger, pmtct_stat_numerator_indicator_metadata_port)
        pmtct_stat_numerator_patients_disaggregation = pmtct_stat_numerator_disaggregation_service.compute(pmtct_stat_numerator_patients, self.end_period)
        self.logger.info('PMTCT_STAT_NUMERATOR completed!')

        dpi_enrollments = pd.read_csv('DPI_ENROLLMENTS.csv')
        dpi_enrollments = dpi_enrollments.to_dict(orient='records')

        pmtct_eid_use_case: ComputePmtctEidUseCase = ComputePmtctEidService()
        pmtct_eid_patients = pmtct_eid_use_case.compute(dpi_enrollments)
        pmtct_eid_indicators_metadata_port: IndicatorMetadataPort = PmtctEidIndicatorMedatadaAdapter(self.api)
        pmtct_eid_use_case: ComputePmtctEidDisaggregationUseCase = ComputePmtctEidDisaggregationService(self.logger, pmtct_eid_indicators_metadata_port)
        pmtct_eid_patients_disaggregation = pmtct_eid_use_case.compute(pmtct_eid_patients, self.end_period)
        self.logger.info('PMTCT_STAT_EID completed!')

        pmtct_hei_use_case: ComputePmtctHeiUseCase = ComputePmtctHeiService()
        pmtct_hei_patients = pmtct_hei_use_case.compute(dpi_enrollments)
        pmtct_hei_indicators_metadata_port: IndicatorMetadataPort = PmtctHeiIndicatorsMetadataAdapter(self.api)
        pmtct_hei_pos_indicators_metadata_port: IndicatorMetadataPort = PmtctHeiPosIndicatorsMetadataAdapter(self.api)
        self.logger.info('PMTCT_STAT_POS completed!')
        
        pmtct_hei_disaggregation_use_case: ComputePmtctHeiDisaggregationUseCase = ComputePmtctHeiDisaggregationService(self.logger, pmtct_hei_indicators_metadata_port, pmtct_hei_pos_indicators_metadata_port)
        pmtct_hei_patients_disaggregation = pmtct_hei_disaggregation_use_case.compute(pmtct_hei_patients, self.end_period)

        combination = pmtct_art_numerator_patients_disaggregation + pmtct_stat_denominator_patients_disaggregation + pmtct_stat_numerator_patients_disaggregation + pmtct_eid_patients_disaggregation + pmtct_hei_patients_disaggregation

        if combination:
            # extract data
            indicators = pd.json_normalize(combination)
            indicators['period'] = self.period
            indicators = indicators[['dataElement','period','orgUnit', 'categoryOptionCombo','attributeOptionCombo', 'value']]
            indicators = indicators.sort_values(['orgUnit', 'dataElement', 'period'])
            indicators.to_csv('PMTCT_DATA.csv', index=False)
    

    def run(self):
        # self.extract_pmtct_enrollments()
        self.logger.info('PMTCT_ENROLLMENTS.csv file is completed.')

        # self.extract_pmtct_dpi_enrollments()
        self.logger.info('DPI_ENROLLMENTS.csv file is completed.')

        self.process_pmtct_indicators()
        self.logger.info('PMTCT_DATA.csv file is completed.')