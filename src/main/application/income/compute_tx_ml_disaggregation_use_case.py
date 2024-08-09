from abc import ABC, abstractmethod


class ComputeTxMlDisaggregationUseCase(ABC):
    GENDERS = ['Female', 'Male']
    
    LESS_THAN_ONE_YEAR = '<1'
    
    SIXTY_FIVE_MORE = '65+'

    OUTCOMES = ['Died','Interruption in Treatment (<3 Months Treatment)', 'Interruption in Treatment (3-5 Months Treatment)', 'Interruption In Treatment (6+ Months Treatment)', 'Transferred Out', 'Refused (Stopped) Treatment']

    THREE_MONTHS = 90

    FIVE_MONTHS = 179

    SIX_MONTHS = 180

    @abstractmethod
    def compute(self, patients, end_period):
        pass