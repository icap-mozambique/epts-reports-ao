from src.main.application.income import ComputePmtctHeiUseCase

class ComputePmtctHeiService(ComputePmtctHeiUseCase):

    def compute(self, patients_enrolled):
        patients = []

        for patient in patients_enrolled:

            if str(patient['testResult']) == 'nan':
                continue

            if patient['testResult'] != 'POSITIVO' and patient['testResult'] != 'NEGATIVO':
                continue

            if patient['testResult'] == 'POSITIVO' :
                if 'outcome' in patient and (patient['outcome'] == 'SEGUIMENTO_NESTA_US' or patient['outcome'] == 'SEGUIMENTO_NOUTRA_US' or patient['outcome'] == 'OBITO'):
                    patients.append(patient)
            else:
                patients.append(patient)
        
        return patients


