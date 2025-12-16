def converter_lista(texto):
    """
    Converte uma string de dezenas em lista de inteiros.
    Aceita espaços, vírgulas ou hífen.
    """
    if not texto:
        return []

    texto = texto.replace(",", " ").replace("-", " ")
    partes = texto.split()

    dezenas = []
    for p in partes:
        try:
            n = int(p)
            if 1 <= n <= 25:
                dezenas.append(n)
        except ValueError:
            pass

    return sorted(set(dezenas))
