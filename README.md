# Avaliação Sprint 8 - Programa de Bolsas Compass UOL / AWS e IFCE

[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/LogoCompasso-positivo.png/440px-LogoCompasso-positivo.png)](https://compass.uol/pt/home/)

Avaliação da oitava sprint do programa de bolsas Compass UOL para formação em machine learning para AWS.

---

## Sumário
- [Objetivo](#objetivo)
- [Ferramentas](#ferramentas)
- [Equipe](#equipe)

---

## Objetivo

Este projeto tem como objetivo demonstrar a utilização do serviço de reconhecimento de imagens da AWS, o Amazon Rekognition, através de rotas de API Gateway em uma aplicação serverless na AWS Lambda. Além disso, também utilizaremos o CloudWatch para gravar os logs dos resultados obtidos na análise das imagens. As rotas disponíveis são responsáveis por extrair tags das imagens armazenadas no S3 através do Rekognition e retornar essas informações em formato JSON para a aplicação cliente. As funções Lambda implementadas serão acionadas pela API Gateway, que será responsável por direcionar as requisições HTTP para as funções Lambda apropriadas.

## Ferramentas

* [AWS](https://aws.amazon.com/pt/) plataforma de computação em nuvem da Amazon.
  * [DynamoDB](https://aws.amazon.com/dynamodb/) banco de dados não relacional que oferece rápida e escalável performance.
  * [S3](https://aws.amazon.com/s3/) serviço de armazenamento.
  * [API Gateway](https://aws.amazon.com/api-gateway/) serviço para criação, implantação e gerenciamento de APIs.
  * [Lambda](https://aws.amazon.com/lambda/) serviço de computação *serverless* que permite a execução de código sem a preocupação de gerenciar servidores.

## Estrutura do projeto
```
visao-computacional/
│└──handler.py
│└──serverless.yml
├── routes/
│   └── homepage.py
│   └── v1.py
│   └── v2.py
│   └── v3.py
├── utils/
│   └── classifyEmotion.py
│   └── detectFaces.py
│   └── detectLabels.py
│   └── getCreationDate.py
│   └── loadImageS3.py
│   └── loadVariables.py
├── templates/
│   └── index.html
```
## Desenvolvimento
### Rotas
### /v1/vision:

Essa rota tem como objetivo receber uma imagem armazenada em um bucket S3 e extrair suas tags por meio do serviço Rekognition da AWS. Além disso, ela também faz uso do serviço de log do CloudWatch para gravar as informações da imagem processada e as tags identificadas.

O trecho de código em questão registra as informações de log no CloudWatch, contendo a URL da imagem, o horário de criação e as tags extraídas do Amazon Rekognition. Em seguida, a função retorna um objeto JSON com as mesmas informações das tags, mas em um formato mais legível para o usuário.
```
# Log do CloudWatch
        log_data = {
            "url_to_image": imageUrl,
            "created_image": timestamp,
            "labels": labels
        }
        print(json.dumps(log_data))
        
        response_data = {
            "url_to_image": imageUrl,
            "created_image": timestamp,
            "labels": [
                {"Name": label["Name"], "Confidence": label["Confidence"]} for label in labels
            ]
        }
```
### /v2/vision:

 Essa rota utiliza o serviço de detecção de labels do Amazon Rekognition para identificar as faces presentes na imagem, retornando uma lista com as faces detectadas.

Nesse trecho, a função detectFaces é chamada para detectar as faces na imagem. O resultado da detecção é registrado em um objeto de log que é impresso no console. Em seguida, é verificado se alguma face foi detectada e, se houver, a posição de cada face é registrada em um array. Essas informações são então retornadas como parte da resposta da API.
```
# Log do CloudWatch
        # Chamando faces do Rekognition
        response = detectFaces(file_path)
        
        log_data = {
            "url_to_image": imageUrl,
            "created_image": timestamp,
            "response": response
        }
        print(json.dumps(log_data))
        
        if response:
            haveFaces = True
            positions = [
                {
                    "Height": details["BoundingBox"]["Height"],
                    "Left": details["BoundingBox"]["Left"],
                    "Top": details["BoundingBox"]["Top"],
                    "Width": details["BoundingBox"]["Width"]
                } for details in response
            ]
        else:
            haveFaces = False
            positions = None

        response_data = {
            "url_to_image": imageUrl,
            "created_image": timestamp,
            "have_faces": haveFaces,
            "position_faces": positions
        }
```
### /v3/vision:

Essa rota tem como objetivo ...
```
```

### Funções
### classifyEmotion:
A função recebe detalhes da face de uma imagem e classifica a emoção predominante e sua confiança. Ele percorre a lista de emoções e armazena a confiança de cada emoção em um dicionário. Em seguida, determina a emoção com a maior confiança e retorna seu nome e confiança.
```
def classifyEmotion(face_details):
    emotions = face_details['Emotions']
    emotion_confidence = {}

    for emotion in emotions:
        emotion_type = emotion['Type']
        emotion_confidence[emotion_type] = emotion['Confidence']
    classified_emotion = max(emotion_confidence, key=emotion_confidence.get)
    classified_emotion_confidence = emotion_confidence[classified_emotion]

    return classified_emotion, classified_emotion_confidence
```
### detectFaces:
Essa utiliza o cliente boto3 para acessar o serviço Amazon Rekognition e detectar faces em uma imagem passada como parâmetro. A imagem é lida em bytes e passada para o método detect_faces, que retorna detalhes das faces encontradas. Esses detalhes são armazenados em uma variável e retornados pela função.
```
import boto3

def detectFaces(image_file):
    rekognition = boto3.client('rekognition')
    with open(image_file, 'rb') as f:
        response = rekognition.detect_faces(
            Image={
                'Bytes': f.read()
            },
            Attributes=['ALL']
        )
    faces = response['FaceDetails']
    return faces

```
### detectLabels
Essa função também utiliza a biblioteca boto3 para chamar o serviço Rekognition da AWS e reconhecer as labels da imagem passada como parâmetro. Em seguida, retorna uma lista com as labels identificadas, com no máximo 10 labels e com uma confiança mínima de 75%.
```
import boto3

# Reconhece as labels da imagem
def detectLabels(image_file):
    rekognition = boto3.client('rekognition')
    with open(image_file, 'rb') as f:
        response = rekognition.detect_labels(
            Image={
                'Bytes': f.read()
            },
            MaxLabels=10,
            MinConfidence=75
        )
    labels = response['Labels']
    return labels

```
### getCreationDate
Função que retorna a data e hora de criação de um objeto em um bucket do Amazon S3.
```
import boto3
from datetime import datetime

# Fornece a data e o horário da imagem no bucket
def getCreationDate(bucket_name, object_key):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    creation_date = response['LastModified']
    return creation_date.strftime('%d-%m-%Y %H:%M:%S')
```

### loadImageS3
Essa função usa a biblioteca boto3 para baixar uma imagem de um bucket S3 e salvá-la. Retornando o caminho do arquivo onde a imagem foi salva.

```
import boto3

# Carrega a imagem do S3
def loadImageS3(bucket, imageName):
    s3 = boto3.resource('s3')
    file_path = f'/tmp/{imageName}'
    s3.Bucket(bucket).download_file(imageName, file_path)
    return file_path

```

### loadVariables
Essa função usa a biblioteca json para analisar o corpo do objeto de evento e extrair as variáveis ​​"bucket" e "imageName". A função também cria uma URL de imagem com essas variáveis ​​e retorna todas as variáveis.
```
import json

# Carrega as variáveis usadas nas rotas
def loadVariables(event):
    body = json.loads(event['body'])
    bucket = body['bucket']
    imageName = body['imageName']
    imageUrl = f"https://{bucket}.s3.amazonaws.com/{imageName}"
    
    return bucket, imageName, imageUrl
```


## Acesso
Para utilizar os recursos das rotas acesse este [link](https://n3bay1s6wi.execute-api.us-east-1.amazonaws.com/home). Para testar, você pode usar informações do seu próprio bucket, ou inserir o nome do bucket como "photos-sprint8-davi", e o nome da imagem como "gato.jpg" ou "homem.jpg", pois é um bucket para teste público de um dos integrantes da equipe.
## Equipe

- [Davi](https://github.com/davi222-santos)
- [Dayanne](https://github.com/dayannebugarim)
- [Josiana](https://github.com/JosianaSilva)
- [Rafael](https://github.com/Kurokishin)

