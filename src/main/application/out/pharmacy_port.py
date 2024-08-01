from abc import ABC, abstractmethod

class PharmacyPort(ABC):
    
    @abstractmethod
    def find_last_pickup_of_the_period(self, patient, period):
        pass