from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    virtual_machines = relationship("VirtualMachine", back_populates="owner")


class VirtualMachine(Base):
    __tablename__ = "virtual_machines"

    vm_name = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    memory_gb = Column(Integer)
    cpu_cores = Column(Integer)
    os_type = Column(String)

    owner = relationship("User", back_populates="virtual_machines")
