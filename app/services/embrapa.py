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

    resultado = []
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
          resultado.append(grupo_atual)
      elif produto.lower() == "total":
          continue
      else:
          if grupo_atual:
              grupo_atual["Subprodutos"].append(
                  {"Produto": produto, "Quantidade (L.)": quantidade}
              )
          else:
              resultado.append({"Produto": produto, "Quantidade (L.)": quantidade})
    return resultado


def extrair_tabela_cultivo(opt: str, ano: int):
    registros, df = get_table(opt=opt, ano=ano)

    resultado = []
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
          resultado.append(grupo_atual)
      elif produto.lower() == "total":
          continue
      else:
          if grupo_atual:
              grupo_atual["Subprodutos"].append(
                  {"Produto": produto, "Quantidade (L.)": quantidade}
              )
          else:
              resultado.append({"Produto": produto, "Quantidade (L.)": quantidade})
    return resultado


def extrair_tabela_venda(opt: str, ano: int):
    registros, df = get_table(opt=opt, ano=ano)

    resultado = []
    grupo_atual = None

    for item in registros:
      pais = item["Países"]
      quantidade = check_none(item[df.columns[1]])
      valor = check_none(item[df.columns[2]])
      grupo_atual = {
          "País": pais,
          "Quantidade (L.)": quantidade,
          "Valor": valor,
      }
      resultado.append(grupo_atual)
      
    return resultado


# def extrair_tabela_produto(opt: str, ano: int):
#     url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opt}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         html_content = response.text
#     else:
#         print(f"Erro ao acessar a página. Código de status: {response.status_code} ")
#         return

#     soup = BeautifulSoup(html_content, "html.parser")
#     table = soup.find("table", {"class": "tb_base tb_dados"})

#     if table is None:
#         print(f"Nenhuma tabela encontrada para ano {ano} e opção {opt}")
#         return pd.DataFrame()

#     rows = table.find_all("tr")
#     data = []
#     for row in rows:
#         cells = row.find_all(["th", "td"])
#         cells_text = [cell.get_text(strip=True) for cell in cells]
#         data.append(cells_text)

#     if not data or len(data) < 2:
#         print("Tabela sem dados")
#         return pd.DataFrame()

#     headers = [h if h else f"col_{i}" for i, h in enumerate(data[0])]
#     df = pd.DataFrame(data[1:], columns=headers)

#     for col in df.columns[1:]:
#         df[col] = df[col].str.replace(".", "", regex=False)
#         df[col] = df[col].str.replace(",", ".", regex=False)
#         df[col] = pd.to_numeric(df[col], errors="coerce")

#     registros = df.to_dict(orient="records")

#     resultado = []
#     grupo_atual = None

#     for item in registros:
#       produto = item["Produto"]
#       quantidade = item[df.columns[1]]

#       # substitui NaN por None
#       if isinstance(quantidade, float) and math.isnan(quantidade):
#           quantidade = None

#       if produto.isupper() and not produto.startswith("TOTAL"):
#           grupo_atual = {
#               "Produto": produto,
#               "Quantidade (L.)": quantidade,
#               "Subprodutos": [],
#           }
#           resultado.append(grupo_atual)
#       elif produto.lower() == "total":
#           continue
#       else:
#           if grupo_atual:
#               # Subprodutos também podem ter NaN, trate da mesma forma
#               sub_quantidade = quantidade
#               if isinstance(sub_quantidade, float) and math.isnan(sub_quantidade):
#                   sub_quantidade = None
#               grupo_atual["Subprodutos"].append(
#                   {"Produto": produto, "Quantidade (L.)": sub_quantidade}
#               )
#           else:
#               resultado.append({"Produto": produto, "Quantidade (L.)": quantidade})
#     return resultado


# def extrair_tabela_cultivo(opt: str, ano: int):
#     url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opt}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         html_content = response.text
#     else:
#         print(f"Erro ao acessar a página. Código de status: {response.status_code} ")
#         return

