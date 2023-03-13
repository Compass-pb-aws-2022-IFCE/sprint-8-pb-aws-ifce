def v1Vision(event, context):
	#Identificação de Labels
	import boto3
	from datetime import datetime
	import json
	from utils.modulos import valida_image, detect_faces, get_image_creation_date
	
	body = json.loads(event['body'])
	bucket = body['bucket']
	photo = body['imageName']
	region = 'us-east-1'

	s3 = boto3.resource('s3')
	rekognition = boto3.client('rekognition')

	def detect_labels(bucket, key, max_labels=10, min_confidence=90):
		try:
			response = rekognition.detect_labels(
				Image={
					"S3Object": {
						"Bucket": bucket,
						"Name": key,
					}
				},
				MaxLabels=max_labels,
				MinConfidence=min_confidence,
			)
			return response
		except:
			return {"status": 500,
							"body": "Error"}

	response = detect_labels(bucket,photo)
	response = [{'Confidence': label['Confidence'], 'Name': label['Name']} for label in response['Labels']]

	return {
        "url_to_image": f"https://{bucket}.s3.amazonaws.com/{photo}",
        "created_image": get_image_creation_date(bucket,photo),
        "labels": response
    }

	#def exporta_dados(dados_json):
	#	arquivo =s3.Object('','dados.json')
	#	arquivo.put(Body=json.dumps(dados_json))

	#def main(event, context):
	#	bucket = 'imagens-rekognition'
	#	key = urllib.parse.quote_plus(event['Records'][0]['s3']['object']['key'])
	#	detect_labels(bucket, key)

