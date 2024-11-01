
import pandas as pd
from src.main.application.income import ComputePmtctStatNumeratorUseCase

class ComputePmtctStatNumeratorService(ComputePmtctStatNumeratorUseCase):

    def compute(self, enrolled_patients, start_period):

        patients = []
        
        for enrolled_patient in enrolled_patients:

            if str(enrolled_patient['ancType']) == 'nan':
                continue

            if enrolled_patient['ancType'] != 'PRIMEIRA_CONSULTA':
                continue

            if str(enrolled_patient['testResult']) == 'nan':
                continue

            if enrolled_patient['testResult'] == 'POSITIVO_CONHECIDO' :
                if 'outcome' in enrolled_patient and (enrolled_patient['outcome'] == 'FAZ_TARV' or enrolled_patient['outcome'] == 'VIH_POSITIVO'):
                    patients.append(enrolled_patient)
                    continue

            if str(enrolled_patient['testDate']) == 'nan':
                continue

            if pd.to_datetime(start_period) > pd.to_datetime(enrolled_patient['testDate']):
                continue

            if enrolled_patient['testResult'] != 'POSITIVO' and enrolled_patient['testResult'] != 'NEGATIVO':
                continue
            
            if enrolled_patient['result'] == 'POSITIVO':
                if 'outcome' in enrolled_patient and (enrolled_patient['outcome'] == 'SEGUIMENTO_NESTA_US' or enrolled_patient['outcome'] == 'SEGUIMENTO_NOUTRA_US' or enrolled_patient['outcome'] == 'OBITO'):
                    patients.append(enrolled_patient)
            else:
                patients.append(enrolled_patient)
        
        return patients





