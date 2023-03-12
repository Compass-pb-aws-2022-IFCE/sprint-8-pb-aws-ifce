#Identificação de Labels
import boto3
import urllib
import json

s3 = boto3.resource('s3')
rekognition = boto3.client('rekognition')

def detect_labels(bucket, key, max_labels=10, min_confidence=90):
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

	return response['Labels']

def exporta_dados(dados_json):
    arquivo =s3.Object('','dados.json')
    arquivo.put(Body=json.dumps(dados_json))

def main(event, context):
    bucket = 'imagens-rekognition'
    key = urllib.parse.quote_plus(event['Records'][0]['s3']['object']['key'])
    detect_labels(bucket, key)


