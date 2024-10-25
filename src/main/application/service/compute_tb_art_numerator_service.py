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

            if patient['testResult'] != 'POSITIVO':
                continue

            if patient['artStatus'] != 'NOVO' and patient['artStatus'] != 'ANTIGO':
                continue

            patients.append(patient)

        return patients
