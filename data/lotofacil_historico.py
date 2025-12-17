import requests

URL = "https://raw.githubusercontent.com/SEU_USUARIO/loteria-dados/main/lotofacil.json"

def carregar_historico(qtd=50):
    """
    Carrega os últimos N concursos da Lotofácil
    """
    dados = requests.get(URL, timeout=10).json()
    concursos = dados.get("concursos", [])
    return concursos[:qtd]
