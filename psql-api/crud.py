from sqlalchemy.orm import Session
import models

def get_vm(db: Session, vm_id: int):
    return db.query(models.VirtualMachine).filter(models.VirtualMachine.id == vm_id).first()

def get_vms(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.VirtualMachine).offset(skip).limit(limit).all()

def create_vm(db: Session, vm: models.VirtualMachine):
    db.add(vm)
    db.commit()
    db.refresh(vm)
    return vm

def update_vm(db: Session, vm_id: int, updated_vm: models.VirtualMachine):
    vm = db.query(models.VirtualMachine).filter(models.VirtualMachine.id == vm_id).first()
    if vm:
        vm.name = updated_vm.name
        vm.ip_address = updated_vm.ip_address
        vm.status = updated_vm.status
        db.commit()
        db.refresh(vm)
        return vm
    return None

def delete_vm(db: Session, vm_id: int):
    vm = db.query(models.VirtualMachine).filter(models.VirtualMachine.id == vm_id).first()
    if vm:
        db.delete(vm)
        db.commit()
        return vm
    return None
