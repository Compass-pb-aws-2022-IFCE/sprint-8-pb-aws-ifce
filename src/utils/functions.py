import json

import boto3


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

def detectFaces(bucket, filename):
    filename = f'v2/{filename}'
    rekognition = boto3.client('rekognition')
    image_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
    rek_response = rekognition.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': filename}})
    position_faces = [{'Height': face_detail['BoundingBox']['Height'],
                       'Left': face_detail['BoundingBox']['Left'],
                       'Top': face_detail['BoundingBox']['Top'],
                       'Width': face_detail['BoundingBox']['Width']}
                      for face_detail in rek_response['FaceDetails']]
    position_faces = position_faces if position_faces else None
    return position_faces

def retorno_v2(positions, bucket, filename):
    filename = f'v2/{filename}'
    image_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
    have_faces = bool(positions)
    s3 = boto3.client("s3")
    dados_imagem = s3.head_object(Bucket=bucket, Key=filename)
    data_upload = dados_imagem['LastModified']
    return {
        "url_to_image": image_url,
        "created_image": str(data_upload).split('+')[0],
        "have_faces": have_faces,
        "position_faces": positions
    }

def detectFacesEmotions(bucket, filename):
    filename = f'v3/{filename}'
    rekognition = boto3.client('rekognition')
    image_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
    rek_response = rekognition.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': filename}}, Attributes=['ALL'])
    # Obtém a posição e a emoção principal de cada face
    position_faces = [{'Height': face_detail['BoundingBox']['Height'],
                       'Left': face_detail['BoundingBox']['Left'],
                       'Top': face_detail['BoundingBox']['Top'],
                       'Width': face_detail['BoundingBox']['Width'],
                       'classified_emotion': max(face_detail['Emotions'], key=lambda x: x['Confidence'])['Type'],
                       'classified_emotion_confidence': max(face_detail['Emotions'], key=lambda x: x['Confidence'])['Confidence']}
                      for face_detail in rek_response['FaceDetails']]
    default = [
    {
        "position": {
            "Height": None,
            "Left": None,
            "Top": None,
            "Width": None
        },
        "classified_emotion": None,
        "classified_emotion_confidence": None
    }
    ]

    position_faces = position_faces if position_faces else default

    return position_faces

def retorno_v3(positions, bucket, filename):
    filename = f'v3/{filename}'
    image_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
    s3 = boto3.client("s3")
    dados_imagem = s3.head_object(Bucket=bucket, Key=filename)
    data_upload = dados_imagem['LastModified']
    return {
        "url_to_image": image_url,
        "created_image": str(data_upload).split('+')[0],
        "faces": positions
    }