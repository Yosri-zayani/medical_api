# app/services/research_papers.py
from sqlalchemy.orm import Session
from .. import schemas, models
from fastapi import HTTPException, status

def get_all(db: Session):
    return db.query(models.ResearchPaper).all()

def create(request: schemas.ResearchPaperCreate, db: Session):
    new_research_papers = models.ResearchPaper(**request.dict())
    db.add(new_research_papers)
    db.commit()
    db.refresh(new_research_papers)
    return new_research_papers

def show(id: int, db: Session):
    research_papers = db.query(models.ResearchPaper).filter(models.ResearchPaper.id == id).first() #Corrected model
    if not research_papers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ResearchPaper with the id {id} is not available")
    return research_papers

def update(id: int, request: schemas.ResearchPaperCreate, db: Session):  # Use ResearchPaperCreate or a dedicated ResearchPaperUpdate schema
    research_papers = db.query(models.ResearchPaper).filter(models.ResearchPaper.id == id) #Corrected model
    if not research_papers.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ResearchPaper with id {id} not found")

    research_papers.update(request.dict())  # Make sure 'id' is not in request.dict() if using ResearchPaperCreate
    db.commit()
    return 'updated'  # Or return the updated research_papers object

def destroy(id: int, db: Session):
    research_papers = db.query(models.ResearchPaper).filter(models.ResearchPaper.id == id) #Corrected model
    if not research_papers.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ResearchPaper with id {id} not found")
    research_papers.delete(synchronize_session=False)
    db.commit()
    return 'done'