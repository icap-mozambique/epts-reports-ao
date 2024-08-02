
from src.main.application.income import ComputePmtctStatDenominatorUseCase

class ComputePmtctStatDenominatorService(ComputePmtctStatDenominatorUseCase):

    def compute(self, enrolled_patients):

        patients = []
        
        for enrolled_patient in enrolled_patients:

            if str(enrolled_patient['ancType']) == 'nan':
                continue

            if enrolled_patient['ancType'] != 'PRIMEIRA_CONSULTA':
                continue
            
            patients.append(enrolled_patient)
        
        return patients





