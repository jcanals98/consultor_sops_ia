import os
from dotenv import load_dotenv
from openai import OpenAI
from app.services.qdrant_services import buscar_fragmentos_similares

load_dotenv()
cliente_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def construir_prompt_rag(pregunta: str, fragmentos: list[str]) -> str:
    """
    Construye un prompt con el contexto recuperado y la pregunta del usuario.
    """
    contexto = "\n---\n".join(fragmentos)
    prompt = f"""
Eres un asistente experto en procedimientos internos de empresa. Responde únicamente basándote en el siguiente contexto:

{contexto}

Pregunta: {pregunta}
Respuesta:"""
    return prompt.strip()

def obtener_respuesta_con_rag(pregunta: str, k: int = 3) -> str:
    """
    Ejecuta una búsqueda semántica en Qdrant, construye el prompt y obtiene la respuesta con GPT.
    """
    fragmentos_similares = buscar_fragmentos_similares(pregunta, top_k=k)
    prompt = construir_prompt_rag(pregunta, fragmentos_similares)

    respuesta = cliente_openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return respuesta.choices[0].message.content.strip()
