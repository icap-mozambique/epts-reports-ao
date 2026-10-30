import unittest

from src.main.application.service import ComputeTxTbDenominatorService

class TestComputeTxTbDenominatorUseCase(unittest.TestCase):

    def setUp(self):
        self.patients = [{'tb_entry_type': 'ROTINA','tb_screened': 'true', 'tb_screening_type':'SINAIS_SINTOMAS', 'tb_status':'Rastreado e sem sinais'},
                         {'tb_entry_type': 'CASO_NOVO', 'tb_screened': 'true', 'tb_screening_type':'SINAIS_SINTOMAS', 'tb_status':'Rastreado e sem sinais'},
                         {'tb_entry_type': 'CASO_NOVO', 'tb_screened': 'false', 'tb_screening_type':'SINAIS_SINTOMAS', 'tb_status':'Rastreado e sem sinais'}]

    
    def test_compute_tx_tb_denominator(self):
        tx_tb_denominaor = ComputeTxTbDenominatorService()

        tx_tb_denominator_patients = tx_tb_denominaor.compute(self.patients)

        self.assertEqual(len(tx_tb_denominator_patients), 2)
        
if __name__ == '__main__':
    unittest.main()



