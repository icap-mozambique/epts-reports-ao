from src.main.application.out import PatientDemographicsPort
from src.main.application.out import EventPort
from src.main.application.income import ComputeHtsPmtctAncUseCase

class ComputeHtsPmtctAncService(ComputeHtsPmtctAncUseCase):

    def __init__(self, events_port: EventPort, patient_demographics_port: PatientDemographicsPort):
        self.events_port = events_port
        self.patient_demographics_port = patient_demographics_port

    def compute(self, org_unit, start_period, end_period):
        patients = []

        patient_events = self.events_port.find_patient_events_by_program_unit_and_period(self.PROGRAM, org_unit, start_period, end_period)

        for patient_event in patient_events:
            if 'result' not in patient_event:
                continue

            if 'cpn_type' not in patient_event:
                continue

            if patient_event['result'] != 'POSITIVO' and patient_event['result'] != 'NEGATIVO':
                continue
            
            if patient_event['cpn_type'] != 'PRIMEIRA_CONSULTA':
                continue

            self.patient_demographics_port.add_patient_demographics(patient_event)

            patients.append(patient_event)
            
        return patients

