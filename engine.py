from itertools import combinations
import random


def gerar_fechamento_21_dezenas(dezenas_21):
    """
    Estratégia principal — Cobertura Combinatória Educacional

    Entrada:
    - 21 dezenas escolhidas pelo usuário

    Saída:
    - 8 jogos de 15 dezenas

    Observação:
    Modelo clássico de fechamento, usado para estudo
    de cobertura matemática. Não garante premiação.
    """

    if len(dezenas_21) != 21:
        raise ValueError("Informe exatamente 21 dezenas.")

    dezenas = sorted(set(dezenas_21))

    if any(n < 1 or n > 25 for n in dezenas):
        raise ValueError("As dezenas devem estar entre 1 e 25.")

    # Divide em 12 fixas + 9 variáveis (educacional)
    fixas = dezenas[:12]
    variaveis = dezenas[12:]

    jogos = []

    # Gera combinações das variáveis (educacional)
    combinacoes_variaveis = list(combinations(variaveis, 3))
    random.shuffle(combinacoes_variaveis)

    for combo in combinacoes_variaveis:
        jogo = sorted(fixas + list(combo))
        if len(jogo) == 15:
            jogos.append(jogo)

        if len(jogos) >= 8:
            break

    return jogos


def gerar_jogos_frequenciais(dezenas_21):
    """
    Estratégia secundária (opcional futura):
    apenas reorganiza as dezenas em jogos balanceados
    """
    random.shuffle(dezenas_21)
    return [sorted(dezenas_21[i:i+15]) for i in range(0, 15, 15)]
