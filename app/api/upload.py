# app/api/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.lector_pdf import extraer_texto_pdf

router = APIRouter()

@router.post("/subir_pdf")
async def subir_pdf(archivo: UploadFile = File(...)):
    """
    Recibe un archivo PDF, verifica su tipo y extrae su contenido.
    """
    if archivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos PDF.")

    contenido = await archivo.read()  # Leemos el archivo en bytes
    texto_extraido = extraer_texto_pdf(contenido)  # Procesamos el PDF con PyMuPDF

    # Mostramos solo los primeros 500 caracteres como ejemplo
    return {"mensaje": "Texto extraído correctamente", "fragmento": texto_extraido[:500]}
