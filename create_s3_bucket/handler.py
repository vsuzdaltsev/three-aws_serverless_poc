import json


def create_s3_bucket(event, context):
    body = {
        "input": event,
        "context": type(context)
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
