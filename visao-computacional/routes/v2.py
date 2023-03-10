import json
import boto3
from utils.getCreationDate import getCreationDate

from utils.v2 import functions

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
cloudwatch = boto3.client('logs')

def v2Vision(event, context):
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

        # Log do CloudWatch
        timestamp = getCreationDate(bucket, imageName).strftime('%d-%m-%Y %H:%M:%S')
        
        log_data = {
            "url_to_image": imageUrl,
            "created_image": timestamp,
            "response": response
        }
        print(json.dumps(log_data))
        
        if  response["FaceDetails"]:
            haveFaces = True
            positions = [
                {
                    "Height": details["BoundingBox"]["Height"],
                    "Left": details["BoundingBox"]["Left"],
                    "Top": details["BoundingBox"]["Top"],
                    "Width": details["BoundingBox"]["Width"]
                } for details in response["FaceDetails"]
            ]
        else:
            haveFaces = False
            positions = None

        response_data = {
            "url_to_image": imageUrl,
            "created_image": timestamp,
            "have_faces": haveFaces,
            "position_faces": positions
        }

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
            "body": json.dumps({"message": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
    return response
