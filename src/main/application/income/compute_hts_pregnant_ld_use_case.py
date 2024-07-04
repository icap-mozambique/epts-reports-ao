from abc import ABC, abstractmethod

class ComputeHtsPregnantLdUseCase(ABC):

    PROGRAM_SAT = 'grpiGkcSlNN'

    PROGRAM_PTV = 'BgTTypHIWom'
    
    @abstractmethod
    def compute(self, org_unit, start_period, end_period):
        pass