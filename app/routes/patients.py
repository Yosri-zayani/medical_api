from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
from .. services import patients
router = APIRouter(prefix="/patients", tags=["patients"])

get_db = database.get_db

@router.post("/", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    new_patient = models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@router.get("/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient



@router.get("/", response_model=list[schemas.Patient])
def get_all_patients(db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return patients



@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(patient_id: int, updated_patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    for field, value in updated_patient.dict(exclude_unset=True).items(): # Use exclude_unset=True to only update provided fields.
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
    return  # Return 204 No Content

    

