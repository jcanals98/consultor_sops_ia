# app/services/lector_pdf.py

import fitz  # PyMuPDF
from typing import Union

def extraer_texto_pdf(contenido_pdf: Union[bytes, bytearray]) -> str:
    """
    Abre un PDF desde bytes y extrae todo su texto concatenado.
    """
    texto = ""
    with fitz.open(stream=contenido_pdf, filetype="pdf") as documento:
        for pagina in documento:
            texto += pagina.get_text()  # Extraemos el texto de cada página
    return texto
