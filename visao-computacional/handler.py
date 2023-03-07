import json
import boto3
from datetime import datetime
import os
from botocore.exceptions import ClientError


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
    # Recebe o objeto enviado pelo cliente
    try:
        image_info = json.loads(event['body'])
        bucket = image_info['bucket']
        image_name = image_info['imageName']
    except:
        # Em caso de erro, retorna uma resposta com o código HTTP 500
        return {"statusCode": 500, "body": json.dumps({"error": "Invalid input"})}

    # Cria o URL da imagem
    url_to_image = f"https://{bucket}/{image_name}"

    # Cria uma instância do cliente Amazon Rekognition
    rekognition = boto3.client('rekognition')

    # Detecta as etiquetas da imagem
    try:
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': image_name,
                },
            },
        )
    except:
        # Em caso de erro, retorna uma resposta com o código HTTP 500
         return {"statusCode": 500, "body": json.dumps({"error": "Could not detect labels."})}

    # Cria a lista de etiquetas detectadas
    labels = [{'Confidence': label['Confidence'], 'Name': label['Name']} for label in response['Labels']]

    # Cria a resposta com as informações solicitadas
    response_data = {
        'url_to_image': url_to_image,
        'created_image': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        'labels': labels
    }

    # mostrando a resposta no CloudWatch:
    print("RETURN:", json.dumps(response_data))

    # Retorna a resposta com o código HTTP 200
    return {"statusCode": 200, "body": json.dumps(response_data)}

def v2_vision(event, context):

    image_info = json.loads(event['body'])
    bucket = image_info['bucket']
    image_name = image_info['imageName']

    # Cria uma instância do cliente Amazon Rekognition
    rekognition = boto3.client('rekognition')

    # Detecta as faces da imagem
    try:
        response_faces = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': image_name,
            },
        },
        Attributes=['DEFAULT']
    )
    except:
        # Em caso de erro, retorna uma resposta com o código HTTP 500
        return {'statusCode': 500, 'body': {'error': 'Could not detect faces.'}}

    # Cria a lista de faces detectadas
    position_faces = []
    if len(response_faces['FaceDetails']) > 0:
        for face in response_faces['FaceDetails']:
            position_faces.append({
                'Left': face['BoundingBox']['Left'],
                'Top': face['BoundingBox']['Top'],
                'Width': face['BoundingBox']['Width'],
                'Height': face['BoundingBox']['Height']
            })
        have_faces = True
    else:
        have_faces = False

    # Cria a resposta com as informações solicitadas
    response_data = {
        'url_to_image': f"https://{bucket}/{image_name}",
        'created_image': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        'have_faces': have_faces,
        'position_faces': position_faces if have_faces else None,
    }

    # mostrando a resposta no CloudWatch:
    print("RETURN:", json.dumps(response_data))

    # Retorna a resposta com o código HTTP 200
    return {
        "statusCode": 200,
        "body": json.dumps(response_data)
    }

def v3_vision(event, context):

    # Recebe o objeto enviado pelo cliente
    try:
        image_info = json.loads(event['body'])
        bucket = image_info['bucket']
        image_name = image_info['imageName']
    except:
        # Em caso de erro, retorna uma resposta com o código HTTP 400
        return {"statusCode": 500, "body": json.dumps({"error": "Invalid input"})}

    # Cria uma instância do cliente Amazon Rekognition
    rekognition = boto3.client('rekognition')

    try:
        # Detecta emoções
        response = rekognition.detect_faces(
            Image={
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': image_name
                    }
                },
                    Attributes=['ALL']
            )
    except:
        # Em caso de erro, retorna uma resposta com o código HTTP 500
        return {'statusCode': 500, 'body': {'error': 'Could not detect emotions.'}}

    # Cria uma lista com as emoções de todos os rostos detectados
    emotions = []
    for face in response['FaceDetails']:
        highest_emotion = max(face['Emotions'], key=lambda e: e['Confidence'])
        emotions.append({
            "type": highest_emotion['Type'].upper(),
                "confidence": highest_emotion['Confidence']
        })

    # Cria o objeto de resposta
    response_data = {
        "url_to_image": f"https://{bucket}/{image_name}",
        "created_image": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "classified_emotions": emotions
    }

    # mostrando a resposta no CloudWatch:
    print("RETURN:", json.dumps(response_data))

    # Retorna resposta com sucesso
    return {
        "statusCode": 200,
        "body": json.dumps(response_data)
    }