from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.user == username).first()

def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.pass + "notreallyhashed"
    db_user = User(user=user.user, pass=fake_hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user