from itertools import combinations
import random
from collections import Counter


# ================================
# ESTRATÉGIA PRINCIPAL
# Fechamento 21 dezenas → 8 jogos
# ================================
def gerar_fechamento_21_8(dezenas_21):
    if len(dezenas_21) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    dezenas = sorted(set(dezenas_21))

    if any(n < 1 or n > 25 for n in dezenas):
        raise ValueError("As dezenas devem estar entre 1 e 25.")

    # 9 fixas + 12 variáveis (modelo educacional)
    fixas = dezenas[:9]
    variaveis = dezenas[9:]

    jogos = []
    combinacoes = list(combinations(variaveis, 6))
    random.shuffle(combinacoes)

    for combo in combinacoes:
        jogo = sorted(fixas + list(combo))
        if len(jogo) == 15:
            jogos.append(jogo)

        if len(jogos) == 8:
            break

    return jogos


# =========================================
# ESTRATÉGIA FREQUENCIAL (QUENTES & FRIOS)
# =========================================
def gerar_jogos_quentes_frios(historico, total_jogos=8):
    """
    Gera jogos balanceados usando dezenas mais e menos frequentes
    """
    contador = Counter()

    for sorteio in historico:
        contador.update(sorteio)

    dezenas_ordenadas = [n for n, _ in contador.most_common()]

    quentes = dezenas_ordenadas[:12]
    frios = dezenas_ordenadas[-12:]

    jogos = []

    for _ in range(total_jogos):
        jogo = set()
        jogo.update(random.sample(quentes, 8))
        jogo.update(random.sample(frios, 7))
        jogos.append(sorted(jogo))

    return jogos
