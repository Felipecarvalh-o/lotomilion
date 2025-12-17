import requests

URL = "https://raw.githubusercontent.com/Felipecarvalh-o/loteria-dados/main/lotofacil.json"

def carregar_historico(qtd=50):
    dados = requests.get(URL, timeout=10).json()
    concursos = dados.get("concursos", [])
    return concursos[:qtd]
