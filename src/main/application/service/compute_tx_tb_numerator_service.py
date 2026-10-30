from src.main.application.income import ComputeTxTbNumeratorUseCase

class ComputeTxTbNumeratorService(ComputeTxTbNumeratorUseCase):

    def compute(self, enrolled_patients):
        patients = []

        for patient in enrolled_patients:
            if patient['tb_screened'] != True:
                continue

            if patient['tb_status'] != 'Diagnosticado e Iniciou Tratamento da TB':
                continue

            patients.append(patient)

        return patients


            


