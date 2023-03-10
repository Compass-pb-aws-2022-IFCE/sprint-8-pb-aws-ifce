import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from datetime import datetime


def validate_image_info(image_info):
    
    # Recebe o objeto enviado pelo cliente e se certifica que ele passou nome do bucket e nome da imagem.

    try:
        if 'bucket' not in image_info:
            raise KeyError("The 'bucket' key was not found.")
        if 'imageName' not in image_info:
            raise KeyError("The 'imageName' key was not found.")
        bucket = image_info['bucket']
        image_name = image_info['imageName']
    except KeyError as e:
        error_message = str(e).replace("\\", "").replace("\"", "")
        raise ValueError(error_message)
    return bucket, image_name


def get_labels_response(bucket, image_name):

    # Retorna o objeto de resposta das funções detect_labels do Amazon Rekognition.

    rekognition = boto3.client('rekognition')
    try:
        response_labels = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': image_name
                }
            }
        )
    except ClientError as e:
        error_message = e.response['Error']['Message']
        raise ValueError(error_message)
    return response_labels


def get_faces_response(bucket, image_name):

    # Retorna o objeto de resposta das funções detect_faces do Amazon Rekognition.

    rekognition = boto3.client('rekognition')
    try:
        response_faces = rekognition.detect_faces(
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
        raise ValueError(error_message)
    return response_faces

def get_image_creation_date(bucket, image_name):
    s3_client = boto3.client('s3')
    response = s3_client.head_object(Bucket=bucket, Key=image_name)
    creation_time = response['LastModified'].astimezone()
    return creation_time.strftime("%d-%m-%Y %H:%M:%S")
