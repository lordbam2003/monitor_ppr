"""
Modelos de dominio para Monitor PPR v2
"""
from enum import Enum


class UserRoleEnum(str, Enum):
    """
    Enumeración de roles de usuario
    """
    ADMIN = "admin"
    PLANIFICADOR = "planificador"
    RESPONSABLE_PPR = "responsable_ppr"


class PPREnum(str, Enum):
    """
    Estados posibles para un PPR
    """
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"


class MesEnum(str, Enum):
    """
    Enumeración de meses
    """
    ENERO = "ene"
    FEBRERO = "feb"
    MARZO = "mar"
    ABRIL = "abr"
    MAYO = "may"
    JUNIO = "jun"
    JULIO = "jul"
    AGOSTO = "ago"
    SEPTIEMBRE = "sep"
    OCTUBRE = "oct"
    NOVIEMBRE = "nov"
    DICIEMBRE = "dic"


class NotificationEnum(str, Enum):
    """
    Tipos de notificaciones
    """
    META_MODIFICADA = "meta_modificada"
    AVANCE_ACTUALIZADO = "avance_actualizado"
    NUEVO_PPR_ASIGNADO = "nuevo_ppr_asignado"