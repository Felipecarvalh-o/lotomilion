from itertools import combinations
import random
from collections import Counter

# ======================================================
# MOTOR INTERNO — CLASSIFICAÇÃO QUENTE / MORNA / FRIA
# ======================================================
def classificar_frequencia(dezenas, pesos=None):
    """
    Classifica dezenas em quentes, mornas e frias.
    Se pesos não for informado, usa distribuição neutra.
    """

    if pesos:
        contador = Counter(pesos)
    else:
        contador = Counter({n: 1 for n in dezenas})

    ordenadas = [n for n, _ in contador.most_common()]

    # segurança
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
# CLASSIFICAÇÃO FREQUENCIAL (SIMULADA — MOTOR INTERNO)
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

    # Frequência real baseada em concursos
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
