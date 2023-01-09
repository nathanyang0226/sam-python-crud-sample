import boto3
import sys
import os
import json
import uuid
import logging
import traceback
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(message, context):

    if ('body' not in message or
            message['httpMethod'] != 'POST'):
        return {
            'statusCode': 400,
            'headers': {},
            'body': json.dumps({'msg': 'Bad Request'})
        }


    '''Simple Lambda function add logger component'''
    try:
        logger.info(f'message: {message}')

        table_name = os.environ.get('TABLE', 'Activities')
        region = os.environ.get('REGION', 'cn-northwest-1')
        aws_environment = os.environ.get('AWSENV', 'AWS')

        if aws_environment == 'AWS_SAM_LOCAL':
            activities_table = boto3.resource(
                'dynamodb',
                endpoint_url='http://dynamodb:8000'
            )
        else:
            activities_table = boto3.resource(
                'dynamodb',
                region_name=region
            )

        table = activities_table.Table(table_name)
        activity = json.loads(message['body'])

        params = {
            'id': str(uuid.uuid4()),
            'date': str(datetime.timestamp(datetime.now())),
            'stage': activity['stage'],
            'description': activity['description']
        }

        response = table.put_item(
            TableName=table_name,
            Item=params
        )
        print(response)

        return {
            'statusCode': 201,
            'headers': {},
            'body': json.dumps({'msg': 'Activity created'})
        }

      
    except Exception as exp:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
        err_msg = json.dumps({
            "errorType": exception_type.__name__,
            "errorMessage": str(exception_value),
            "stackTrace": traceback_string
        })
        logger.error(err_msg)

    
