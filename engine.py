from itertools import combinations
import random
from collections import Counter
import json
import os
from datetime import datetime
from statistics import mean, stdev

ARQ_HISTORICO = "historico.json"
ARQ_RANKING = "ranking.json"

# ======================================================
# MOTOR INTERNO — CLASSIFICAÇÃO QUENTE / MORNA / FRIA
# ======================================================
def classificar_frequencia(dezenas, pesos=None):
    if pesos:
        contador = Counter(pesos)
    else:
        contador = Counter({n: 1 for n in dezenas})

    ordenadas = [n for n, _ in contador.most_common()]

    while len(ordenadas) < len(dezenas):
        for n in dezenas:
            if n not in ordenadas:
                ordenadas.append(n)

    return {
        "quentes": ordenadas[:7],
        "mornas": ordenadas[7:14],
        "frias": ordenadas[14:21]
    }


# ======================================================
# FECHAMENTO 21 → 8 JOGOS DE 15
# ======================================================
def gerar_fechamento_21_8(dezenas_21):
    dezenas = sorted(set(dezenas_21))

    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    fixas = dezenas[:9]
    variaveis = dezenas[9:]

    jogos = []
    combinacoes = list(combinations(variaveis, 6))
    random.shuffle(combinacoes)

    for combo in combinacoes:
        jogo = sorted(fixas + list(combo))
        jogos.append(jogo)
        if len(jogos) == 8:
            break

    return jogos


# ======================================================
# CLASSIFICAÇÃO FREQUENCIAL (SIMULADA)
# ======================================================
def gerar_classificacao_simulada(dezenas_21):
    dezenas = sorted(set(dezenas_21))

    pesos = []
    for n in dezenas:
        pesos.extend([n] * random.randint(1, 6))

    return classificar_frequencia(dezenas, pesos)


# ======================================================
# HISTÓRICO REAL — LOTOFÁCIL
# ======================================================
def gerar_jogos_historico_real(dezenas_21, historico, total_jogos=8):
    dezenas = sorted(set(dezenas_21))

    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    pesos = []
    for concurso in historico:
        for n in concurso.get("numeros", []):
            if n in dezenas:
                pesos.append(n)

    classificacao = classificar_frequencia(dezenas, pesos)

    jogos = []
    for _ in range(total_jogos):
        jogo = set()
        jogo.update(random.sample(classificacao["quentes"], 5))
        jogo.update(random.sample(classificacao["mornas"], 5))
        jogo.update(random.sample(classificacao["frias"], 5))
        jogos.append(sorted(jogo))

    return jogos, classificacao


# ======================================================
# 🔥 BLOCO PREMIUM — HISTÓRICO + RANKING
# ======================================================

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


def registrar_analise(usuario, estrategia, dezenas_base, resumo_simulacao):
    historico = _ler_json(ARQ_HISTORICO)

    historico.append({
        "usuario": usuario,
        "estrategia": estrategia,
        "dezenas_base": dezenas_base,
        "media_acertos": resumo_simulacao["media"],
        "melhor_resultado": resumo_simulacao["maximo"],
        "freq_11+": resumo_simulacao["freq_11"],
        "freq_12+": resumo_simulacao["freq_12"],
        "freq_13+": resumo_simulacao["freq_13"],
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    })

    _salvar_json(ARQ_HISTORICO, historico)
    _atualizar_ranking(usuario, resumo_simulacao["maximo"])


def listar_analises_usuario(usuario):
    historico = _ler_json(ARQ_HISTORICO)
    return [h for h in historico if h["usuario"] == usuario]


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

    ranking.sort(key=lambda x: x["melhor_pontuacao"], reverse=True)
    _salvar_json(ARQ_RANKING, ranking)


def gerar_ranking():
    return _ler_json(ARQ_RANKING)
