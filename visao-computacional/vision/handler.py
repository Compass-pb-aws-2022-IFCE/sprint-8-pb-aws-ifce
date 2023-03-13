import json


def health(event, context):
    try:
        body = {
            "message": "Go Serverless v3.0! Your function executed successfully!",
            "input": event,
        }
        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def v1_description(event, context):
    try:
        body = {"message": "VISION api version 1."}
        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def v2_description(event, context):
    try:
        body = {"message": "VISION api version 2."}
        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response