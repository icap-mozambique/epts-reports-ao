import unittest
from unittest.mock import MagicMock

from src.infrastructure.forms import PatientLaboratoryForm
from src.main.application.service import ComputeTxPvlsDenominatorService
from src.main.application.service import ComputeTxCurrService
from src.infrastructure.adapters import LaboratoryAdapter

class TestComputeTxPvlsDenominatorUseCase(unittest.TestCase):
    
    def setUp(self):
        self.patients = [{'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2019-03-13', 'firstConsultationDate': '2019-03-13', 'pickupQuantity': '90', 'lastPickupDate': '2024-03-07', 'nextPickupDate': '2024-06-05', 'lastCD4': '2082', 'viralLoadResultDate':'2024-03-17', 'viralLoadResultValue':'1000'}]

    def test_compute_tx_pvls_denominator_use_case(self):
        start_period = '2024-01-01'
        end_period = '2024-03-31'

        tx_curr = ComputeTxCurrService()

        patient_laboratory = PatientLaboratoryForm('khKgyHv2ELM', 'KUNENE', {})
        laboratory_adapter = LaboratoryAdapter(patient_laboratory)

        patient_laboratory.add_last_viral_load_date_of_the_period = MagicMock()

        tx_pls_denominator_service = ComputeTxPvlsDenominatorService(tx_curr, laboratory_adapter)
        tx_pls_denominator_service.compute(self.patients, end_period)

        for patient in self.patients:
            self.assertTrue(patient['txPvlsD'] == True)

if __name__ == '__main__':
    unittest.main()