from src.main.application.out import EventPort
from src.main.application.out import PatientDemographicsPort
from src.main.application.income import ComputeHtsBreastfeedingUseCase

class ComputeHtsBreastfeedingService(ComputeHtsBreastfeedingUseCase):

    def __init__(self, event_port: EventPort, patient_demographics_port: PatientDemographicsPort):
       self.event_port = event_port
       self.patient_demographics_port = patient_demographics_port

    def compute(self, org_unit, start_period, end_period):
        patients = []

        patient_events = self.event_port.find_patient_events_by_program_unit_and_period(self.PROGRAM, org_unit, start_period, end_period)

        for patient_event in patient_events:
            
            if 'timeOfTesting' not in patient_event:
                continue

            if 'result' not in patient_event:
                continue

            if 'section' not in patient_event:
                continue

            if 'breastfeeding' not in patient_event:
                continue

            if patient_event['timeOfTesting'] != 'PRIMEIRO_TESTE' and patient_event['timeOfTesting'] != 'RETESTAGEM':
                continue

            if patient_event['result'] != 'POSITIVO' and patient_event['result'] != 'NEGATIVO':
                continue

            if patient_event['section'] != 'AT' and patient_event['section'] != 'PF':
                continue

            self.patient_demographics_port.add_patient_demographics(patient_event)

            patients.append(patient_event)
        
        return patients
