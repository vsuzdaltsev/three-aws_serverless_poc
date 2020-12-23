import json
from logging import Logger

import boto3


def create_s3_bucket(event, _context):
    def log(severity, message):
        Logger(name='__name__').__getattribute__(severity)(message)

    def create(region, bucket_name):
        try:
            if region is None:
                client = boto3.client('s3')
                client.create_bucket(Bucket=bucket_name)
            else:
                client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        except BaseException as err:
            log("error", f">> Failed while creating s3 bucket {bucket_name}. Error: {err}")
            return False, str(err)
        return True, None

    where = event['region'] if event['region'] and event['region'] != 'us-east-1' else None
    bucket = event['bucket_name']

    created, error = create(region=where, bucket_name=bucket)

    return {
        "status_code": 200,
        "input": event,
        "created": created,
        "error": error
    }
