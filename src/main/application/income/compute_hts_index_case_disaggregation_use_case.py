from abc import ABC, abstractmethod

class ComputeHtsIndexCaseDisaggregationUseCase(ABC):

    GENDERS = ['Female', 'Male']
    
    RESULTS = ['Known at Entry Positive', 'Newly Identified Positive', 'Newly Identified Negative', 'Documented Negative']

    LESS_THAN_ONE_YEAR = '<1'
    
    FIXTY_MORE = '50+'

    DOCUMENTED_NEGATIVE_BANDS = ['1-4', '5-9', '10-14']

    @abstractmethod
    def compute(self, index_case_patients, end_period):
        pass