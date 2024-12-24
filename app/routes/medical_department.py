from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
from .. services import medical_department
router = APIRouter(prefix="/medicaldepartments", tags=["medicaldepartments"])

get_db = database.get_db

@router.post("/", response_model=schemas.MedicalDepartment, status_code=status.HTTP_201_CREATED)
def create_doctor(medicaldepartment: schemas.DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = models.MedicalDepartment(**medicaldepartment.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


@router.get("/{medicaldepartment_id}", response_model=schemas.MedicalDepartment)
def get_doctor(medicaldepartment_id: int, db: Session = Depends(get_db)):
    medicaldepartment = db.query(models.MedicalDepartment).filter(models.MedicalDepartment.id == medicaldepartment_id).first()
    if not medicaldepartment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalDepartment not found")
    return medicaldepartment



@router.get("/", response_model=list[schemas.MedicalDepartment])
def get_all_doctors():
    medical_department.get_all



@router.put("/{medicaldepartment_id}", response_model=schemas.MedicalDepartment)
def update_doctor(medicaldepartment_id: int, updated_doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    medicaldepartment = db.query(models.MedicalDepartment).filter(models.MedicalDepartment.id == medicaldepartment_id).first()
    if not medicaldepartment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalDepartment not found")

    for field, value in updated_doctor.dict(exclude_unset=True).items(): # Use exclude_unset=True to only update provided fields.
        setattr(medicaldepartment, field, value)

    db.commit()
    db.refresh(medicaldepartment)
    return medicaldepartment




@router.delete("/{medicaldepartment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(medicaldepartment_id: int, db: Session = Depends(get_db)):
    medicaldepartment = db.query(models.MedicalDepartment).filter(models.MedicalDepartment.id == medicaldepartment_id).first()
    if not medicaldepartment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalDepartment not found")
    
    db.delete(medicaldepartment)
    db.commit()
    return  # Return 204 No Content

    

