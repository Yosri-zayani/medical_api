from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
from ..utils import hash_password
router = APIRouter(prefix="/patients", tags=["patients"])
get_db = database.get_db

@router.get("/", response_model=list[str])
def get_all_patients(db: Session = Depends(get_db)):
    patient_names = [patient.name for patient in db.query(models.Patient).all()] # Extract only names
    return patient_names

@router.post("/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(patient.password)
    new_patient = models.Patient(password=hashed_password, **patient.dict(exclude={"password"})) # <-- Key change
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient  #The error was here.

@router.get("/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(patient_id: int, updated_patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    for field, value in updated_patient.dict(exclude_unset=True).items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    db.delete(patient)
    db.commit()
    return