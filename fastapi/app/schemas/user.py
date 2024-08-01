from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    user: str
    email: EmailStr

class UserCreate(UserBase):
    pass: str

class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True