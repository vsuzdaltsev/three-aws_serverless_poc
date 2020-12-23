import json


def create_s3_bucket(event, context):
    body = {
        "input": event,
        "context": str(type(context))
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
