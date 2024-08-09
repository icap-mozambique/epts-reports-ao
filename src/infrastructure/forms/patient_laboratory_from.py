
import json
from logging import Logger
from dhis2 import RequestException
from src.infrastructure.forms import CARE_AND_TREATMENT

class PatientLaboratoryForm:

    LAB_STAGE = 'KXYMcOQZXLf'

    VIRAL_LOAD_RESULT_DATE = 'zY8C9WSkt4n'

    def __init__(self, logger: Logger ,api) -> None:
        self.logger = logger
        self.api = api

    def add_laboratory(self, patient):

        patient_id = patient['trackedEntity']
        org_unit = patient['orgUnit']
        
        last_lab = self.api.get('tracker/events', params={'orgUnit':org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.LAB_STAGE, 'trackedEntity':patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'order':'occurredAt:desc', 'pageSize':'1'})
        
        if last_lab.json()['instances']:
            
            last_lab = last_lab.json()['instances'][0]
            
            for data in last_lab['dataValues']:
                # get last CD4 value 
                if data['dataElement'] == 'mHMBFxYe46z':
                    patient['lastCD4'] = data['value']
    

    def add_last_viral_load_date_of_the_period(self, patient, end_period):

        patient_id = patient['trackedEntity']
        org_unit = patient['orgUnit']
        
        try:
            viral_load = self.api.get('tracker/events', params={'orgUnit':org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.LAB_STAGE, 'trackedEntity':patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}','filter':f'{self.VIRAL_LOAD_RESULT_DATE}:LE:{end_period}', 'order':f'{self.VIRAL_LOAD_RESULT_DATE}:desc', 'pageSize':'1'})
        except RequestException as e:
            description = json.loads(e.description)
            message = description['message']
            self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed. {message}")
            return
        
        if viral_load.json()['instances']:
            
            viral_load = viral_load.json()['instances'][0]
            
            for data in viral_load['dataValues']:
                # viral load result date
                if data['dataElement'] == 'zY8C9WSkt4n':
                    patient['viralLoadResultDate'] = data['value']

                # viral load result value
                if data['dataElement'] == 'SstcDVhu5ah':
                    patient['viralLoadResultValue'] = data['value']
