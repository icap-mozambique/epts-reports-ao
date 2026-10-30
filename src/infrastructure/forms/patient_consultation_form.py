
import pandas as pd
from src.infrastructure.forms import CARE_AND_TREATMENT

class PatientConsultationForm:
    
    CONSULTATION_STAGE = 'SvhTuAlw3zl'

    FIRST_CONSULTATION_ELEMENT_ID = 'UydTSzRCUZe'

    LAST_CONSULTATION_DATE = 'pF0rp5jbCU8'

    def __init__(self, api) -> None:
        self.api = api

    def add_first_consultation(self, patient):
        org_unit = patient['orgUnit']
        patient_id = patient['trackedEntity']

        consultation = self.api.get('tracker/events', params={'orgUnit':org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.CONSULTATION_STAGE, 'trackedEntity':patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'order':f'{self.FIRST_CONSULTATION_ELEMENT_ID}:asc', 'pageSize':'1'})
       
        if consultation.json()['instances']:

            consultation = consultation.json()['instances'][0]
            
            for data in consultation['dataValues']:
                # get first consultation date 
                if data['dataElement'] == 'UydTSzRCUZe':
                    patient['firstConsultationDate'] = data['value']
                
                # ART start date
                if data['dataElement'] == 'QUgeSSXNzQB':
                    patient['artStartDate'] = data['value']

                # entry type
                if data['dataElement'] == 'coUpJW0EwSl':
                    patient['entryType'] = data['value']


    def add_patient_pregnant_or_breastfeeding_status(self, patient, end_period):
        org_unit = patient['orgUnit']
        patient_id = patient['trackedEntity']

        consultation = self.api.get('tracker/events', params={'orgUnit':org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.CONSULTATION_STAGE, 'trackedEntity':patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'filter':f'{self.LAST_CONSULTATION_DATE}:LE:{end_period}' ,'order':f'{self.LAST_CONSULTATION_DATE}:desc', 'pageSize':'1'})
       
        if consultation.json()['instances']:

            consultation = consultation.json()['instances'][0]
            
            for data in consultation['dataValues']:
                # Pregnant
                if data['dataElement'] == 'mrAbW8SIox9':
                    patient['pregnant'] = data['value']
                
                # Breastfeeding
                if data['dataElement'] == 'pnwHXKiDPD9':
                    patient['breastfeeding'] = data['value']

    def add_tb_screening_info(self, patient, start_period, end_period):
        org_unit = patient['orgUnit']
        patient_id = patient['trackedEntity']

        start_period_three_months_before = pd.to_datetime(start_period) - pd.DateOffset(months=3)
        start_period_three_months_before = start_period_three_months_before.strftime('%Y-%m-%d')
        
        events = self.api.get('tracker/events', params=[('skipPaging',True), ('fields','event, status, program, trackedEntity, orgUnit, occurredAt, dataValues[dataElement,value]'),('trackedEntity', patient_id), ('program', CARE_AND_TREATMENT), ('programStage', self.CONSULTATION_STAGE), ('orgUnit', org_unit), ('filter',f'{self.LAST_CONSULTATION_DATE}:GE:{start_period_three_months_before}'), ('filter', f'{self.LAST_CONSULTATION_DATE}:LE:{end_period}'), ('order', 'occurredAt:asc')])
        events = events.json()['instances']

        tb_entry_type = ''
        
        if events:
            for event in events:
                
                for data in event['dataValues']:
                    
                    if tb_entry_type == '' and data['dataElement'] == 'coUpJW0EwSl':
                        tb_entry_type = data['value']
                        patient['tb_entry_type'] = tb_entry_type
                    
                    # tb screening 
                    if data['dataElement'] == 'AWiqP7HQTV9':
                        patient['tb_screened'] = data['value']

                    # type of screening
                    if data['dataElement'] == 'uw9Y3HL4Qoe':
                        patient['tb_screening_type'] = data['value']
                    
                    # tb status
                    if data['dataElement'] == 'W2qpMQmbRqq':
                        patient['tb_status'] = data['value']

                    

                    

