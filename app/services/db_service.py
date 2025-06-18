from sqlalchemy.ext.asyncio import AsyncSession
from app.models.prescription import Prescription

async def save_prescription(data: dict, db: AsyncSession):
    prescription = Prescription(
        patient_name=data["patient"]["name"],
        patient_age=data["patient"]["age"],
        patient_gender=data["patient"]["gender"],
        doctor_name=data["doctor_name"],
        date_issued=data["date_issued"],
        medicines=data["medicines"],
        notes=data.get("notes", "")
    )
    db.add(prescription)
    await db.commit()
    await db.refresh(prescription)
    return prescription
