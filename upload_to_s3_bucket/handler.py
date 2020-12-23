import json
from logging import Logger

import boto3


def upload_to_s3_bucket(event, _context):


    return {
        "status_code": 200,
        "input": event,
        "uploaded": True,
        "error": 'error'
    }
