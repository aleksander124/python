from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Update this URL with your external database connection details
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/logowanie"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()