"""
Modelos de CEPLAN para Monitor PPR v2
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CEPLANBase(BaseModel):
    codigo_sub_producto: str
    subproducto: str
    ano_ejecucion: int  # Año al que pertenecen estos datos
    ene_eje: Optional[float] = 0.0  # Enero ejecutado
    ene_prog: Optional[float] = 0.0  # Enero programado
    feb_eje: Optional[float] = 0.0  # Febrero ejecutado
    feb_prog: Optional[float] = 0.0  # Febrero programado
    mar_eje: Optional[float] = 0.0  # Marzo ejecutado
    mar_prog: Optional[float] = 0.0  # Marzo programado
    abr_eje: Optional[float] = 0.0  # Abril ejecutado
    abr_prog: Optional[float] = 0.0  # Abril programado
    may_eje: Optional[float] = 0.0  # Mayo ejecutado
    may_prog: Optional[float] = 0.0  # Mayo programado
    jun_eje: Optional[float] = 0.0  # Junio ejecutado
    jun_prog: Optional[float] = 0.0  # Junio programado
    jul_eje: Optional[float] = 0.0  # Julio ejecutado
    jul_prog: Optional[float] = 0.0  # Julio programado
    ago_eje: Optional[float] = 0.0  # Agosto ejecutado
    ago_prog: Optional[float] = 0.0  # Agosto programado
    sep_eje: Optional[float] = 0.0  # Septiembre ejecutado
    sep_prog: Optional[float] = 0.0  # Septiembre programado
    oct_eje: Optional[float] = 0.0  # Octubre ejecutado
    oct_prog: Optional[float] = 0.0  # Octubre programado
    nov_eje: Optional[float] = 0.0  # Noviembre ejecutado
    nov_prog: Optional[float] = 0.0  # Noviembre programado
    dic_eje: Optional[float] = 0.0  # Diciembre ejecutado
    dic_prog: Optional[float] = 0.0  # Diciembre programado


class CEPLANCreate(CEPLANBase):
    pass


class CEPLANUpdate(BaseModel):
    subproducto: Optional[str] = None
    ano_ejecucion: Optional[int] = None
    ene_eje: Optional[float] = None
    ene_prog: Optional[float] = None
    feb_eje: Optional[float] = None
    feb_prog: Optional[float] = None
    mar_eje: Optional[float] = None
    mar_prog: Optional[float] = None
    abr_eje: Optional[float] = None
    abr_prog: Optional[float] = None
    may_eje: Optional[float] = None
    may_prog: Optional[float] = None
    jun_eje: Optional[float] = None
    jun_prog: Optional[float] = None
    jul_eje: Optional[float] = None
    jul_prog: Optional[float] = None
    ago_eje: Optional[float] = None
    ago_prog: Optional[float] = None
    sep_eje: Optional[float] = None
    sep_prog: Optional[float] = None
    oct_eje: Optional[float] = None
    oct_prog: Optional[float] = None
    nov_eje: Optional[float] = None
    nov_prog: Optional[float] = None
    dic_eje: Optional[float] = None
    dic_prog: Optional[float] = None


class CEPLAN(CEPLANBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True