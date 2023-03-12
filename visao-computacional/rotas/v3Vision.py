def v3Vision(event, context):
    import json
    import boto3
    import datetime
    import logging
    import base64
    from urllib.parse import urlparse

    s3 = boto3.client('s3')
    rekognition = boto3.client('rekognition')
    cloudwatch = boto3.client('logs')
    #config = load_config()
    #logger = configure_logger(config['aws']['cloudwatch_log_group'])
    
    try:
        # Extrai o bucket e o nome da imagem a partir do corpo da requisição
        body = json.loads(event['body'])
        bucket = body['bucket']
        imageName = body['imageName']
        
        # Carrega a imagem do S3
        image = s3.get_object(Bucket=bucket, Key=imageName)['Body'].read()    # Parêntese extra removido
        
        # Chama o Rekognition para detectar faces na imagem
        response = rekognition.detect_faces(
            Image={'Bytes': image},
            Attributes=['ALL']
        )
        
        # Cria a estrutura de resposta
        result = {
            "url_to_image": f"https://{bucket}/{imageName}",
            "created_image": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            "faces": []
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        #logger.error(str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error"})
        }

