from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List
import models
import crud
import schemas
from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi

app = FastAPI()

# Function to generate OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Virtual Machines API",
        version="1.0.0",
        description="This is a FastAPI application to manage virtual machines.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

router = APIRouter(prefix="/api")

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
@router.post("/vms/", response_model=schemas.VirtualMachine, status_code=status.HTTP_201_CREATED)
def create_virtual_machine(vm: schemas.VirtualMachineCreate, db: Session = Depends(get_db)):
    db_vm = models.VirtualMachine(**vm.dict())
    return crud.create_vm(db=db, vm=db_vm)

@router.get("/vms/{vm_id}", response_model=schemas.VirtualMachine)
def read_virtual_machine(vm_id: int, db: Session = Depends(get_db)):
    db_vm = crud.get_vm(db, vm_id=vm_id)
    if db_vm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VM not found")
    return db_vm

@router.get("/vms/", response_model=List[schemas.VirtualMachine])
def read_virtual_machines(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_vms(db, skip=skip, limit=limit)

@router.put("/vms/{vm_id}", response_model=schemas.VirtualMachine)
def update_virtual_machine(vm_id: int, vm: schemas.VirtualMachineCreate, db: Session = Depends(get_db)):
    db_vm = models.VirtualMachine(**vm.dict())
    updated_vm = crud.update_vm(db, vm_id=vm_id, updated_vm=db_vm)
    if updated_vm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VM not found")
    return updated_vm

@router.delete("/vms/{vm_id}", response_model=schemas.SuccessResponse)
def delete_virtual_machine(vm_id: int, db: Session = Depends(get_db)):
    db_vm = crud.delete_vm(db, vm_id=vm_id)
    if db_vm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="VM not found")
    return schemas.SuccessResponse(message="VM deleted successfully")

# Include router in the main app
app.include_router(router)

# Include custom OpenAPI schema generator
app.openapi = custom_openapi

# Add CORS middleware if necessary
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Run with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
