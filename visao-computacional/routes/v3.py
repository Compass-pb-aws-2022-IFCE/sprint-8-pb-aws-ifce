import json
import boto3
from utils.getCreationDate import getCreationDate
from utils.classifyEmotion import classifyEmotion

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
cloudwatch = boto3.client('logs')

def v3Vision(event, context):
    try:
        body = json.loads(event['body'])
        bucket = body['bucket']
        imageName = body['imageName']
        imageUrl = f"https://{bucket}.s3.amazonaws.com/{imageName}"

        # Carregando imagem do s3
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, imageName).download_file('/tmp/' + imageName)

        # Chamando a função detect_faces do Rekognition
        with open('/tmp/' + imageName, 'rb') as f:
            response = rekognition.detect_faces(
                Image = {
                    'Bytes': f.read()
                },
                Attributes=['ALL']
            )

        timestamp = getCreationDate(bucket, imageName).strftime('%d-%m-%Y %H:%M:%S')

        log_data = {
            "url_to_image": imageUrl,
            "created_image": timestamp,
            "response": response
        }

        response_data = {
            'url_to_image': imageUrl,
            'created_image': timestamp,
        }

        # Armazena a emoção e a confiança no response_data
        face_details_list = response['FaceDetails']
        if len(face_details_list) == 0:
            response_data['faces'] = [{'position': {'Height': None, 'Left': None, 'Top': None, 'Width': None}, 'classified_emotion': None, 'classified_emotion_confidence': None}]
        elif len(face_details_list) == 1:
            face_details = face_details_list[0]
            classified_emotion, classified_emotion_confidence = classifyEmotion(face_details)
            response_data['faces'] = [{'position': face_details['BoundingBox'], 'classified_emotion': classified_emotion, 'classified_emotion_confidence': classified_emotion_confidence}]
        else:
            # Cria um array de objetos para cada face, caso exista mais de uma
            response_data['faces'] = []
            for face_details in face_details_list:
                classified_emotion, classified_emotion_confidence = classifyEmotion(face_details)
                response_data['faces'].append({
                    'position': face_details['BoundingBox'],
                    'classified_emotion': classified_emotion,
                    'classified_emotion_confidence': classified_emotion_confidence
                })

        print(json.dumps(log_data))

        response = {
            "statusCode": 200,
            "body": json.dumps(response_data),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    return response