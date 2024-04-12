import pandas as pd

from src.main.application.out import LaboratoryPort
from src.main.application.income import ComputeTxPvlsDenominatorUseCase
from src.main.application.income import ComputeTxCurrUseCase

class ComputeTxPvlsDenominatorService(ComputeTxPvlsDenominatorUseCase):

    def __init__(self, tx_curr_use_case: ComputeTxCurrUseCase, laboratory_port: LaboratoryPort) -> None:
        self.tx_curr_use_case = tx_curr_use_case
        self.laboratory_port = laboratory_port

    def compute(self, patients, end_period):
        for patient in patients:
            if self.tx_curr_use_case.is_currently_on_art(patient, end_period):
                
                self.laboratory_port.add_last_viral_load_result_date_of_the_period(patient, end_period)

                if 'viralLoadResultDate' in patient:
                    art_start_date = pd.to_datetime(patient['artStartDate'])
                    last_vl_date = pd.to_datetime(patient['viralLoadResultDate'])

                    days_between = (last_vl_date - art_start_date).days

                    if days_between >= self.DAYS_IN_ART:
                        patient['txPvlsD'] = True