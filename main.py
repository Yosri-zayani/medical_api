# main.py
from fastapi import FastAPI
from app.routes import appointments , patients , doctors , medical_speciality , medical_department , medical_services , research_papers


app = FastAPI()

# Include all routers:
app.include_router(appointments.router)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(medical_speciality.router)
app.include_router(medical_department.router)
app.include_router(medical_services.router)
app.include_router(research_papers.router)




@app.get("/")
async def root():
    return {"message": "Welcome to the Hospital API!"}




# app/__init__.py
#  This file can remain empty in many simple FastAPI projects.  
# If you need application-level initialization, database setup handled with SQLAlchemy's create_all,
# or other shared resources, put them here.


# Example of what you might add to __init__.py for database creation (using SQLAlchemy):

# from .database import engine, Base  # Import from your database.py
# Base.metadata.create_all(bind=engine)  # Create database tables (if they don't exist).