from src.main.application.out import PatientDemographicsPort
from src.main.application.out import EventPort
from src.main.application.income import ComputeHtsPregnantLdUseCase


class ComputeHtsPregnantLdService(ComputeHtsPregnantLdUseCase):

    def __init__(self, event_port: EventPort, patient_demographics_port: PatientDemographicsPort) -> None:

        self.event_port = event_port
        self.patient_demographics_port = patient_demographics_port
       
    def compute(self, org_unit, start_period, end_period):
        patients = []

        ptv_patient_events = self.event_port.find_patient_events_by_program_unit_and_period(self.PROGRAM_PTV, org_unit, start_period, end_period)
        sat_patient_events = self.event_port.find_patient_events_by_program_unit_and_period(self.PROGRAM_SAT, org_unit, start_period, end_period)

        patient_events = ptv_patient_events + sat_patient_events

        for patient_event in patient_events:

            if patient_event['program'] == self.PROGRAM_SAT:

                if 'timeOfTesting' not in patient_event:
                    continue

                if 'result' not in patient_event:
                    continue

                if 'section' not in patient_event:
                    continue

                if 'breastfeeding' in patient_event:
                    continue

                if patient_event['timeOfTesting'] != 'PRIMEIRO_TESTE' and patient_event['timeOfTesting'] != 'RETESTAGEM':
                    continue

                if patient_event['result'] != 'POSITIVO' and patient_event['result'] != 'NEGATIVO':
                    continue

                if patient_event['section'] != 'PARTO_BU_MATERNIDADE':
                    continue

                if patient_event['result'] == 'POSITIVO':
                    if patient_event['outcome'] == 'SEGUIMENTO_NESTA_US' or patient_event['outcome'] == 'SEGUIMENTO_NOUTRA_US' or patient_event['outcome'] == 'OBITO':
                        self.patient_demographics_port.add_patient_demographics(patient_event)
                        patients.append(patient_event)
                else:
                    self.patient_demographics_port.add_patient_demographics(patient_event)
                    patients.append(patient_event)

            else:

                if 'result' not in patient_event:
                    continue

                if 'cpn_type' not in patient_event:
                    continue

                if patient_event['result'] != 'POSITIVO' and patient_event['result'] != 'NEGATIVO':
                    continue
                
                if patient_event['cpn_type'] != 'RETORNO':
                    continue

                if patient_event['result'] == 'POSITIVO':
                    if patient_event['outcome'] == 'SEGUIMENTO_NESTA_US' or patient_event['outcome'] == 'SEGUIMENTO_NOUTRA_US' or patient_event['outcome'] == 'OBITO':
                        self.patient_demographics_port.add_patient_demographics(patient_event)
                        patients.append(patient_event)
                else:
                    self.patient_demographics_port.add_patient_demographics(patient_event)
                    patients.append(patient_event)

        return patients

