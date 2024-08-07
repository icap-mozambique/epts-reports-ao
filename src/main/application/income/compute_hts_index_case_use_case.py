from abc import ABC, abstractmethod

class ComputeHtsIndexCaseUseCase(ABC):
    
    @abstractmethod
    def compute(self, index_case_patients):
        pass