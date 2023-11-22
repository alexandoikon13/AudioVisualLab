import os
import boto3
from urllib.parse import urlparse

def upload_file_to_cloudcube(file_stream, filename, content_type):
    parsed_url = urlparse(os.environ.get('CLOUDCUBE_URL'))
    bucket_name = parsed_url.netloc.split('.')[0]

    s3_client = boto3.client('s3')

    s3_client.put_object(
        Bucket=bucket_name,
        Key=f"{parsed_url.path[1:]}/{filename}",  # Path in Cloudcube
        Body=file_stream,
        ContentType=content_type
    )

def get_cloudcube_file_url(filename):
    parsed_url = urlparse(os.environ.get('CLOUDCUBE_URL'))
    bucket_name = parsed_url.netloc.split('.')[0]

    s3_client = boto3.client('s3')
    file_url = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name,
                                                        'Key': f"{parsed_url.path[1:]}/{filename}"},
                                                ExpiresIn=3600)  #available for 1h
    return file_url