import json
import boto3
from datetime import datetime
import os
from botocore.exceptions import ClientError

def v1_vision(event, context):
    
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
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}

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