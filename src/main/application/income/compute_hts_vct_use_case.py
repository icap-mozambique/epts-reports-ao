from abc import ABC, abstractmethod


class ComputeHtsVctUseCase(ABC):
    
    PROGRAM = 'grpiGkcSlNN'
    
    @abstractmethod
    def compute(self, org_unit, start_date, end_date):
        pass