from abc import ABC, abstractmethod

class ComputeHtsIndexCaseAcceptedUseCase(ABC):

    @abstractmethod
    def compute(self, index_case_patients):
        pass