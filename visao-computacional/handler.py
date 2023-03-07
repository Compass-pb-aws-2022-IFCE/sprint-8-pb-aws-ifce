import json
import boto3
import datetime


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


s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
cloudwatch = boto3.client('logs')

#Gera URL para o objeto do s3
def getImageUrl(bucket, imageName):
    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket,
            'Key': imageName
        },
        ExpiresIn=3600
    )
    return url

#Detecta as Labels
def detectLabels(imageUrl, bucket):
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': imageUrl.split('/')[3]
            }
        },
        MaxLabels=10,
        MinConfidence=75
    )
    return response

def v1Vision(event, context):
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
    return response