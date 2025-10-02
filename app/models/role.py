"""
Modelo de rol para la lógica de negocio
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RolBase(BaseModel):
    name: str
    description: Optional[str] = None


class RolCreate(RolBase):
    pass


class RolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Rol(RolBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True