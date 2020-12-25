import json
from logging import Logger

import boto3


def create_s3_bucket(event, _context):
    print(f"!!!!!!!!!!!!!!event{event}")

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": "sssss"
    }

