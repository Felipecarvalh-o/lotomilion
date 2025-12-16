from itertools import combinations
import random

def gerar_fechamento_21_8(dezenas_21):
    if len(dezenas_21) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    dezenas = sorted(set(dezenas_21))

    if any(n < 1 or n > 25 for n in dezenas):
        raise ValueError("Dezenas devem estar entre 1 e 25.")

    # 9 fixas + 12 variáveis (educacional)
    fixas = dezenas[:9]
    variaveis = dezenas[9:]

    jogos = []
    combinacoes = list(combinations(variaveis, 6))
    random.shuffle(combinacoes)

    for combo in combinacoes:
        jogo = sorted(fixas + list(combo))
        if len(jogo) == 15:
            jogos.append(jogo)

        if len(jogos) >= 8:
            break

    return jogos
