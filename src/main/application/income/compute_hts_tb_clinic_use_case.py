from abc import ABC, abstractmethod

class ComputeHtsTbClinicUseCase(ABC):

    PROGRAM = 'eewA8qgQWbX'

    @abstractmethod
    def compute(self, org_unit, start_period, end_period):
        pass
