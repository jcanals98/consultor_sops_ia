# app/api/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.lector_pdf import extraer_texto_pdf
from app.services.procesador_texto import dividir_en_chunks
from app.services.generador_embeddings import generar_embeddings
from app.services.qdrant_services import crear_coleccion_si_no_existe, insertar_embeddings

router = APIRouter()

@router.post("/subir_pdf")
async def subir_pdf(archivo: UploadFile = File(...)):
    """
    Endpoint que procesa un PDF:
    1. Extrae el texto.
    2. Lo divide en fragmentos.
    3. Genera embeddings con OpenAI.
    4. Inserta los vectores en Qdrant.
    """
    if archivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF.")

    # Leer el archivo en memoria
    contenido = await archivo.read()

    # 1. Extraer texto del PDF
    texto = extraer_texto_pdf(contenido)
    if not texto.strip():
        raise HTTPException(status_code=400, detail="El PDF no contiene texto válido.")

    # 2. Dividir en chunks de máximo 200 palabras
    chunks = dividir_en_chunks(texto, max_palabras=200)
    if not chunks:
        raise HTTPException(status_code=400, detail="No se pudo dividir el texto.")

    # 3. Generar embeddings
    embeddings = generar_embeddings(chunks)
    if not embeddings or len(embeddings) != len(chunks):
        raise HTTPException(status_code=500, detail="Error generando embeddings.")

    # 4. Crear la colección (si no existe) e insertar en Qdrant
    crear_coleccion_si_no_existe()
    insertar_embeddings(chunks, embeddings)

    return {
        "mensaje": "PDF procesado correctamente",
        "chunks_insertados": len(chunks)
    }
