import json
import github
import os
import boto3


GIT_TOKEN=os.environ['GIT_TOKEN']
REPO=os.environ['REPOSITORY']

git = github.Github(GIT_TOKEN)
repo = git.get_repo(REPO)
print(repo.get_contents("cf_templates"))



def lambda_handler(event, context):
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

#lambda_handler(None,None)