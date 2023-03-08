import json
import boto3
from datetime import datetime
import os
from botocore.exceptions import ClientError

def v2_vision(event, context):
    
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
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {"statusCode": 500, "body": json.dumps({"error": error_message})}

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