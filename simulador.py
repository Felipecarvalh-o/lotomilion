import random
from statistics import mean, stdev


def simular_cenario(jogos, total_sorteios=500, universo=25, tamanho_jogo=15):
    resultados = []

    for _ in range(total_sorteios):
        sorteio = set(random.sample(range(1, universo + 1), tamanho_jogo))
        melhor = 0

        for jogo in jogos:
            pontos = len(sorteio & set(jogo))
            if pontos > melhor:
                melhor = pontos

        resultados.append(melhor)

    media_acertos = round(mean(resultados), 2)
    desvio = round(stdev(resultados), 2) if len(resultados) > 1 else 0
    maximo = max(resultados)

    freq_11 = round((sum(1 for r in resultados if r >= 11) / total_sorteios) * 100, 2)
    freq_12 = round((sum(1 for r in resultados if r >= 12) / total_sorteios) * 100, 2)
    freq_13 = round((sum(1 for r in resultados if r >= 13) / total_sorteios) * 100, 2)

    return {
        "media": media_acertos,
        "desvio": desvio,
        "maximo": maximo,
        "freq_11": freq_11,
        "freq_12": freq_12,
        "freq_13": freq_13,
        "total": total_sorteios
    }
