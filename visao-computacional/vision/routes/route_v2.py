import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

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

        print(body)

        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response