def converter_lista(texto):
    """
    Converte texto digitado pelo usuário em lista de dezenas.
    Aceita separação por vírgula, espaço ou quebra de linha.
    """
    if not texto:
        return []

    try:
        dezenas = [
            int(x.strip())
            for x in texto.replace("\n", ",").replace(" ", ",").split(",")
            if x.strip().isdigit()
        ]
        return sorted(set(dezenas))
    except Exception:
        return []


def validar_dezenas_lotofacil(dezenas):
    """
    Valida dezenas da Lotofácil:
    - entre 1 e 25
    - quantidade mínima esperada
    """
    if not dezenas:
        return False, "Nenhuma dezena informada."

    if any(n < 1 or n > 25 for n in dezenas):
        return False, "As dezenas devem estar entre 1 e 25."

    return True, dezenas


def formatar_jogo(jogo):
    """
    Retorna o jogo formatado para exibição/cópia
    """
    return " ".join(f"{n:02d}" for n in sorted(jogo))
