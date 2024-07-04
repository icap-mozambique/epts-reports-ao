import pandas as pd
from src.infrastructure.forms import CARE_AND_TREATMENT

class PatientPharmacyForm:

    PHARMACY_STAGE = 'P2kauR0fz6C'

    LAST_PICKUP_DATA_ELEMENT_ID = 'f1E1lgVGby4'

    def __init__(self, patient_id, org_unit, api) -> None:
        self.patient_id = patient_id
        self.org_unit = org_unit
        self.api = api

    def add_last_pharmacy(self, patient, end_period):
      
        last_pharmacy = self.api.get('tracker/events', params={'orgUnit':self.org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.PHARMACY_STAGE, 'trackedEntity':self.patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'filter':f'{self.LAST_PICKUP_DATA_ELEMENT_ID}:LE:{end_period}', 'order':f'{self.LAST_PICKUP_DATA_ELEMENT_ID}:desc', 'pageSize':'1'})

        if last_pharmacy.json()['instances']:
            last_pharmacy = last_pharmacy.json()['instances'][0]
            
            for data in last_pharmacy['dataValues']:
                # get last pickup date 
                if data['dataElement'] == 'f1E1lgVGby4':
                    patient['lastPickupDate'] = data['value']
                
                # drugs pickup quantity
                if data['dataElement'] == 'PWY0qgJN37G':
                    patient['pickupQuantity'] = data['value']
            
            #calculate next pickupDate
            if ('lastPickupDate' in patient and 'pickupQuantity' in patient):
                patient['nextPickupDate'] = pd.to_datetime(patient['lastPickupDate']) + pd.Timedelta(days=int(patient['pickupQuantity']))
