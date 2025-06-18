# app/models/schemas.py

from pydantic import BaseModel
from typing import List, Optional

class MedicineSchema(BaseModel):
    name: str
    dosage: Optional[str]
    frequency: Optional[str]
    duration: Optional[str]
    instructions: Optional[str]

class PatientSchema(BaseModel):
    name: Optional[str]
    age: Optional[str]
    gender: Optional[str]

class PrescriptionResponse(BaseModel):
    patient: Optional[PatientSchema]
    doctor_name: Optional[str]
    date_issued: Optional[str]
    medicines: List[MedicineSchema]
    notes: Optional[str]

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
