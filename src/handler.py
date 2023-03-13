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
    # Lê os arquivos html, css e javascript e os guarda em variáveis
    with io.open('templates/index-head.html', mode='r', encoding='utf-8') as f:
        html_head = f.read()
        
    with io.open('templates/index-body.html', mode='r', encoding='utf-8') as f:
        html_body = f.read()
    
    with io.open('templates/static/styles.css', mode='r', encoding='utf-8') as f:
        css_content = f.read()
    
    with io.open('templates/static/scripts.js', mode='r', encoding='utf-8') as f:
        js_scripts = f.read()
    
    # Monta um arquivo html completo utilizando css e javascript inline
    html = html_head + '<style>' + css_content + '</style></head><body>' + html_body + '</body><script>' + js_scripts +' </script></html>'
    
    # Retorna o html montado para ser carregado pela rota
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html,
    }

def v1_vision(event, context):
    # Retorno em caso de erro
    body = {
        "message": "error"
    }
    try:
        payload = functions.payload(event)
        # Realiza a detecção, passando respectivamente o nome do bucket e da imagem
        detectLabels = functions.detectObject(payload[0], payload[1])
        # Chama o retorno da função, passando respectivamente a lista de labels detectadas, o nome do bucket e da imagem
        response = functions.retorno_v1(detectLabels, payload[0], payload[1])
        # Logando a resposta no CloudWatch
        print(response)
        return {"statusCode": 200, "body": json.dumps(response)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(body)}

def v2_vision(event, context):
    # Retorno em caso de erro
    body = {
        "message": "error"
    }
    try:
        payload = functions.payload(event)
        # Realiza a detecção, passando respectivamente o nome do bucket e da imagem
        detectFaces = functions.detectFaces(payload[0], payload[1])
        # Chama o retorno da função, passando respectivamente a lista de faces detectadas, o nome do bucket e da imagem
        response = functions.retorno_v2(detectFaces,payload[0], payload[1])
        # Logando a resposta no CloudWatch
        print(response)
        return {"statusCode": 200, "body": json.dumps(response)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(body)}

def v3_vision(event, context):
    # Retorno em caso de erro
    body = {
        "message": "error"
    }
    try:
        payload = functions.payload(event)
        # Realiza a detecção, passando respectivamente o nome do bucket e da imagem
        detectEmotions=functions.detectFacesEmotions(payload[0], payload[1])
        # Chama o retorno da função, passando respectivamente a lista de emoções detectadas, o nome do bucket e da imagem
        response = functions.retorno_v3(detectEmotions,payload[0], payload[1])
        # Logando a resposta no CloudWatch
        print(response)
        return {"statusCode": 200, "body": json.dumps(response)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(body)}