import boto3
import json
from datetime import datetime

rekognition = boto3.client('rekognition')

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

        faces = []
        if len(response['FaceDetails']) > 0:
            for face_detail in response['FaceDetails']:
                emotions = face_detail['Emotions']
                classified_emotions = {}
                for emotion in emotions:
                    if emotion['Type'] in classified_emotions:
                        if emotion['Confidence'] > classified_emotions[emotion['Type']]['Confidence']:
                            classified_emotions[emotion['Type']] = {
                                'Confidence': emotion['Confidence'],
                                'Type': emotion['Type']
                            }
                    else:
                        classified_emotions[emotion['Type']] = {
                            'Confidence': emotion['Confidence'],
                            'Type': emotion['Type']
                        }
                if classified_emotions:
                    classified_emotion = max(classified_emotions, key=lambda k: classified_emotions[k]['Confidence'])
                    classified_emotion_confidence = classified_emotions[classified_emotion]['Confidence']
                else:
                    classified_emotion = None
                    classified_emotion_confidence = None

                face = {
                    "position": {
                        'Width': face_detail['BoundingBox']['Width'],
                        'Height': face_detail['BoundingBox']['Height'],
                        'Left': face_detail['BoundingBox']['Left'],
                        'Top': face_detail['BoundingBox']['Top']
                    },
                    "classified_emotion": classified_emotion,
                    "classified_emotion_confidence": classified_emotion_confidence
                }

                faces.append(face)
        else:
            faces.append({
                "position": {
                    'Width': None,
                    'Height': None,
                    'Left': None,
                    'Top': None
                },
                "classified_emotion": None,
                "classified_emotion_confidence": None
            })

        if len(faces) > 0:
            current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        else:
            current_datetime = None

        body = {
            "url_to_image": url_to_image,
            "created_image": current_datetime,
            "faces": faces
        }

        print(body)

        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response
