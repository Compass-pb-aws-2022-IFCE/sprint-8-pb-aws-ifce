import json
import boto3
from datetime import datetime
import os
from botocore.exceptions import ClientError

def v3_vision(event, context):

    # Recebe o objeto enviado pelo cliente
    try:
        image_info = json.loads(event['body'])
        if 'bucket' not in image_info:
            raise KeyError("'bucket' not found")
        bucket = image_info['bucket']
        image_name = image_info['imageName']
    except KeyError as e:
        error_message = str(e)
        return {"statusCode": 400, "body": json.dumps({"error": error_message})}
    except ClientError as e:
        error_message = str(e)
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}

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
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}

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