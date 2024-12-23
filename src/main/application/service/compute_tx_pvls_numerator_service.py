
from src.main.application.income import ComputeTxPvlsNumeratorUseCase

class ComputeTxPvlsNumeratorService(ComputeTxPvlsNumeratorUseCase):

    def compute(self, tx_pvls_patients):
        patients = []
        
        for patient in tx_pvls_patients:
            
            viral_load_result = int(float(patient['viralLoadResultValue']))
            
            if viral_load_result <= self.MAX_VIRAL_LOAD_SUPPPRESSED_VALUE:
                patients.append(patient)

        return patients