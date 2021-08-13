import os
import io
import boto3
import json
import csv

# grab environment variables
ENDPOINT_NAME = os.environ['endpoint_name2']
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.dumps(event)
    payload = data
    print(payload)
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       #ContentType='text/csv',
                                       ContentType='application/json',
                                       Body=payload)
    print(response)
    result = json.loads(response['Body'].read().decode())
    print(result)
    predictions = result['predictions']
    
    return predictions