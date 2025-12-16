import json
import os
from datetime import datetime

ARQ_HISTORICO = "historico.json"
ARQ_RANKING = "ranking.json"


def _ler_json(arquivo):
    if not os.path.exists(arquivo):
        return []
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _salvar_json(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


# ==================================================
# REGISTRO DE ANÁLISES (efeito psicológico forte)
# ==================================================

def registrar_analise(usuario, estrategia, dezenas_base, melhor_pontuacao):
    """
    Registra cada análise feita pelo usuário.
    Isso cria histórico, percepção de evolução
    e sensação de jogo 'bem trabalhado'.
    """

    historico = _ler_json(ARQ_HISTORICO)

    historico.append({
        "usuario": usuario,
        "estrategia": estrategia,
        "dezenas_base": dezenas_base,
        "melhor_pontuacao": melhor_pontuacao,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    })

    _salvar_json(ARQ_HISTORICO, historico)

    _atualizar_ranking(usuario, melhor_pontuacao)


# ==================================================
# HISTÓRICO POR USUÁRIO
# ==================================================

def listar_analises_usuario(usuario):
    historico = _ler_json(ARQ_HISTORICO)

    return [
        h for h in historico
        if h["usuario"] == usuario
    ]


# ==================================================
# RANKING (efeito comparação / gamificação)
# ==================================================

def _atualizar_ranking(usuario, pontuacao):
    ranking = _ler_json(ARQ_RANKING)

    encontrado = False
    for r in ranking:
        if r["usuario"] == usuario:
            r["melhor_pontuacao"] = max(r["melhor_pontuacao"], pontuacao)
            encontrado = True
            break

    if not encontrado:
        ranking.append({
            "usuario": usuario,
            "melhor_pontuacao": pontuacao
        })

    ranking = sorted(
        ranking,
        key=lambda x: x["melhor_pontuacao"],
        reverse=True
    )

    _salvar_json(ARQ_RANKING, ranking)


def gerar_ranking():
    """
    Ranking educacional.
    Mostra quem costuma chegar mais perto
    (13, 14 ou até 15 pontos em simulações).
    """
    return _ler_json(ARQ_RANKING)
