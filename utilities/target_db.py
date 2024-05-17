import boto3

def upload_to_s3(bucket, key, obj):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=key, Body=obj.getvalue())

