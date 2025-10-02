"""
Modelo de permisos para la lógica de negocio
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PermisoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    recurso: str
    accion: str


class PermisoCreate(PermisoBase):
    pass


class PermisoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    recurso: Optional[str] = None
    accion: Optional[str] = None


class Permiso(PermisoBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True