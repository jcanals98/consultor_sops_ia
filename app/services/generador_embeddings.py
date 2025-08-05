import openai
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generar_embeddings(chunks: List[str]) -> List[List[float]]:
    """
    Genera una lista de embeddings (vectores) para cada chunk de texto.
    """
    embeddings = []

    for chunk in chunks:
        respuesta = openai.embeddings.create(
            input=chunk,
            model="text-embedding-3-small"
        )
        vector = respuesta.data[0].embedding
        embeddings.append(vector)

    return embeddings
