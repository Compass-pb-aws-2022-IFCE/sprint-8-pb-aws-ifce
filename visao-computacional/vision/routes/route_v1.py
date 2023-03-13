import json
import boto3
from datetime import datetime

s3 = boto3.client("s3")
rekognition = boto3.client("rekognition")

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

        print(body)

        response = {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        response = {"statusCode": 500, "body": str(e)}
    return response