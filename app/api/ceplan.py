"""
Endpoints de CEPLAN para Monitor PPR v2
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.ceplan import CEPLAN, CEPLANCreate, CEPLANUpdate
from app.database.models import CEPLAN as DBCEPLAN
from app.utils.logger import log_error, log_info

router = APIRouter()


@router.get("/", response_model=List[CEPLAN])
def get_ceplans(skip: int = 0, limit: int = 100, ano_ejecucion: int = None, db: Session = Depends(get_db)):
    """
    Obtener lista de CEPLAN
    """
    try:
        query = db.query(DBCEPLAN)
        
        if ano_ejecucion:
            query = query.filter(DBCEPLAN.ano_ejecucion == ano_ejecucion)
        
        ceplans = query.offset(skip).limit(limit).all()
        log_info(f"Obtenidos {len(ceplans)} CEPLAN")
        return ceplans
    except Exception as e:
        log_error(e, "get_ceplans")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{ceplan_id}", response_model=CEPLAN)
def get_ceplan(ceplan_id: int, db: Session = Depends(get_db)):
    """
    Obtener CEPLAN por ID
    """
    try:
        ceplan = db.query(DBCEPLAN).filter(DBCEPLAN.id == ceplan_id).first()
        if not ceplan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CEPLAN no encontrado"
            )
        return ceplan
    except HTTPException:
        raise
    except Exception as e:
        log_error(e, f"get_ceplan - ID: {ceplan_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/", response_model=CEPLAN)
def create_ceplan(ceplan: CEPLANCreate, db: Session = Depends(get_db)):
    """
    Crear nuevo CEPLAN
    """
    try:
        # Verificar si el código de subproducto ya existe para el mismo año
        existing_ceplan = db.query(DBCEPLAN).filter(
            DBCEPLAN.codigo_sub_producto == ceplan.codigo_sub_producto,
            DBCEPLAN.ano_ejecucion == ceplan.ano_ejecucion
        ).first()
        
        if existing_ceplan:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un CEPLAN con este código de subproducto para el año especificado"
            )
        
        # Crear nuevo CEPLAN
        db_ceplan = DBCEPLAN(
            codigo_sub_producto=ceplan.codigo_sub_producto,
            subproducto=ceplan.subproducto,
            ano_ejecucion=ceplan.ano_ejecucion,
            ene_eje=ceplan.ene_eje,
            ene_prog=ceplan.ene_prog,
            feb_eje=ceplan.feb_eje,
            feb_prog=ceplan.feb_prog,
            mar_eje=ceplan.mar_eje,
            mar_prog=ceplan.mar_prog,
            abr_eje=ceplan.abr_eje,
            abr_prog=ceplan.abr_prog,
            may_eje=ceplan.may_eje,
            may_prog=ceplan.may_prog,
            jun_eje=ceplan.jun_eje,
            jun_prog=ceplan.jun_prog,
            jul_eje=ceplan.jul_eje,
            jul_prog=ceplan.jul_prog,
            ago_eje=ceplan.ago_eje,
            ago_prog=ceplan.ago_prog,
            sep_eje=ceplan.sep_eje,
            sep_prog=ceplan.sep_prog,
            oct_eje=ceplan.oct_eje,
            oct_prog=ceplan.oct_prog,
            nov_eje=ceplan.nov_eje,
            nov_prog=ceplan.nov_prog,
            dic_eje=ceplan.dic_eje,
            dic_prog=ceplan.dic_prog
        )
        
        db.add(db_ceplan)
        db.commit()
        db.refresh(db_ceplan)
        
        log_info(f"CEPLAN creado: {db_ceplan.codigo_sub_producto}")
        return db_ceplan
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, "create_ceplan")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/{ceplan_id}", response_model=CEPLAN)
def update_ceplan(ceplan_id: int, ceplan: CEPLANUpdate, db: Session = Depends(get_db)):
    """
    Actualizar CEPLAN existente
    """
    try:
        db_ceplan = db.query(DBCEPLAN).filter(DBCEPLAN.id == ceplan_id).first()
        if not db_ceplan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CEPLAN no encontrado"
            )
        
        # Actualizar campos
        update_data = ceplan.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ceplan, field, value)
        
        db.commit()
        db.refresh(db_ceplan)
        
        log_info(f"CEPLAN actualizado: {db_ceplan.codigo_sub_producto}")
        return db_ceplan
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, f"update_ceplan - ID: {ceplan_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete("/{ceplan_id}")
def delete_ceplan(ceplan_id: int, db: Session = Depends(get_db)):
    """
    Eliminar CEPLAN
    """
    try:
        db_ceplan = db.query(DBCEPLAN).filter(DBCEPLAN.id == ceplan_id).first()
        if not db_ceplan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CEPLAN no encontrado"
            )
        
        db.delete(db_ceplan)
        db.commit()
        
        log_info(f"CEPLAN eliminado: {db_ceplan.codigo_sub_producto}")
        return {"message": "CEPLAN eliminado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(e, f"delete_ceplan - ID: {ceplan_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )