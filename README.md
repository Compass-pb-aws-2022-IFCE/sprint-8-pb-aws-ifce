![Logo_CompassoUOL_Positivo](https://user-images.githubusercontent.com/94761781/212589731-3d9e9380-e9ea-4ea2-9f52-fc6595f8d3f0.png)
# 📑 Avaliação Sprint 8 - Programa de Bolsas Compass.uol / AWS e IFCE

## 📌 Tópicos 

- [📝 Descrição do projeto](#-descrição-do-projeto)

- [💻 Ferramentas e Tecnologias](#-ferramentas-e-tecnologias)

- [😌 Impedimentos resolvidos](#-impedimentos-resolvidos)

- [📂 Organização do código](#-descrição-do-projeto)

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
| ROTA 3 | GET         | Definida no escopo do projeto, status code para sucesso da requisição será 200. |
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

## ⚙️ Estrutura das rotas

## 📤 Deploy

## 📌 Considerações finais

## 👤 Equipe

- [Edivalço Araújo](https://github.com/EdivalcoAraujo)
- [Humberto Sampaio](https://github.com/Humbert010)
- [Luan Ferreira](https://github.com/fluanbrito)
- [Mylena Soares](https://github.com/mylensoares)
