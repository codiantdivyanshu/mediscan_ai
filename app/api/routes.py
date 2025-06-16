# app/api/routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.processor import PrescriptionProcessor

api_router = APIRouter()

@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        processor = PrescriptionProcessor()
        result = processor.process_file(content, file.filename)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
