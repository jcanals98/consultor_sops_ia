from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

from openai import OpenAI
import os
from dotenv import load_dotenv

# 🔐 Cargar variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔗 Conexión a Qdrant
qdrant = QdrantClient(
    url=os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY")
)

coleccion = os.getenv("COLLECTION_NAME", "sops_docs")

# 🧩 Fragmento de texto simulado
texto = "Este es un documento de prueba que contiene información útil sobre procedimientos internos de la empresa. El proceso de alta de clientes nuevos incluye verificación de datos, aceptación de condiciones y asignación de un gestor de cuenta."

# 1. Dividir en chunks (a mà per la prova)
chunks = texto.split(". ")

# 2. Generar embeddings
embeddings = []
for chunk in chunks:
    respuesta = client.embeddings.create(
        input=chunk,
        model="text-embedding-3-small"
    )
    vector = respuesta.data[0].embedding
    embeddings.append(vector)

# 3. Crear colección si no existe
if coleccion not in [c.name for c in qdrant.get_collections().collections]:
    qdrant.create_collection(
        collection_name=coleccion,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )
    print("✅ Colección creada")

# 4. Insertar a Qdrant
puntos = []
for i, (texto, vector) in enumerate(zip(chunks, embeddings)):
    punto = PointStruct(id=i, vector=vector, payload={"texto": texto})
    puntos.append(punto)

qdrant.upsert(collection_name=coleccion, points=puntos)
print(f"✅ {len(puntos)} puntos insertados correctamente.")
