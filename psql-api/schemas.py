from pydantic import BaseModel

class VirtualMachineBase(BaseModel):
    name: str
    ip_address: str
    status: str

    class Config:
        from_attributes = True  # Use from_attributes instead of orm_mode

class VirtualMachineCreate(VirtualMachineBase):
    pass

class VirtualMachine(VirtualMachineBase):
    id: int

    class Config:
        from_attributes = True  # Use from_attributes instead of orm_mode

class SuccessResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str
