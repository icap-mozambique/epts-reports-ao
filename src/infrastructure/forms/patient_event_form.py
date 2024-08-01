from dhis2 import Api

from src.infrastructure.forms.program import PTV

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

                # TIPO de CPN
                if data_value['dataElement'] == 'A2KEZYwGcBm':
                    patient_event['cpn_type'] = data_value['value']
                    continue

                 # TB time of testing
                if data_value['dataElement'] == 'KVuFpsYQ2iS':
                    patient_event['timeOfTesting'] = data_value['value']
                    continue

                # TB result
                if data_value['dataElement'] == 'aFAkYYmy78J':
                    patient_event['result'] = data_value['value']
                    continue

            del patient_event['dataValues']

        return patient_events
    
    def find_patient_events_by_program_program_stage_unit_and_period(self, program, program_stage, unit, stard_date, end_date):
        patient_events = self.api.get('tracker/events', params={'skipPaging':True, 'fields':'event, status, program, trackedEntity, orgUnit, occurredAt, dataValues[dataElement,value]', 'program':program, 'programStage':program_stage, 'orgUnit':unit, 'occurredAfter':stard_date, 'occurredBefore':end_date, 'order':'occurredAt:asc'})

        patient_events = patient_events.json()['instances']

        patient_events = self.remove_duplicates(patient_events)

        for patient_event in patient_events:

            data_values = patient_event['dataValues']
            
            for data_value in data_values:
                
                # INDEX CASE New case
                if data_value['dataElement'] == 'v3pBLn8T0aF':
                    patient_event['ic_new_case'] = data_value['value']
                    continue

                # INDEX CASE result
                if data_value['dataElement'] == 'kYwM1zzUgrg':
                    patient_event['result'] = data_value['value']
                    continue

                # INDEX CASE Test Date
                if data_value['dataElement'] == 'u4P9Vo7xnBi':
                    patient_event['ic_date'] = data_value['value']
                    continue

                # INDEX CASE Age
                if data_value['dataElement'] == 'h3t89GiutbB':
                    patient_event['patientAge'] = data_value['value']
                    continue

                # INDEX CASE SEX
                if data_value['dataElement'] == 'dGhN36P3NdR':
                    patient_event['patientSex'] = data_value['value']
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
    
    def add_patient_first_anc_event(self, patient, anc_stage):
       first_anc = self.api.get('tracker/events', params={'orgUnit':patient['orgUnit'], 'program':PTV, 'programStage':anc_stage, 'trackedEntity':patient['trackedEntity'], 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'order':'occurredAt:desc', 'pageSize':'1'})
       first_anc = first_anc.json()['instances']

       if len(first_anc) != 0:
           data_values = first_anc[0]['dataValues']

           for data_value in data_values:
               
               # ANC TYPE
               if data_value['dataElement'] == 'A2KEZYwGcBm':
                   patient['ancType'] =  data_value['value'] 

               # ANC TEST RESULT
               if data_value['dataElement'] == 'GhlV6KkqSrl':
                   patient['testResult'] =  data_value['value'] 

               # ANC ART START DATE
               if data_value['dataElement'] == 'PPCZ7VP2D32':
                   patient['artStartDate'] =  data_value['value'] 

               # ANC ART STATUS
               if data_value['dataElement'] == 'OiJQUObDjsY':
                   patient['artStatus'] =  data_value['value'] 

               # ANC ON ART
               if data_value['dataElement'] == 'XzilEjpZy3g':
                   patient['onArt'] =  data_value['value'] 