from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
router = APIRouter(prefix="/medicalservices", tags=["medicalservices"])

get_db = database.get_db

@router.post("/", response_model=schemas.MedicalService, status_code=status.HTTP_201_CREATED)
def create_MedicalService(medicalservice: schemas.MedicalServiceCreate, db: Session = Depends(get_db)):
    new_MedicalService = models.MedicalService(**medicalservice.dict())
    db.add(new_MedicalService)
    db.commit()
    db.refresh(new_MedicalService)
    return new_MedicalService


@router.get("/{MedicalService_id}", response_model=schemas.MedicalService)
def get_MedicalService(MedicalService_id: int, db: Session = Depends(get_db)):
    medicalservice = db.query(models.MedicalService).filter(models.MedicalService.id == MedicalService_id).first()
    if not medicalservice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalService not found")
    return medicalservice



@router.get("/", response_model=list[schemas.MedicalService])
def get_all_MedicalServices(db: Session = Depends(get_db)):
    medicalservices = db.query(models.MedicalService).all()
    return medicalservices



@router.put("/{MedicalService_id}", response_model=schemas.MedicalService)
def update_MedicalService(MedicalService_id: int, updated_MedicalService: schemas.MedicalServiceCreate, db: Session = Depends(get_db)):
    medicalservice = db.query(models.MedicalService).filter(models.MedicalService.id == MedicalService_id).first()
    if not medicalservice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalService not found")

    for field, value in updated_MedicalService.dict(exclude_unset=True).items(): # Use exclude_unset=True to only update provided fields.
        setattr(medicalservice, field, value)

    db.commit()
    db.refresh(medicalservice)
    return medicalservice




@router.delete("/{MedicalService_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_MedicalService(MedicalService_id: int, db: Session = Depends(get_db)):
    medicalservice = db.query(models.MedicalService).filter(models.MedicalService.id == MedicalService_id).first()
    if not medicalservice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalService not found")
    
    db.delete(medicalservice)
    db.commit()
    return  # Return 204 No Content

    

