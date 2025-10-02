"""
Modelos de base de datos para Monitor PPR v2
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Role(BaseModel):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)  # admin, planificador, responsable_ppr
    description = Column(Text)

    # Relaciones
    users = relationship("User", back_populates="role")


class User(BaseModel):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    # Relaciones
    role = relationship("Role", back_populates="users")
    assigned_pprs = relationship("PPR", secondary="ppr_responsables", back_populates="responsables_ppr")


class PPR(BaseModel):
    __tablename__ = "pprs"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False)  # Código del PPR
    nombre = Column(String(255), nullable=False)  # Nombre del PPR
    descripcion = Column(Text)
    unidad_medida = Column(String(50))
    responsable_planificacion_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Usuario que planifica
    estado = Column(String(20), default="activo")  # activo, inactivo, suspendido
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    ano_ejecucion = Column(Integer, nullable=False)  # Año de ejecución del PPR
    
    # Relaciones
    responsable_planificacion = relationship("User", foreign_keys=[responsable_planificacion_id])
    responsables_ppr = relationship("User", secondary="ppr_responsables", back_populates="assigned_pprs")
    metas = relationship("PPRMeta", back_populates="ppr")
    avances = relationship("PPRAvance", back_populates="ppr")


# Tabla intermedia para la relación muchos a muchos entre PPR y Usuarios
ppr_responsables = Table(
    'ppr_responsables',
    Base.metadata,
    Column('ppr_id', Integer, ForeignKey('pprs.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class PPRMeta(BaseModel):
    __tablename__ = "ppr_metas"
    
    id = Column(Integer, primary_key=True, index=True)
    ppr_id = Column(Integer, ForeignKey("pprs.id"), nullable=False)
    ano_ejecucion = Column(Integer, nullable=False)  # Año al que pertenece esta meta
    descripcion = Column(Text)
    meta_programada_anual = Column(Float, nullable=False)  # Meta total anual programada
    ene_prog = Column(Float, default=0.0)  # Enero programado
    feb_prog = Column(Float, default=0.0)  # Febrero programado
    mar_prog = Column(Float, default=0.0)  # Marzo programado
    abr_prog = Column(Float, default=0.0)  # Abril programado
    may_prog = Column(Float, default=0.0)  # Mayo programado
    jun_prog = Column(Float, default=0.0)  # Junio programado
    jul_prog = Column(Float, default=0.0)  # Julio programado
    ago_prog = Column(Float, default=0.0)  # Agosto programado
    sep_prog = Column(Float, default=0.0)  # Septiembre programado
    oct_prog = Column(Float, default=0.0)  # Octubre programado
    nov_prog = Column(Float, default=0.0)  # Noviembre programado
    dic_prog = Column(Float, default=0.0)  # Diciembre programado
    
    # Relaciones
    ppr = relationship("PPR", back_populates="metas")


class PPRAvance(BaseModel):
    __tablename__ = "ppr_avances"
    
    id = Column(Integer, primary_key=True, index=True)
    ppr_id = Column(Integer, ForeignKey("pprs.id"), nullable=False)
    ano_ejecucion = Column(Integer, nullable=False)  # Año al que pertenece este avance
    mes = Column(String(10), nullable=False)  # ene, feb, mar, etc.
    valor_ejecutado = Column(Float, default=0.0)
    valor_programado = Column(Float, default=0.0)
    comentario = Column(Text)
    acumulado_anual = Column(Boolean, default=False)  # Si es avance acumulado anual
    
    # Relaciones
    ppr = relationship("PPR", back_populates="avances")


class CEPLAN(BaseModel):
    __tablename__ = "ceplans"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_sub_producto = Column(String(10), nullable=False)  # 7 dígitos con ceros iniciales
    subproducto = Column(String(255), nullable=False)
    ano_ejecucion = Column(Integer, nullable=False)  # Año al que pertenecen estos datos
    ene_eje = Column(Float, default=0.0)  # Enero ejecutado
    ene_prog = Column(Float, default=0.0)  # Enero programado
    feb_eje = Column(Float, default=0.0)  # Febrero ejecutado
    feb_prog = Column(Float, default=0.0)  # Febrero programado
    mar_eje = Column(Float, default=0.0)  # Marzo ejecutado
    mar_prog = Column(Float, default=0.0)  # Marzo programado
    abr_eje = Column(Float, default=0.0)  # Abril ejecutado
    abr_prog = Column(Float, default=0.0)  # Abril programado
    may_eje = Column(Float, default=0.0)  # Mayo ejecutado
    may_prog = Column(Float, default=0.0)  # Mayo programado
    jun_eje = Column(Float, default=0.0)  # Junio ejecutado
    jun_prog = Column(Float, default=0.0)  # Junio programado
    jul_eje = Column(Float, default=0.0)  # Julio ejecutado
    jul_prog = Column(Float, default=0.0)  # Julio programado
    ago_eje = Column(Float, default=0.0)  # Agosto ejecutado
    ago_prog = Column(Float, default=0.0)  # Agosto programado
    sep_eje = Column(Float, default=0.0)  # Septiembre ejecutado
    sep_prog = Column(Float, default=0.0)  # Septiembre programado
    oct_eje = Column(Float, default=0.0)  # Octubre ejecutado
    oct_prog = Column(Float, default=0.0)  # Octubre programado
    nov_eje = Column(Float, default=0.0)  # Noviembre ejecutado
    nov_prog = Column(Float, default=0.0)  # Noviembre programado
    dic_eje = Column(Float, default=0.0)  # Diciembre ejecutado
    dic_prog = Column(Float, default=0.0)  # Diciembre programado


class Notification(BaseModel):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    related_entity_type = Column(String(50))  # ppr, ceplan, etc.
    related_entity_id = Column(Integer)
    
    # Relaciones
    user = relationship("User")