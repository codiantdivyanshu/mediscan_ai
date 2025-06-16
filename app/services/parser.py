# app/services/parser.py

import re
from datetime import datetime
from app.models.entities import Prescription, Patient, Medicine
from app.utils.helpers import clean_text, extract_first_match, extract_all_matches, normalize_date

class PrescriptionParser:
    def __init__(self, text: str):
        self.text = clean_text(text)

    def parse(self) -> Prescription:
        patient = Patient(
            name=extract_first_match(r"Name[:\-]?\s*([A-Za-z ]+)", self.text),
            age=extract_first_match(r"Age[:\-]?\s*(\d+)", self.text),
            gender=extract_first_match(r"Gender[:\-]?\s*(Male|Female|Other)", self.text)
        )

        doctor_name = extract_first_match(r"Dr\.?\s*([A-Za-z ]+)", self.text)
        date_str = extract_first_match(r"Date[:\-]?\s*([0-9/\-\.]+)", self.text)
        date_issued = datetime.strptime(normalize_date(date_str), "%Y-%m-%d") if date_str else None

        meds = []
        for match in re.findall(r"(\w[\w\s]+)\s+(\d+mg)?\s*(\d+x\d+)?\s*(\d+ days)?\s*(.*)?", self.text):
            name, dosage, freq, dur, instr = match
            if name.strip():
                meds.append(Medicine(
                    name=name.strip(),
                    dosage=dosage or None,
                    frequency=freq or None,
                    duration=dur or None,
                    instructions=instr.strip() or None
                ))

        return Prescription(
            patient=patient,
            doctor_name=doctor_name,
            date_issued=date_issued,
            medicines=meds,
            notes=None
        )

