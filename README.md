[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/LogoCompasso-positivo.png/440px-LogoCompasso-positivo.png)](https://compass.uol/pt/home/)

> Avaliação da oitava sprint do programa de bolsas Compass.UOL para formação em Machine learning para AWS.
***

## 📌 Tópicos
- [📝 Descrição do projeto](#📝-descrição-do-projeto)
- [💻 Tecnologias e ferramentas](#💻-tecnologias-e-ferramentas)
- [🛠 Execução](#🛠-execução)
- [🤝 Dependências](#🤝-dependecias)
- [⚙ Configuração](#⚙-configuracao)
- [💔 Impedimentos](#💔-impedimentos)
- [👥 Equipe](#👥-equipe)
***

## 💻 Tecnologias e ferramentas

- [Lambda](https://aws.amazon.com/pt/lambda/)
- [S3](https://aws.amazon.com/pt/s3/)
- [IAM](https://aws.amazon.com/pt/iam/)
- [CloudWatch](https://aws.amazon.com/pt/cloudwatch/)
- [VisualStudioCode](https://code.visualstudio.com/)
- [Postman](https://www.postman.com/)
- [Python](https://www.python.org/)


***
## 📝 Descrição do projeto

Este é um conjunto de funções para uma API de Visão Computacional que utiliza o serviço Amazon Rekognition para detectar rótulos e rostos em imagens armazenadas no Amazon S3.

| ROTA           | MÉTODO HTTP | DEFINIÇÃO                                                                                                                                                                                                                                                                      |
| --------------| -----------| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| health         | GET        | A função "health" é definida com dois argumentos: o objeto de evento e o contexto. O objeto de evento contém informações sobre o evento que desencadeou a execução da função. O contexto contém informações adicionais sobre o ambiente de execução da função, como tempo de execução e limites de recursos. |
| v1_description| GET        | Ambas as rotas v1_description e v2_description são responsáveis por definir funções que são usadas no serviço AWS Lambda. O objetivo destas funções é fornecer uma resposta HTTP com um código de status 200 e uma mensagem JSON que indica a versão da API de visão (VISION) usada. |
| v2_description| GET        |                                                                                                                                                                                                                                                                             |
| post_vision    | POST       | Detecta rótulos em uma imagem especificada por um usuário, rótulos esses tais como: Objeto, espécie, parentesco e etc. A imagem deve estar armazenada no Amazon S3 e o usuário deve fornecer o nome do bucket e o nome da imagem.                                         |
| v2_vision      | POST       | Procura encontrar algum rosto e seu posicionamento em uma imagem especificada por um usuário, caso não encontre nenhum rosto ele sinaliza na variável `have_faces` como **false** e na `position_faces` como **null**. A imagem deve estar armazenada no Amazon S3 e o usuário deve fornecer o nome do bucket e o nome da imagem.   |
| v3_vision      | POST       | Detecta rostos e emoções em uma imagem especificada por um usuário, caso encontre mais de um rosto ela deve abordar os dados de posicionamento especifico junto com a classifição da emoção da pessoa na imagem e a confiança de classificação da emoção. Caso não encontre nenhuma face, deve-se trazer as informações de posicionamento, classificação da emoção e confiança de classificação da emoção todas como Null. A imagem deve estar armazenada no Amazon S3 e o usuário deve fornecer o nome do bucket e o nome da imagem. |

# Estrutura do projeto

![estrutura](https://user-images.githubusercontent.com/119500249/224730792-588efbcd-290f-4017-8cd3-a14f4cbae380.png)

## 🛠 Execução
Aqui se encontra todos os códigos executados nessa aplicação, é importante enfatizar que para que a aplicação seja executada, primeiro é necessário configurar o serverless framework, você pode encontrar o passo a passo de como configurar nas seções de 🤝 Dependências e ⚙ Configuração.
As funções atualmente disponíveis na API são:

`health`
Retorna uma mensagem de sucesso indicando que a função foi executada corretamente.
```python
import json
import boto3
import logging
from datetime import datetime

s3 = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

rekognition = boto3.client("rekognition")
```
O código começa importando alguns módulos necessários, incluindo o módulo json para manipulação de objetos JSON, o módulo boto3 para interagir com serviços da AWS, o módulo logging para registrar mensagens de log e o módulo datetime para trabalhar com datas e horas.
Em seguida, o código define uma instância do cliente S3 da AWS e um objeto logger para registrar informações. A função também define uma instância do cliente Rekognition da AWS, que é usado para análise de imagem.

`post_vision`
  
Explicação: O código dentro do **handler.py** é uma função chamada "post_vision" que faz parte de um serviço de reconhecimento de imagens usando a API da AWS. A função recebe um evento que pode ser uma solicitação HTTP ou uma ação realizada em um serviço específico. O código extrai as informações do nome do bucket e do nome da imagem, cria uma URL para a imagem e usa o serviço de Reconhecimento de Imagem da AWS (Rekognition) para detectar rótulos na imagem especificada. Os rótulos detectados são armazenados em uma variável e um objeto de resposta HTTP é retornado com um código de status 200 e o corpo da resposta contém informações sobre a imagem e os rótulos detectados. Se ocorrer uma exceção durante a execução da função, um objeto de resposta HTTP com um código de status 500 e uma mensagem de erro é retornado.

`v2_vision`

Explicação: Esta é uma função em Python que recebe um evento e um contexto do AWS Lambda e retorna uma resposta com informações sobre faces detectadas em uma imagem armazenada em um bucket S3.
A função começa analisando o corpo do evento de entrada para obter o nome do bucket S3 e o nome da imagem. Em seguida, ele constrói uma URL para a imagem usando esses valores.
Em seguida, a função usa o serviço AWS Rekognition para detectar faces na imagem. Ele solicita todos os atributos disponíveis para cada face detectada. Se nenhuma face for detectada, a lista position_faces é definida como None.
A função então cria um dicionário contendo informações sobre as faces detectadas, incluindo se alguma foi detectada, suas posições dentro da imagem e a URL para a imagem. Este dicionário é então convertido em JSON e retornado como corpo da resposta da função.

Se ocorrer uma exceção durante a execução, uma resposta de erro 500 é retornada com a mensagem de erro como corpo.

`v3_vision`

Explicação: O código apresentado é uma função em Python chamada v3_vision que utiliza o serviço Amazon Rekognition para detectar emoções em faces presentes em imagens armazenadas no serviço Amazon S3.
A função recebe um evento e um contexto, sendo que o evento deve conter o nome do bucket S3 e o nome da imagem que será processada. A partir desses dados, é montada uma URL para acessar a imagem no S3.

A função utiliza o método detect_faces do Amazon Rekognition para identificar as faces presentes na imagem e as emoções associadas a cada face. Em seguida, as emoções são classificadas de acordo com sua intensidade e um objeto JSON é criado com informações sobre as faces detectadas, incluindo a URL da imagem, a data de criação da imagem, a posição das faces e as emoções associadas a cada face.
Se apenas uma face for detectada, a função retorna um objeto JSON com as informações da face e suas emoções associadas. Se houver mais de uma face, um objeto JSON com as informações de todas as faces é retornado.

Em caso de erro, a função retorna um objeto JSON com o status code 500 e uma mensagem de erro.

`serverless.yml`
O arquivo serverless.yml é utilizado pelo framework Serverless para definir a configuração do serviço que será criado na nuvem e gerenciado por ele. Ele define as funções Lambda, eventos, permissões e outras configurações necessárias para implantar e executar o serviço.

No contexto do código do handler.py, o serverless.yml define as funções que são implementadas no arquivo, seus nomes, os eventos que acionam essas funções (no caso, eventos HTTP), bem como as rotas que acionam cada uma das funções. Você pode encontrar o arquivo `serverless.yml` dentro da pasta visao-computacional/vision.

## 🤝 Dependências
As funções utilizam o SDK do boto3 e o serviço Amazon Rekognition da Amazon Web Services. O código é executado em um ambiente serverless usando o AWS Lambda. 
Para rodar toda a aplicação, primeiro você deve configurar o serverless framework, segue como configurar:
1. Instale o Node.js: O Serverless Framework é construído sobre o Node.js, portanto, é necessário instalar o Node.js antes de começar. Você pode baixá-lo e instalá-lo a partir do site oficial do Node.js: https://nodejs.org/en/.
2. Instale o Serverless Framework: Você pode instalar o Serverless Framework globalmente usando o npm (Node Package Manager), executando o seguinte comando no terminal: 
```css
npm install -g serverless
```
3. Configure as credenciais de acesso: O Serverless Framework usa as credenciais da sua conta AWS para implantar suas funções Lambda e outros recursos na nuvem. Para configurar as credenciais, você precisa criar um usuário IAM na sua conta AWS com as permissões necessárias e, em seguida, configurar as credenciais no seu computador. Para fazer isso, execute o seguinte comando no terminal:
```css
serverless config credentials --provider aws --key SUA_CHAVE_ACESSO --secret SUA_CHAVE_SECRETA
```
Substitua SUA_CHAVE_ACESSO e SUA-CHAVE-SECRETA pelas suas credenciais da AWS
4. Implantar o serviço: Para implantar o serviço na nuvem, execute o seguinte comando no terminal:
```bash
cd my-service
serverless deploy
```

Sobre as credenciais de acesso, será necessário que você as crie e gerencie diretamente na AWS, através do serviço IAM. Para fazer isso, siga os seguintes passos:

1. Acesse o IAM
2. Clique em "Usuários" dentro da seção "Gerenciamento de acesso"
3. Adicione um novo usuário e defina um nome
4. Em "Definir permissões", selecione a opção "Anexar políticas diretamente"
5. Em "Políticas de permissões", busque pelas políticas "AmazonRekognitionFullAccess", "AmazonS3FullAccess" e "AdministratorAccess"
6. Revise as permissões e crie o usuário.

Após ter criado o usuário, siga os seguintes passos para gerar a chave de acesso:

1. Acesse as "Credenciais de segurança" com o usuário criado
2. Procure por "Chave de acesso" e clique em "Criar chave de acesso"
3. Em "Práticas recomendadas e alternativas para chaves de acesso", clique em "Aplicação em execução em um serviço computacional da AWS" - isso gerará uma mensagem de alternativa recomendada
4. Clique em "Compreendo a recomendação acima e quero prosseguir" para criar uma chave de acesso
5. Na seção "Definir etiqueta de descrição", adicione uma descrição (caso queira)
6. Clique em "Criar chave de acesso"
7. Você será direcionado para a página de criação das chaves, onde estarão presentes a chave de acesso e a chave secreta.

Agora só configurar o seu serverless adicionando as credenciais criadas, é só repetir o primeiro passo a passo logo acima.

## ⚙ Configuração 
Para configurar as funções, é necessário criar uma função Lambda no AWS Lambda e adicionar as funções fornecidas neste repositório. Além disso, é necessário conceder permissões para que a função tenha acesso ao Amazon S3 e ao Amazon Rekognition. Por fim, é necessário configurar as variáveis de ambiente que especificam as informações de autenticação do AWS SDK.

Para configurar as permissões, siga os seguintes passos:

1. Acesse o serviço IAM na AWS.
2. Clique em "Funções" dentro da seção "Gerenciamento de acesso".
3. Clique em "Criar função".
4. Em "Tipo de entidade confiável", selecione "Serviço da AWS".
5. Em "Caso de uso", selecione "Lambda".
6. Em "Casos de uso para outros serviços da AWS lambda também", clique em "Próximo".
7. Em "Políticas de permissões", clique em "Criar política".
8. Você será redirecionado para outra página. Selecione "JSON".
9. Adicione a permissão abaixo:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "rekognition:DetectLabels",
                "rekognition:DetectFaces"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "logs:CreateLogStream",
                "logs:TagResource",
                "logs:CreateLogGroup"
            ],
            "Resource": [
                "arn:aws:s3:::<NOME-DO-BUCEKET>/*",
                "arn:aws:logs:<regiao>:<ID>:log-group:<NOME-DO-SEU-GRUPO-LOGS>*:*"
            ]
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<NOME-DO-SEGUNDO-BUCKET>/*"
        }
    ]
}
```
O código acima define três blocos de permissões com o seguinte significado:

1. O primeiro bloco permite que o usuário faça uso dos serviços Rekognition da AWS para detectar labels e faces em imagens, podendo acessar recursos de qualquer tipo.
2. O segundo bloco permite que o usuário acesse objetos do seu primeiro bucket do Amazon S3, além de criar e gerenciar logs de eventos relacionados a funções lambda. O usuário pode acessar somente esses recursos específicos e não pode criar outros logs ou grupos de logs.
3. O terceiro bloco permite que o usuário acesse objetos do segundo bucket do Amazon S3, podendo acessar somente esses recursos específicos e não podendo criar outros objetos no bucket ou fazer alterações no mesmo.

## 💔 Impedimentos
- Implementar a v2_vision criando o tratamento do 'if' para caso se houvesse face executasse todo a execução e sair a resposta exata como a atividade pede. Para isso, no fim foi criado a variavél `FaceDetals` responsável por listar os detalhes do rosto.
- Já na v3_vision, a dificuldade maior foi em torno do tratamento no caso quando houvesse mais de uma face, listasse a `classified_emotion` e `classified_emotion_confidence` de cada rosto encontrado.

## 👥 Equipe
- [Jefferson Moreira](https://github.com/Jeef-Moreira)
- [Nicolas Ferreira](https://github.com/TeclaFernandes)