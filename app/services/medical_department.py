# app/services/medicaldepartments.py
from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import HTTPException, status

def get_all(db: Session):
    return db.query(models.MedicalDepartment).all()

def create(request: schemas.MedicalDepartmentCreate, db: Session):
    new_medicaldepartment = models.MedicalDepartment(**request.dict())
    db.add(new_medicaldepartment)
    db.commit()
    db.refresh(new_medicaldepartment)
    return new_medicaldepartment

def show(id: int, db: Session):
    medicaldepartment = db.query(models.MedicalDepartment).filter(models.MedicalDepartment.id == id).first() #Corrected model
    if not medicaldepartment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MedicalDepartment with the id {id} is not available")
    return medicaldepartment

def update(id: int, request: schemas.MedicalDepartmentCreate, db: Session):  # Use MedicalDepartmentCreate or a dedicated MedicalDepartmentUpdate schema
    medicaldepartment = db.query(models.MedicalDepartment).filter(models.MedicalDepartment.id == id) #Corrected model
    if not medicaldepartment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MedicalDepartment with id {id} not found")

    medicaldepartment.update(request.dict())  # Make sure 'id' is not in request.dict() if using MedicalDepartmentCreate
    db.commit()
    return 'updated'  # Or return the updated medicaldepartment object

def destroy(id: int, db: Session):
    medicaldepartment = db.query(models.MedicalDepartment).filter(models.MedicalDepartment.id == id) #Corrected model
    if not medicaldepartment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"MedicalDepartment with id {id} not found")
    medicaldepartment.delete(synchronize_session=False)
    db.commit()
    return 'done'