# app/services/MedicalSpecialty.py
from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import HTTPException, status

def get_all(db: Session):
    return db.query(models.MedicalSpecialty).all()

def create(request: schemas.DoctorCreate, db: Session):
    new_doctor = models.MedicalSpecialty(**request.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

def show(id: int, db: Session):
    medicalspeciality = db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.id == id).first() #Corrected model
    if not medicalspeciality:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MedicalSpecialty with the id {id} is not available")
    return medicalspeciality

def update(id: int, request: schemas.DoctorCreate, db: Session):  # Use DoctorCreate or a dedicated DoctorUpdate schema
    medicalspeciality = db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.id == id) #Corrected model
    if not medicalspeciality.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MedicalSpecialty with id {id} not found")

    medicalspeciality.update(request.dict())  # Make sure 'id' is not in request.dict() if using DoctorCreate
    db.commit()
    return 'updated'  # Or return the updated medicalspeciality object

def destroy(id: int, db: Session):
    medicalspeciality = db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.id == id) #Corrected model
    if not medicalspeciality.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MedicalSpecialty with id {id} not found")
    medicalspeciality.delete(synchronize_session=False)
    db.commit()
    return 'done'