from src.infrastructure.forms import PatientEventForm
from src.main.application.out import EventPort

class EventAdapter(EventPort):

    def __init__(self, patient_event_form: PatientEventForm):
       self.patient_event_form = patient_event_form

    def find_patient_events_by_program_unit_and_period(self, program, unit, start_date, end_date):
       return self.patient_event_form.find_patient_events_by_program_unit_and_period(program, unit, start_date, end_date)

    def find_index_patient_details_event(self, patient):
       return self.patient_event_form.find_index_patient_details_event(patient)
