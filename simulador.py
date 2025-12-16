import random

print("SIMULADOR CARREGADO")

def simular_cenario(jogos, total_sorteios=500, universo=25, tamanho_jogo=15):
    """
    Simulação estatística educacional da Lotofácil.
    Não prevê resultados reais.
    """

    resultados = []
    zeros = 0
    maximo = 0

    for _ in range(total_sorteios):
        sorteio = set(random.sample(range(1, universo + 1), tamanho_jogo))
        melhor = 0

        for jogo in jogos:
            pontos = len(sorteio & set(jogo))
            if pontos > melhor:
                melhor = pontos

        resultados.append(melhor)

        if melhor == 0:
            zeros += 1

        if melhor > maximo:
            maximo = melhor

    media = round(sum(resultados) / len(resultados), 2)

    return {
        "media": media,
        "maximo": maximo,
        "zeros": zeros,
        "total": total_sorteios
    }
