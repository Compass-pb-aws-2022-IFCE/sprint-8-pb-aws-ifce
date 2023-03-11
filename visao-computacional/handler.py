import io
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

    with io.open('templates/index-head.html', mode='r', encoding='utf-8') as f:
        html_head = f.read()
        
    with io.open('templates/index-body.html', mode='r', encoding='utf-8') as f:
        html_body = f.read()
    
    with io.open('templates/static/styles.css', mode='r', encoding='utf-8') as f:
        css_content = f.read()
    
    with io.open('templates/static/scripts.js', mode='r', encoding='utf-8') as f:
        js_scripts = f.read()
    

    html = html_head + '<style>' + css_content + '</style></head><body>' + html_body + '</body><script>' + js_scripts +' </script></html>'

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html,
    }

def v1_vision(event, context):
    payload = functions.payload(event)
    detectLabels = functions.detectObject(payload[0], payload[1])
    response = functions.retorno_v1(detectLabels, payload[0], payload[1])

    return response

def v2_vision(event, context):
    payload = functions.payload(event)
    detectFaces = functions.detectFaces(payload[0], payload[1])
    response = functions.retorno_v2(detectFaces,payload[0], payload[1])
    #response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v3_vision(event, context):
    body = {
        "message": "Rota v3 vision."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response