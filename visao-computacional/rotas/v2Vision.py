# Detecção de faces
import boto3
import json


def detect_faces(photo, bucket, region):

    rekognition = boto3.client('rekognition', region_name=region)

    response = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': photo}
        },
        Attributes=['ALL'])

    return response


def v2Vision(event, context):

    body = json.loads(event['body'])
    bucket = body['bucket']
    photo = body['imageName']
    region = 'us-east-1'

    try:
        faceData = detect_faces(photo, bucket, region)

        print(type(faceData))

        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=photo)
        creation_date = response['LastModified']

        creation_date = creation_date.strftime('%d-%m-%Y %H:%M:%S')

        positions = [{'Height': face ['BoundingBox']['Height'],
                       'Left': face ['BoundingBox']['Left'],
                       'Top': face ['BoundingBox']['Top'],
                       'Width': face ['BoundingBox']['Width']}
                      for face in faceData ['FaceDetails']]
		

        if faceData["FaceDetails"]:
            have_faces = True
        else:
            have_faces = False
            positions = None
					
        body = {
            "url_to_image": f"https://{bucket}.s3.amazonaws.com/{photo}",
            "created_image": creation_date,
            "have_faces": have_faces,
            "position_faces": positions
        }

        print(json.dumps(body))

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }

    return response
