from src.infrastructure.forms import PatientDemographicForm
from src.main.application.out import PatientDemographicsPort


class PatientDemographicsAdapter(PatientDemographicsPort):
    
    def __init__(self, patient_demographics_form: PatientDemographicForm) -> None:
        self.patient_demographics_form = patient_demographics_form

    def add_patient_demographics(self, patient):
       self.patient_demographics_form.add_demographics(patient)