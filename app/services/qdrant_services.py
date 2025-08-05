# app/services/qdrant_service.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Distance, VectorParams
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

qdrant = QdrantClient(
    url=os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY")
)

NOMBRE_COLECCION = os.getenv("COLLECTION_NAME", "sops_docs")

def crear_coleccion_si_no_existe(dim: int = 1536):
    """
    Crea la colección en Qdrant si aún no existe.
    """
    colecciones = qdrant.get_collections().collections
    nombres = [c.name for c in colecciones]

    if NOMBRE_COLECCION not in nombres:
        qdrant.create_collection(
            collection_name=NOMBRE_COLECCION,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )

def insertar_embeddings(chunks: list[str], embeddings: list[list[float]]):
    """
    Inserta los embeddings con su texto original como metadatos.
    """
    puntos = []

    for i, (texto, vector) in enumerate(zip(chunks, embeddings)):
        punto = PointStruct(
            id=i,
            vector=vector,
            payload={"texto": texto}
        )
        puntos.append(punto)

    qdrant.upsert(
        collection_name=NOMBRE_COLECCION,
        points=puntos
    )

def buscar_fragmentos_similares(pregunta: str, top_k: int = 3) -> list[str]:
    """
    Genera el embedding de la pregunta y devuelve los fragmentos más relevantes desde Qdrant.
    """
    cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    respuesta = cliente.embeddings.create(
        input=pregunta,
        model="text-embedding-3-small"
    )
    vector = respuesta.data[0].embedding

    resultados = qdrant.search(
        collection_name=NOMBRE_COLECCION,
        query_vector=vector,
        limit=top_k
    )

    # Extraemos solo el texto del payload
    return [resultado.payload["texto"] for resultado in resultados]