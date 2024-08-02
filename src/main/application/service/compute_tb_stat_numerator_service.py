from src.main.application.income import ComputeTbStatNumeratorUseCase

class ComputeTbStatNumeratorService(ComputeTbStatNumeratorUseCase):

    def compute(self, tb_stat_patients):
        
        patients = []

        for patient in tb_stat_patients:

            if str(patient['testResult']) == 'nan':
                continue

            if patient['testResult'] != 'POSITIVO' and patient['testResult'] != 'POSITIVO_CONHECIDO' and patient['testResult'] != 'NEGATIVO' and patient['testResult'] != 'NEGATIVO_CONHECIDO':
                continue

            patients.append(patient)

        return patients


