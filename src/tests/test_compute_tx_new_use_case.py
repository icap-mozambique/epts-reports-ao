import unittest
from unittest.mock import patch
from pandas import Timestamp

from src.main.application.service import ComputeTxCurrService
from src.main.application.service import ComputeTxNewService

class TestComputeTxNewUseCase(unittest.TestCase):

    def setUp(self):
       self.patients = [{'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2024-01-01', 'firstConsultationDate': '2024-01-01', 'pickupQuantity': '30', 'lastPickupDate': '2024-01-01', 'nextPickupDate': Timestamp('2024-03-31 00:00:00'), 'lastCD4': '2082', 'entryType':'CASO_NOVO'}]
       
    @patch('logging.getLogger')
    def test_comupute_tx_new_use_case(self, logger):

      tx_new = ComputeTxNewService(logger)
      tx_new.compute(self.patients, '2024-01-01', '2024-03-31')
      
      for patient in self.patients:
         self.assertTrue(patient['txNew'] == True)

if __name__ == '__main__':
    unittest.main()