def dividir_en_chunks(texto: str, max_palabras: int = 200) -> list[str]:
    """
    Divide un texto largo en fragmentos (chunks) de máximo 'max_palabras'.
    """
    palabras = texto.split()
    chunks = []

    for i in range(0, len(palabras), max_palabras):
        fragmento = " ".join(palabras[i:i + max_palabras])
        chunks.append(fragmento)

    return chunks
