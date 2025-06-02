# Tech Challenger - Fiap


## Fase 1
### O problema

Você foi contratado(a) para uma consultoria e seu trabalho envolve analisar os dados de vitivinicultura da Embrapa, os quais estão disponíveis [aqui.](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01)

A ideia do projeto é a criação de uma API pública de consulta nos dados do site nas respectivas abas:

- Produção.
- Processamento.
- Comercialização.
- Importação.
- Exportação.

A API vai servir para alimentar uma base de dados que futuramente será usada para um modelo de Machine Learning.

Seus objetivos incluem:

- [ ]  Criar uma Rest API em Python que faça a consulta no site da Embrapa.
- [ ]  Sua API deve estar documentada.
- [ ]  É recomendável (não obrigatório) a escolha de um método de
autenticação (JWT, por exemplo).
- [ ]  Criar um plano para fazer o deploy da API, desenhando a arquitetura
do projeto desde a ingestão até a alimentação do modelo (aqui não é
necessário elaborar um modelo de ML, mas é preciso que vocês
escolham um cenário interessante em que a API possa ser utilizada).
- [ ]  Fazer um MVP realizando o deploy com um link compartilhável e um
repositório no github


A API disponibiliza 5 rotas para consulta dos dados de vitivinicultura da Embrapa, nas seguintes rotas:
- /Produção.
- /Processamento.
- /Comercialização.
- /Importação.
- /Exportação.

Pode ser enviado o ano cujos dados devem ser consultados, desde que disponíveis no site.

A API pode ser utilizada para a análise dos dados histórico, para ajudar a prever quanto será importado ou exportado de acordo com a produção e o processamento, assim como a comercialiazação. 

Para o depploy, será utilizado o S3 para armazenamento dos dados, um ECS para hospedar da API e o sagemaker para realizar as inferências. 