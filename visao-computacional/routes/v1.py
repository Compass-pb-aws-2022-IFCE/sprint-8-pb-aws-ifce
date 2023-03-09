import json
import boto3
from datetime import datetime
import os
from botocore.exceptions import ClientError
from utils.functions import validate_image_info, get_labels_response

def v1_vision(event, context):

    # Recebe o objeto enviado pelo cliente
    try:
        image_info = json.loads(event['body'])
        bucket, image_name = validate_image_info(image_info)
    except ValueError as e:
        error_message = str(e)
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}

    # Detecta as etiquetas da imagem
    try:
        response_labels = get_labels_response(bucket, image_name)
    except ValueError as e:
        error_message = str(e)
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}

    # Cria a lista de etiquetas detectadas
    labels = [{'Confidence': label['Confidence'], 'Name': label['Name']} for label in response_labels['Labels']]

    # Cria a resposta com as informações solicitadas
    response_data = {
        'url_to_image': f"https://{bucket}/{image_name}",
        'created_image': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        'labels': labels
    }

    # Mostra a resposta no CloudWatch:
    print("RETURN:", json.dumps(response_data))

    # Retorna a resposta com o código HTTP 200
    return {"statusCode": 200, "body": json.dumps(response_data)}