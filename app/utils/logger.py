"""
Sistema de logging para Monitor PPR v2
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logger(name: str, log_file: str = 'logs/error.log', level: int = logging.INFO):
    """
    Configura un logger con rotación de archivos
    
    Args:
        name: Nombre del logger
        log_file: Ruta del archivo de log
        level: Nivel de logging
    """
    # Crear directorio de logs si no existe
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Crear formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Crear handler con rotación
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    handler.setFormatter(formatter)
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger


# Crear logger principal
logger = setup_logger('monitor_ppr', 'logs/error.log')


def log_error(error: Exception, context: str = ""):
    """
    Registra un error en el log
    
    Args:
        error: Excepción a registrar
        context: Contexto adicional del error
    """
    error_msg = f"{context} - Error: {str(error)} - Type: {type(error).__name__}"
    logger.error(error_msg, exc_info=True)


def log_info(message: str, context: str = ""):
    """
    Registra un mensaje informativo en el log
    
    Args:
        message: Mensaje a registrar
        context: Contexto adicional
    """
    log_msg = f"{context} - {message}"
    logger.info(log_msg)


def log_warning(message: str, context: str = ""):
    """
    Registra un mensaje de advertencia en el log
    
    Args:
        message: Mensaje a registrar
        context: Contexto adicional
    """
    log_msg = f"{context} - {message}"
    logger.warning(log_msg)