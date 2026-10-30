from src.main.application.income import ComputeTxTbDenominatorUseCase

class ComputeTxTbDenominatorService(ComputeTxTbDenominatorUseCase):
    
    def compute(self, enrolled_patients):
        patients = []

        for patient in enrolled_patients:
            if patient['tb_screened'] == True:
                patients.append(patient)

        return patients



