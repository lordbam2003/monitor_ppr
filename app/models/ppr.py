"""
Modelo de PPR para la lógica de negocio
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models import PPREnum


class PPRBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    unidad_medida: Optional[str] = None
    responsable_planificacion_id: int
    estado: Optional[PPREnum] = PPREnum.ACTIVO
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    ano_ejecucion: int  # Año de ejecución del PPR


class PPRCreate(PPRBase):
    responsable_ppr_ids: Optional[List[int]] = []  # IDs de los responsables del PPR


class PPRUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    unidad_medida: Optional[str] = None
    responsable_planificacion_id: Optional[int] = None
    estado: Optional[PPREnum] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    ano_ejecucion: Optional[int] = None
    responsable_ppr_ids: Optional[List[int]] = None  # IDs de los responsables del PPR


class PPR(PPRBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PPRMetaBase(BaseModel):
    ppr_id: int
    ano_ejecucion: int  # Año al que pertenece esta meta
    descripcion: Optional[str] = None
    meta_programada_anual: float  # Meta total anual programada
    ene_prog: Optional[float] = 0.0  # Enero programado
    feb_prog: Optional[float] = 0.0  # Febrero programado
    mar_prog: Optional[float] = 0.0  # Marzo programado
    abr_prog: Optional[float] = 0.0  # Abril programado
    may_prog: Optional[float] = 0.0  # Mayo programado
    jun_prog: Optional[float] = 0.0  # Junio programado
    jul_prog: Optional[float] = 0.0  # Julio programado
    ago_prog: Optional[float] = 0.0  # Agosto programado
    sep_prog: Optional[float] = 0.0  # Septiembre programado
    oct_prog: Optional[float] = 0.0  # Octubre programado
    nov_prog: Optional[float] = 0.0  # Noviembre programado
    dic_prog: Optional[float] = 0.0  # Diciembre programado


class PPRMetaCreate(PPRMetaBase):
    pass


class PPRMeta(PPRMetaBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PPRAvanceBase(BaseModel):
    ppr_id: int
    ano_ejecucion: int  # Año al que pertenece este avance
    mes: str  # Mes de ejecución (ene, feb, mar, etc.)
    valor_ejecutado: Optional[float] = 0.0
    valor_programado: Optional[float] = 0.0
    comentario: Optional[str] = None
    acumulado_anual: Optional[bool] = False  # Si es avance acumulado anual


class PPRAvanceCreate(PPRAvanceBase):
    pass


class PPRAvanceUpdate(BaseModel):
    valor_ejecutado: Optional[float] = None
    valor_programado: Optional[float] = None
    comentario: Optional[str] = None
    acumulado_anual: Optional[bool] = None


class PPRAvance(PPRAvanceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True