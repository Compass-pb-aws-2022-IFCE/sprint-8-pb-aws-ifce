import json
import boto3

# Função que recebe o evento da requisição HTTP feita pelo JavaScript
def payload(event):
    payload = json.loads(event["body"])
    filename = payload["imageName"]
    bucket = payload["bucket"]
    return bucket, filename

# Função que realiza a detecção de objetos da rota v1/vision 
def detectObject(bucket, filename):
    # Inicializa o client rekognition 
    rekognition = boto3.client('rekognition')
    # Define o nome do arquivo já com a pasta destinada a rota v1 no bucket S3
    filename = f'v1/{filename}'
    # Envia os dados do nome do bucket e arquivo para que o rekognition busque a imagem no s3 e realize a detecção
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': filename
            }
        }
    )
    # Extraindo apenas as labels da resposta do Rekognition, retorna a lista de objetos detectados, assim como sua porcentagem de confiança
    labels = [{'Confidence': label['Confidence'], 'Name': label['Name']} for label in response['Labels']]
    return labels

def retorno_v1(labels, bucket, filename):
    filename = f'v1/{filename}'
    # Inicializa o client do s3
    s3 = boto3.client("s3")

    # Busca nos dados do bucket a data em que foi feito o upload da imagem no s3
    dados_imagem = s3.head_object(Bucket=bucket, Key=filename)
    data_upload = dados_imagem['LastModified']

    # Retorno em JSON com o link para a imagem no s3 e a data já formatados
    return {
        "url_to_image": f"https://{bucket}.s3.amazonaws.com/{filename}",
        "created_image": str(data_upload).split('+')[0],
        "labels": labels
    }

def detectFaces(bucket, filename):
    filename = f'v2/{filename}'
    rekognition = boto3.client('rekognition')

    # Realiza a detecção das faces, com estrutura semelhante a da função detectObject()
    rek_response = rekognition.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': filename}})

    # Resgata da detecção apenas a posição das faces dentro da label "FaceDetails" retornada pelo rekognition
    position_faces = [{'Height': face_detail['BoundingBox']['Height'],
                       'Left': face_detail['BoundingBox']['Left'],
                       'Top': face_detail['BoundingBox']['Top'],
                       'Width': face_detail['BoundingBox']['Width']}
                      for face_detail in rek_response['FaceDetails']]
    
    # Tratamento de erros, definindo o retorno "null" caso o rekognition não retorne as posições da face
    position_faces = position_faces if position_faces else None

    return position_faces

def retorno_v2(positions, bucket, filename):
    filename = f'v2/{filename}'
    # True caso haja uma ou mais faces, false caso nenhuma.
    have_faces = bool(positions)

    # Estrutura de retorno de url e data semelhantes à função retorno_v1
    s3 = boto3.client("s3")
    image_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
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
    # Mesma estrutura para detecção, com a diferença do atributo 'Attributes=["ALL"]' que sinaliza ao rekognition que retorne todos os atributos da detecção
    rek_response = rekognition.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': filename}}, Attributes=['ALL'])

    # Obtém a posição e a emoção principal de cada face
    position_faces = [{'Height': face_detail['BoundingBox']['Height'],
                       'Left': face_detail['BoundingBox']['Left'],
                       'Top': face_detail['BoundingBox']['Top'],
                       'Width': face_detail['BoundingBox']['Width'],
                       'classified_emotion': max(face_detail['Emotions'], key=lambda x: x['Confidence'])['Type'],
                       'classified_emotion_confidence': max(face_detail['Emotions'], key=lambda x: x['Confidence'])['Confidence']}
                      for face_detail in rek_response['FaceDetails']]
    
    # Defifnição de retorno nulo caso não seja encontrada nenhuma face (portanto, nenhuma emoção).
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

    # Estrutura de retorno de url e data semelhantes à função retorno_v1
    image_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
    s3 = boto3.client("s3")
    dados_imagem = s3.head_object(Bucket=bucket, Key=filename)
    data_upload = dados_imagem['LastModified']
    
    return {
        "url_to_image": image_url,
        "created_image": str(data_upload).split('+')[0],
        "faces": positions
    }