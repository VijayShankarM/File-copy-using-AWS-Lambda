import json
import boto3
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket name and object key from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Destination bucket
    destination_bucket = os.environ['DEST_BUCKET']

    try:
        # Copy the object from source bucket to destination bucket
        copy_source = {'Bucket': source_bucket, 'Key': object_key}
        s3.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=object_key)
        
        print(f"Successfully copied {object_key} from {source_bucket} to {destination_bucket}")
        
    except Exception as e:
        print(f"Error copying object: {str(e)}")
        raise e