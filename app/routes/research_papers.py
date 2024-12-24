from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
from .. services import research_papers
router = APIRouter(prefix="/researchpaper", tags=["researchpaper"])

get_db = database.get_db

@router.post("/", response_model=schemas.ResearchPaper, status_code=status.HTTP_201_CREATED)
def create_researchpaper(researchpaper: schemas.ResearchPaperCreate, db: Session = Depends(get_db)):
    new_researchpaper = models.ResearchPaper(**researchpaper.dict())
    db.add(new_researchpaper)
    db.commit()
    db.refresh(new_researchpaper)
    return new_researchpaper


@router.get("/{researchpaper_id}", response_model=schemas.ResearchPaper)
def get_researchpaper(researchpaper_id: int, db: Session = Depends(get_db)):
    researchpaper = db.query(models.ResearchPaper).filter(models.ResearchPaper.id == researchpaper_id).first()
    if not researchpaper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ResearchPaper not found")
    return researchpaper



@router.get("/", response_model=list[schemas.ResearchPaper])
def get_all_researchpapers(db: Session = Depends(get_db)):
    researchpaper = db.query(models.ResearchPaper).all()
    return researchpaper



@router.put("/{researchpaper_id}", response_model=schemas.ResearchPaper)
def update_researchpaper(researchpaper_id: int, updated_researchpaper: schemas.ResearchPaperCreate, db: Session = Depends(get_db)):
    researchpaper = db.query(models.ResearchPaper).filter(models.ResearchPaper.id == researchpaper_id).first()
    if not researchpaper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ResearchPaper not found")

    for field, value in updated_researchpaper.dict(exclude_unset=True).items(): # Use exclude_unset=True to only update provided fields.
        setattr(researchpaper, field, value)

    db.commit()
    db.refresh(researchpaper)
    return researchpaper




@router.delete("/{researchpaper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_researchpaper(researchpaper_id: int, db: Session = Depends(get_db)):
    researchpaper = db.query(models.ResearchPaper).filter(models.ResearchPaper.id == researchpaper_id).first()
    if not researchpaper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ResearchPaper not found")
    
    db.delete(researchpaper)
    db.commit()
    return  # Return 204 No Content

    

