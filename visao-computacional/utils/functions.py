import boto3
import json

def payload(event):
    payload = json.loads(event["body"])
    filename = payload["imageName"]
    bucket = payload["bucket"]
    return bucket, filename

def detectObject(bucket, filename):
    rekognition = boto3.client('rekognition')
    filename = f'v1/{filename}'
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
    filename = f'v1/{filename}'
    s3 = boto3.client("s3")
    dados_imagem = s3.head_object(Bucket=bucket, Key=filename)
    data_upload = dados_imagem['LastModified']
    return {
        "url_to_image": f"https://{bucket}.s3.amazonaws.com/{filename}",
        "created_image": str(data_upload).split('+')[0],
        "labels": labels
    }