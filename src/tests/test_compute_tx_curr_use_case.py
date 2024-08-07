import unittest
from pandas import Timestamp
from src.main.application.service import ComputeTxCurrService

class TestComputeTxCurrUseCase(unittest.TestCase):

    def setUp(self):
       self.patients = [{'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2019-03-13', 'firstConsultationDate': '2019-03-13', 'pickupQuantity': '90', 'lastPickupDate': '2024-03-07', 'nextPickupDate': Timestamp('2024-06-05 00:00:00'), 'lastCD4': '2082'}]

    def test_compute_tx_curr_use_case(self):
        period= '2024-03-31'

        tx_curr = ComputeTxCurrService()
        tx_curr_patients = tx_curr.compute(self.patients, period)

        self.assertEquals(len(tx_curr_patients), 1)

if __name__ == '__main__':
    unittest.main()
