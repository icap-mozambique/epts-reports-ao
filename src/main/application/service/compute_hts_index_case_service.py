from src.main.application.out import PatientDemographicsPort
from src.main.application.out import EventPort
from src.main.application.income import ComputeHtsIndexCaseUseCase

class ComputeHtsIndexCaseService(ComputeHtsIndexCaseUseCase):

    def __init__(self, events_port: EventPort):
        self.events_port = events_port

    def compute(self, org_unit, start_period, end_period):
        patients = []

        patient_events = self.events_port.find_patient_events_by_program_program_stage_unit_and_period(self.PROGRAM, self.PROGRAM_STAGE, org_unit, start_period, end_period)

        for patient_event in patient_events:

            if 'ic_new_case' not in patient_event:
                continue

            if 'ic_date' not in patient_event:
                continue

            if 'result' not in patient_event:
                continue

            if 'patientAge' not in patient_event:
                continue

            if 'patientSex' not in patient_event:
                continue

            if patient_event['result'] != 'POSITIVO' and patient_event['result'] != 'NEGATIVO':
                continue

            patients.append(patient_event)

        return patients

    
    
