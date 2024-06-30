from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI
from database import SessionLocal
from schemas import UserCreate, UserUpdate, UserOut, VMCreate, VMUpdate, VMOut
from models import User, VirtualMachine

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    db_users = db.query(User).all()
    if not db_users:
        raise HTTPException(status_code=404, detail="Users not found")
    return db_users

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/virtualmachines/", response_model=VMOut)
def create_vm(vm: VMCreate, db: Session = Depends(get_db)):
    db_vm = VirtualMachine(**vm.dict())
    db.add(db_vm)
    db.commit()
    db.refresh(db_vm)
    return db_vm

@router.get("/virtualmachines/{vm_name}", response_model=VMOut)
def read_vm(vm_name: str, db: Session = Depends(get_db)):
    db_vm = db.query(VirtualMachine).filter(VirtualMachine.vm_name == vm_name).first()
    if db_vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    return db_vm

@router.get("/virtualmachines/", response_model=List[VMOut])
def read_vms(db: Session = Depends(get_db)):
    db_vms = db.query(VirtualMachine).all()
    if not db_vms:
        raise HTTPException(status_code=404, detail="VMs not found")
    return db_vms

@router.put("/virtualmachines/{vm_name}", response_model=VMOut)
def update_vm(vm_name: str, vm: VMUpdate, db: Session = Depends(get_db)):
    db_vm = db.query(VirtualMachine).filter(VirtualMachine.vm_name == vm_name).first()
    if db_vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    for var, value in vars(vm).items():
        setattr(db_vm, var, value) if value is not None else None
    db.commit()
    db.refresh(db_vm)
    return db_vm

@router.delete("/virtualmachines/{vm_name}")
def delete_vm(vm_name: str, db: Session = Depends(get_db)):
    db_vm = db.query(VirtualMachine).filter(VirtualMachine.vm_name == vm_name).first()
    if db_vm is None:
        raise HTTPException(status_code=404, detail="VM not found")
    db.delete(db_vm)
    db.commit()
    return {"message": "VM deleted successfully"}
