from itertools import combinations
import random
from collections import Counter


# ================================
# ESTRATÉGIA PRINCIPAL
# Fechamento 21 dezenas → 8 jogos
# ================================
def gerar_fechamento_21_8(dezenas_21):
    """
    Fechamento educacional:
    21 dezenas → 8 jogos de 15
    Modelo clássico (9 fixas + 12 variáveis)
    """

    dezenas = sorted(set(dezenas_21))

    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas sem repetição.")

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
# ESTRATÉGIA FREQUENCIAL (QUENTES & FRIOS)
# =========================================
def gerar_jogos_quentes_frios(dezenas_21, total_jogos=8):
    """
    Estratégia educacional de Quentes & Frios

    Usa APENAS as dezenas escolhidas pelo usuário,
    simulando uma leitura frequencial (sem histórico real).
    """

    dezenas = sorted(set(dezenas_21))

    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    # Simula pesos frequenciais (educacional)
    pesos = []
    for n in dezenas:
        pesos.extend([n] * random.randint(1, 5))

    contador = Counter(pesos)

    ordenadas = [n for n, _ in contador.most_common()]

    quentes = ordenadas[:12]
    frias = ordenadas[-12:]

    jogos = []

    for _ in range(total_jogos):
        jogo = set()
        jogo.update(random.sample(quentes, 8))
        jogo.update(random.sample(frias, 7))
        jogos.append(sorted(jogo))

    return jogos, {
        "quentes": quentes,
        "frias": frias
    }
