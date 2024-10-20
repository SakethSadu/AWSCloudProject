'''
@author - Saketh Sadu
Created On 10/19/24
'''
import paramiko
from paramiko import SFTPClient
from getSftpCreds import get_secret
from SftpCredsFromLambdaEnvVar import get_sftp_credentials
from s3FileTransfer import uploadToS3, transferFileSFTPToS3, uploadFileFromSFTPToS3

def lambda_handler(event, context):
    try:
        credentials = get_sftp_credentials()
        transport = paramiko.Transport((credentials['sftp_host'], int(credentials['sftp_port'])))
        transport.connect(username=credentials['sftp_username'], password=credentials['sftp_password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
    except paramiko.AuthenticationException as auth_err:
        raise paramiko.AuthenticationException(f"SFTP Authentication failed: {auth_err}")
    except paramiko.SSHException as ssh_err:
        raise paramiko.SSHException(f"SSH connection failed: {ssh_err}")
    
    try:
        response = uploadFileFromSFTPToS3(sftp, credentials)
        return response
    except KeyError as env_err:
        print(f"Environment variable error: {env_err}")
        return {'error': str(env_err)}

    except paramiko.AuthenticationException as auth_err:
        print(f"SFTP Authentication failed: {auth_err}")
        return {'error': str(auth_err)}

    except paramiko.SSHException as ssh_err:
        print(f"SSH/SFTP connection error: {ssh_err}")
        return {'error': str(ssh_err)}

    except boto3.exceptions.S3UploadFailedError as s3_err:
        print(f"S3 upload failed: {s3_err}")
        return {'error': str(s3_err)}

    except FileNotFoundError as fnf_err:
        print(f"File not found: {fnf_err}")
        return {'error': str(fnf_err)}

    except Exception as e:
        print(f"Unhandled exception: {e}")
        return {'error': str(e)}
    
    finally:
            if sftp:
                sftp.close()
            if transport:
                transport.close()



''' Commenting this - Since this is done using AWS Secret manager.
def lambda_handler(event, context):
    secret_name = "sftp_details"
    
    # Get SFTP credentials from AWS Secrets Manager
    try:
        credentials = get_secret(secret_name)
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return {
            'statusCode': 500,
            'body': f"Error retrieving secret: {e}"
        }

    if credentials:
        s3BucketName = "my-s3_bucket_name"

        # Establish the SFTP connection using Paramiko
        try:
            transport = paramiko.Transport((credentials['sftp_host'], int(credentials['sftp_port'])))
            transport.connect(username=credentials['sftp_username'], password=credentials['sftp_password'])
            sftp = SFTPClient.from_transport(transport)

            # Specify the SFTP server's remote directory and file details
            remoteDirectory = "C:/Users/saketh/RemoteFolder"
            remoteFileName = "file1.txt"
            s3FileKey = "File1Today"

            # Transfer the file from SFTP to S3
            transferFileSFTPToS3(sftp, remoteDirectory, remoteFileName, s3BucketName, s3FileKey)

            return {
                'statusCode': 200,
                'body': f"File {remoteFileName} transferred successfully to S3 bucket {s3BucketName}."
            }

        except Exception as e:
            print(f"Error connecting to SFTP or transferring file: {e}")
            return {
                'statusCode': 500,
                'body': f"Error connecting to SFTP or transferring file: {e}"
            }

        finally:
            if sftp:
                sftp.close()
            if transport:
                transport.close()

    return {
        'statusCode': 400,
        'body': "No credentials found or an error occurred."
    }
'''