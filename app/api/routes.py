from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Body, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import tempfile

from app.services.ocr_service import OCRService
from app.services.parser import PrescriptionParser
from app.services.processor import PrescriptionProcessor
from app.services.db_service import save_prescription
from app.services.ai_service import ask_groq
from app.services.auth_service import decode_token  

from app.utils.db_utils import get_db
from fpdf import FPDF

api_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return username

@api_router.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    return {"message": f"Hello {user}, you're authenticated!"}

@api_router.get("/health")
def health_check():
    return {"status": "OK", "message": "MediScan AI is alive"}

@api_router.get("/routes")
def list_routes():
    return [
        "/upload", "/extract-text", "/parse-text", "/convert-text-to-pdf",
        "/sample-prescription", "/save-prescription", "/ask",
        "/protected", "/health", "/routes"
    ]


@api_router.get("/sample-prescription")
def sample_prescription():
    return {
        "patient": {"name": "John Doe", "age": "35", "gender": "Male"},
        "doctor_name": "Dr. A. Kumar",
        "date_issued": "2024-12-01",
        "medicines": [
            {
                "name": "Paracetamol", "dosage": "500mg",
                "frequency": "2x1", "duration": "5 days",
                "instructions": "After meals"
            },
            {
                "name": "Amoxicillin", "dosage": "250mg",
                "frequency": "3x1", "duration": "7 days",
                "instructions": "Before meals"
            }
        ],
        "notes": "Stay hydrated and get rest"
    }


@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        result = PrescriptionProcessor().process_file(content, file.filename)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = OCRService().extract_text(content, file.filename)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TextInput(BaseModel):
    text: str

@api_router.post("/parse-text")
def parse_text(input: TextInput):
    try:
        parser = PrescriptionParser(input.text)
        parsed = parser.parse()
        return {
            "patient": {
                "name": parsed.patient.name,
                "age": parsed.patient.age,
                "gender": parsed.patient.gender
            },
            "doctor_name": parsed.doctor_name,
            "date_issued": parsed.date_issued.strftime("%Y-%m-%d") if parsed.date_issued else None,
            "medicines": [
                {
                    "name": m.name,
                    "dosage": m.dosage,
                    "frequency": m.frequency,
                    "duration": m.duration,
                    "instructions": m.instructions
                } for m in parsed.medicines
            ],
            "notes": parsed.notes
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class MedicineItem(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None

class PrescriptionPDFInput(BaseModel):
    patient: Optional[dict]
    doctor_name: Optional[str]
    date_issued: Optional[str]
    medicines: List[MedicineItem]
    notes: Optional[str]

@api_router.post("/convert-text-to-pdf")
def convert_to_pdf(data: PrescriptionPDFInput):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        if data.doctor_name:
            pdf.cell(200, 10, txt=f"Doctor: {data.doctor_name}", ln=True)
        if data.date_issued:
            pdf.cell(200, 10, txt=f"Date: {data.date_issued}", ln=True)

        if data.patient:
            pdf.cell(200, 10, txt=f"Patient: {data.patient.get('name')}, Age: {data.patient.get('age')}, Gender: {data.patient.get('gender')}", ln=True)

        pdf.cell(200, 10, txt="Medicines:", ln=True)
        for m in data.medicines:
            pdf.cell(200, 10, txt=f"- {m.name} ({m.dosage or ''}) - {m.frequency or ''} for {m.duration or ''} | {m.instructions or ''}", ln=True)

        if data.notes:
            pdf.cell(200, 10, txt=f"Notes: {data.notes}", ln=True)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_file.name)

        return FileResponse(temp_file.name, media_type='application/pdf', filename="prescription.pdf")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/save-prescription")
async def save_prescription_api(
    data: PrescriptionPDFInput,
    db: AsyncSession = Depends(get_db)
):
    try:
        prescription = await save_prescription(data.dict(), db)
        return {"status": "saved", "id": prescription.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/ask")
def ask_question(question: str = Body(..., embed=True)):
    try:
        result = ask_groq(question)
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
