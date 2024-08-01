from src.main.application.income.compute_pmtct_art_numerator_use_case import ComputePmtctArtNumeratorUseCase

class ComputePmtctArtNumeratorService(ComputePmtctArtNumeratorUseCase):

    def compute(self, enrolled_patients):

        patients = []
        
        for enrolled_patient in enrolled_patients:

            if str(enrolled_patient['ancType']) == 'nan':
                continue

            if enrolled_patient['ancType'] != 'PRIMEIRA_CONSULTA':
                continue

            if str(enrolled_patient['testResult']) == 'nan':
                continue 

            if str(enrolled_patient['testResult']) != 'POSITIVO' and str(enrolled_patient['testResult']) != 'POSITIVO_CONHECIDO':
                continue

            if str(enrolled_patient['onArt']) == 'nan':
                continue

            if enrolled_patient['onArt'] != True:
                continue

            patients.append(enrolled_patient)
        
        return patients





