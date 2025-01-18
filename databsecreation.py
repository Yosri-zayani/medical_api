from api.database import engine, Base
from api.models import Appointment , Patient , Doctor , MedicalDepartment, MedicalSpecialty ,MedicalService , ResearchPaper

# Create all tables in the database
Base.metadata.create_all(bind=engine)
