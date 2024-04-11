
from src.infrastructure.forms import CARE_AND_TREATMENT

class PatientOutcomeForm:
    
    FINAL_OUTCOME_STAGE = 'LsiTuPWVsOC'

    def __init__(self, patient_id, org_unit, api) -> None:
        self.patient_id = patient_id
        self.org_unit = org_unit
        self.api = api

    def add_final_outcome(self, patient):
   
        final_outcome = self.api.get('tracker/events', params={'skipPaging':'true','orgUnit':self.org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.FINAL_OUTCOME_STAGE, 'trackedEntity':self.patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}'})

        if final_outcome.json()['instances']:

            final_outcome = final_outcome.json()['instances'][0]
            
            for data in final_outcome['dataValues']:
                # Transfered out
                if data['dataElement'] == 'JfsZJNCPYMy':
                    patient['transferedOut'] = data['value']
                
                # date of transfer
                if data['dataElement'] == 'tlBekbbYASc':
                    patient['dateOfTransfer'] = data['value']

                # dead
                if data['dataElement'] == 'ZmoHwddq6DD':
                    patient['dead'] = data['value']

                # date of death
                if data['dataElement'] == 'KmRHXvsQy2W':
                    patient['dateOfDeath'] = data['value']
