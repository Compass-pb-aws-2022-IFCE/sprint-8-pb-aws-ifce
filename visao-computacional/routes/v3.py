import json
import boto3
from datetime import datetime
import os
from botocore.exceptions import ClientError
from utils.functions import validate_image_info, get_faces_response

def v3_vision(event, context):

    # Recebe o objeto enviado pelo cliente e valida as informações
    try:
        image_info = json.loads(event['body'])
        bucket, image_name = validate_image_info(image_info)
    except ValueError as e:
        error_message = str(e)
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}
    
    # Detecta as faces da imagem
    try:
        response_faces = get_faces_response(bucket, image_name)
    except ValueError as e:
        error_message = str(e)
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}
    
    # Cria uma lista com as emoções de todos os rostos detectados
    emotions = []
    for face in response_faces['FaceDetails']:
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

    # Mostra a resposta no CloudWatch:
    print("RETURN:", json.dumps(response_data))

    # Retorna resposta com sucesso
    return {
        "statusCode": 200,
        "body": json.dumps(response_data)
    }