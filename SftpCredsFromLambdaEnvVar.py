import boto3;
import os
import json;
from datetime import datetime


#Function to retrieve Our SFTP Credentials from Lambda Function's Environmental Variables.
def get_sftp_credentials():
    
    #region_name = "us-east-2"
    try :
        credentials = {
            'sftp_host' : os.environ['SFTP_Host'],
            'sftp_port' : int(os.environ.get('SFTP_Port')) ,
            'sftp_username' : os.environ['SFTP_Username'],
            'sftp_password' : os.environ['SFTP_Password'],
            'remote_directory' : os.environ['Remote_Directory'],
            's3_bucket_name' : os.environ['InitialFileFrom_SFTP_S3BucketName'],
            's3_key_name' : os.environ['S3_KeyName'] +  "-" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return credentials;    
   
    except KeyError as e:

        print(f"Error retrieving Credentials from Lambda environment Variables. : {e}")
        raise KeyError(f"Missing required environment variables: {e}")
    

  