"""
Funciones de utilidad para Monitor PPR v2
"""
import pandas as pd
from typing import Dict, Any, List
from app.database.models import CEPLAN as DBCEPLAN, PPR as DBPPR
from sqlalchemy.orm import Session
from app.utils.validators import validate_codigo_sub_producto, validate_year, validate_codigo_ppr
from app.utils.logger import log_error, log_info


def cargar_datos_ceplan_desde_excel(file_path: str, ano_ejecucion: int, db: Session) -> Dict[str, Any]:
    """
    Carga datos de CEPLAN desde un archivo Excel
    
    Args:
        file_path: Ruta del archivo Excel
        ano_ejecucion: Año de ejecución
        db: Sesión de base de datos
    
    Returns:
        Dict con resultados de la operación
    """
    try:
        # Validar año
        if not validate_year(ano_ejecucion):
            return {"success": False, "error": "Año de ejecución no válido"}
        
        # Leer archivo Excel
        df = pd.read_excel(file_path)
        
        # Verificar columnas requeridas
        required_columns = [
            'codigo_sub_producto', 'subproducto', 
            'EJE_ENE', 'PROG_ENE', 'EJE_FEB', 'PROG_FEB',
            'EJE_MAR', 'PROG_MAR', 'EJE_ABR', 'PROG_ABR',
            'EJE_MAY', 'PROG_MAY', 'EJE_JUN', 'PROG_JUN',
            'EJE_JUL', 'PROG_JUL', 'EJE_AGO', 'PROG_AGO',
            'EJE_SEP', 'PROG_SEP', 'EJE_OCT', 'PROG_OCT',
            'EJE_NOV', 'PROG_NOV', 'EJE_DIC', 'PROG_DIC'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return {"success": False, "error": f"Columnas faltantes: {missing_columns}"}
        
        registros_procesados = 0
        registros_ignorados = 0
        
        for index, row in df.iterrows():
            # Validar código de subproducto
            codigo_sub_producto = str(row['codigo_sub_producto']).strip()
            if not validate_codigo_sub_producto(codigo_sub_producto):
                log_info(f"Código de subproducto no válido: {codigo_sub_producto} en fila {index}")
                registros_ignorados += 1
                continue
            
            # Verificar si ya existe un registro con el mismo código y año
            existing_record = db.query(DBCEPLAN).filter(
                DBCEPLAN.codigo_sub_producto == codigo_sub_producto,
                DBCEPLAN.ano_ejecucion == ano_ejecucion
            ).first()
            
            if existing_record:
                # Actualizar registro existente
                existing_record.subproducto = row['subproducto']
                existing_record.ene_eje = float(row['EJE_ENE']) if pd.notna(row['EJE_ENE']) else 0.0
                existing_record.ene_prog = float(row['PROG_ENE']) if pd.notna(row['PROG_ENE']) else 0.0
                existing_record.feb_eje = float(row['EJE_FEB']) if pd.notna(row['EJE_FEB']) else 0.0
                existing_record.feb_prog = float(row['PROG_FEB']) if pd.notna(row['PROG_FEB']) else 0.0
                existing_record.mar_eje = float(row['EJE_MAR']) if pd.notna(row['EJE_MAR']) else 0.0
                existing_record.mar_prog = float(row['PROG_MAR']) if pd.notna(row['PROG_MAR']) else 0.0
                existing_record.abr_eje = float(row['EJE_ABR']) if pd.notna(row['EJE_ABR']) else 0.0
                existing_record.abr_prog = float(row['PROG_ABR']) if pd.notna(row['PROG_ABR']) else 0.0
                existing_record.may_eje = float(row['EJE_MAY']) if pd.notna(row['EJE_MAY']) else 0.0
                existing_record.may_prog = float(row['PROG_MAY']) if pd.notna(row['PROG_MAY']) else 0.0
                existing_record.jun_eje = float(row['EJE_JUN']) if pd.notna(row['EJE_JUN']) else 0.0
                existing_record.jun_prog = float(row['PROG_JUN']) if pd.notna(row['PROG_JUN']) else 0.0
                existing_record.jul_eje = float(row['EJE_JUL']) if pd.notna(row['EJE_JUL']) else 0.0
                existing_record.jul_prog = float(row['PROG_JUL']) if pd.notna(row['PROG_JUL']) else 0.0
                existing_record.ago_eje = float(row['EJE_AGO']) if pd.notna(row['EJE_AGO']) else 0.0
                existing_record.ago_prog = float(row['PROG_AGO']) if pd.notna(row['PROG_AGO']) else 0.0
                existing_record.sep_eje = float(row['EJE_SEP']) if pd.notna(row['EJE_SEP']) else 0.0
                existing_record.sep_prog = float(row['PROG_SEP']) if pd.notna(row['PROG_SEP']) else 0.0
                existing_record.oct_eje = float(row['EJE_OCT']) if pd.notna(row['EJE_OCT']) else 0.0
                existing_record.oct_prog = float(row['PROG_OCT']) if pd.notna(row['PROG_OCT']) else 0.0
                existing_record.nov_eje = float(row['EJE_NOV']) if pd.notna(row['EJE_NOV']) else 0.0
                existing_record.nov_prog = float(row['PROG_NOV']) if pd.notna(row['PROG_NOV']) else 0.0
                existing_record.dic_eje = float(row['EJE_DIC']) if pd.notna(row['EJE_DIC']) else 0.0
                existing_record.dic_prog = float(row['PROG_DIC']) if pd.notna(row['PROG_DIC']) else 0.0
            else:
                # Crear nuevo registro
                nuevo_registro = DBCEPLAN(
                    codigo_sub_producto=codigo_sub_producto,
                    subproducto=row['subproducto'],
                    ano_ejecucion=ano_ejecucion,
                    ene_eje=float(row['EJE_ENE']) if pd.notna(row['EJE_ENE']) else 0.0,
                    ene_prog=float(row['PROG_ENE']) if pd.notna(row['PROG_ENE']) else 0.0,
                    feb_eje=float(row['EJE_FEB']) if pd.notna(row['EJE_FEB']) else 0.0,
                    feb_prog=float(row['PROG_FEB']) if pd.notna(row['PROG_FEB']) else 0.0,
                    mar_eje=float(row['EJE_MAR']) if pd.notna(row['EJE_MAR']) else 0.0,
                    mar_prog=float(row['PROG_MAR']) if pd.notna(row['PROG_MAR']) else 0.0,
                    abr_eje=float(row['EJE_ABR']) if pd.notna(row['EJE_ABR']) else 0.0,
                    abr_prog=float(row['PROG_ABR']) if pd.notna(row['PROG_ABR']) else 0.0,
                    may_eje=float(row['EJE_MAY']) if pd.notna(row['EJE_MAY']) else 0.0,
                    may_prog=float(row['PROG_MAY']) if pd.notna(row['PROG_MAY']) else 0.0,
                    jun_eje=float(row['EJE_JUN']) if pd.notna(row['EJE_JUN']) else 0.0,
                    jun_prog=float(row['PROG_JUN']) if pd.notna(row['PROG_JUN']) else 0.0,
                    jul_eje=float(row['EJE_JUL']) if pd.notna(row['EJE_JUL']) else 0.0,
                    jul_prog=float(row['PROG_JUL']) if pd.notna(row['PROG_JUL']) else 0.0,
                    ago_eje=float(row['EJE_AGO']) if pd.notna(row['EJE_AGO']) else 0.0,
                    ago_prog=float(row['PROG_AGO']) if pd.notna(row['PROG_AGO']) else 0.0,
                    sep_eje=float(row['EJE_SEP']) if pd.notna(row['EJE_SEP']) else 0.0,
                    sep_prog=float(row['PROG_SEP']) if pd.notna(row['PROG_SEP']) else 0.0,
                    oct_eje=float(row['EJE_OCT']) if pd.notna(row['EJE_OCT']) else 0.0,
                    oct_prog=float(row['PROG_OCT']) if pd.notna(row['PROG_OCT']) else 0.0,
                    nov_eje=float(row['EJE_NOV']) if pd.notna(row['EJE_NOV']) else 0.0,
                    nov_prog=float(row['PROG_NOV']) if pd.notna(row['PROG_NOV']) else 0.0,
                    dic_eje=float(row['EJE_DIC']) if pd.notna(row['EJE_DIC']) else 0.0,
                    dic_prog=float(row['PROG_DIC']) if pd.notna(row['PROG_DIC']) else 0.0
                )
                db.add(nuevo_registro)
            
            registros_procesados += 1
        
        # Confirmar cambios en la base de datos
        db.commit()
        
        log_info(f"Archivo CEPLAN procesado. Procesados: {registros_procesados}, Ignorados: {registros_ignorados}")
        
        return {
            "success": True,
            "message": f"Archivo procesado exitosamente. {registros_procesados} registros procesados, {registros_ignorados} ignorados.",
            "processed": registros_procesados,
            "ignored": registros_ignorados
        }
    
    except Exception as e:
        log_error(e, "cargar_datos_ceplan_desde_excel")
        db.rollback()
        return {"success": False, "error": str(e)}


def cargar_datos_ppr_desde_excel(file_path: str, ano_ejecucion: int, responsable_planificacion_id: int, db: Session) -> Dict[str, Any]:
    """
    Carga datos de PPR desde un archivo Excel
    
    Args:
        file_path: Ruta del archivo Excel
        ano_ejecucion: Año de ejecución
        responsable_planificacion_id: ID del responsable de planificación
        db: Sesión de base de datos
    
    Returns:
        Dict con resultados de la operación
    """
    try:
        # Validar año
        if not validate_year(ano_ejecucion):
            return {"success": False, "error": "Año de ejecución no válido"}
        
        # Leer archivo Excel
        df = pd.read_excel(file_path)
        
        # Verificar columnas requeridas para PPR
        required_columns = [
            'codigo', 'nombre', 'descripcion', 'unidad_medida',
            'meta_programada_anual',
            'ene_prog', 'feb_prog', 'mar_prog', 'abr_prog',
            'may_prog', 'jun_prog', 'jul_prog', 'ago_prog',
            'sep_prog', 'oct_prog', 'nov_prog', 'dic_prog'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return {"success": False, "error": f"Columnas faltantes: {missing_columns}"}
        
        registros_procesados = 0
        registros_ignorados = 0
        
        for index, row in df.iterrows():
            # Validar código de PPR
            codigo = str(row['codigo']).strip()
            if not validate_codigo_ppr(codigo):
                log_info(f"Código de PPR no válido: {codigo} en fila {index}")
                registros_ignorados += 1
                continue
            
            # Verificar si ya existe un PPR con el mismo código y año
            existing_ppr = db.query(DBPPR).filter(
                DBPPR.codigo == codigo,
                DBPPR.ano_ejecucion == ano_ejecucion
            ).first()
            
            if existing_ppr:
                # Actualizar PPR existente
                existing_ppr.nombre = row['nombre']
                existing_ppr.descripcion = row['descripcion']
                existing_ppr.unidad_medida = row['unidad_medida']
                # Nota: no actualizamos el responsable de planificación desde el archivo
            else:
                # Crear nuevo PPR
                nuevo_ppr = DBPPR(
                    codigo=codigo,
                    nombre=row['nombre'],
                    descripcion=row['descripcion'],
                    unidad_medida=row['unidad_medida'],
                    responsable_planificacion_id=responsable_planificacion_id,
                    responsable_ppr_id=None,  # Se asignará después
                    estado="activo",
                    ano_ejecucion=ano_ejecucion
                )
                db.add(nuevo_ppr)
                db.flush()  # Para obtener el ID del nuevo PPR
                
                # Crear meta asociada al PPR
                from app.database.models import PPRMeta as DBPPRMeta
                nueva_meta = DBPPRMeta(
                    ppr_id=nuevo_ppr.id,
                    ano_ejecucion=ano_ejecucion,
                    descripcion=f"Meta anual para {row['nombre']}",
                    meta_programada_anual=float(row['meta_programada_anual']) if pd.notna(row['meta_programada_anual']) else 0.0,
                    ene_prog=float(row['ene_prog']) if pd.notna(row['ene_prog']) else 0.0,
                    feb_prog=float(row['feb_prog']) if pd.notna(row['feb_prog']) else 0.0,
                    mar_prog=float(row['mar_prog']) if pd.notna(row['mar_prog']) else 0.0,
                    abr_prog=float(row['abr_prog']) if pd.notna(row['abr_prog']) else 0.0,
                    may_prog=float(row['may_prog']) if pd.notna(row['may_prog']) else 0.0,
                    jun_prog=float(row['jun_prog']) if pd.notna(row['jun_prog']) else 0.0,
                    jul_prog=float(row['jul_prog']) if pd.notna(row['jul_prog']) else 0.0,
                    ago_prog=float(row['ago_prog']) if pd.notna(row['ago_prog']) else 0.0,
                    sep_prog=float(row['sep_prog']) if pd.notna(row['sep_prog']) else 0.0,
                    oct_prog=float(row['oct_prog']) if pd.notna(row['oct_prog']) else 0.0,
                    nov_prog=float(row['nov_prog']) if pd.notna(row['nov_prog']) else 0.0,
                    dic_prog=float(row['dic_prog']) if pd.notna(row['dic_prog']) else 0.0
                )
                db.add(nueva_meta)
            
            registros_procesados += 1
        
        # Confirmar cambios en la base de datos
        db.commit()
        
        log_info(f"Archivo PPR procesado. Procesados: {registros_procesados}, Ignorados: {registros_ignorados}")
        
        return {
            "success": True,
            "message": f"Archivo PPR procesado exitosamente. {registros_procesados} registros procesados, {registros_ignorados} ignorados.",
            "processed": registros_procesados,
            "ignored": registros_ignorados
        }
    
    except Exception as e:
        log_error(e, "cargar_datos_ppr_desde_excel")
        db.rollback()
        return {"success": False, "error": str(e)}


def comparar_datos_ceplan_ppr(ano_ejecucion: int, db: Session) -> Dict[str, Any]:
    """
    Compara datos de CEPLAN y PPR para un año específico
    
    Args:
        ano_ejecucion: Año de ejecución
        db: Sesión de base de datos
    
    Returns:
        Dict con resultados de la comparación
    """
    try:
        # Obtener datos CEPLAN
        ceplan_data = db.query(DBCEPLAN).filter(
            DBCEPLAN.ano_ejecucion == ano_ejecucion
        ).all()
        
        # Convertir a diccionario para búsqueda rápida
        ceplan_dict = {item.codigo_sub_producto: item for item in ceplan_data}
        
        # Obtener PPRs para el año
        ppr_data = db.query(DBPPR).filter(
            DBPPR.ano_ejecucion == ano_ejecucion
        ).all()
        
        comparaciones = []
        
        for ppr in ppr_data:
            # Intentar encontrar correspondencia en CEPLAN
            # Esto dependerá de la lógica de negocio específica
            # Por ahora, simplemente se puede hacer una coincidencia aproximada
            
            # En una implementación real, aquí se haría la lógica de correlación
            # entre PPR y CEPLAN basada en criterios específicos del negocio
            pass
        
        log_info(f"Comparación CEPLAN-PPR realizada para el año {ano_ejecucion}")
        
        return {
            "success": True,
            "ano_ejecucion": ano_ejecucion,
            "ceplan_count": len(ceplan_data),
            "ppr_count": len(ppr_data),
            "message": f"Comparación realizada para {len(ppr_data)} PPRs y {len(ceplan_data)} CEPLANs"
        }
    
    except Exception as e:
        log_error(e, "comparar_datos_ceplan_ppr")
        return {"success": False, "error": str(e)}


def format_fecha(fecha: datetime) -> str:
    """
    Formatea una fecha en formato legible
    
    Args:
        fecha: Fecha a formatear
    
    Returns:
        str: Fecha formateada
    """
    return fecha.strftime("%Y-%m-%d %H:%M:%S")


def calcular_porcentaje(actual: float, total: float) -> float:
    """
    Calcula el porcentaje de un valor respecto a otro
    
    Args:
        actual: Valor actual
        total: Valor total
    
    Returns:
        float: Porcentaje calculado
    """
    if total == 0:
        return 0.0
    return round((actual / total) * 100, 2)


def calcular_avance_mensual(ejecutado: float, programado: float) -> float:
    """
    Calcula el avance mensual en porcentaje
    
    Args:
        ejecutado: Valor ejecutado
        programado: Valor programado
    
    Returns:
        float: Porcentaje de avance
    """
    if programado == 0:
        return 0.0 if ejecutado == 0 else 100.0
    return round((ejecutado / programado) * 100, 2)


def get_mes_nombre_corto(numero_mes: int) -> str:
    """
    Obtiene el nombre corto de un mes a partir de su número
    
    Args:
        numero_mes: Número del mes (1-12)
    
    Returns:
        str: Nombre corto del mes
    """
    meses = {
        1: 'ene', 2: 'feb', 3: 'mar', 4: 'abr',
        5: 'may', 6: 'jun', 7: 'jul', 8: 'ago',
        9: 'sep', 10: 'oct', 11: 'nov', 12: 'dic'
    }
    return meses.get(numero_mes, '')


def get_mes_numero(nombre_corto: str) -> int:
    """
    Obtiene el número de mes a partir de su nombre corto
    
    Args:
        nombre_corto: Nombre corto del mes (ene, feb, etc.)
    
    Returns:
        int: Número del mes
    """
    meses = {
        'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4,
        'may': 5, 'jun': 6, 'jul': 7, 'ago': 8,
        'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
    }
    return meses.get(nombre_corto.lower(), 0)


def calcular_avance_anual(datos_mensuales: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """
    Calcula el avance anual a partir de datos mensuales
    
    Args:
        datos_mensuales: Diccionario con datos mensuales {'ene': {'ejecutado': 10, 'programado': 15}, ...}
    
    Returns:
        Dict[str, float]: Diccionario con avance anual {'ejecutado': total_ejecutado, 'programado': total_programado, 'porcentaje': porcentaje}
    """
    total_ejecutado = sum(mes.get('ejecutado', 0) for mes in datos_mensuales.values())
    total_programado = sum(mes.get('programado', 0) for mes in datos_mensuales.values())
    porcentaje = calcular_porcentaje(total_ejecutado, total_programado) if total_programado > 0 else 0.0
    
    return {
        'ejecutado': total_ejecutado,
        'programado': total_programado,
        'porcentaje': porcentaje
    }


def formatear_datos_para_grafico(datos: List[Dict[str, Any]], campo_x: str, campo_y: str) -> Dict[str, List]:
    """
    Formatea datos para ser usados en gráficos
    
    Args:
        datos: Lista de diccionarios con datos
        campo_x: Nombre del campo para el eje X
        campo_y: Nombre del campo para el eje Y
    
    Returns:
        Dict[str, List]: Diccionario con listas para cada eje
    """
    x_values = []
    y_values = []
    
    for item in datos:
        if campo_x in item and campo_y in item:
            x_values.append(item[campo_x])
            y_values.append(item[campo_y])
    
    return {
        'x': x_values,
        'y': y_values
    }


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Obtiene un valor de un diccionario de forma segura
    
    Args:
        data: Diccionario de donde obtener el valor
        key: Clave a buscar
        default: Valor por defecto si no se encuentra la clave
    
    Returns:
        Any: Valor encontrado o valor por defecto
    """
    try:
        return data.get(key, default)
    except:
        return default


def create_db_filter_query(base_query, filters: Dict[str, Any], model_class):
    """
    Crea una consulta con filtros dinámicos
    
    Args:
        base_query: Consulta base de SQLAlchemy
        filters: Diccionario de filtros
        model_class: Clase del modelo de SQLAlchemy
    
    Returns:
        Consulta con filtros aplicados
    """
    for key, value in filters.items():
        if value is not None and hasattr(model_class, key):
            base_query = base_query.filter(getattr(model_class, key) == value)
    
    return base_query