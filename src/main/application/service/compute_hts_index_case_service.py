from src.main.application.income import ComputeHtsIndexCaseUseCase

class ComputeHtsIndexCaseService(ComputeHtsIndexCaseUseCase):

    def compute(self, index_case_patients):
        
        patients = []

        for patient in index_case_patients:

            if str(patient['result']) == 'nan':
                continue

            if patient['result'] != 'POSITIVO_CONHECIDO' and patient['result'] != 'POSITIVO' and patient['result'] != 'NEGATIVO' and patient['result'] != 'NEGATIVO_CONHECIDO':
                continue

            if 'testingLocation' not in patient:
                continue

            if patient['testingLocation'] != 'US':
                continue

            if patient['testResult'] == 'POSITIVO_CONHECIDO' :
                if 'outcome' in patient and (patient['outcome'] == 'FAZ_TARV' or patient['outcome'] == 'VIH_POSITIVO'):
                    patients.append(patient)
                    continue

            if patient['result'] == 'POSITIVO':
                if 'outcome' in patient and (patient['outcome'] == 'SEGUIMENTO_NESTA_US' or patient['outcome'] == 'SEGUIMENTO_NOUTRA_US' or patient['outcome'] == 'OBITO'):
                    patients.append(patient)
            else:
                patients.append(patient)

        return patients

    
    
