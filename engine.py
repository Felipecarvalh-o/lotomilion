from itertools import combinations
import random
from collections import Counter

# ================================
# FECHAMENTO 21 → 8 JOGOS DE 15
# ================================
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


# =========================================
# QUENTES • MORNAS • FRIAS (15 dezenas)
# =========================================
def gerar_jogos_quentes_frios(dezenas_21, total_jogos=8):

    dezenas = sorted(set(dezenas_21))
    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    # Simulação frequencial educacional
    pesos = []
    for n in dezenas:
        pesos.extend([n] * random.randint(1, 6))

    contador = Counter(pesos)
    ordenadas = [n for n, _ in contador.most_common()]

    quentes = ordenadas[:7]
    mornas = ordenadas[7:14]
    frias = ordenadas[14:]

    jogos = []
    for _ in range(total_jogos):
        jogo = set()
        jogo.update(random.sample(quentes, 5))
        jogo.update(random.sample(mornas, 5))
        jogo.update(random.sample(frias, 5))
        jogos.append(sorted(jogo))

    return jogos, {
        "quentes": quentes,
        "mornas": mornas,
        "frias": frias
    }
from collections import Counter
import random

def gerar_jogos_historico_real(dezenas_21, historico, total_jogos=8):
    """
    Estratégia baseada em resultados reais da Lotofácil.
    """

    dezenas = sorted(set(dezenas_21))
    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    # Conta frequência real
    contador = Counter()
    for concurso in historico:
        for n in concurso["numeros"]:
            if n in dezenas:
                contador[n] += 1

    ordenadas = [n for n, _ in contador.most_common()]

    # Classificação clara
    quentes = ordenadas[:7]
    mornas = ordenadas[7:14]
    frias = ordenadas[14:]

    jogos = []
    for _ in range(total_jogos):
        jogo = set()
        jogo.update(random.sample(quentes, 5))
        jogo.update(random.sample(mornas, 5))
        jogo.update(random.sample(frias, 5))
        jogos.append(sorted(jogo))

    return jogos, {
        "quentes": quentes,
        "mornas": mornas,
        "frias": frias
    }

from collections import Counter
import random

def gerar_jogos_historico_real(dezenas_21, historico, total_jogos=8):
    dezenas = sorted(set(dezenas_21))
    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    contador = Counter()

    for concurso in historico:
        for n in concurso.get("numeros", []):
            if n in dezenas:
                contador[n] += 1

    ordenadas = [n for n, _ in contador.most_common()]

    # fallback de segurança
    while len(ordenadas) < 21:
        for n in dezenas:
            if n not in ordenadas:
                ordenadas.append(n)

    quentes = ordenadas[:7]
    mornas = ordenadas[7:14]
    frias = ordenadas[14:21]

    jogos = []
    for _ in range(total_jogos):
        jogo = set()
        jogo.update(random.sample(quentes, 5))
        jogo.update(random.sample(mornas, 5))
        jogo.update(random.sample(frias, 5))
        jogos.append(sorted(jogo))

    return jogos, {
        "quentes": quentes,
        "mornas": mornas,
        "frias": frias
    }


