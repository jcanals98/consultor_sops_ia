from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag import obtener_respuesta_con_rag

router = APIRouter()

class PreguntaEntrada(BaseModel):
    pregunta: str

@router.post("/preguntar")
def preguntar(data: PreguntaEntrada):
    """
    Endpoint que recibe una pregunta, busca contexto y responde con GPT.
    """
    if not data.pregunta.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    respuesta = obtener_respuesta_con_rag(data.pregunta)
    return {"respuesta": respuesta}
