import json
import boto3
from datetime import datetime

s3 = boto3.client("s3")
rekognition = boto3.client("rekognition")

def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

def v1_description(event, context):
    body = {"message": "VISION api version 1."}
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

def v2_description(event, context):
    body = {"message": "VISION api version 2."}
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

def post_vision(event, context):
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
    
    print(body)
    
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

def v2_vision(event, context):
    
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

    print(body)

    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

def v3_vision(event, context):
    body = json.loads(event["body"])
    bucket_name = body["bucket"]
    image_name = body["imageName"]

    url_to_image = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"

    response = rekognition.detect_faces(
        Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
        Attributes=["ALL"]
    )
    emotion_response = rekognition.detect_faces(
        Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
        Attributes=["EMOTIONS"]
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
    
    have_emotions = len(emotion_response['FaceDetails']) > 0

    classified_emotion = None
    classified_emotion_confidence = None
    if have_emotions:
        main_emotion = max(emotion_response['FaceDetails'][0]['Emotions'], key=lambda x: x['Confidence'])
        classified_emotion = main_emotion['Type']
        classified_emotion_confidence = main_emotion['Confidence']

    current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    body = {
        "url_to_image": url_to_image,
        "created_image": current_datetime,
        "have_faces": have_faces,
        "position_faces": position_faces,
        "classified_emotion": classified_emotion,
        "classified_emotion_confidence": classified_emotion_confidence
    }

    print(body)

    response = {"statusCode": 200, "body": json.dumps(body)}
    return response
