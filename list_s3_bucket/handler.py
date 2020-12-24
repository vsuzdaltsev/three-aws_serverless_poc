import json
from logging import Logger

import boto3

def list_s3_bucket(event, _context):
    """
    Payload example:
        https://uri/{bucket_name}
    """
    def log(severity, message):
        Logger(name='__name__').__getattribute__(severity)(message)

    def list_files(bucket_name):
      s3 = boto3.resource('s3')
      bucket = s3.Bucket(bucket_name)

      aggr = []

      for file in bucket.objects.all():
          aggr.append(file.key)
      return aggr, None
    
    lambda_input = event.get('path').split('/')[-1]
    output, error = list_files(bucket_name=lambda_input)

    body = {
        "input": lambda_input,
        "output": output,
        "error": error
    }

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(body)
    }