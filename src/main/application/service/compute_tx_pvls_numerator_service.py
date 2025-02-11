
from src.main.application.income import ComputeTxCurrUseCase
from src.main.application.income import ComputeTxPvlsNumeratorUseCase

class ComputeTxPvlsNumeratorService(ComputeTxPvlsNumeratorUseCase):

    def __init__(self, tx_curr_service: ComputeTxCurrUseCase, end_period):
        self.tx_curr_service = tx_curr_service
        self.end_period = end_period

    def compute(self, tx_pvls_patients):
        
        patients = []
        
        for patient in tx_pvls_patients:

            if not self.tx_curr_service.is_currently_on_art(patient, self.end_period):
                continue
            
            viral_load_result = int(float(patient['viralLoadResultValue']))
            
            if viral_load_result <= self.MAX_VIRAL_LOAD_SUPPPRESSED_VALUE:
                patients.append(patient)

        return patients