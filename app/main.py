from fastapi import FastAPI, Query, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.embrapa import extrair_tabela_produto, extrair_tabela_cultivo, extrair_tabela_venda
from app.services.authentication import verify_token

app = FastAPI(
  title="API Vitivinicultura Embrapa",
  version="1.0.0",
  description="API Vitivinicultura Embrapa"
)

@app.get("/")
async def home():
  return  f"API Vitivinicultura Embrapa"


# @app.get("/hello")
# async def hello(username: str = Depends(verify_token)):
#   return  f"{username}, Bem-vindo a API Vitivinicultura Embrapa"


@app.get("/producao")
async def producao(
    ano: Optional[int] = Query(default=2023, description="Ano da produção [1970-2023"),
    username: str = Depends(verify_token)
):
    """
    Extrai a tabela de produção da Embrapa para um determinado ano
    """
    dados = extrair_tabela_produto("opt_02", ano)

    if not dados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado encontrado para o ano {ano}."
        )
    print(dados)
    # return JSONResponse(content="ok")
    return dados


@app.get("/processamento")
async def processamento(
    ano: Optional[int] = Query(default=2023, description="Ano do processamento [1970-2023"),
    username: str = Depends(verify_token)
):
    """
    Extrai a tabela do processamento da Embrapa para um determinado ano
    """
    dados = extrair_tabela_cultivo("opt_03", ano)

    if not dados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado encontrado para o ano {ano}."
        )
    print(dados)
    # return JSONResponse(content="ok")
    return dados



@app.get("/comercializacao")
async def comercializacao(
    ano: Optional[int] = Query(default=2023, description="Ano da comercializacao [1970-2023"),
    username: str = Depends(verify_token)
):
    """
    Extrai a tabela de comercializacao da Embrapa para um determinado ano
    """
    dados = extrair_tabela_produto("opt_04", ano)

    if not dados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado encontrado para o ano {ano}."
        )
    print(dados)
    # return JSONResponse(content="ok")
    return dados



@app.get("/importacao")
async def importacao(
    ano: Optional[int] = Query(default=2023, description="Ano da importacao [1970-2024]"),
    username: str = Depends(verify_token)
):
    """
    Extrai a tabela da importacao da Embrapa para um determinado ano
    """
    dados = extrair_tabela_venda("opt_05", ano)

    if not dados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado encontrado para o ano {ano}."
        )
    print(dados)
    # return JSONResponse(content="ok")
    return dados



@app.get("/exportacao")
async def exportacao(
    ano: Optional[int] = Query(default=2023, description="Ano da exportacao [1970-2024]"),
    username: str = Depends(verify_token)
):
    """
    Extrai a tabela da exportacao da Embrapa para um determinado ano
    """
    dados = extrair_tabela_venda("opt_06", ano)

    if not dados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado encontrado para o ano {ano}."
        )
    print(dados)
    # return JSONResponse(content="ok")
    return dados