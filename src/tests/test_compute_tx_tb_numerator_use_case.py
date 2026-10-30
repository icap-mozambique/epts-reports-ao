import unittest

from src.main.application.service import ComputeTxTbNumeratorService

class TestComputeTxTbNumeratorUseCase(unittest.TestCase):

    def setUp(self):
        self.patients = [{'tb_entry_type': 'ROTINA','tb_screened': 'true', 'tb_screening_type':'SINAIS_SINTOMAS', 'tb_status':'Rastreado e sem sinais'},
                         {'tb_entry_type': 'CASO_NOVO', 'tb_screened': 'true', 'tb_screening_type':'SINAIS_SINTOMAS', 'tb_status':'Rastreado e sem sinais'},
                         {'tb_entry_type': 'CASO_NOVO', 'tb_screened': 'false', 'tb_screening_type':'SINAIS_SINTOMAS', 'tb_status':'Rastreado e sem sinais'},
                         {'tb_entry_type': 'CASO_NOVO', 'tb_screened': 'true', 'tb_screening_type':'SINAIS_SINTOMAS', 'tb_status':'Diagnosticado e Iniciou Tratamento da TB'}]

    def test_compute_tx_tb_numerator(self):
        tx_tb_numerator = ComputeTxTbNumeratorService()

        tx_tb_numerator_patients = tx_tb_numerator.compute(self.patients)

        self.assertEqual(len(tx_tb_numerator_patients), 1)

if __name__ == '__main__':
    unittest.main()
        
        