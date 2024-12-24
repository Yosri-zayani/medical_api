from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://HospitalAzizaothmana_owner:6jMXTR5voKNq@ep-noisy-star-a2g2z30s.eu-central-1.aws.neon.tech/HospitalAzizaothmana?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # For declaring models (see next step)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()