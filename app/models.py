from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    date_of_birth = Column(DateTime)  
    address = Column(String)
    medical_history = Column(Text) # For storing medical history information

    appointments = relationship("Appointment", back_populates="patient")


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialty_id = Column(Integer, ForeignKey("medical_specialties.id"))
    email = Column(String, unique=True, index=True)  
    phone = Column(String)

    specialty = relationship("MedicalSpecialty", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor")


class MedicalDepartment(Base):
    __tablename__ = "medical_departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    specialties = relationship("MedicalSpecialty", back_populates="department")



class MedicalSpecialty(Base):
    __tablename__ = "medical_specialties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    department_id = Column(Integer, ForeignKey("medical_departments.id"))

    department = relationship("MedicalDepartment", back_populates="specialties")
    doctors = relationship("Doctor", back_populates="specialty")
    services = relationship("MedicalService", back_populates="specialty")


class MedicalService(Base):
    __tablename__ = "medical_services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    specialty_id = Column(Integer, ForeignKey("medical_specialties.id"))
    price = Column(Integer) # Adding a price field


    specialty = relationship("MedicalSpecialty", back_populates="services")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    service_id = Column(Integer, ForeignKey("medical_services.id"))
    appointment_time = Column(DateTime)
    status = Column(Enum("scheduled", "completed", "cancelled", name="appointment_status"), default="scheduled")
    notes = Column(Text)


    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    service = relationship("MedicalService", backref="appointments")



class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    authors = Column(String)
    publication_date = Column(DateTime)
    abstract = Column(Text)
