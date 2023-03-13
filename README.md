# Avaliação Sprint 8 - Programa de Bolsas Compass.uol / AWS e IFCE

Avaliação da oitava sprint do programa de bolsas Compass.uol para formação em machine learning para AWS.

![Logo_CompassoUOL_Positivo](https://user-images.githubusercontent.com/94761781/212589731-3d9e9380-e9ea-4ea2-9f52-fc6595f8d3f0.png)

---

## Tópicos
- [🧪 Tecnologias](#🧪-tecnologias)
- [📝Organização e descrição do código](#📝organização-e-descrição-do-código)
- [🎨 Execução](#🎨-execução)
- [💔 Impedimentos](#💔-impedimentos)
- [👥 Equipe](#👥-equipe)
 ---
## 🧪 Tecnologias

### Linguagens:
- HTML/CSS
- Javascript
- Python

### Serviços AWS:
- Serverless
- Rekognition
- Lambda
- Api Gateway
- S3

---
## 📝Organização e descrição do código 
<br>

![img](https://imgur.com/RRIAaVc.png)

#### Pastas:
- ```src```: pasta principal do projeto
- ```templates```: armazena os arquivos HTML e a pasta ```static```
- ```static```: armazena o arquivo de estilo e o script responsável pela solicitação HTTP
- ```utils```: armazena o arquivo functions.py que possui as funções que serão utilizadas nos handlers.

#### Arquivos:
- ```index-head``` e ```index-body.html```: separação do ```<head>``` e ```<body>``` do arquivo html para montagem do site da rota /menu. Mais detalhes em ```handler.py```
- ```styles.css```: arquivo de estilos do site html
- ```scripts.js```: aqui se encontra o script responsável por capturar a resposta do usuário e fazer uma requisição HTTP para a rota selecionada, gerando um evento que será capturado pela função payload. Mais detalhes em ```functions.py```
- ```functions.py```: aqui são definidas as funções que tratam de capturar o evento javascript, realizar a lógica por trás de cada uma das três rotas do projeto (detectObject, detectFaces e detectFacesEmotions) e o retorno específico de cada rota
- ```handler.py```: arquivo onde são definidas as funções que serão executadas em cada rota pelo arquivo ```serverless.yml```. Foram adicionadas ao projeto original as funções mainpage, v1_vision, v2_vision e v3_vision, tratando, respectivamente, do site principal e das 3 rotas post.

---

## 🎨 Execução 

### Rota /menu (Mainpage HTML)

Nesta rota encontra-se o site HTML onde o usuário poderá inserir o nome da imagem, selecionar uma das 3 rotas POST através de um seletor e, ao clicar em "Enviar", é realizada a requisição para a rota escolhida, retornando um JSON com os resultados abaixo do botão.

![img](https://imgur.com/8nNcjcM.png) 

### Rota v1/vision (Detecção de Objetos)

Esta rota analisa a presença de objetos na imagem, incluindo desde pessoas e animais até objetos cotidianos, prédios, árvores, etc.
Ao realizar a requisição, Deverá ser retornada a url da imagem no s3, a data em que a imagem foi postada no s3 e uma lista de objetos reconhecidos pelo Rekognition, assim como a porcentagem de confiança de cada um deles, da seguinte forma:

![img](https://imgur.com/dATCYXb.png)

### Rota v2/vision (Detecção de Faces)

Esta rota realizará a detecção de faces em uma imagem, buscando a presença ou não de uma ou mais faces. Deverá retornar a url da imagem no s3, a data em que a imagem foi postada no s3 e se há alguma face na imagem assim como a sua posição

![img](https://imgur.com/l3K2ufv.png)

Em caso de nenhuma face encontrada, todos os dados da detecção são definidos como "null".

![img](https://imgur.com/dPdl494.png)

### Rota v3/vision (Detecção de Emoções)

Esta rota realizará a detecção de emoções nas faces de uma imagem, buscando a presença ou não de uma ou mais faces. Deverá retornar a url da imagem no s3, a data em que a imagem foi postada no s3 e, caso haja uma face, uma lista com as posições de cada face, assim como a emoção reconhecida e a porcentagem de confiança do reconhecimento. 

![img](https://imgur.com/jO5ZSxl.png) 

Em caso de nenhuma face encontrada, todos os dados de detecção são definidos como "null".

![img](https://imgur.com/7DEid5h.png) 

### ✏ Requisições manuais

Também é possível realizar manualmente as requisições enviando uma requisição POST com o seguinte JSON (o corpo é o mesmo para as três rotas):
```
{
  "bucket": "imagens-grupo1",
  "imageName": "imagem.extensão"
}
```
Basta substituir o nome da imagem por um nome de imagem + extensão (jpg, png, etc.) inserido no S3 e enviar a requisição. Deverá ser retornado um JSON com os dados retornados pelo Rekognition para cada rota. Aqui está um exemplo com o software Postman para a rota v1/vision:

![img](https://imgur.com/eXZ6G1r.png)

A lógica é a mesma para as demais rotas:

![img](https://imgur.com/VwZP8dB.png)
![img](https://imgur.com/kawCkxb.png)

### Logs:

Rota v1/vision:
![img](https://imgur.com/Q9QF0xc.png)

Rota v2/vision:
![img](https://imgur.com/xDFbFiB.png)

Rota v3/vision:
![img](https://imgur.com/aE8O1ad.png)

---

## 💔 Impedimentos

- Leitura dos arquivos estáticos (estilos css e scripts javascript) pelo serverless.

---

## 👥 Equipe
- [Nicolas Ferreira](https://github.com/Niccofs)
- [Herisson Hyan](https://github.com/herissonhyan)
- [Rangel Melo](https://github.com/Rangelmello)
- [Luiz Carlos](https://github.com/luiz2CC)
