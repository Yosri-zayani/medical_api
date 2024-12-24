# app/services/MedicalServices.py

from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import HTTPException, status

def get_all(db: Session):
    """Get all MedicalServices."""
    return db.query(models.MedicalService).all()


def create(request: schemas.MedicalServiceCreate, db: Session):
    """Create a new medicalservice."""
    new_MedicalService = models.MedicalService(**request.dict())
    db.add(new_MedicalService)
    db.commit()
    db.refresh(new_MedicalService)
    return new_MedicalService


def show(id: int, db: Session):
    """Get a specific medicalservice by ID."""
    medicalservice = db.query(models.MedicalService).filter(models.MedicalService.id == id).first()
    if not medicalservice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MedicalService with the id {id} is not available")
    return medicalservice


def update(id: int, request: schemas.MedicalServiceCreate, db: Session):
    """Update an existing medicalservice."""
    medicalservice = db.query(models.MedicalService).filter(models.MedicalService.id == id)
    if not medicalservice.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MedicalService with id {id} not found")

    medicalservice.update(request.dict())  # Update fields from the request
    db.commit()
    return 'updated'


def destroy(id: int, db: Session):
    """Delete an medicalservice."""
    medicalservice = db.query(models.MedicalService).filter(models.MedicalService.id == id)
    if not medicalservice.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MedicalService with id {id} not found")
    medicalservice.delete(synchronize_session=False)
    db.commit()
    return 'done'