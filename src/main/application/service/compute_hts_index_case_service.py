from src.main.application.income import ComputeHtsIndexCaseUseCase

class ComputeHtsIndexCaseService(ComputeHtsIndexCaseUseCase):

    def compute(self, index_case_patients):
        
        patients = []

        for patient in index_case_patients:

            if str(patient['result']) == 'nan':
                continue

            if patient['result'] != 'POSITIVO_CONHECIDO' and patient['result'] != 'POSITIVO' and patient['result'] != 'NEGATIVO':
                continue

            if patient['testingLocation'] != 'US':
                continue

            if patient['result'] == 'POSITIVO_CONHECIDO' or patient['result'] == 'POSITIVO':
                if patient['outcome'] == 'SEGUIMENTO_NESTA_US' or patient['outcome'] == 'SEGUIMENTO_NOUTRA_US' or patient['outcome'] == 'OBITO':
                    patients.append(patient)
            else:
                patients.append(patient)

        return patients

    
    
