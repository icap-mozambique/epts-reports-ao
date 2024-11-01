from src.main.application.income import ComputeHtsIndexCaseAcceptedUseCase

class ComputeHtsIndexCaseAcceptedService(ComputeHtsIndexCaseAcceptedUseCase):

    def compute(self, index_case_patients):
        patients = []

        for patient in index_case_patients:

            if patient['childrenLessThan15Years'] == True or patient['testPartner'] == True:
                patients.append(patient)
        
        return patients

