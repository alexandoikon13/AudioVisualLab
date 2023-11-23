import os
import boto3
from urllib.parse import urlparse

def upload_file_to_cloudcube(file_stream, filename, content_type):
    parsed_url = urlparse(os.environ.get('CLOUDCUBE_URL'))
    bucket_name = parsed_url.netloc.split('.')[0]

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('CLOUDCUBE_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('CLOUDCUBE_SECRET_ACCESS_KEY')
    )

    s3_client.put_object(
        Bucket=bucket_name,
        Key=f"{parsed_url.path[1:]}/{filename}",  # Path in Cloudcube
        Body=file_stream,
        ContentType=content_type
    )

def get_cloudcube_file_url(filename):
    parsed_url = urlparse(os.environ.get('CLOUDCUBE_URL'))
    bucket_name = parsed_url.netloc.split('.')[0]

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('CLOUDCUBE_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('CLOUDCUBE_SECRET_ACCESS_KEY')
    )
    
    file_url = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name,
                                                        'Key': f"{parsed_url.path[1:]}/{filename}"},
                                                ExpiresIn=300)  #available for 5 minutes
    return file_url
