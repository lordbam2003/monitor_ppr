"""
Utilidades de autenticación para Monitor PPR v2
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from app.database.session import get_db
from app.database.models import User as DBUser, Role as DBRole

# Cargar variables de entorno
load_dotenv()

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_para_desarrollo")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Esquema de seguridad OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña coincida con su hash
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash de la contraseña
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un token de acceso JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verifica un token JWT y devuelve los datos del usuario
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        if username is None or user_id is None or role is None:
            return None
        token_data = TokenData(username=username, user_id=user_id, role=role)
        return token_data
    except JWTError:
        return None


def get_current_user(token: str):
    """
    Obtiene el usuario actual desde el token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    return token_data


def get_current_active_user(current_user: TokenData = Depends(get_current_user)):
    """
    Verifica que el usuario actual esté activo
    """
    # Esta función se usaría si necesitamos verificar que el usuario esté activo
    # En este caso, la verificación ya se hace en el login
    return current_user


def get_current_active_user_db(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Obtiene el usuario actual activo desde la base de datos
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    
    user = db.query(DBUser).filter(DBUser.id == token_data.user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception
        
    return user


def get_current_user_role(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Obtiene el rol del usuario actual
    """
    user = get_current_active_user_db(db, token)
    role = db.query(DBRole).filter(DBRole.id == user.role_id).first()
    return role