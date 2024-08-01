from abc import ABC, abstractmethod

class ConsultationPort(ABC):
    
    @abstractmethod
    def add_patient_pregnant_or_breastfeeding_status(self, patient, end_period):
        pass