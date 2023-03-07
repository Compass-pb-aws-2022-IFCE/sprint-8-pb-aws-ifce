import boto3
import json
from datetime import datetime

def payload(event):
    payload = json.loads(event["body"])
    filename = payload["imageName"]
    bucket = payload["bucket"]
    return bucket, filename

def detectObject(bucket, filename):
    rekognition = boto3.client('rekognition')

    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': filename
            }
        }
    )
    labels = [{'Confidence': label['Confidence'], 'Name': label['Name']} for label in response['Labels']]
    return labels


def retorno_v1(labels, bucket, filename):
    return {
        "url_to_image": f"https://{bucket}.s3.amazonaws.com/{filename}",
        "created_image": str(datetime.now()).split(".")[0],
        "labels": labels
    }