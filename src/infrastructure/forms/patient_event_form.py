from dhis2 import Api

from src.infrastructure.forms.program import DPI, DPI_STAGE, PTV, PTV_STAGE, TB, TB_STAGE

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
    
    def add_patient_first_anc_event(self, patient):
       first_anc = self.api.get('tracker/events', params={'orgUnit':patient['orgUnit'], 'program':PTV, 'programStage':PTV_STAGE, 'trackedEntity':patient['trackedEntity'], 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'order':'occurredAt:desc', 'pageSize':'1'})
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

    def add_patient_first_tb_event(self, patient):
       first_tb = self.api.get('tracker/events', params={'orgUnit':patient['orgUnit'], 'program':TB, 'programStage':TB_STAGE, 'trackedEntity':patient['trackedEntity'], 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'order':'occurredAt:asc', 'pageSize':'1'})
       first_tb = first_tb.json()['instances']

       if len(first_tb) != 0:
           data_values = first_tb[0]['dataValues']

           for data_value in data_values:
               
               # TB ENROLLMENT DATE
               if data_value['dataElement'] == 'kvEVYX7nMso':
                   patient['enrollmentDate'] =  data_value['value'] 

               # TB HIV TEST DATE
               if data_value['dataElement'] == 'tdDPWBFtKfM':
                   patient['hivTestDate'] =  data_value['value'] 

               # TB HIV TEST RESULT
               if data_value['dataElement'] == 'aFAkYYmy78J':
                   patient['testResult'] =  data_value['value'] 

               # TB ART START DATE
               if data_value['dataElement'] == 'ZAgN1kYejG2':
                   patient['artStartDate'] =  data_value['value'] 

               # TB ART STATUS
               if data_value['dataElement'] == 'PaB03WOer8w':
                   patient['artStatus'] =  data_value['value'] 

    def add_patient_last_dpi_event(self, patient):
       last_dpi = self.api.get('tracker/events', params={'orgUnit':patient['orgUnit'], 'program':DPI, 'programStage':DPI_STAGE, 'trackedEntity':patient['trackedEntity'], 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'order':'occurredAt:desc', 'pageSize':'1'})
       last_dpi = last_dpi.json()['instances']

       if len(last_dpi) != 0:
           data_values = last_dpi[0]['dataValues']

           for data_value in data_values:
               
               # DPI CHILD EXPOSED
               if data_value['dataElement'] == 'MGIuReFLpqs':
                   patient['exposed'] =  data_value['value'] 

               # DPI PCR NUMBER
               if data_value['dataElement'] == 'ibcg89iMWHN':
                   patient['pcrNumber'] =  data_value['value'] 

               # DPI PCR RESULT
               if data_value['dataElement'] == 'RTgqf4cyKpK':
                   patient['testResult'] =  data_value['value'] 

               # DPI ART START DATE
               if data_value['dataElement'] == 'F8UJoKnqf9k':
                   patient['artStartDate'] =  data_value['value']