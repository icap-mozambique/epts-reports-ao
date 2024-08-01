from abc import ABC, abstractmethod

class ComputeTxNewDisaggregationUseCase(ABC):
     
     GENDERS = ['Female', 'Male']
     
     CD4S = ['<200 CD4', '>=200 CD4', 'CD4 Unknown']

     LESS_THAN_ONE_YEAR = '<1'

     SIXTY_FIVE_MORE = '65+'

     CD4_MINIMUM_VALUE = 200

     @abstractmethod
     def compute(self, patients):
      pass