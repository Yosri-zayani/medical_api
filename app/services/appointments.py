# app/services/appointments.py

from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import HTTPException, status

def get_all(db: Session):
    """Get all appointments."""
    return db.query(models.Appointment).all()


def create(request: schemas.AppointmentCreate, db: Session):
    """Create a new appointment."""
    new_appointment = models.Appointment(**request.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


def show(id: int, db: Session):
    """Get a specific appointment by ID."""
    appointment = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Appointment with the id {id} is not available")
    return appointment


def update(id: int, request: schemas.AppointmentCreate, db: Session):
    """Update an existing appointment."""
    appointment = db.query(models.Appointment).filter(models.Appointment.id == id)
    if not appointment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Appointment with id {id} not found")

    appointment.update(request.dict())  # Update fields from the request
    db.commit()
    return 'updated'


def destroy(id: int, db: Session):
    """Delete an appointment."""
    appointment = db.query(models.Appointment).filter(models.Appointment.id == id)
    if not appointment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Appointment with id {id} not found")
    appointment.delete(synchronize_session=False)
    db.commit()
    return 'done'