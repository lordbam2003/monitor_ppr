"""
Endpoints de PPR para Monitor PPR v2
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.ppr import PPR, PPRCreate, PPRUpdate, PPRMeta, PPRMetaCreate, PPRAvance, PPRAvanceCreate, PPRAvanceUpdate
from app.database.models import PPR as DBPPR, PPRMeta as DBPPRMeta, PPRAvance as DBPPRAvance
from app.utils.logger import log_error, log_info

router = APIRouter()


@router.get("/", response_model=List[PPR])
def get_pprs(skip: int = 0, limit: int = 100, ano_ejecucion: int = None, db: Session = Depends(get_db)):
    """
    Obtener lista de PPRs
    """
    try:
        query = db.query(DBPPR)
        
        if ano_ejecucion:
            query = query.filter(DBPPR.ano_ejecucion == ano_ejecucion)
        
        pprs = query.offset(skip).limit(limit).all()
        log_info(f"Obtenidos {len(pprs)} PPRs")
        return pprs
    except Exception as e:
        log_error(e, "get_pprs")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{ppr_id}", response_model=PPR)
def get_ppr(ppr_id: int, db: Session = Depends(get_db)):
    """
    Obtener PPR por ID
    """
    try:
        ppr = db.query(DBPPR).filter(DBPPR.id == ppr_id).first()
        if not ppr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PPR no encontrado"
            )
        return ppr
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, f"get_ppr - ID: {ppr_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/", response_model=PPR)
def create_ppr(ppr: PPRCreate, db: Session = Depends(get_db)):
    """
    Crear nuevo PPR
    """
    try:
        # Verificar si el código del PPR ya existe
        existing_ppr = db.query(DBPPR).filter(DBPPR.codigo == ppr.codigo).first()
        
        if existing_ppr:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código de PPR ya existe"
            )
        
        # Verificar que el responsable de planificación exista
        responsable_planificacion = db.query(DBUser).filter(DBUser.id == ppr.responsable_planificacion_id).first()
        if not responsable_planificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El responsable de planificación no existe"
            )
        
        # Verificar que los responsables del PPR existan si se proporcionan
        if ppr.responsable_ppr_ids:
            responsables = db.query(DBUser).filter(DBUser.id.in_(ppr.responsable_ppr_ids)).all()
            if len(responsables) != len(ppr.responsable_ppr_ids):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Uno o más responsables del PPR no existen"
                )
        
        # Crear nuevo PPR
        db_ppr = DBPPR(
            codigo=ppr.codigo,
            nombre=ppr.nombre,
            descripcion=ppr.descripcion,
            unidad_medida=ppr.unidad_medida,
            responsable_planificacion_id=ppr.responsable_planificacion_id,
            estado=ppr.estado,
            fecha_inicio=ppr.fecha_inicio,
            fecha_fin=ppr.fecha_fin,
            ano_ejecucion=ppr.ano_ejecucion
        )
        
        db.add(db_ppr)
        db.flush()  # Para obtener el ID del nuevo PPR antes de hacer commit
        
        # Asociar responsables del PPR si se proporcionan
        if ppr.responsable_ppr_ids:
            for user_id in ppr.responsable_ppr_ids:
                # Añadir relación en la tabla intermedia
                db.execute(
                    text("INSERT INTO ppr_responsables (ppr_id, user_id) VALUES (:ppr_id, :user_id)"),
                    {"ppr_id": db_ppr.id, "user_id": user_id}
                )
        
        db.commit()
        db.refresh(db_ppr)
        
        log_info(f"PPR creado: {db_ppr.codigo}")
        return db_ppr
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, "create_ppr")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/{ppr_id}", response_model=PPR)
def update_ppr(ppr_id: int, ppr: PPRUpdate, db: Session = Depends(get_db)):
    """
    Actualizar PPR existente
    """
    try:
        db_ppr = db.query(DBPPR).filter(DBPPR.id == ppr_id).first()
        if not db_ppr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PPR no encontrado"
            )
        
        # Actualizar campos
        update_data = ppr.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ppr, field, value)
        
        db.commit()
        db.refresh(db_ppr)
        
        log_info(f"PPR actualizado: {db_ppr.codigo}")
        return db_ppr
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, f"update_ppr - ID: {ppr_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete("/{ppr_id}")
def delete_ppr(ppr_id: int, db: Session = Depends(get_db)):
    """
    Eliminar PPR
    """
    try:
        db_ppr = db.query(DBPPR).filter(DBPPR.id == ppr_id).first()
        if not db_ppr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PPR no encontrado"
            )
        
        db.delete(db_ppr)
        db.commit()
        
        log_info(f"PPR eliminado: {db_ppr.codigo}")
        return {"message": "PPR eliminado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, f"delete_ppr - ID: {ppr_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# Endpoints para metas de PPR
@router.get("/{ppr_id}/metas", response_model=List[PPRMeta])
def get_ppr_metas(ppr_id: int, ano_ejecucion: int = None, db: Session = Depends(get_db)):
    """
    Obtener metas de un PPR
    """
    try:
        query = db.query(DBPPRMeta).filter(DBPPRMeta.ppr_id == ppr_id)
        
        if ano_ejecucion:
            query = query.filter(DBPPRMeta.ano_ejecucion == ano_ejecucion)
        
        metas = query.all()
        log_info(f"Obtenidas {len(metas)} metas para PPR ID: {ppr_id}")
        return metas
    except Exception as e:
        log_error(e, f"get_ppr_metas - PPR ID: {ppr_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/{ppr_id}/metas", response_model=PPRMeta)
def create_ppr_meta(ppr_id: int, meta: PPRMetaCreate, db: Session = Depends(get_db)):
    """
    Crear nueva meta para un PPR
    """
    try:
        # Verificar que el PPR exista
        ppr = db.query(DBPPR).filter(DBPPR.id == ppr_id).first()
        if not ppr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PPR no encontrado"
            )
        
        # Crear nueva meta
        db_meta = DBPPRMeta(
            ppr_id=ppr_id,
            ano_ejecucion=meta.ano_ejecucion,
            descripcion=meta.descripcion,
            meta_programada_anual=meta.meta_programada_anual,
            ene_prog=meta.ene_prog,
            feb_prog=meta.feb_prog,
            mar_prog=meta.mar_prog,
            abr_prog=meta.abr_prog,
            may_prog=meta.may_prog,
            jun_prog=meta.jun_prog,
            jul_prog=meta.jul_prog,
            ago_prog=meta.ago_prog,
            sep_prog=meta.sep_prog,
            oct_prog=meta.oct_prog,
            nov_prog=meta.nov_prog,
            dic_prog=meta.dic_prog
        )
        
        db.add(db_meta)
        db.commit()
        db.refresh(db_meta)
        
        log_info(f"Meta creada para PPR ID: {ppr_id}")
        return db_meta
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, f"create_ppr_meta - PPR ID: {ppr_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


# Endpoints para avances de PPR
@router.get("/{ppr_id}/avances", response_model=List[PPRAvance])
def get_ppr_avances(ppr_id: int, ano_ejecucion: int = None, db: Session = Depends(get_db)):
    """
    Obtener avances de un PPR
    """
    try:
        query = db.query(DBPPRAvance).filter(DBPPRAvance.ppr_id == ppr_id)
        
        if ano_ejecucion:
            query = query.filter(DBPPRAvance.ano_ejecucion == ano_ejecucion)
        
        avances = query.all()
        log_info(f"Obtenidos {len(avances)} avances para PPR ID: {ppr_id}")
        return avances
    except Exception as e:
        log_error(e, f"get_ppr_avances - PPR ID: {ppr_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/{ppr_id}/avances", response_model=PPRAvance)
def create_ppr_avance(ppr_id: int, avance: PPRAvanceCreate, db: Session = Depends(get_db)):
    """
    Crear nuevo avance para un PPR
    """
    try:
        # Verificar que el PPR exista
        ppr = db.query(DBPPR).filter(DBPPR.id == ppr_id).first()
        if not ppr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="PPR no encontrado"
            )
        
        # Crear nuevo avance
        db_avance = DBPPRAvance(
            ppr_id=ppr_id,
            ano_ejecucion=avance.ano_ejecucion,
            mes=avance.mes,
            valor_ejecutado=avance.valor_ejecutado,
            valor_programado=avance.valor_programado,
            comentario=avance.comentario,
            acumulado_anual=avance.acumulado_anual
        )
        
        db.add(db_avance)
        db.commit()
        db.refresh(db_avance)
        
        log_info(f"Avance creado para PPR ID: {ppr_id}, mes: {avance.mes}")
        return db_avance
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, f"create_ppr_avance - PPR ID: {ppr_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )