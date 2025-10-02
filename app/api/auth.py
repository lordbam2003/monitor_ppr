"""
Endpoints de autenticación para Monitor PPR v2
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database.session import get_db
from app.utils.auth import verify_password, create_access_token, get_password_hash
from app.models.user import UsuarioCreate, Usuario
from app.database.models import User as DBUser, Role as DBRole
from app.utils.logger import log_error, log_info

router = APIRouter()


@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint para iniciar sesión
    """
    try:
        # Buscar usuario por username
        user = db.query(DBUser).filter(DBUser.username == form_data.username).first()
        
        if not user or not verify_password(form_data.password, user.hashed_password):
            log_info(f"Intento fallido de login para usuario: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nombre de usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario inactivo",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Obtener información del rol
        role = db.query(DBRole).filter(DBRole.id == user.role_id).first()
        
        # Crear token de acceso
        access_token_expires = timedelta(minutes=30)  # Ajustar según sea necesario
        access_token = create_access_token(
            data={
                "sub": user.username, 
                "user_id": user.id, 
                "role": role.name if role else "unknown"
            },
            expires_delta=access_token_expires
        )
        
        log_info(f"Login exitoso para usuario: {user.username}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "role": role.name if role else "unknown"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, "login")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/register", response_model=Usuario)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo usuario (solo para administradores)
    """
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(DBUser).filter(
            (DBUser.username == usuario.username) | (DBUser.email == usuario.email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario o email ya existe"
            )
        
        # Crear nuevo usuario
        # Convertir el enum a valor entero o string según la estructura de la base de datos
        # Asumiendo que los roles tienen IDs numéricos: 1=admin, 2=planificador, 3=responsable_ppr
        role_mapping = {
            "admin": 1,
            "planificador": 2,
            "responsable_ppr": 3
        }
        
        role_id = role_mapping.get(usuario.role, 2)  # Por defecto planificador
        
        db_user = DBUser(
            username=usuario.username,
            email=usuario.email,
            full_name=usuario.full_name,
            hashed_password=get_password_hash(usuario.password),
            is_active=usuario.is_active,
            role_id=role_id
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        log_info(f"Usuario registrado: {db_user.username}")
        
        return db_user
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, "register")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )