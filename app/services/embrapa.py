import requests
from bs4 import BeautifulSoup
import pandas as pd


def extrair_tabela(opt: str, ano: int):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={opt}"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Erro ao acessar a página. Código de status: {response.status_code} ")
        return

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

    registros = df.to_dict(orient="records")

    resultado = []
    grupo_atual = None

    for item in registros:
        produto = item["Produto"]
        quantidade = item[df.columns[1]]

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


if __name__ == "__main__":
    print(extrair_tabela("opt_02", "2022"))
