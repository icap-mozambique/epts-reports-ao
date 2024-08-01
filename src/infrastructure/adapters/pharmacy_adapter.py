
from src.infrastructure.forms import PatientPharmacyForm
from src.main.application.out import PharmacyPort

class PharmacyAdapter(PharmacyPort):

    def __init__(self, pharmacy_form: PatientPharmacyForm) -> None:
        self.pharmacy_form = pharmacy_form

    def find_last_pickup_of_the_period(self, patient, period):
        self.pharmacy_form.find_last_pickup_of_the_period(patient, period)