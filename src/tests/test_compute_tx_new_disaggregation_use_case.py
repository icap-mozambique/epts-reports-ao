import unittest

from pandas import Timestamp

from src.main.application.service import ComputeTxNewDisaggregationService

class TestComputeTxNewDisaggregationUseCase (unittest.TestCase):

    def setUp(self) -> None:
        self.patients = [{'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2019-03-13', 'firstConsultationDate': '2019-03-13', 'pickupQuantity': '90', 'lastPickupDate': '2024-03-07', 'nextPickupDate': Timestamp('2024-06-05 00:00:00'), 'lastCD4': '2082', 'txNew':True},
                         {'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Masculino', 'patientIdentifier': '1609800880/2019T/00034', 'patientAge': '2024-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2019-03-13', 'firstConsultationDate': '2019-03-13', 'pickupQuantity': '90', 'lastPickupDate': '2024-03-07', 'nextPickupDate': Timestamp('2024-06-05 00:00:00'), 'lastCD4': '100', 'txNew':True},
                         {'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Masculino', 'patientIdentifier': '1609800880/2019T/00034', 'patientAge': '2024-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2019-03-13', 'firstConsultationDate': '2019-03-13', 'pickupQuantity': '90', 'lastPickupDate': '2024-03-07', 'nextPickupDate': Timestamp('2024-06-05 00:00:00'), 'lastCD4': '100', 'txNew':True},
                         {'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Masculino', 'patientIdentifier': '1609800880/2019T/00034', 'patientAge': '1958-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2019-03-13', 'firstConsultationDate': '2019-03-13', 'pickupQuantity': '90', 'lastPickupDate': '2024-03-07', 'nextPickupDate': Timestamp('2024-06-05 00:00:00'), 'txNew':True},
                         {'enrollment': 'DEkwpYZyGXO', 'trackedEntity': 'khKgyHv2ELM', 'program': 'YKs1kXOLb0u', 'status': 'ACTIVE', 'enrolledAt': '2024-03-07T00:00:00.000', 'patientSex': 'Masculino', 'patientIdentifier': '1609800880/2019T/00034', 'patientAge': '1958-03-03', 'patientName': 'Joao Hilifavali', 'artStartDate': '2019-03-13', 'firstConsultationDate': '2019-03-13', 'pickupQuantity': '90', 'lastPickupDate': '2024-03-07', 'nextPickupDate': Timestamp('2024-06-05 00:00:00'), 'txNew':True}]

    def test_compute_tx_new_disaggregation_use_case(self):
        end_period = '2024-05-31'
        
        tx_new_desaggregation = ComputeTxNewDisaggregationService()
        indicators = tx_new_desaggregation.compute(self.patients, end_period)

        self.assertFalse(len(indicators) == 0)
        self.assertEqual(indicators['5-9_Female_>=200']['value'], 1)
        self.assertEqual(indicators['<1_Male_<200']['value'], 2)
        self.assertEqual(indicators['65+_Male_CD4 Unknown']['value'], 2)

if __name__ == '__main__':
    unittest.main()