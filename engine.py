from itertools import combinations
import random


def gerar_fechamento_21_8(dezenas_21):
    """
    Estratégia Principal — Fechamento Lotofácil Educacional

    Entrada:
    - 21 dezenas escolhidas pelo usuário
      (9 FIXAS + 12 VARIÁVEIS)

    Saída:
    - 8 jogos de 15 dezenas

    Observação:
    Modelo combinatório inspirado em fechamentos clássicos
    usados por apostadores para estudo de cobertura.
    Não garante premiação.
    """

    dezenas = sorted(set(dezenas_21))

    if len(dezenas) != 21:
        raise ValueError("Informe exatamente 21 dezenas (9 fixas + 12 variáveis).")

    if any(n < 1 or n > 25 for n in dezenas):
        raise ValueError("As dezenas devem estar entre 1 e 25.")

    # 🔒 9 FIXAS (núcleo de confiança)
    fixas = dezenas[:9]

    # 🔄 12 VARIÁVEIS (rotação do jogo)
    variaveis = dezenas[9:]

    jogos = []

    # Combina 6 variáveis + 9 fixas = 15 dezenas
    combinacoes_variaveis = list(combinations(variaveis, 6))
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
    Estratégia Frequencial (futura expansão)

    Reorganiza dezenas para estudo de equilíbrio
    entre números mais e menos recorrentes.
    """

    dezenas = sorted(set(dezenas_21))

    if len(dezenas) < 15:
        raise ValueError("Informe pelo menos 15 dezenas.")

    random.shuffle(dezenas)

    return [sorted(dezenas[:15])]
