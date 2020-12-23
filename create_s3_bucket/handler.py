import json
from logging import Logger

import boto3


def create_s3_bucket(event, _context):
    region = event['region']
    if region == 'us-east-1':
        region = None

    bucket_name = event['bucket_name']

    def log(severity, message):
        Logger(name='__name__').__getattribute__(severity)(message)

    def create():
        try:
            if region is None:
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        except BaseException as err:
            log("error", f">> Failed while creating s3 bucket {bucket_name}. Error: {err}")
            return False, str(err)
        return True, None

    created, error = create()
    return {
        "status_code": 200,
        "body": event,
        "created": created,
        "error": error
    }
