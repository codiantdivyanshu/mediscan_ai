from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from .database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    patient_age = Column(String)
    patient_gender = Column(String)
    doctor_name = Column(String)
    date_issued = Column(DateTime, default=datetime.utcnow)
    medicines = Column(JSON)
    notes = Column(String)
