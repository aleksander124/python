from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models.user import Base

DATABASE_URL = "postgresql://user:password@localhost/logowanie"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()