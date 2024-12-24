# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
class AppointmentCreate(BaseModel):
    patient_id: int
    service_id: int
    appointment_time: datetime
    status: str = "scheduled"  # Default status
    notes: str = None  # Optional notes


class Appointment(AppointmentCreate):
    id: int

    class Config:
        orm_mode = True


class PatientCreate(BaseModel):
    name: str
    email: str = None  # Optional
    phone: str = None   # Optional
    date_of_birth: datetime = None # Optional

class Patient(PatientCreate):
    id: int

    class Config:
        orm_mode = True



class DoctorCreate(BaseModel):
    name: str
    specialty_id: int


class Doctor(DoctorCreate):
    id: int

    class Config:
        orm_mode = True



class MedicalSpecialtyCreate(BaseModel):
    name: str
    department_id: int


class MedicalSpecialty(MedicalSpecialtyCreate):
    id: int

    class Config:
        orm_mode = True


class MedicalDepartmentCreate(BaseModel):
    name: str


class MedicalDepartment(MedicalDepartmentCreate):
    id: int

    class Config:
        orm_mode = True


class MedicalServiceCreate(BaseModel):
    name: str
    description: str = None #optional
    specialty_id: int
    


class MedicalService(MedicalServiceCreate):
    id: int

    class Config:
        orm_mode = True

# Research Paper Schemas
class ResearchPaperCreate(BaseModel):
    title: str
    abstract: str
    authors: List[str]
    publication_date: datetime
    journal: Optional[str] = None
    doi: Optional[str] = None

class ResearchPaper(ResearchPaperCreate):
    id: int

    class Config:
        orm_mode = True