from src.main.application.income import ComputeHtsIndexCaseAcceptedUseCase

class ComputeHtsIndexCaseAcceptedService(ComputeHtsIndexCaseAcceptedUseCase):

    def compute(self, index_case_patients):
        patients = []

        for patient in index_case_patients:

            if patient['childrenLessThan15Years'] == 'Sim' or patient['childrenLessThan15Years'] == 'true' or patient['testPartner'] == 'true' or patient['testPartner'] == 'Sim':
                patients.append(patient)
        
        return patients

