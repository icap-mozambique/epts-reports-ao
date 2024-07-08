from abc import ABC, abstractmethod


class ComputeHtsEmergenceWardUseCase(ABC):

    PROGRAM = 'grpiGkcSlNN'

    @abstractmethod
    def compute(org_unit, start_period, end_period):
        pass