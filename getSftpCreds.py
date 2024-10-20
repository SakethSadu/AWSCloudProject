import boto3;

import json;
from botocore.exceptions import ClientError


#Function to retrieve Our SFTP Credentials from AWS Secret Manager
def get_secret(secret_name):

    
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name )           
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        print(f"Error retrieving secrets")
        raise e
  