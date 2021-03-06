import json
import os
import uuid

import boto3


LINK_EXPIRATION = os.getenv('LINK_EXPIRATION') or 3600


def upload_to_s3_bucket(event, _context):
    """
    Payload example:
        --data '{"bucket_name": "uniqnamedbucket"}'
    """
    client = boto3.client('s3')
    upload_key = uuid.uuid4().hex

    lambda_input = json.loads(event.get('body'))
    bucket = lambda_input.get('bucket_name')

    presigned_url = client.generate_presigned_url(
        ClientMethod='put_object',
        ExpiresIn=LINK_EXPIRATION,
        Params={
            'Bucket': bucket,
            'Key': upload_key
        }
    )

    response_body = {"upload_url": presigned_url, "expires": presigned_url.split("=")[-1]}

    return {
        "isBase64Encoded": False,
        "headers": {
            "Location": presigned_url
        },
        "statusCode": 302,
        "body": json.dumps(response_body),
    }
