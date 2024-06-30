from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get environment variables
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    virtual_machines = relationship("VirtualMachine", back_populates="owner")


class VirtualMachine(Base):
    __tablename__ = "virtual_machines"

    vm_name = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    memory_gb = Column(Integer)
    cpu_cores = Column(Integer)
    os_type = Column(String)

    owner = relationship("User", back_populates="virtual_machines")


Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI(openapi_prefix="/api")

# Pydantic models
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    user_id: int

    class Config:
        orm_mode = True


class VMBase(BaseModel):
    vm_name: str
    user_id: int
    memory_gb: int = None
    cpu_cores: int = None
    os_type: str = None


class VMCreate(VMBase):
    pass


class VMUpdate(VMBase):
    pass


class VMOut(VMBase):
    class Config:
        orm_mode = True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


@app.post("/virtualmachines/", response_model=VMOut)
def create_vm(vm: VMCreate, db: Session = Depends(get_db)):
    db_vm = VirtualMachine(**vm.dict())
    db.add(db_vm)
    db.commit()
    db.refresh(db_vm)
    return db_vm


@app.get("/virtualmachines/{vm_name}", response_model=VMOut)
def read_vm(vm_name: str, db: Session = Depends(get_db)):
    db_vm = db.query(VirtualMachine).filter(VirtualMachine.vm_name == vm_name).first()
    if db_vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    return db_vm


@app.put("/virtualmachines/{vm_name}", response_model=VMOut)
def update_vm(vm_name: str, vm: VMUpdate, db: Session = Depends(get_db)):
    db_vm = db.query(VirtualMachine).filter(VirtualMachine.vm_name == vm_name).first()
    if db_vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    for var, value in vars(vm).items():
        setattr(db_vm, var, value) if value is not None else None
    db.commit()
    db.refresh(db_vm)
    return db_vm


@app.delete("/virtualmachines/{vm_name}")
def delete_vm(vm_name: str, db: Session = Depends(get_db)):
    db_vm = db.query(VirtualMachine).filter(VirtualMachine.vm_name == vm_name).first()
    if db_vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    db.delete(db_vm)
    db.commit()
    return {"message": "VM deleted successfully"}
