from src.infrastructure.forms import PatientConsultationForm
from src.main.application.out import ConsultationPort

class ConsultationAdapter(ConsultationPort):

    def __init__(self, patient_consultation_form: PatientConsultationForm) -> None:
        self.patient_consultation_form = patient_consultation_form
       
    def add_patient_pregnant_or_breastfeeding_status(self, patient, end_period):
        self.patient_consultation_form.add_patient_pregnant_or_breastfeeding_status(patient, end_period)

