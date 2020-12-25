import json
from logging import Logger

import boto3


def create_s3_bucket(event, _context):
    """
    Payload example:
        --data '{"region": "us-east-1", "bucket_name": "uniq_named_bucket"}'
    """

    def log(severity, message):
        Logger(name='__name__').__getattribute__(severity)(message)

    def create(region, bucket_name):
        try:
            if region in [None, 'us-east-1']:
                log("warning", f">> Use default location ('us-east-1') for {bucket_name}")
                client = boto3.client('s3')
                client.create_bucket(Bucket=bucket_name)
            else:
                log("warning", f">> Use {region} location for {bucket_name}")
                client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

            client.get_waiter('bucket_exists')
        except BaseException as err:
            log("error", f">> Failed while creating s3 bucket {bucket_name}. Error: {err}")
            return False, str(err)
        return True, None

    lambda_input = json.loads(event.get('body'))
    where = lambda_input.get('region')
    bucket = lambda_input.get('bucket_name')

    created, error = create(region=where, bucket_name=bucket)

    response_body = {
        "input": lambda_input,
        "created": created,
        "error": error
    }

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(response_body)
    }
