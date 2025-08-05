from fastapi import FastAPI
from app.api import upload, query

app = FastAPI(
    title="Consultor SOPs IA",
    description="API que responde preguntas sobre documentos cargados utilizando RAG",
    version="0.1.0"
)

app.include_router(upload.router)
app.include_router(query.router)

@app.get("/")
def raiz():
    """
    Endpoint raíz para verificar que la API está funcionando correctamente.
    """
    return {"mensaje": "Consultor SOPs IA - API lista"}
