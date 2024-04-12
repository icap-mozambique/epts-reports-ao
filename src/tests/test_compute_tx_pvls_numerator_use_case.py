import unittest

from src.main.application.service import ComputeTxPvlsNumeratorService

class TestComputeTxPvlsNumeratorUseCase(unittest.TestCase):
    
    def setUp(self):
        self.patients = [{'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2019-03-13', 'firstConsultationDate': '2019-03-13', 'pickupQuantity': '90', 'lastPickupDate': '2024-03-07', 'nextPickupDate': '2024-06-05', 'lastCD4': '2082', 'viralLoadResultDate':'2024-03-17', 'viralLoadResultValue':'100', 'txPvlsD': True}]
        
    def test_compute_tx_pvls_denominator_use_case(self):
       
       tx_pvls_n = ComputeTxPvlsNumeratorService()
       tx_pvls_n.compute(self.patients)

       for patient in self.patients:
           self.assertTrue(patient['txPvlsN'] == True)

if __name__ == '__main__':
    unittest.main()
