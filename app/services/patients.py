# app/services/patients.py
from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import HTTPException, status

def get_all(db: Session):
    return db.query(models.Patient).all()

def create(request: schemas.PatientCreate, db: Session):
    new_patient = models.Patient(**request.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

def show(id: int, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first() #Corrected model
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with the id {id} is not available")
    return patient

def update(id: int, request: schemas.PatientCreate, db: Session):  # Use PatientCreate or a dedicated PatientUpdate schema
    patient = db.query(models.Patient).filter(models.Patient.id == id) #Corrected model
    if not patient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with id {id} not found")

    patient.update(request.dict())  # Make sure 'id' is not in request.dict() if using PatientCreate
    db.commit()
    return 'updated'  # Or return the updated patient object

def destroy(id: int, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.id == id) #Corrected model
    if not patient.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with id {id} not found")
    patient.delete(synchronize_session=False)
    db.commit()
    return 'done'