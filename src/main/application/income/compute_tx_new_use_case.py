from abc import ABC, abstractmethod
from src.main.application.income import ComputeTxCurrUseCase

class ComputeTxNewUseCase(ABC):

    def __init__(self, compute_tx_curr_use_case: ComputeTxCurrUseCase):
        self.compute_tx_curr_use_case = compute_tx_curr_use_case

    @abstractmethod
    def compute(self, patients, start_period, end_period):
        pass