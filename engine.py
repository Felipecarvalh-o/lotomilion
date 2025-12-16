from itertools import combinations
import random
from collections import Counter

# ================================
# ESTRATÉGIA PRINCIPAL
# Fechamento 21 dezenas → 8 jogos
# ================================
def gerar_fechamento_21_8(dezenas_21):
    dezenas = sorted(set(dezenas_21))

    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    if any(n < 1 or n > 25 for n in dezenas):
        raise ValueError("As dezenas devem estar entre 1 e 25.")

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
# ESTRATÉGIA FREQUENCIAL (QUENTES / MORNAS / FRIAS)
# =========================================
def gerar_jogos_quentes_frios(dezenas_21, total_jogos=8):
    dezenas = sorted(set(dezenas_21))

    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    # Simulação educacional de frequência
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
