import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

def get_content(opt: str, ano:int):
  url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opt}"
  response = requests.get(url)

  if response.status_code == 200:
      html_content = response.text
  else:
      print(f"Erro ao acessar a página. Código de status: {response.status_code} ")
      raise Exception
      
  return html_content


def get_table(opt: str, ano:int):
    
    html_content = get_content(opt=opt, ano=ano)
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", {"class": "tb_base tb_dados"})

    if table is None:
        print(f"Nenhuma tabela encontrada para ano {ano} e opção {opt}")
        return pd.DataFrame()

    rows = table.find_all("tr")
    data = []
    for row in rows:
        cells = row.find_all(["th", "td"])
        cells_text = [cell.get_text(strip=True) for cell in cells]
        data.append(cells_text)

    if not data or len(data) < 2:
        print("Tabela sem dados")
        return pd.DataFrame()

    headers = [h if h else f"col_{i}" for i, h in enumerate(data[0])]
    df = pd.DataFrame(data[1:], columns=headers)

    for col in df.columns[1:]:
        df[col] = df[col].str.replace(".", "", regex=False)
        df[col] = df[col].str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.to_dict(orient="records"), df


def check_none(value):
  # substitui NaN por None
  if isinstance(value, float) and math.isnan(value):
      value = None
  return value


def extrair_tabela_produto(opt: str, ano: int):

    registros, df = get_table(opt=opt, ano=ano)

    resultado = {
      "dados": [],
      "total": {}
    }
    grupo_atual = None

    for item in registros:
      produto = item["Produto"]
      quantidade = check_none(item[df.columns[1]])

      if produto.isupper() and not produto.startswith("TOTAL"):
          grupo_atual = {
              "Produto": produto,
              "Quantidade (L.)": quantidade,
              "Subprodutos": [],
          }
          resultado["dados"].append(grupo_atual)
      elif produto.lower() == "total":
        grupo_atual = {
          "Quantidade (L.)": quantidade
        }
        resultado["total"] = grupo_atual
      else:
          if grupo_atual:
              grupo_atual["Subprodutos"].append(
                  {"Produto": produto, "Quantidade (L.)": quantidade}
              )
          else:
              resultado["dados"].append({"Produto": produto, "Quantidade (L.)": quantidade})
    return resultado


def extrair_tabela_cultivo(opt: str, ano: int):
    registros, df = get_table(opt=opt, ano=ano)

    resultado = {
      "dados": [],
      "total": {}
    }

    grupo_atual = None

    for item in registros:
      produto = item["Cultivar"]
      quantidade = check_none(item[df.columns[1]])

      if produto.isupper() and not produto.startswith("TOTAL"):
          grupo_atual = {
              "Produto": produto,
              "Quantidade (L.)": quantidade,
              "Subprodutos": [],
          }
          resultado["dados"].append(grupo_atual)
      elif produto.lower() == "total":
        grupo_atual = {
          "Quantidade (L.)": quantidade
        }
        resultado["total"] = grupo_atual
      else:
          if grupo_atual:
              grupo_atual["Subprodutos"].append(
                  {"Produto": produto, "Quantidade (L.)": quantidade}
              )
          else:
              resultado["dados"].append({"Produto": produto, "Quantidade (L.)": quantidade})
    return resultado


def extrair_tabela_venda(opt: str, ano: int):
    registros, df = get_table(opt=opt, ano=ano)

    resultado = {
      "dados": [],
      "total": {}
    }

    grupo_atual = None

    for item in registros:
      pais = item["Países"]
      quantidade = check_none(item[df.columns[1]])
      valor = check_none(item[df.columns[2]])
      if pais.lower() != "total":
        grupo_atual = {
            "País": pais,
            "Quantidade (L.)": quantidade,
            "Valor": valor,
        }
        resultado["dados"].append(grupo_atual)
      else:
        grupo_atual = {
          "Quantidade (L.)": quantidade,
          "Valor": valor,
        }
        resultado["total"] = grupo_atual
      
    return resultado
