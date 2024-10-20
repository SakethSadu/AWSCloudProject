# AWSCloudProject
This project is to perform actions using Lambda, S3, SageMaker, Glue, EventBridge etc.,

**Pre-Requisites:**
1.Python(Latest Version)
2.AWS Account. (Free Tier is good enough)
3.GitHub Repository - Github actions for Continous Deployment to AWS.
4. SFTP. (Local is also good enough, but here in this code - we are transfering files from SFTP to S3 bucket. You can change code accordingly if required)

**Steps:**

1) Create a Local Folder and pull request the python files - S3FileTransfer.py, lambdaHandler.py, sftpCredsFromlambdaEnvVar.py
    i) S3FileTransfer.py - To upload file/files from remote root (any) directory in SFTP to S3 Bucket. - You can mention all your required directory name, file name, S3  bucket name, Key name etc., in lambda           function's environment variables.
    ii) lambdaHandler.py - This class handles your lambda function - To invoke our lambda use lambda_handler function in the class, and based on our code it gets credentials and other details of SFTP from               Lambda env variables.
    iii) sftpCredsFromLambdaEnvVar.py - This is to get the values from our Lambda Function's Environment Variables.

2) Create a Lambda Function in AWS, and then go to Configuration -> Environment Variables -> and give all the necessary Key value pairs of your fields.
   i) Go to Lambda -> Create layer -> Give names and other details, and add the py_paramiko_libraries_layer.zip packages to import paramiko, and other dependencies.
   ii) Go to Code Tab -> Add Layer -> Customer layer -> Select a layer from the dropdown which you created from the previous Step.
   iii) Once you are done, upload the code (here all the 3 files) as Zip folder or we can automate the deployment using Github actions or AWS code Pipeline. (Here we are using Github actions as its free for less code changes. AWS Codepipeline has a flat fee of 1$ every month.Compare both and use as per your requirement)
3) We can create EventBridge to trigger the lambda function everyday/every 3 hours based on the requirement.
   i) Go to Event Bridge -> create Rule -> Add Schedule as required -> Select your Lambda function.
4) Test your code.
5) Once the code works as expected, and the file is uploaded to S3 bucket, other following process continues.....)
