from flask import Flask, jsonify, request
from services.embrapa import extrair_tabela
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger

users = {
    "user1": "password1",
    "user2": "password2"
}

app  = Flask(__name__)
auth = HTTPBasicAuth()

app.config["SWAGGER"] = {
    "title": "API Vitivinicultura Embrapa", 
    "uiversion": 3
}

swagger_template = {
    "securityDefinitions": {
        "basicAuth": {
            "type": "basic"
        }
    }
}

swagger = Swagger(app, template=swagger_template)


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def home():
    return "API Vitivinicultura Embrapa"

@app.route('/producao', methods=["GET"])
def get_producao():
    """
    Extract production table
    ---
    tags:
      - Produção
    parameters:
      - name: ano
        in: query
        type: integer
        required: false
        description: Ano da produção (ex: 2023)
    security:
      - basicAuth: []
    responses:
      200:
        description: Tabela de produção extraída com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              Produto:
                type: string
              Quantidade (L.):
                type: number
              Subprodutos:
                type: array
                items:
                  type: object
                  properties:
                    Produto:
                      type: string
                    Quantidade (L.):
                      type: number
    """     
    ano = request.args.get("ano", default=2023, type=int)
    return jsonify(extrair_tabela("opt_02", ano))

@app.route('/processamento', methods=["GET"])
def get_processamento():
    """
    Extract production table
    ---
    tags:
      - Produção
    parameters:
      - name: ano
        in: query
        type: integer
        required: false
        description: Ano da produção (ex: 2023)
    security:
      - basicAuth: []
    responses:
      200:
        description: Tabela de produção extraída com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              Produto:
                type: string
              Quantidade (L.):
                type: number
              Subprodutos:
                type: array
                items:
                  type: object
                  properties:
                    Produto:
                      type: string
                    Quantidade (L.):
                      type: number
    """     
    ano = request.args.get("ano", default=2023, type=int)
    return jsonify(extrair_tabela("opt_03", ano))

@app.route('/comercializacao', methods=["GET"])
def get_comercializacao():
    """
    Extract comercialization table
    ---
    tags:
      - Comercialização
    parameters:
      - name: ano
        in: query
        type: integer
        required: false
        description: Ano da comercialização (ex: 2023)
    security:
      - basicAuth: []
    responses:
      200:
        description: Tabela de comercialização extraída com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              Produto:
                type: string
              Quantidade (L.):
                type: number
              Subprodutos:
                type: array
                items:
                  type: object
                  properties:
                    Produto:
                      type: string
                    Quantidade (L.):
                      type: number
    """     
    ano = request.args.get("ano", default=2023, type=int)
    return jsonify(extrair_tabela("opt_04", ano))

@app.route('/importacao', methods=["GET"])
def get_importacao():
    """
    Extract importation table
    ---
    tags:
      - Importação
    parameters:
      - name: ano
        in: query
        type: integer
        required: false
        description: Ano da importação (ex: 2023)
    security:
      - basicAuth: []
    responses:
      200:
        description: Tabela de importação extraída com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              Produto:
                type: string
              Quantidade (L.):
                type: number
              Subprodutos:
                type: array
                items:
                  type: object
                  properties:
                    Produto:
                      type: string
                    Quantidade (L.):
                      type: number
    """     
    ano = request.args.get("ano", default=2023, type=int)
    return jsonify(extrair_tabela("opt_05", ano))

@app.route('/exportacao', methods=["GET"])
def get_exportacao():
    """
    Extract exportation table
    ---
    tags:
      - Exportação
    parameters:
      - name: ano
        in: query
        type: integer
        required: false
        description: Ano da exportacao (ex: 2023)
    security:
      - basicAuth: []
    responses:
      200:
        description: Tabela de exportacao extraída com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              Produto:
                type: string
              Quantidade (L.):
                type: number
              Subprodutos:
                type: array
                items:
                  type: object
                  properties:
                    Produto:
                      type: string
                    Quantidade (L.):
                      type: number
    """     
    ano = request.args.get("ano", default=2023, type=int)
    return jsonify(extrair_tabela("opt_06", ano))


if __name__ == "__main__":
    app.run(debug=True)