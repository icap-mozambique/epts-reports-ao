

from src.infrastructure.forms import PatientLaboratoryForm
from src.main.application.out import LaboratoryPort

class LaboratoryAdapter(LaboratoryPort):

    def __init__(self, patient_laboratory: PatientLaboratoryForm) -> None:
        self.patient_laboratory = patient_laboratory

    def add_last_viral_load_result_date_of_the_period(self, patient, end_period):
        self.patient_laboratory.add_last_viral_load_date_of_the_period(patient, end_period)
      