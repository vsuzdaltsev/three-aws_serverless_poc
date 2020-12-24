import json
import uuid

import boto3


EXPIRATION = 3600


def upload_to_s3_bucket(event, _context):
    """
    Payload example:
        --data '"bucket_name": "uniq_named_bucket"}'
    """
    client = boto3.client('s3')
    upload_key = uuid.uuid4().hex

    lambda_input = json.loads(event.get('body'))
    bucket = lambda_input.get('bucket_name')

    presigned_url = client.generate_presigned_url(
        ClientMethod='put_object',
        ExpiresIn=EXPIRATION,
        Params={
            'Bucket': bucket,
            'Key': upload_key
        }
    )

    body = {"upload_url": presigned_url, "expires": presigned_url.split("=")[-1]}

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": json.dumps(body)
    }
