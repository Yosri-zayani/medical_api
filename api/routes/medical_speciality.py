from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
router = APIRouter(prefix="/medicalspecialties", tags=["medicalspecialties"])

get_db = database.get_db

@router.post("/", response_model=schemas.MedicalSpecialty, status_code=status.HTTP_201_CREATED)
def create_medicalspeciality(medicalspeciality: schemas.MedicalSpecialtyCreate, db: Session = Depends(get_db)):
    new_medicalspeciality = models.MedicalSpecialty(**medicalspeciality.dict())
    db.add(new_medicalspeciality)
    db.commit()
    db.refresh(new_medicalspeciality)
    return new_medicalspeciality


@router.get("/{medicalspeciality_id}", response_model=schemas.MedicalSpecialty)
def get_medicalspeciality(medicalspeciality_id: int, db: Session = Depends(get_db)):
    medicalspeciality = db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.id == medicalspeciality_id).first()
    if not medicalspeciality:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalSpecialty not found")
    return medicalspeciality



@router.get("/", response_model=list[schemas.MedicalSpecialty])
def get_all_medicalspecialitys(db: Session = Depends(get_db)):
    return db.query(models.MedicalSpecialty).all()
 
 
@router.put("/{medicalspeciality_id}", response_model=schemas.MedicalSpecialty)
def update_medicalspeciality(medicalspeciality_id: int, updated_medicalspeciality: schemas.DoctorCreate, db: Session = Depends(get_db)):
    medicalspeciality = db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.id == medicalspeciality_id).first()
    if not medicalspeciality:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalSpecialty not found")

    for field, value in updated_medicalspeciality.dict(exclude_unset=True).items(): # Use exclude_unset=True to only update provided fields.
        setattr(medicalspeciality, field, value)

    db.commit()
    db.refresh(medicalspeciality)
    return medicalspeciality




@router.delete("/{medicalspeciality_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicalspeciality(medicalspeciality_id: int, db: Session = Depends(get_db)):
    medicalspeciality = db.query(models.MedicalSpecialty).filter(models.MedicalSpecialty.id == medicalspeciality_id).first()
    if not medicalspeciality:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MedicalSpecialty not found")
    
    db.delete(medicalspeciality)
    db.commit()
    return  # Return 204 No Content

    

