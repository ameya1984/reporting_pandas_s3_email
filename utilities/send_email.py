"""
Send email with S3 file attachment.
IAM role should be created that allows SES to access S3. 
""" 
import config
import boto3
from botocore.exceptions import ClientError




def send_email_with_s3(bucket_name, object_key):
    # Specify the attachment
    attachment = {
        'Bucket': bucket_name,
        'Key': object_key
    }

    # Create an SES client
    ses_client = boto3.client('ses', region_name=config.aws_region, aws_access_key_id=config.aws_access_key_id, aws_secret_access_key=config.aws_secret_access_key)

    # Try to send the email
    try:
        response = ses_client.send_email(
            Source=config.sender,
            Destination={'ToAddresses': [config.recipient]},
            Message={
                'Subject': {'Data': config.subject},
                'Body': {'Text': {'Data': config.body_text}},
                'Attachments': [attachment]
            }
        )

    except ClientError as e:
        print("Error:", e.response['Error']['Message'])
