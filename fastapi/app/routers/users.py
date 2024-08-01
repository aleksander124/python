from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.users import create_user, get_user, get_users
from ..schemas.users import UserCreate, UserResponse
from ..dependencies import get_db

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = get_users(db=db, skip=skip, limit=limit)
    return users
