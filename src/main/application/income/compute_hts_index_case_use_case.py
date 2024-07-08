from abc import ABC, abstractmethod


class ComputeHtsIndexCaseUseCase(ABC):

    PROGRAM = 'h5ZjECdvShC'

    PROGRAM_STAGE = 'TOImEk5U0dw'

    @abstractmethod
    def compute(self, org_unit, start_period, end_period):
        pass