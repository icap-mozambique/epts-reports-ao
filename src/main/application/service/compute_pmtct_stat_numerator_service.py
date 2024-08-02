
from src.main.application.income import ComputePmtctStatNumeratorUseCase

class ComputePmtctStatNumeratorService(ComputePmtctStatNumeratorUseCase):

    def compute(self, enrolled_patients):

        patients = []
        
        for enrolled_patient in enrolled_patients:

            if str(enrolled_patient['ancType']) == 'nan':
                continue

            if enrolled_patient['ancType'] != 'PRIMEIRA_CONSULTA':
                continue

            if str(enrolled_patient['testResult']) == 'nan':
                continue

            if enrolled_patient['testResult'] != 'POSITIVO' and enrolled_patient['testResult'] != 'POSITIVO_CONHECIDO' and enrolled_patient['testResult'] != 'NEGATIVO':
                continue
            
            patients.append(enrolled_patient)
        
        return patients





