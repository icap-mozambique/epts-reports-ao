class PatientDemographicForm:

    def __init__(self, api) -> None:
        self.api = api

    def add_demographics(self, patient):
        
        patient_id = patient['trackedEntity']
        org_unit = patient['orgUnit']

        patient_demographic = self.api.get(f'tracker/trackedEntities/{patient_id}', params={'orgUnit':org_unit, 'trackedEntityType':'F3jh38FNCkP', 'skipPaging':'true','fields':'{,trackedEntity,trackedEntityType, attributes=[attribute, displayName,value]}'})

        patient_demographic = patient_demographic.json()

        for patient_demographic in patient_demographic['attributes']:
            # get patient ID
            if patient_demographic['attribute'] == 'UcHFpmknDEX':
                patient['patientIdentifier'] = patient_demographic['value']

            # get patient NAME
            if patient_demographic['attribute'] == 'sJk1y9bHXxj':
                patient['patientName'] = patient_demographic['value']

            # get patient AGE
            if patient_demographic['attribute'] == 'WHMtrrYH1WA':
                patient['patientAge'] = patient_demographic['value']
            
            # get patient GENDER
            if patient_demographic['attribute'] == 'DIcP7BuFpar':
                patient['patientSex'] = patient_demographic['value']