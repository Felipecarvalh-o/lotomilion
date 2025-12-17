import requests

URL = "https://raw.githubusercontent.com/Felipecarvalh-o/loteria-dados/main/lotofacil.json"

def carregar_historico(qtd=50):
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
        dados = r.json()
        concursos = dados.get("concursos", [])
        return concursos[:qtd]
    except Exception as e:
        # Segurança total: app nunca quebra
        return []
