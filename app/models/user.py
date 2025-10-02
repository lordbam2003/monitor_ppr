"""
Modelo de usuario para la lógica de negocio
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import UserRoleEnum


class UsuarioBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    role: UserRoleEnum


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRoleEnum] = None
    password: Optional[str] = None


class Usuario(UsuarioBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True