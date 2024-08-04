from src.main.application.income import ComputePmtctEidUseCase

class ComputePmtctEidService(ComputePmtctEidUseCase):

    def compute(self, patients_enrolled):
        patients = []

        for patient in patients_enrolled:

            if str(patient['testResult']) == 'nan':
                continue

            patients.append(patient)

        return patients

