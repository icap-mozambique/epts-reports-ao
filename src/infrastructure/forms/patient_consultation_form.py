
from src.infrastructure.forms import CARE_AND_TREATMENT

class PatientConsultationForm:
    
    CONSULTATION_STAGE = 'SvhTuAlw3zl'

    FIRST_CONSULTATION_ELEMENT_ID = 'UydTSzRCUZe'

    LAST_CONSULTATION_DATE = 'pF0rp5jbCU8'

    def __init__(self, patient_id, org_unit, api) -> None:
        self.patient_id = patient_id
        self.org_unit = org_unit
        self.api = api

    def __init__(self, api) -> None:
        self.api = api

    def add_first_consultation(self, patient):
        consultation = self.api.get('tracker/events', params={'orgUnit':self.org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.CONSULTATION_STAGE, 'trackedEntity':self.patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'order':f'{self.FIRST_CONSULTATION_ELEMENT_ID}:asc', 'pageSize':'1'})
       
        if consultation.json()['instances']:

            consultation = consultation.json()['instances'][0]
            
            for data in consultation['dataValues']:
                # get first consultation date 
                if data['dataElement'] == 'UydTSzRCUZe':
                    patient['firstConsultationDate'] = data['value']
                
                # ART start date
                if data['dataElement'] == 'QUgeSSXNzQB':
                    patient['artStartDate'] = data['value']

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