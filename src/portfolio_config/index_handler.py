import cfnresponse
import csv
import json
import boto3
import os
import logging 
from botocore.vendored import requests

print("Inicio do programa")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    sc_client = boto3.client('servicecatalog')
except Exception as e:
    cfnresponse.send(event, context, cfnresponse.FAILED, responseData)
                        
PORTFOLIO_ID = os.environ['PORTFOLIO_ID']
ORGANIZATION_ID = os.environ['ORGANIZATION_ID']  
ROLELIST = os.environ['ROLELIST']  

print("Portfolio ID", PORTFOLIO_ID)

def lambda_handler(event, context):
    print("Estamos no inicio do handler")
    print("evento: ", event)
    print("context: ", context)
    logger.info('got event {}'.format(event))
    
    responseData = {}
    print("Inicio do programa - Handler")
    try: 
        if event['RequestType'] == 'Create':
            response = sc_client.create_portfolio_share(
                AcceptLanguage='en',
                PortfolioId=PORTFOLIO_ID,
                OrganizationNode={
                    'Type': 'ORGANIZATION',
                    'Value': ORGANIZATION_ID
                },
                ShareTagOptions=True,
                SharePrincipals=True
            )
            
            servicecataloguserlist=ROLELIST.split(',')
            try:
                for user in servicecataloguserlist:
                    sc_client.associate_principal_with_portfolio(
                    AcceptLanguage='en',
                    PortfolioId=PORTFOLIO_ID,
                    PrincipalARN='arn:aws:iam:::role/' + user,
                    PrincipalType='IAM_PATTERN'
                    )
            except Exception as e: 
                pass
        if event['RequestType'] == 'Update':
            response = sc_client.update_portfolio_share(
                AcceptLanguage='en',
                PortfolioId=PORTFOLIO_ID,
                OrganizationNode={
                    'Type': 'ORGANIZATION',
                    'Value': ORGANIZATION_ID
                },
                ShareTagOptions=True,
                SharePrincipals=True
            )
            
            try:
                for user in servicecataloguserlist:
                    sc_client.associate_principal_with_portfolio(
                    AcceptLanguage='en',
                    PortfolioId=PORTFOLIO_ID,
                    PrincipalARN='arn:aws:iam:::role/' + user,
                    PrincipalType='IAM_PATTERN'
                    )
            except Exception as e: 
                pass
        if event['RequestType'] == 'Delete':

            response = sc_client.delete_portfolio_share(
                    AcceptLanguage='en',
                    PortfolioId=PORTFOLIO_ID,
                    OrganizationNode={
                        'Type': 'ORGANIZATION',
                        'Value': ORGANIZATION_ID
                    }
                )

            servicecataloguserlist=ROLELIST.split(',')

            try:
                for user in servicecataloguserlist:
                    sc_client.disassociate_principal_with_portfolio(
                    AcceptLanguage='en',
                    PortfolioId=PORTFOLIO_ID,
                    PrincipalARN='arn:aws:iam:::role/' + user,
                    PrincipalType='IAM_PATTERN'
                    )
            except Exception as e: 
                pass

        print("Fim do programa")
        logger.info('responseData {}'.format(responseData))
        cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)

    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, responseData)               