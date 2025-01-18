from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
router = APIRouter(prefix="/medicaldepartments", tags=["medicaldepartments"])

get_db = database.get_db

@router.post("/", response_model=schemas.MedicalDepartment, status_code=status.HTTP_201_CREATED)
def create_medical_department(medicaldepartment: schemas.MedicalDepartmentCreate, db: Session = Depends(get_db)):
    new_medical_department = models.MedicalDepartment(**medicaldepartment.dict())
    db.add(new_medical_department)
    db.commit()
    db.refresh(new_medical_department)
    return new_medical_department


@router.get("/{medicaldepartment_id}", response_model=schemas.MedicalDepartment)
def get_medical_department(medicaldepartment_id: int, db: Session = Depends(get_db)):
    medicaldepartment = db.query(models.MedicalDepartment).filter(models.MedicalDepartment.id == medicaldepartment_id).first()
    if not medicaldepartment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalDepartment not found")
    return medicaldepartment



@router.get("/", response_model=list[schemas.MedicalDepartment])
def get_all_medical_departments():
    return database.get_db().query(models.MedicalDepartment).all()


@router.put("/{medicaldepartment_id}", response_model=schemas.MedicalDepartment)
def update_medical_department(medicaldepartment_id: int, updated_medical_department: schemas.MedicalDepartmentCreate, db: Session = Depends(get_db)):
    medicaldepartment = db.query(models.MedicalDepartment).filter(models.MedicalDepartment.id == medicaldepartment_id).first()
    if not medicaldepartment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalDepartment not found")

    for field, value in updated_medical_department.dict(exclude_unset=True).items(): # Use exclude_unset=True to only update provided fields.
        setattr(medicaldepartment, field, value)

    db.commit()
    db.refresh(medicaldepartment)
    return medicaldepartment




@router.delete("/{medicaldepartment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medical_department(medicaldepartment_id: int, db: Session = Depends(get_db)):
    medicaldepartment = db.query(models.MedicalDepartment).filter(models.MedicalDepartment.id == medicaldepartment_id).first()
    if not medicaldepartment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalDepartment not found")
    
    db.delete(medicaldepartment)
    db.commit()
    return  # Return 204 No Content

    

