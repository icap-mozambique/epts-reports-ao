
from src.infrastructure.forms import CARE_AND_TREATMENT

class PatientConsultationForm:
    
    CONSULTATION_STAGE = 'SvhTuAlw3zl'
    FIRST_CONSULTATION_ELEMENT_ID = 'UydTSzRCUZe'

    def __init__(self, patient_id, org_unit, api) -> None:
        self.patient_id = patient_id
        self.org_unit = org_unit
        self.api = api

    def add_first_consultation(self, patient):
        consultation = self.api.get('tracker/events', params={'orgUnit':self.org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.CONSULTATION_STAGE, 'trackedEntity':self.patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'order':f'{self.FIRST_CONSULTATION_ELEMENT_ID}:asc', 'pageSize':'1'})
        
        consultation = consultation.json()['instances'][0]
        
        for data in consultation['dataValues']:
            # get first consultation date 
            if data['dataElement'] == 'UydTSzRCUZe':
                patient['firstConsultationDate'] = data['value']
            
            # ART start date
            if data['dataElement'] == 'QUgeSSXNzQB':
                patient['artStartDate'] = data['value']