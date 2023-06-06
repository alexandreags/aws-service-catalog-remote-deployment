import boto3
import os
import cfnresponse
import logging 
import time
from botocore.vendored import requests
######

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Set Logger to stdout too
logger.addHandler(logging.StreamHandler())

####
# Env Variables:

DEPLOY_ACCOUNT_ID = os.eviron['DEPLOY_ACCOUNT_ID']

AWS_REGION_NAME = 'us-east-1'

org_client = boto3.client('organizations', region_name=AWS_REGION_NAME)

def enable_service_access(Principal):
    try:
        logger.info(f'Habilitando Service Access {Principal}')
        
        service_access_response = org_client.enable_aws_service_access(
            ServicePrincipal=Principal
        )
        
        return service_access_response
    
    except Exception as e:
        error_handler(e)

def manage_delegated_admin(AccountId,Service,event):
    try:
        if event['RequestType'] == 'Create':
            logger.info(f'Registrando delegated Admin para conta {AccountId}')
            delegated_admin_response = org_client.register_delegated_administrator(
            AccountId=AccountId,
            ServicePrincipal=Service
            )
            return delegated_admin_response
        if event['RequestType'] == 'Delete':
            logger.info(f'Removendo delegated Admin para conta {AccountId}')
            delegated_admin_response = org_client.deregister_delegated_administrator(
            AccountId=AccountId,
            ServicePrincipal=Service
            )
            return delegated_admin_response
    except Exception as e:
        error_handler(e)

def log(message, severity):
    if severity == 'error':
        logger.error(message)
    else:
        logger.info(message)
        

def error_handler(Ex,event,context):
    responsedata = {}
    responsedata['Erro'] = str(Ex)
    log(f'### Ocorreu um erro durante o provisionamento: \n {responsedata}')
    cfnresponse.send(event, context, cfnresponse.FAILED, responsedata) 



def lambda_handler(event,context):
    
    if event['RequestType'] == 'Create':
        
        enable_service_access('servicecatalog.amazonaws.com')
        enable_service_access('member.org.stacksets.cloudformation.amazonaws.com')
        manage_delegated_admin(DEPLOY_ACCOUNT_ID,'servicecatalog.amazonaws.com', event)
        manage_delegated_admin(DEPLOY_ACCOUNT_ID,'cloudformation.amazonaws.com', event)

    if event['RequestType'] == 'Delete':

        manage_delegated_admin(DEPLOY_ACCOUNT_ID,'servicecatalog.amazonaws.com', event)
        manage_delegated_admin(DEPLOY_ACCOUNT_ID,'cloudformation.amazonaws.com', event)
