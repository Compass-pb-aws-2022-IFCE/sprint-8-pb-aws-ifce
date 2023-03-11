![Logo_CompassoUOL_Positivo](https://user-images.githubusercontent.com/94761781/212589731-3d9e9380-e9ea-4ea2-9f52-fc6595f8d3f0.png)
# 📑 Avaliação Sprint 8 - Programa de Bolsas Compass.uol / AWS e IFCE

## 📌 Tópicos 

- [📝 Descrição do projeto](#-descrição-do-projeto)

- [💻 Ferramentas e Tecnologias](#-ferramentas-e-tecnologias)

- [😌 Impedimentos resolvidos](#-impedimentos-resolvidos)

- [📂 Organização do código](#-organização-do-código)

- [⬇️ Arquivo Functions.py](#-arquivo-functions.py)

- [⚙️ Estrutura das rotas](#-estrutura-das-rotas)

- [📤 Deploy](#deploy)

- [📌 Considerações finais](#-considerações-finais)

## 📝 Descrição do projeto

Elaboração de um conjunto de funções lambda que oferecerão suporte a APIs responsáveis por executar o serviço de "rekognition" e extrair tags de imagens hospedadas no S3. Além disso, utilizar o CloudWatch para registrar os registros dos resultados obtidos.

Sendo:

| ROTA   | MÉTODO HTTP | ARQUITETURA |
| ---    | ---         | --- |
| ROTA 1 | GET         | Definida no escopo do projeto, status code para sucesso da requisição será 200. |
| ROTA 2 | GET         | Definida no escopo do projeto, status code para sucesso da requisição será 200. |
| ROTA 3 | GET         | Definida no escopo do projeto, status code para sucesso da requisição será 200.    |
| ROTA 4 | POST        | Com a imagem hospedada no S3, o post irá chamar o Rekognition e o resultado(body) da chamada deve estar logado na aplicação através do CloudWatch. |
| ROTA 5 | POST        | Implementar o post de uma imagem hospedada no S3, é necessário adicionar novos campos de retorno que informem se a imagem contém algum rosto e sua posição. Para isso, é preciso utilizar um modelo de identificação de faces do serviço Rekognition. O post deve chamar o Rekognition para realizar a análise e o resultado da chamada (body) deve ser registrado na aplicação por meio do CloudWatch |
| ROTA 6 | POST        | Fazer o upload manual de uma imagem no S3 e implementar novos campos de retorno que indiquem a emoção principal detectada pelo modelo de identificação de faces do Rekognition. O resultado da chamada deve ser registrado na aplicação por meio do CloudWatch, exibindo todas as emoções detectadas caso haja mais de uma face na imagem. O post deve chamar o serviço Rekognition para obter essa informação. |

## 💻 Ferramentas e tecnologias

- Visual Studio Code;
- Amazon Web Services(AWS Lambda, S3, Rekognition, Serverless);
- Python;
- Postman.

## 😌 Impedimentos resolvidos

- Interpretação inicial da construção, organização do código como também de sua arquitetura em cada rota.
- Erro na inserção das credenciais e execução do comando  ```"serverless config credentials" ```, resolvido após pesquisa e alteração do  ```"Set-ExecutionPolicy" ``` para o status de ```"RemoteSigned" ``` no PowerShell.
- Construção das rotas, como também a sua "successfully executed", cada rota haviam erros que foram resolvidos após reuniões,estudo e pequisa.

## 📂 Organização do código

![Pastas](https://i.imgur.com/5g0uunU.png)

Acima é o demonstrativo de como foi organizado o projeto e subdivido em pastas conforme era a atuação do código.

A organização do código ajudou a evitar erros e bugs, uma vez que as partes do código estão claramente separadas e identificadas. Ela também facilitou a implementação de novas funcionalidades e a resolução de problemas, pois se tornou mais fácil localizar e corrigir o código relevante.

Em resumo, a organização do código foi fundamental para o sucesso do projeto, pois tornou o processo de desenvolvimento mais eficiente e efetivo.

## ⬇️ Arquivo Functions.py

Código em Python que define quatro funções para trabalhar com imagens na AWS: 

```bash
- validate_image_info(); 
- get_labels_response();
- get_faces_response();
- get_image_creation_date(). 
```
Essas funções utilizam os módulos boto3, json e datetime para se comunicar com serviços os da AWS, validar informações de imagem, obter informações de rótulos e faces de uma imagem, e obter a data de criação de uma imagem em um bucket do S3.

## ⚙️ Estrutura das rotas

### **V1 (ROTA 4)**

Função Lambda que recebe um evento e um contexto e retorna uma resposta em formato JSON contendo informações sobre uma imagem.

A função principal, "v1_vision", tenta obter informações sobre uma imagem a partir do evento recebido. Em seguida, as etiquetas da imagem são detectadas e uma lista de etiquetas é criada.

Por fim, as informações solicitadas sobre a imagem, como o link para a imagem, a data de criação e as etiquetas detectadas, são organizadas em um dicionário e retornadas como uma resposta em formato JSON com o código de status 200.

Se ocorrer um erro durante o processo, uma mensagem de erro será retornada como uma resposta em formato JSON com o código de status 500.

### **V2 (ROTA 5)**

Função Lambda que recebe um evento e um contexto e retorna uma resposta em formato JSON contendo informações sobre uma imagem, com ênfase na detecção de faces.

A função principal, "v2_vision", tenta obter informações sobre uma imagem a partir do evento recebido. Em seguida, as faces na imagem são detectadas e uma lista de informações sobre a posição das faces é criada.

Dependendo se foram encontradas faces ou não, um valor booleano é atribuído à variável "have_faces". As informações solicitadas sobre a imagem, como o link para a imagem, a data de criação e a lista de informações sobre a posição das faces são organizadas em um dicionário e retornadas como uma resposta em formato JSON com o código de status 200.

Se ocorrer um erro durante o processo, uma mensagem de erro será retornada como uma resposta em formato JSON com o código de status 500.

### **V3 (ROTA 6)**

Função chamada "v3_vision" que é utilizada para detectar faces e emoções em uma imagem, retornando uma lista de rostos detectados com as emoções classificadas.

A função começa validando as informações da imagem recebida pelo cliente, caso seja inválida retorna uma mensagem de erro.

Em seguida, a função detecta as faces na imagem utilizando a função "get_faces_response" e cria uma lista de rostos detectados com as emoções classificadas. Caso não exista nenhuma face detectada, é adicionado um objeto de rosto vazio com valores nulos.

Depois, a função cria um objeto de resposta que contém a URL da imagem, a data de criação e a lista de rostos detectados com as emoções classificadas.

Por fim, a função retorna a resposta com sucesso, com um código de status 200 e o objeto de resposta convertido em uma string JSON. A resposta também é mostrada no CloudWatch através de uma mensagem de log.

## 📤 Deploy

## 📌 Considerações finais

Em resumo, o projeto envolvendo o uso da plataforma AWS com Amazon Rekognition, S3 e CloudWatch foi muito proveitoso.

Com o Amazon Rekognition é possível analisar imagens e vídeos para detecção e reconhecimento de objetos, cenas, textos e faces. Com ele, é possível identificar, classificar e indexar imagens para pesquisa e organização, além de automatizar tarefas como verificação de identidade, monitoramento de segurança e análise de sentimentos. 

Ao usar o Amazon CloudWatch em conjunto com o Amazon Rekognition, é possível visualizar métricas importantes, como o número de solicitações de análise de imagem por minuto, o número de análises de imagem bem-sucedidas e o tempo médio de resposta.

Portanto, os serviços da AWS, como o Rekognition, fornecem recursos poderosos de processamento de imagem e reconhecimento de padrões para diversas aplicações. Ao integrar o Amazon CloudWatch, é possível monitorar e analisar o desempenho das aplicações. Essa integração é importante para garantir a qualidade do serviço oferecido, bem como para auxiliar no gerenciamento de custos e na tomada de decisões estratégicas.

## 👤 Equipe

- [Edivalço Araújo](https://github.com/EdivalcoAraujo)
- [Humberto Sampaio](https://github.com/Humbert010)
- [Luan Ferreira](https://github.com/fluanbrito)
- [Mylena Soares](https://github.com/mylensoares)
