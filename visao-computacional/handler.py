import json
from utils import functions


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

def mainpage(event, context):

    with open('templates/index.html', 'r') as f:
        html_content = f.read()
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html_content,
    }

def v1_vision(event, context):
    payload = functions.payload(event)
    detectLabels = functions.detectObject(payload[0], payload[1])
    response = functions.retorno_v1(detectLabels, payload[0], payload[1])

    return response

def v2_vision(event, context):
    body = {
        "message": "Rota v2 vision."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v3_vision(event, context):
    body = {
        "message": "Rota v3 vision."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response