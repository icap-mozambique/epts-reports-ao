import unittest
from unittest.mock import patch

from src.main.application.service import ComputeHtsPregnantLdService
from src.main.application.out import EventPort
from src.main.application.out import PatientDemographicsPort

class TestComputeHtsPregnantLdUseCase(unittest.TestCase):

    def setUp(self) -> None:
       self.patients = [{'event': 'IFsA9XIYW2p', 'status': 'COMPLETED', 'program': 'grpiGkcSlNN', 'trackedEntity': 'TzzIoKSRJR9','orgUnit': 'PN6vjlhFZOc', 'occurredAt': '2024-05-01T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'timeOfTesting':'PRIMEIRO_TESTE', 'result':'POSITIVO_CONHECIDO', 'section':'AT'},
                    {'event': 'IFsA9XIYW2p', 'status': 'COMPLETED', 'program': 'grpiGkcSlNN', 'trackedEntity': 'TzzIoKSRJR9','orgUnit': 'PN6vjlhFZOc', 'occurredAt': '2024-05-01T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'timeOfTesting':'RETESTAGEM', 'result':'NEGATIVO', 'section':'PARTO_BU_MATERNIDADE'}, 
                    {'event': 'IFsA9XIYW2p', 'status': 'COMPLETED', 'program': 'BgTTypHIWom', 'trackedEntity': 'TzzIoKSRJR9','orgUnit': 'PN6vjlhFZOc', 'occurredAt': '2024-05-01T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'timeOfTesting':'RETESTAGEM', 'result':'NEGATIVO'}]
       
    @patch('src.main.application.out.event_port')
    @patch('src.main.application.out.patient_demographics_port')    
    def test_compute_hts_pregnant_ld_use_case(self, mock_event_port: EventPort, mock_patient_demograhics_port: PatientDemographicsPort):

        mock_event_port.find_patient_events_by_program_unit_and_period.return_value = self.patients

        start_date = '2024-05-01'
        end_date = '2024-05-31'
        org_unit = 'PN6vjlhFZOc'

        hts_pregnant_ld = ComputeHtsPregnantLdService(mock_event_port, mock_patient_demograhics_port)
        patients = hts_pregnant_ld.compute(org_unit, start_date, end_date)

        self.assertEqual(len(patients), 4)

if __name__ == '__main__':
    unittest.main()
