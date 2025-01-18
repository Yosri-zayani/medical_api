from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
router = APIRouter(prefix="/doctors", tags=["doctors"])

get_db = database.get_db

@router.post("/", response_model=schemas.Doctor, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = models.Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


@router.get("/{doctor_id}", response_model=schemas.Doctor)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return doctor



@router.get("/", response_model=list[schemas.Doctor])
def get_all_doctors(db: Session = Depends(get_db)):
    doctors = db.query(models.Doctor).all()
    return doctors



@router.put("/{doctor_id}", response_model=schemas.Doctor)
def update_doctor(doctor_id: int, updated_doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    for field, value in updated_doctor.dict(exclude_unset=True).items(): # Use exclude_unset=True to only update provided fields.
        setattr(doctor, field, value)

    db.commit()
    db.refresh(doctor)
    return doctor




@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    db.delete(doctor)
    db.commit()
    return  # Return 204 No Content

    

