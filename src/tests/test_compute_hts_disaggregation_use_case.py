import unittest
from unittest.mock import patch

from src.main.application.service import ComputeHtsDisaggregationService
from src.main.application.out import IndicatorMetadataPort


class TestComputeHtsDisaggregationUseCase(unittest.TestCase):

    def setUp(self) -> None:
        self.patients = [{'event': 'IFsA9XIYW2p', 'status': 'COMPLETED', 'program': 'grpiGkcSlNN', 'trackedEntity': 'TzzIoKSRJR9','orgUnit': 'PN6vjlhFZOc', 'occurredAt': '2024-05-01T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2015-03-03', 'patientName': 'Joao Hilifavali', 'timeOfTesting':'PRIMEIRO_TESTE', 'result':'POSITIVO', 'section':'AT'},
                         {'event': 'IFsA9XIYW2p', 'status': 'COMPLETED', 'program': 'grpiGkcSlNN', 'trackedEntity': 'TzzIoKSRJR9','orgUnit': 'PN6vjlhFZOc', 'occurredAt': '2024-05-01T00:00:00.000', 'patientSex': 'Masculino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '1998-03-03', 'patientName': 'Joao Hilifavali', 'timeOfTesting':'RETESTAGEM', 'result':'NEGATIVO', 'section':'AT'}, 
                         {'event': 'IFsA9XIYW2p', 'status': 'COMPLETED', 'program': 'grpiGkcSlNN', 'trackedEntity': 'TzzIoKSRJR9','orgUnit': 'PN6vjlhFZOc', 'occurredAt': '2024-05-01T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '1998-03-03', 'patientName': 'Joao Hilifavali', 'timeOfTesting':'RETESTAGEM', 'result':'NEGATIVO', 'section':'AT'},
                         {'event': 'IFsA9XIYW2p', 'status': 'COMPLETED', 'program': 'grpiGkcSlNN', 'trackedEntity': 'TzzIoKSRJR9','orgUnit': 'PN6vjlhFZOc', 'occurredAt': '2024-05-01T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '1998-03-03', 'patientName': 'Joao Hilifavali', 'timeOfTesting':'RETESTAGEM', 'result':'NEGATIVO', 'section':'AT'},
                         {'event': 'IFsA9XIYW2p', 'status': 'COMPLETED', 'program': 'grpiGkcSlNN', 'trackedEntity': 'TzzIoKSRJR9','orgUnit': 'PN6vjlhFZOc', 'occurredAt': '2024-05-01T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2024-03-03', 'patientName': 'Joao Hilifavali', 'timeOfTesting':'PRIMEIRO_TESTE', 'result':'POSITIVO', 'section':'AT'},
                         {'event': 'IFsA9XIYW2p', 'status': 'COMPLETED', 'program': 'grpiGkcSlNN', 'trackedEntity': 'TzzIoKSRJR9','orgUnit': 'PN6vjlhFZOc', 'occurredAt': '2024-05-01T00:00:00.000', 'patientSex': 'Feminino', 'patientIdentifier': '1609800880/2019T/00033', 'patientAge': '2024-03-03', 'patientName': 'Joao Hilifavali', 'timeOfTesting':'PRIMEIRO_TESTE', 'result':'POSITIVO', 'section':'AT'}]
        
        self.AGE_BANDS = ['<1', '1-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50+']

        self.metadata = [{"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results <1, Female, Positive","id": "YBdu7j2gGjC.PPg7Yzjq0oF", 'indicator_key':'<1_F_P'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results <1, Female, Negative","id": "YBdu7j2gGjC.X9GstRdTsEy", 'indicator_key':'<1_F_N'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results <1, Male, Positive","id": "YBdu7j2gGjC.renXtk3VqTM", 'indicator_key':'<1_M_P'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results <1, Male, Negative","id": "YBdu7j2gGjC.QNgjY1xNF2S", 'indicator_key':'<1_M_N'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results 5-9, Female, Positive","id": "YBdu7j2gGjC.OdBhPUGWQ5m", 'indicator_key':'5-9_F_P'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results 5-9, Female, Negative","id": "YBdu7j2gGjC.PFWJho4V0Bq", 'indicator_key':'5-9_F_N'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results 5-9, Male, Positive","id": "YBdu7j2gGjC.T6zWRBnlJhR", 'indicator_key':'5-9_M_P'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results 5-9, Male, Negative","id": "YBdu7j2gGjC.X8pGUJitiVE", 'indicator_key':'5-9_M_N'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results 25-29, Female, Positive","id": "YBdu7j2gGjC.BoN2WhPnYl1", 'indicator_key':'25-29_F_P'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results 25-29, Female, Negative","id": "YBdu7j2gGjC.TU97qv4vJ5O", 'indicator_key':'25-29_F_N'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results 25-29, Male, Positive","id": "YBdu7j2gGjC.FmEMWg0TP1j", 'indicator_key':'25-29_M_P'},
                         {"name": "HTS_TST (N, TA, VCT/Age/Sex/Result): HTS received results 25-29, Male, Negative","id": "YBdu7j2gGjC.c4FaWCHZi2O", 'indicator_key':'25-29_M_N'}]
        
    @patch('src.main.application.out.indicator_metadata_port')
    def test_compute_hts_disaggregation_use_case(self, mock_indicator_metadata_port: IndicatorMetadataPort):

        mock_indicator_metadata_port.age_bands.return_value = self.AGE_BANDS
        mock_indicator_metadata_port.find_indicator_metadata.return_value = self.metadata

        compute_hts_disaggregation = ComputeHtsDisaggregationService(mock_indicator_metadata_port)

        indicators = compute_hts_disaggregation.compute(self.patients, '2024-05-31')

        self.assertTrue(len(indicators) != 0)
        self.assertEqual(int([indicator for indicator in indicators if '<1_F_P' == indicator['indicator_key']][0]['value']), 2)
        self.assertEqual(int([indicator for indicator in indicators if '5-9_F_P' == indicator['indicator_key']][0]['value']), 1)
        self.assertEqual(int([indicator for indicator in indicators if '25-29_F_N' == indicator['indicator_key']][0]['value']), 2)
        self.assertEqual(int([indicator for indicator in indicators if '25-29_M_N' == indicator['indicator_key']][0]['value']), 1)

if __name__ == '__main__':
    unittest.main()