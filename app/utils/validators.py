"""
Validadores para Monitor PPR v2
"""
from typing import Any
import re


def validate_email(email: str) -> bool:
    """
    Valida si un email tiene formato correcto
    
    Args:
        email: Email a validar
    
    Returns:
        bool: True si el email es válido, False en caso contrario
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_codigo_ppr(codigo: str) -> bool:
    """
    Valida si un código de PPR tiene el formato correcto
    
    Args:
        codigo: Código de PPR a validar
    
    Returns:
        bool: True si el código es válido, False en caso contrario
    """
    # Puede ajustarse según el formato real de los códigos PPR
    pattern = r'^[A-Z0-9]{10,20}$'  # Ejemplo: entre 10 y 20 caracteres alfanuméricos mayúsculas
    return re.match(pattern, codigo) is not None


def validate_codigo_sub_producto(codigo: str) -> bool:
    """
    Valida si un código de subproducto CEPLAN tiene el formato correcto
    
    Args:
        codigo: Código de subproducto a validar
    
    Returns:
        bool: True si el código es válido, False en caso contrario
    """
    # Debe tener 7 dígitos numéricos
    pattern = r'^\d{7}$'
    return re.match(pattern, codigo) is not None


def validate_percentage(value: float) -> bool:
    """
    Valida si un valor está en el rango de porcentaje (0-100)
    
    Args:
        value: Valor a validar
    
    Returns:
        bool: True si el valor es un porcentaje válido, False en caso contrario
    """
    return 0 <= value <= 100


def validate_year(year: int) -> bool:
    """
    Valida si un año es razonable para el sistema
    
    Args:
        year: Año a validar
    
    Returns:
        bool: True si el año es válido, False en caso contrario
    """
    current_year = 2025  # Ajustar según sea necesario
    return 2000 <= year <= current_year + 10


def validate_month(mes: str) -> bool:
    """
    Valida si un mes tiene formato correcto
    
    Args:
        mes: Mes a validar (ene, feb, mar, etc.)
    
    Returns:
        bool: True si el mes es válido, False en caso contrario
    """
    meses_validos = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 
                     'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
    return mes.lower() in meses_validos


def validate_positive_number(value: float) -> bool:
    """
    Valida si un valor es un número positivo
    
    Args:
        value: Valor a validar
    
    Returns:
        bool: True si el valor es positivo, False en caso contrario
    """
    return value >= 0


def validate_not_empty(value: Any) -> bool:
    """
    Valida si un valor no está vacío
    
    Args:
        value: Valor a validar
    
    Returns:
        bool: True si el valor no está vacío, False en caso contrario
    """
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return True