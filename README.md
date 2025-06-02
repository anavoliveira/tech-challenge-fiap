# Tech Challenger - FIAP

## Fase 1 – Análise e Consulta dos Dados de Vitivinicultura da Embrapa

### Contexto

Você foi contratado(a) para uma consultoria que envolve a análise dos dados de vitivinicultura disponibilizados pela Embrapa, acessíveis [aqui](http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01).

O objetivo principal do projeto é desenvolver uma **API pública** que permita consultar os dados das seguintes categorias presentes no site:

- Produção  
- Processamento  
- Comercialização  
- Importação  
- Exportação  

Esses dados serão usados para alimentar uma base que, futuramente, servirá para treinar um modelo de Machine Learning.

---

### Objetivos do Projeto

- Desenvolver uma API REST em Python para consulta dos dados da Embrapa.  
- Documentar a API de forma clara e acessível.  
- Implementar um método de autenticação (recomenda-se JWT, mas não é obrigatório).  
- Criar um plano arquitetural para o deploy da API, contemplando o fluxo desde a ingestão dos dados até a alimentação do modelo ML (ainda sem necessidade de criar o modelo neste momento).  
- Construir um MVP, fazer o deploy da API, disponibilizar um link público para acesso e manter o código em um repositório GitHub.

---

### Endpoints da API

A API expõe 5 rotas para consulta dos dados, cada uma referente a uma categoria específica:

- `/producao`  
- `/processamento`  
- `/comercializacao`  
- `/importacao`  
- `/exportacao`  

É possível enviar um parâmetro `ano` para consultar dados específicos daquele ano (desde que disponíveis no site da Embrapa).

---

### Formato dos Dados Retornados

Para as rotas **produção**, **processamento** e **comercialização**, o formato JSON dos dados é:

```json
{
  "dados": [
    {
      "Produto": "VINHO DE MESA",
      "Quantidade (L.)": 169762429.0,
      "Subprodutos": [
        {
          "Produto": "Tinto",
          "Quantidade (L.)": 139320884.0
        }
      ]
    }
  ],
  "total": {
    "Quantidade (L.)": 457792870.0
  }
}
```

As rotas **/importacao** e **/exportacao** retornam dados em formato semelhante.  

```json
{
  "dados": [
    {
      "País": "Africa do Sul",
      "Quantidade (L.)": 522733.0,
      "Valor": 1732850.0
    }
  ],
  "total": {
    "Quantidade (L.)": 137712871.0,
    "Valor": 428292652.0
  }
}
```
Para mais detalhes sobre os campos e estrutura, consulte a [documentação da API](https://tech-challenger.onrender.com/docs).

---

## Uso Futuro da API

Está planejada a criação de uma nova rota:

- **`/predict`**  
  Essa rota fornecerá inferências de um modelo de Machine Learning treinado com os dados históricos obtidos no site da Embrapa.  
  O objetivo é prever, por exemplo, a demanda futura de importação e exportação de vinho no Brasil.

---

## Arquitetura de Deploy

A arquitetura do projeto foi desenhada utilizando serviços da AWS:

- **AWS Lambda + API Gateway**  
  Responsáveis por hospedar a API e lidar com requisições HTTP públicas, realizando a extração e ingestão dos dados da Embrapa.

- **Amazon S3**  
  Utilizado para armazenar os dados históricos processados e servir de base para treinamento e inferência.

- **Amazon SageMaker**  
  Realiza o treinamento do modelo de Machine Learning e hospeda o endpoint para inferência.

---

##  Acesso à API

O MVP da API está disponível em:

🔗 [https://tech-challenger.onrender.com](https://tech-challenger.onrender.com)
