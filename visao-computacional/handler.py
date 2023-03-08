import json
import boto3
import logging
from datetime import datetime

s3 = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

rekognition = boto3.client("rekognition")

def health(event, context):
    try:
        body = {
            "message": "Go Serverless v3.0! Your function executed successfully!",
            "input": event,
        }
        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def v1_description(event, context):
    try:
        body = {"message": "VISION api version 1."}
        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def v2_description(event, context):
    try:
        body = {"message": "VISION api version 2."}
        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def post_vision(event, context):
    try:
        body = json.loads(event["body"])
        bucket_name = body["bucket"]
        image_name = body["imageName"]

        current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        url_to_image = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"

        response = rekognition.detect_labels(
            Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
            MaxLabels=10,
            MinConfidence=90,
        )

        labels = response["Labels"]

        body = {
            "url_to_image": url_to_image,
            "created_image": current_datetime,
            "labels": labels,
        }

        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def v2_vision(event, context):
    try:
        body = json.loads(event["body"])
        bucket_name = body["bucket"]
        image_name = body["imageName"]

        url_to_image = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"

        response = rekognition.detect_faces(
            Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
            Attributes=["ALL"]
        )

        have_faces = len(response['FaceDetails']) > 0

        position_faces = []
        if have_faces:
            for face_detail in response['FaceDetails']:
                position_faces.append({
                    'Width': face_detail['BoundingBox']['Width'],
                    'Height': face_detail['BoundingBox']['Height'],
                    'Left': face_detail['BoundingBox']['Left'],
                    'Top': face_detail['BoundingBox']['Top']
                })
        else:
            position_faces = None

        current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        body = {
            "url_to_image": url_to_image,
            "created_image": current_datetime,
            "have_faces": have_faces,
            "position_faces": position_faces
        }

        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

s3 = boto3.client("s3")
rekognition = boto3.client("rekognition")
# Configuração do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def health(event, context):
    try:
        body = {
            "message": "Go Serverless v3.0! Your function executed successfully!",
            "input": event,
        }
        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def v1_description(event, context):
    try:
        body = {"message": "VISION api version 1."}
        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def v2_description(event, context):
    try:
        body = {"message": "VISION api version 2."}
        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def post_vision(event, context):
    try:
        body = json.loads(event["body"])
        bucket_name = body["bucket"]
        image_name = body["imageName"]

        current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        url_to_image = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"

        response = rekognition.detect_labels(
            Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
            MaxLabels=10,
            MinConfidence=90,
        )

        labels = response["Labels"]

        body = {
            "url_to_image": url_to_image,
            "created_image": current_datetime,
            "labels": labels,
        }

        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def v2_vision(event, context):
    try:
        body = json.loads(event["body"])
        bucket_name = body["bucket"]
        image_name = body["imageName"]

        url_to_image = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"

        response = rekognition.detect_faces(
            Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
            Attributes=["ALL"]
        )

        have_faces = len(response['FaceDetails']) > 0

        position_faces = []
        if have_faces:
            for face_detail in response['FaceDetails']:
                position_faces.append({
                    'Width': face_detail['BoundingBox']['Width'],
                    'Height': face_detail['BoundingBox']['Height'],
                    'Left': face_detail['BoundingBox']['Left'],
                    'Top': face_detail['BoundingBox']['Top']
                })
        else:
            position_faces = None

        current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        body = {
            "url_to_image": url_to_image,
            "created_image": current_datetime,
            "have_faces": have_faces,
            "position_faces": position_faces
        }

        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response

def v3_vision(event, context):
    try:
        body = json.loads(event["body"])
        bucket_name = body["bucket"]
        image_name = body["imageName"]

        url_to_image = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"

        response = rekognition.detect_faces(
            Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
            Attributes=["ALL"]
        )

        logging.info(response)

        have_faces = len(response['FaceDetails']) > 0

        position_faces = []
        classified_emotions = {}
        if have_faces:
            for face_detail in response['FaceDetails']:
                position_faces.append({
                    'Width': face_detail['BoundingBox']['Width'],
                    'Height': face_detail['BoundingBox']['Height'],
                    'Left': face_detail['BoundingBox']['Left'],
                    'Top': face_detail['BoundingBox']['Top']
                })
                emotions = face_detail['Emotions']
                for emotion in emotions:
                    if emotion['Type'] in classified_emotions:
                        if emotion['Confidence'] > classified_emotions[emotion['Type']]['Confidence']:
                            classified_emotions[emotion['Type']] = {
                                'Confidence': emotion['Confidence'],
                                'BoundingBox': face_detail['BoundingBox']
                            }
                    else:
                        classified_emotions[emotion['Type']] = {
                            'Confidence': emotion['Confidence'],
                            'BoundingBox': face_detail['BoundingBox']
                        }
        else:
            position_faces = None

        current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        if classified_emotions:
            classified_emotion = max(classified_emotions, key=lambda k: classified_emotions[k]['Confidence'])
            classified_emotion_confidence = classified_emotions[classified_emotion]['Confidence']
        else:
            classified_emotion = None
            classified_emotion_confidence = None

        body = {
            "url_to_image": url_to_image,
            "created_image": current_datetime,
            "classified_emotion": classified_emotion,
            "classified_emotion_confidence": classified_emotion_confidence
        }

        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response