from abc import ABC, abstractmethod

class ComputeHtsPmtctAncUseCase(ABC):

    PROGRAM = 'BgTTypHIWom'

    @abstractmethod
    def compute(org_unit, start_period, end_period):
        pass
