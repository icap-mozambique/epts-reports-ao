import unittest

from src.main.application.service import ComputeTxMlService

class TestComputeTxMlUseCase(unittest.TestCase):

    def setUp(self):
        self.patients = [{'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2019-03-13', 'firstConsultationDate': '2019-03-13', 'pickupQuantity': '90', 'lastPickupDate': '2024-03-07', 'nextPickupDate': '2024-01-05', 'lastCD4': '2082'}]
    
    def test_compute_tx_ml_use_case(self):
        start_period = '2024-01-01'
        end_period = '2024-03-31'

        compute_tx_ml_service = ComputeTxMlService()
        compute_tx_ml_service.compute(self.patients, start_period, end_period)

        for patient in self.patients:
            self.assertTrue(patient['txML'] == True)

if __name__ == '__main__':
    unittest.main()