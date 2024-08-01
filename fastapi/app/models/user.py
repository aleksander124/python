from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'uzytkownicy'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, unique=True, index=True)
    pass = Column(String)
    email = Column(String)