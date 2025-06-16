# app/models/entities.py

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Patient:
    name: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None

@dataclass
class Medicine:
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    instructions: Optional[str] = None

@dataclass
class Prescription:
    patient: Patient
    doctor_name: Optional[str]
    date_issued: Optional[datetime]
    medicines: List[Medicine]
    notes: Optional[str]
