from src.main.application.income import ComputePmtctHeiUseCase

class ComputePmtctHeiService(ComputePmtctHeiUseCase):

    def compute(self, patients_enrolled):
        patients = []

        for patient in patients_enrolled:

            if str(patient['testResult']) == 'nan':
                continue

            if patient['testResult'] != 'POSITIVO' and patient['testResult'] != 'NEGATIVO':
                continue

            patients.append(patient)
        
        return patients


