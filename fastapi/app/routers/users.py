from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.users import create_user, get_user, get_users
from ..schemas.users import UserCreate, UserResponse
from ..dependencies import get_db

router = APIRouter()


@router.post("/users/", response_model=UserResponse, tags=["Users"])
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    - **user**: User information to create a new user.
    """
    return create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.

    - **user_id**: The ID of the user to retrieve.
    """
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=list[UserResponse], tags=["Users"])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get a list of users.

    - **skip**: Number of users to skip.
    - **limit**: Maximum number of users to return.
    """
    users = get_users(db=db, skip=skip, limit=limit)
    return users
