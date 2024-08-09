
from src.infrastructure.forms import CARE_AND_TREATMENT

class PatientOutcomeForm:
    
    FINAL_OUTCOME_STAGE = 'LsiTuPWVsOC'

    def __init__(self, api) -> None:
        self.api = api

    def add_final_outcome(self, patient):
        patient_id = patient['trackedEntity']
        org_unit = patient['orgUnit']
   
        final_outcome = self.api.get('tracker/events', params={'skipPaging':'true','orgUnit':org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.FINAL_OUTCOME_STAGE, 'trackedEntity':patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}'})

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
