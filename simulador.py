import random


def simular_cenario(jogos, total_sorteios=500):
    """
    Simula sorteios aleatórios da Lotofácil (15 dezenas entre 1 e 25)
    e observa o melhor desempenho dos jogos gerados.
    """

    resultados = []
    zeros = 0
    maximo = 0

    for _ in range(total_sorteios):
        sorteio = set(random.sample(range(1, 26), 15))
        melhor = 0

        for jogo in jogos:
            pontos = len(sorteio & set(jogo))
            melhor = max(melhor, pontos)

        resultados.append(melhor)
        if melhor == 0:
            zeros += 1
        maximo = max(maximo, melhor)

    media = round(sum(resultados) / len(resultados), 2)

    return {
        "media": media,
        "maximo": maximo,
        "zeros": zeros,
        "total": total_sorteios
    }
