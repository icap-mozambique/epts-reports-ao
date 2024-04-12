
from src.main.application.income import ComputeTxPvlsNumeratorUseCase

class ComputeTxPvlsNumeratorService(ComputeTxPvlsNumeratorUseCase):

    MAX_VIRAL_LOAD_SUPPPRESSED_VALUE = 999

    def compute(self, patients):

        for patient in patients:
            if 'txPvlsD' in patient and patient['txPvlsD'] == True:
              viral_load_result = int(float(patient['viralLoadResultValue']))

              if viral_load_result <= self.MAX_VIRAL_LOAD_SUPPPRESSED_VALUE:
                  patient['txPvlsN'] = True