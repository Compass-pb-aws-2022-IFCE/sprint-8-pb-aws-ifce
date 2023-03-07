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
    # Get the bucket and image name from the request body
    body = json.loads(event["body"])
    bucket_name = body["bucket"]
    image_name = body["imageName"]
    # Get the current datetime
    current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    # Construct the URL to the image
    url_to_image = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"
    # Call Rekognition to get labels for the image
    response = rekognition.detect_labels(
        Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
        MaxLabels=10,
        MinConfidence=90,
    )
    # Get the labels from the response
    labels = response["Labels"]
    # Construct the response body
    body = {
        "url_to_image": url_to_image,
        "created_image": current_datetime,
        "labels": labels,
    }
    # Print the response body
    print(body)
    # Return the response
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

def v2_vision(event, context):
    # Get the bucket and image name from the request body
    body = json.loads(event["body"])
    bucket_name = body["bucket"]
    image_name = body["imageName"]
    # Get the current datetime
    current_datetime = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    # Construct the URL to the image
    url_to_image = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"
    # Call Rekognition to get labels for the image
    response = rekognition.detect_labels(
        Image={"S3Object": {"Bucket": bucket_name, "Name": image_name}},
        MaxLabels=10,
        MinConfidence=90,
    )
    # Get the labels from the response
    labels = response["Labels"]
    # Construct the response body
    body = {
        "url_to_image": url_to_image,
        "created_image": current_datetime,
        "labels": labels,
    }
    # Print the response body
    print(body)
    # Return the response
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response
