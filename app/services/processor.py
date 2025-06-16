# app/services/processor.py

from typing import Dict, Any
from app.services.ocr_service import OCRService
from app.services.parser import PrescriptionParser
from app.models.entities import Prescription

class PrescriptionProcessor:
    def __init__(self, lang: str = "eng"):
        self.ocr_service = OCRService(lang=lang)

    def process_file(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        extracted_text = self.ocr_service.extract_text(file_bytes, filename)
        parser = PrescriptionParser(extracted_text)
        prescription: Prescription = parser.parse()

        return {
            "patient": {
                "name": prescription.patient.name,
                "age": prescription.patient.age,
                "gender": prescription.patient.gender
            },
            "doctor_name": prescription.doctor_name,
            "date_issued": prescription.date_issued.strftime("%Y-%m-%d") if prescription.date_issued else None,
            "medicines": [
                {
                    "name": m.name,
                    "dosage": m.dosage,
                    "frequency": m.frequency,
                    "duration": m.duration,
                    "instructions": m.instructions
                } for m in prescription.medicines
            ],
            "notes": prescription.notes
        }


