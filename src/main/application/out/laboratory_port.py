from abc import ABC, abstractmethod

class LaboratoryPort(ABC):

    @abstractmethod
    def add_last_viral_load_result_date_of_the_period(self, patient, end_period):
        pass