#     soup = BeautifulSoup(html_content, "html.parser")
#     table = soup.find("table", {"class": "tb_base tb_dados"})

#     if table is None:
#         print(f"Nenhuma tabela encontrada para ano {ano} e opção {opt}")
#         return pd.DataFrame()

#     rows = table.find_all("tr")
#     data = []
#     for row in rows:
#         cells = row.find_all(["th", "td"])
#         cells_text = [cell.get_text(strip=True) for cell in cells]
#         data.append(cells_text)

#     if not data or len(data) < 2:
#         print("Tabela sem dados")
#         return pd.DataFrame()

#     headers = [h if h else f"col_{i}" for i, h in enumerate(data[0])]
#     df = pd.DataFrame(data[1:], columns=headers)

#     for col in df.columns[1:]:
#         df[col] = df[col].str.replace(".", "", regex=False)
#         df[col] = df[col].str.replace(",", ".", regex=False)
#         df[col] = pd.to_numeric(df[col], errors="coerce")

#     registros = df.to_dict(orient="records")

#     resultado = []
#     grupo_atual = None

#     for item in registros:
#       produto = item["Cultivar"]
#       quantidade = item[df.columns[1]]

#       # substitui NaN por None
#       if isinstance(quantidade, float) and math.isnan(quantidade):
#           quantidade = None

#       if produto.isupper() and not produto.startswith("TOTAL"):
#           grupo_atual = {
#               "Produto": produto,
#               "Quantidade (L.)": quantidade,
#               "Subprodutos": [],
#           }
#           resultado.append(grupo_atual)
#       elif produto.lower() == "total":
#           continue
#       else:
#           if grupo_atual:
#               # Subprodutos também podem ter NaN, trate da mesma forma
#               sub_quantidade = quantidade
#               if isinstance(sub_quantidade, float) and math.isnan(sub_quantidade):
#                   sub_quantidade = None
#               grupo_atual["Subprodutos"].append(
#                   {"Produto": produto, "Quantidade (L.)": sub_quantidade}
#               )
#           else:
#               resultado.append({"Produto": produto, "Quantidade (L.)": quantidade})
#     return resultado


# def extrair_tabela_venda(opt: str, ano: int):
#     url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opt}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         html_content = response.text
#     else:
#         print(f"Erro ao acessar a página. Código de status: {response.status_code} ")
#         return

#     soup = BeautifulSoup(html_content, "html.parser")
#     table = soup.find("table", {"class": "tb_base tb_dados"})

#     if table is None:
#         print(f"Nenhuma tabela encontrada para ano {ano} e opção {opt}")
#         return pd.DataFrame()

#     rows = table.find_all("tr")
#     data = []
#     for row in rows:
#         cells = row.find_all(["th", "td"])
#         cells_text = [cell.get_text(strip=True) for cell in cells]
#         data.append(cells_text)

#     if not data or len(data) < 2:
#         print("Tabela sem dados")
#         return pd.DataFrame()

#     headers = [h if h else f"col_{i}" for i, h in enumerate(data[0])]
#     df = pd.DataFrame(data[1:], columns=headers)

#     for col in df.columns[1:]:
#         df[col] = df[col].str.replace(".", "", regex=False)
#         df[col] = df[col].str.replace(",", ".", regex=False)
#         df[col] = pd.to_numeric(df[col], errors="coerce")

#     registros = df.to_dict(orient="records")

#     resultado = []
#     grupo_atual = None

#     for item in registros:
#       pais = item["Países"]
#       quantidade = item[df.columns[1]]
#       valor = item[df.columns[2]]

#       # substitui NaN por None
#       if isinstance(quantidade, float) and math.isnan(quantidade):
#           quantidade = None

#       if isinstance(valor, float) and math.isnan(valor):
#           valor = None

#       grupo_atual = {
#           "País": pais,
#           "Quantidade (L.)": quantidade,
#           "Valor": valor,
#       }
#       resultado.append(grupo_atual)
      
#     return resultado
