![Logo_CompassoUOL_Positivo](https://user-images.githubusercontent.com/94761781/212589731-3d9e9380-e9ea-4ea2-9f52-fc6595f8d3f0.png)
# Avaliação Sprint 8 - Programa de Bolsas Compass.uol / AWS e IFCE

## 📝 Objetivo

Esse projeto tem como objetivo a criação um conjunto de funções lambda que possam ser usadas para acessar as APIs responsáveis por processar imagens usando o serviço de reconhecimento visual da AWS, o "Rekognition". Essas funções serão usadas para extrair tags de imagens armazenadas no serviço de armazenamento da AWS, o S3. Para acompanhar e registrar os resultados dessas funções, será utilizado o serviço de monitoramento da AWS, o CloudWatch.
<br/>

## ⚙️ Tecnologias

* [Rekognition](https://aws.amazon.com/pt/rekognition/)
* [AWS Lambda](https://aws.amazon.com/pt/lambda/)
* [CloudWatch](https://aws.amazon.com/pt/cloudwatch/)
* [Amazon S3](https://aws.amazon.com/pt/s3/) 
<br/>

## 🔀 Entendendo as rotas

ROTA 1 → Já implementada no projeto.

ROTA 2 → Já implementada no projeto.

ROTA 3 → Já implementada no projeto.

ROTA 4 → Após a imagem ser armazenada no serviço S3, o aplicativo fará uma chamada para o serviço Rekognition. O resultado dessa chamada, que estará contido no corpo da resposta, deverá ser registrado na aplicação por meio do serviço CloudWatch.

ROTA 5 → Implementar o upload de imagens hospedadas no serviço S3, é preciso incluir novos campos que indiquem se a imagem contém rostos e sua localização na imagem. Para obter essas informações, é necessário utilizar um modelo de identificação de faces do serviço Rekognition. Para isso, basta fazer uma chamada ao serviço Rekognition durante o processo de upload da imagem e registrar os resultados no CloudWatch da aplicação. Dessa forma, é possível monitorar as informações geradas pela análise e utilizar esses dados para aprimorar as funcionalidades da aplicação.

ROTA 6 → Para realizar a tarefa de detectar a emoção principal em uma imagem carregada manualmente no Amazon S3, é necessário implementar novos campos de retorno na chamada do modelo de identificação de faces do Rekognition. A resposta da chamada deve ser registrada no CloudWatch e exibir todas as emoções detectadas, caso haja mais de uma face na imagem. Para realizar essa tarefa, o primeiro passo é fazer o upload manual da imagem no Amazon S3. Em seguida, é preciso chamar o serviço Rekognition para identificar as emoções detectadas em cada face presente na imagem. Depois disso, é necessário implementar novos campos de retorno que indiquem a emoção principal detectada pelo modelo de identificação de faces do Rekognition. Esses campos devem ser registrados no CloudWatch para monitoramento e análise. Ao final, o resultado da chamada do serviço Rekognition deve ser exibido na aplicação, mostrando todas as emoções detectadas caso haja mais de uma face na imagem. Com essas informações, os usuários poderão ter uma melhor compreensão das emoções presentes na imagem e tomar decisões mais informadas com base nesses dados.
<br/>


## 🚫 Impedimentos
-
-
-
<br/>

## ✔️ Conclusão

O projeto utiliza a plataforma AWS com Amazon Rekognition, S3 e CloudWatch. Com o Amazon Rekognition, temos a capacidade de analisar precisamente imagens e vídeos para detectar e reconhecer objetos, o que nos traz um gama gigantesca de possibilidades fornecidas por essa ferramenta. Usando o CloudWatch em conjunto com o Amazon Rekognition, é possível monitorar e visualizar métricas importantes, para o pleno funcionamento da aplicação desenvolvida.
<br/>

## 👥 Equipe

* [Rosemelry](https://github.com/Rosemelry)
* [Julio Cesar](https://github.com/JC-Rodrigues)
* [Samara Alcantara](https://github.com/SamaraAlcantara)
* [Jhonnatan Gonçalves](https://github.com/jhonatangoncalvespereira)
