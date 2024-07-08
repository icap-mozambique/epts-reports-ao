from abc import ABC, abstractmethod

class ComputeHtsOtherPitcUseCase(ABC):

    PROGRAM = 'grpiGkcSlNN'

    @abstractmethod
    def compute(self, org_unit, start_period, end_period):
        pass