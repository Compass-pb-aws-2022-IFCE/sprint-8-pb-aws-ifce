import boto3

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
cloudwatch = boto3.client('logs')

#Gera URL para o objeto do s3
def getImageUrl(bucket, imageName):
    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket,
            'Key': imageName
        },
        ExpiresIn=3600
    )
    return url

#Detecta as Labels
def detectLabels(imageUrl, bucket):
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': imageUrl.split('/')[3]
            }
        },
        MaxLabels=10,
        MinConfidence=75
    )
    return response