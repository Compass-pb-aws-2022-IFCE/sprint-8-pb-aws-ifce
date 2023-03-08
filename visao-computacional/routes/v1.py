import json
import boto3
import datetime

from utils.v1 import functions

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
cloudwatch = boto3.client('logs')

def v1Vision(event, context):
    try:
        body = json.loads(event['body'])
        bucket = body['bucket']
        imageName = body['imageName']
        imageUrl = f"https://{bucket}.s3.amazonaws.com/{imageName}"
        
        # Carregando imagem do s3
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, imageName).download_file('/tmp/' + imageName)

        # Chamando labels do Rekognition
        with open('/tmp/' + imageName, 'rb') as f:
            response = rekognition.detect_labels(
                Image={
                    'Bytes': f.read()
                },
                MaxLabels=10,
                MinConfidence=75
            )
        labels = response['Labels']
        
        # Log do CloudWatch
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        log_data = {
            "url_to_image": imageUrl,
            "created_image": timestamp,
            "labels": labels
        }
        print(json.dumps(log_data))
        
        response_data = {
            "url_to_image": imageUrl,
            "created_image": timestamp,
            "labels": [
                {"Name": label["Name"], "Confidence": label["Confidence"]} for label in labels
            ]
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
