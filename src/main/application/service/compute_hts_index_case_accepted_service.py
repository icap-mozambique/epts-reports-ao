from src.main.application.income import ComputeHtsIndexCaseAcceptedUseCase

class ComputeHtsIndexCaseAcceptedService(ComputeHtsIndexCaseAcceptedUseCase):

    def compute(self, index_case_patients):
        patients = []

        for patient in index_case_patients:

            if str(patient['childrenLessThan15Years']) == 'nan':
                continue

            if str(patient['testPartner']) == 'nan':
                continue

            if patient['childrenLessThan15Years'] == False and patient['testPartner'] == False:
                continue
            
            patients.append(patient)
        
        return patients

