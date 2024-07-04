from dhis2 import Api
import pandas as pd

from src.infrastructure.forms import PatientDemographicForm

class PatientEventForm:

    def __init__(self, api: Api):
        self.api = api
        
    def find_patient_events_by_program_unit_and_period(self, program, unit, stard_date, end_date):
        patient_events = self.api.get('tracker/events', params={'skipPaging':True, 'fields':'event, status, program, trackedEntity, orgUnit, occurredAt, dataValues[dataElement,value]', 'program':program, 'orgUnit':unit, 'occurredAfter':stard_date, 'occurredBefore':end_date, 'order':'occurredAt:asc'})

        patient_events = patient_events.json()['instances']

        patient_events = self.remove_duplicates(patient_events)

        for patient_event in patient_events:

            data_values = patient_event['dataValues']
            
            for data_value in data_values:
                
                # HTS time of testing
                if data_value['dataElement'] == 'VTooAB8BVdx':
                    patient_event['timeOfTesting'] = data_value['value']
                    continue

                # HTS result
                if data_value['dataElement'] == 'Td8Ilt00ytE':
                    patient_event['result'] = data_value['value']
                    continue

                # HTS Section
                if data_value['dataElement'] == 'iyCoRAjwAY3':
                    patient_event['section'] = data_value['value']
                    continue

                # HTS breastfeeding
                if data_value['dataElement'] == 'tJcmtHSwGyJ':
                    patient_event['breastfeeding'] = data_value['value']
                    continue

                # CPN Result
                if data_value['dataElement'] == 'GhlV6KkqSrl':
                    patient_event['result'] = data_value['value']
                    continue

            del patient_event['dataValues']

        return patient_events
    
    def remove_duplicates(self, events):
        seen = set()
        unique_events = []

        for event in events:
            key = event['event']
            if key not in seen:
                seen.add(key)
                unique_events.append(event)

        return unique_events