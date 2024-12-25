# app/services/doctors.py
from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import HTTPException, status

def get_all(db: Session):
    return db.query(models.Doctor).all()

def create(request: schemas.DoctorCreate, db: Session):
    new_doctor = models.Doctor(**request.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

def show(id: int, db: Session):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Doctor with the id {id} is not available")
    return doctor

def update(id: int, request: schemas.DoctorCreate, db: Session):  # Use DoctorCreate or a dedicated DoctorUpdate schema
    doctor = db.query(models.Doctor).filter(models.Doctor.id == id)
    if not doctor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Doctor with id {id} not found")

    doctor.update(request.dict())  # Make sure 'id' is not in request.dict() if using DoctorCreate
    db.commit()
    return 'updated'  # Or return the updated doctor object

def destroy(id: int, db: Session):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == id)
    if not doctor.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Doctor with id {id} not found")
    doctor.delete(synchronize_session=False)
    db.commit()
    return 'done'