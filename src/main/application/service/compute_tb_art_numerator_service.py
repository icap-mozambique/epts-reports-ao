from src.main.application.income import ComputeTbArtNumeratorUseCase

class ComputeTbArtNumeratorService(ComputeTbArtNumeratorUseCase):

    def compute(self, patients_enrolled):
        patients = []

        for patient in patients_enrolled:

            if str(patient['testResult']) == 'nan':
                continue

            if str(patient['artStartDate']) == 'nan':
                continue

            if str(patient['artStatus']) == 'nan':
                continue

            if patient['testResult'] != 'POSITIVO' and patient['testResult'] !='POSITIVO_CONHECIDO':
                continue

            if patient['artStatus'] != 'NOVO' and patient['artStatus'] != 'ANTIGO' and patient['artStatus'] != 'TARV_NOUTRA_US':
                continue

            if patient['testResult'] == 'POSITIVO_CONHECIDO' :
                if 'outcome' in patient and (patient['outcome'] == 'FAZ_TARV' or patient['outcome'] == 'VIH_POSITIVO'):
                    patients.append(patient)
                    continue
            else:
                if 'outcome' in patient and (patient['outcome'] == 'SEGUIMENTO_NESTA_US' or patient['outcome'] == 'SEGUIMENTO_NOUTRA_US' or patient['outcome'] == 'OBITO'):
                    patients.append(patient)
                    
        return patients
