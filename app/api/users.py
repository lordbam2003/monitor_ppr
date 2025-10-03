"""
Endpoints de usuarios para Monitor PPR v2
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.user import Usuario, UsuarioCreate, UsuarioUpdate
from app.database.models import User as DBUser
from app.utils.auth import get_password_hash, get_current_active_user_db
from app.utils.logger import log_error, log_info

router = APIRouter()


@router.get("/", response_model=List[Usuario])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_active_user_db)):
    """
    Obtener lista de usuarios (requiere autenticación)
    """
    try:
        users = db.query(DBUser).offset(skip).limit(limit).all()
        log_info(f"Obtenidos {len(users)} usuarios")
        return users
    except Exception as e:
        log_error(e, "get_users")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{user_id}", response_model=Usuario)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener usuario por ID
    """
    try:
        user = db.query(DBUser).filter(DBUser.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, f"get_user - ID: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/", response_model=Usuario)
def create_user(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crear nuevo usuario
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
        
        # Convertir el enum a valor entero o string según la estructura de la base de datos
        role_mapping = {
            "admin": 1,
            "planificador": 2,
            "responsable_ppr": 3
        }
        
        role_id = role_mapping.get(usuario.role, 2)  # Por defecto planificador
        
        # Crear nuevo usuario
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
        
        log_info(f"Usuario creado: {db_user.username}")
        return db_user
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, "create_user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/{user_id}", response_model=Usuario)
def update_user(user_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    """
    Actualizar usuario existente
    """
    try:
        db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Actualizar campos
        update_data = usuario.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        
        log_info(f"Usuario actualizado: {db_user.username}")
        return db_user
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, f"update_user - ID: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Eliminar usuario
    """
    try:
        db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        db.delete(db_user)
        db.commit()
        
        log_info(f"Usuario eliminado: {db_user.username}")
        return {"message": "Usuario eliminado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, f"delete_user - ID: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )