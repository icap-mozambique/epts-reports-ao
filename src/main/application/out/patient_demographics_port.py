from abc import ABC, abstractmethod

class PatientDemographicsPort(ABC):
    
    @abstractmethod
    def add_patient_demographics(self, patient):
        pass
