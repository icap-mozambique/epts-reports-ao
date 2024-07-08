from abc import ABC, abstractmethod

class EventPort(ABC):

    @abstractmethod
    def find_patient_events_by_program_unit_and_period(self, program, unit, start_date, end_date):
        pass

    @abstractmethod
    def find_patient_events_by_program_program_stage_unit_and_period(self, program, program_stage, unit, start_date, end_date):
        pass