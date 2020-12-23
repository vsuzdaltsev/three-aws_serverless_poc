import uuid

import boto3


EXPIRATION = 3600


def upload_to_s3_bucket(event, _context):
    client = boto3.client('s3')
    upload_key = uuid.uuid4().hex
    bucket = event.get('bucket_name')
    presigned_url = client.generate_presigned_url(
        ClientMethod='put_object',
        ExpiresIn=EXPIRATION,
        Params={
            'Bucket': bucket,
            'Key': upload_key
        }
    )

    return {"upload_url": presigned_url, "expires": presigned_url.split("=")[-1]}
