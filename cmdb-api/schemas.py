from pydantic import BaseModel

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
