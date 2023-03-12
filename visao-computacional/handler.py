import io
import json

from rotas import v1Vision
from rotas import v2Vision
from rotas import v3Vision


def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v1_description(event, context):
    body = {
        "message": "VISION api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v2_description(event, context):
    body = {
        "message": "VISION api version 2."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v1_vision(event, context):
   result = v1Vision.v1Vision(event, context)
   return result

def v2_vision(event, context):
   result = v2Vision.v2Vision(event, context)
   return result

def v3_vision(event, context):
    result = v3Vision.v3Vision(event, context)
    return result