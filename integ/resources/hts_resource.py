import pandas as pd

from src.infrastructure.adapters import BreastfeedingIndicatorMetadataAdapter
from src.infrastructure.adapters import EmergenceWardIndicatorMetadataAdapter
from src.infrastructure.adapters import EventAdapter
from src.infrastructure.adapters import InpatientIndicatorMetadataAdapter
from src.infrastructure.adapters import MalnutritionIndicatorMetadataAdapter
from src.infrastructure.adapters import OtherPitcIndicadorMetadataAdapter
from src.infrastructure.adapters import PatientDemographicsAdapter
from src.infrastructure.adapters import PregnantIndicatorMetadataAdapter
from src.infrastructure.adapters import VctIndicatorMetadataAdapter
from src.infrastructure.forms import PatientDemographicForm
from src.infrastructure.forms import PatientEventForm
from src.main.application.service import ComputeHtsVctService
from src.main.application.service import ComputeHtsBreastfeedingService
from src.main.application.service import ComputeHtsDisaggregationService
from src.main.application.service import ComputeHtsEmergenceWardService
from src.main.application.service import ComputeHtsInpatientService
from src.main.application.service import ComputeHtsMalnutritionService
from src.main.application.service import ComputeHtsOtherPitcService
from src.main.application.service import ComputeHtsPregnantLdService


class HtsResource:

    def __init__(self, api, logger, start_period, end_period, period, org_units):
        self.api = api
        self.logger = logger
        self.start_period = start_period
        self.end_period = end_period
        self.period = period
        self.org_units = org_units
    
    def process_hts_indicators(self):
        hts_data = pd.DataFrame(columns=['dataElement','period','orgUnit', 'categoryOptionCombo','attributeOptionCombo', 'value'])
        hts_data.to_csv('HTS_DATA.csv', index=False)

        patient_event_form = PatientEventForm(self.api)
        patient_demographic_form = PatientDemographicForm(self.api)
        event_port = EventAdapter(patient_event_form)
        patient_demographics_port = PatientDemographicsAdapter(patient_demographic_form)

        compute_hts_vct = ComputeHtsVctService(event_port, patient_demographics_port)
        vct_metadata_port = VctIndicatorMetadataAdapter(self.api)
        vct_patients_disaggregation = ComputeHtsDisaggregationService(vct_metadata_port)

        compute_hts_pregnant = ComputeHtsPregnantLdService(event_port, patient_demographics_port)
        pregnant_metadata_port = PregnantIndicatorMetadataAdapter(self.api)
        pregnant_patients_disaggregation = ComputeHtsDisaggregationService(pregnant_metadata_port)

        compute_hts_breastfeeding = ComputeHtsBreastfeedingService(event_port, patient_demographics_port)
        breastfeeding_metadata_port = BreastfeedingIndicatorMetadataAdapter(self.api)
        breastfeeding_patients_disaggregation = ComputeHtsDisaggregationService(breastfeeding_metadata_port)

        compute_hts_other_pitc = ComputeHtsOtherPitcService(event_port, patient_demographics_port)
        other_pitc_metadata_port = OtherPitcIndicadorMetadataAdapter(self.api)
        other_pitc_patients_disaggregation = ComputeHtsDisaggregationService(other_pitc_metadata_port)

        compute_hts_emergence_ward = ComputeHtsEmergenceWardService(event_port, patient_demographics_port)
        emergence_ward_port = EmergenceWardIndicatorMetadataAdapter(self.api)
        emergenc_ward_patients_disaggregation = ComputeHtsDisaggregationService(emergence_ward_port)

        compute_hts_inpatient = ComputeHtsInpatientService(event_port, patient_demographics_port)
        inpatient_port = InpatientIndicatorMetadataAdapter(self.api)
        inpatient_patients_disaggregation = ComputeHtsDisaggregationService(inpatient_port)

        compute_hts_malnutrition = ComputeHtsMalnutritionService(event_port, patient_demographics_port)
        malnutrition_port = MalnutritionIndicatorMetadataAdapter(self.api)
        malnutrition_patients_disaggregation = ComputeHtsDisaggregationService(malnutrition_port)

        count = 1

        for org_unit in self.org_units:

            org_unit = org_unit['id']
            self.logger.info(f'{len(self.org_units)} of {count} - {org_unit}')

            vct_patients = compute_hts_vct.compute(org_unit, self.start_period, self.end_period)
            vct_patients_disaggregated = vct_patients_disaggregation.compute(vct_patients, self.end_period)

            pregnant_patients = compute_hts_pregnant.compute(org_unit, self.start_period, self.end_period)
            pregnant_patients_disaggregated = pregnant_patients_disaggregation.compute(pregnant_patients, self.end_period)

            breastfeeding_patients = compute_hts_breastfeeding.compute(org_unit, self.start_period, self.end_period)
            breastfeeding_patients_disaggregated = breastfeeding_patients_disaggregation.compute(breastfeeding_patients, self.end_period)

            other_pitc_patients = compute_hts_other_pitc.compute(org_unit, self.start_period, self.end_period)
            other_pitc_patients_disaggregated = other_pitc_patients_disaggregation.compute(other_pitc_patients, self.end_period)

            emergence_ward_patients = compute_hts_emergence_ward.compute(org_unit, self.start_period, self.end_period)
            emergence_ward_patients_disaggregated = emergenc_ward_patients_disaggregation.compute(emergence_ward_patients, self.end_period)

            inpatients = compute_hts_inpatient.compute(org_unit, self.start_period, self.end_period)
            inpatients_disaggregated = inpatient_patients_disaggregation.compute(inpatients, self.end_period)

            maltnutrition_patients = compute_hts_malnutrition.compute(org_unit, self.start_period, self.end_period)
            malnutrition_patients_disaggregated = malnutrition_patients_disaggregation.compute(maltnutrition_patients, self.end_period)

            count = count + 1

            combination = vct_patients_disaggregated + pregnant_patients_disaggregated + breastfeeding_patients_disaggregated + other_pitc_patients_disaggregated + emergence_ward_patients_disaggregated + inpatients_disaggregated + malnutrition_patients_disaggregated

            if combination:
                hts = pd.json_normalize(combination)
                hts['period'] = self.period
                hts = hts[['dataElement','period','orgUnit', 'categoryOptionCombo','attributeOptionCombo', 'value']]
                hts_data = pd.read_csv('HTS_DATA.csv')
                hts_data = pd.concat([hts_data, hts])
                hts_data = hts_data.sort_values(['orgUnit', 'dataElement', 'period'])
                hts_data.to_csv('HTS_DATA.csv', index=False)
    
    
    def run(self):
        self.process_hts_indicators()
        self.logger.info('The HTS_DATA.csv file is completed')