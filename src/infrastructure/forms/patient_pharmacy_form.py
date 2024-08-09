import json
from dhis2 import RequestException
import pandas as pd
from src.infrastructure.forms import CARE_AND_TREATMENT

class PatientPharmacyForm:

    PHARMACY_STAGE = 'P2kauR0fz6C'

    LAST_PICKUP_DATA_ELEMENT_ID = 'f1E1lgVGby4'

    def __init__(self, logger, api) -> None:
        self.logger = logger
        self.api = api

    def add_last_pharmacy(self, patient, end_period):
        patient_id = patient['trackedEntity']
        org_unit = patient['orgUnit']
      
        last_pharmacy = self.api.get('tracker/events', params={'orgUnit':org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.PHARMACY_STAGE, 'trackedEntity':patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'filter':f'{self.LAST_PICKUP_DATA_ELEMENT_ID}:LE:{end_period}', 'order':f'{self.LAST_PICKUP_DATA_ELEMENT_ID}:desc', 'pageSize':'1'})

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

    def find_last_pickup_of_the_period(self, patient, end_period):

        patient_id = patient['trackedEntity']
        org_unit = patient['orgUnit']

        try:
            last_pharmacy = self.api.get('tracker/events', params={'orgUnit':org_unit, 'program':CARE_AND_TREATMENT, 'programStage':self.PHARMACY_STAGE, 'trackedEntity':patient_id, 'fields':'{,trackedEntity,programStage,dataValues=[dataElement,value]}', 'filter':f'{self.LAST_PICKUP_DATA_ELEMENT_ID}:LT:{end_period}', 'order':f'{self.LAST_PICKUP_DATA_ELEMENT_ID}:desc', 'pageSize':'1'})
        except RequestException as e:
            description = json.loads(e.description)
            message = description['message']
            self.logger.warning(f"The patient: {patient['trackedEntity']} - {patient['patientIdentifier']} - {patient['patientName']} - {patient['patientSex']} of facility {patient['orgUnit']} was not processed. {message}")
            return
        
        if last_pharmacy.json()['instances']:
            last_pharmacy = last_pharmacy.json()['instances'][0]
            
            lastPickupDate = 'nan'
            pickupQuantity = 'nan'

            for data in last_pharmacy['dataValues']:
                # get last pickup date 
                if data['dataElement'] == 'f1E1lgVGby4':
                    lastPickupDate = data['value']
                
                # drugs pickup quantity
                if data['dataElement'] == 'PWY0qgJN37G':
                    pickupQuantity = data['value']
            
            #calculate next pickupDate of the period
            if lastPickupDate != 'nan' and pickupQuantity != 'nan':
                patient['priorNextPickupDate'] = pd.to_datetime(lastPickupDate) + pd.Timedelta(days=int(pickupQuantity))
