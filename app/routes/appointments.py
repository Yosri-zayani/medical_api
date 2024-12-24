      
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database

router = APIRouter(prefix="/appointments", tags=["appointments"])

get_db = database.get_db

@router.post("/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    new_appointment = models.Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment


@router.get("/{appointment_id}", response_model=schemas.Appointment)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment



@router.get("/", response_model=list[schemas.Appointment])
def get_all_appointments(db: Session = Depends(get_db)):
    appointments = db.query(models.Appointment).all()
    return appointments



@router.put("/{appointment_id}", response_model=schemas.Appointment)
def update_appointment(appointment_id: int, updated_appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

    for field, value in updated_appointment.dict(exclude_unset=True).items(): # Use exclude_unset=True to only update provided fields.
        setattr(appointment, field, value)

    db.commit()
    db.refresh(appointment)
    return appointment




@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    db.delete(appointment)
    db.commit()
    return  # Return 204 No Content

    

