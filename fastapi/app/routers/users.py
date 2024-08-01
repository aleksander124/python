from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import user as user_schema
from ..crud import user as user_crud
from ..dependencies import get_db

router = APIRouter()

@router.post("/users/", response_model=user_schema.UserInDB)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user.user)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_crud.create_user(db=db, user=user)