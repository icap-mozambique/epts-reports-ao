from abc import ABC, abstractmethod

class ComputeTxNewDisaggregationUseCase(ABC):
     
     GENDERS = ['Female', 'Male']
     
     CD4S = ['<200', '>=200', 'CD4 Unknown']

     AGE_BANDS = ['<1', '1-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65+']

     LESS_THAN_ONE_YEAR = '<1'

     SIXTY_FIVE_MORE = '65+'

     CD4_MINIMUM_VALUE = 200

     @abstractmethod
     def compute(self, patients):
      pass