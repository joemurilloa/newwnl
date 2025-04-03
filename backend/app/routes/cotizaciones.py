from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
import os
from fastapi.responses import FileResponse

from .. import models, schemas
from ..database import get_db
from ..utils.pdf_generator import generar_pdf_cotizacion

router = APIRouter()

@router.post("/", response_model=schemas.Cotizacion, status_code=status.HTTP_201_CREATED)
def crear_cotizacion(cotizacion: schemas.CotizacionCreate, db: Session = Depends(get_db)):
    # Verificar que el cliente existe
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cotizacion.cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Crear la cotización
    nueva_cotizacion = models.Cotizacion(
        cliente_id=cotizacion.cliente_id,
        notas=cotizacion.notas
    )
    db.add(nueva_cotizacion)
    db.commit()
    db.refresh(nueva_cotizacion)
    
    # Agregar los ítems
    subtotal_total = 0.0
    for item_data in cotizacion.items:
        subtotal = item_data.cantidad * item_data.precio_unitario
        item = models.ItemCotizacion(
            cotizacion_id=nueva_cotizacion.id,
            descripcion=item_data.descripcion,
            cantidad=item_data.cantidad,
            unidad=item_data.unidad,
            precio_unitario=item_data.precio_unitario,
            subtotal=subtotal
        )
        db.add(item)
        subtotal_total += subtotal
    
    # Calcular totales
    impuesto = subtotal_total * 0.07  # 7% de impuesto
    total = subtotal_total + impuesto
    
    # Actualizar la cotización con los totales
    nueva_cotizacion.subtotal = subtotal_total
    nueva_cotizacion.impuesto = impuesto
    nueva_cotizacion.total = total
    
    db.commit()
    db.refresh(nueva_cotizacion)
    
    return nueva_cotizacion

@router.get("/", response_model=List[schemas.Cotizacion])
def obtener_cotizaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Simplificado para usar directamente los modelos
    cotizaciones = db.query(models.Cotizacion).offset(skip).limit(limit).all()
    return cotizaciones

@router.get("/aprobadas", response_model=List[schemas.Cotizacion])
def obtener_cotizaciones_aprobadas(db: Session = Depends(get_db)):
    cotizaciones = db.query(models.Cotizacion).filter(
        models.Cotizacion.estado == models.EstadoCotizacion.APROBADA
    ).all()
    return cotizaciones

@router.get("/{cotizacion_id}", response_model=schemas.Cotizacion)
def obtener_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = db.query(models.Cotizacion).filter(models.Cotizacion.id == cotizacion_id).first()
    if cotizacion is None:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    return cotizacion

@router.put("/{cotizacion_id}", response_model=schemas.Cotizacion)
def actualizar_cotizacion(cotizacion_id: int, cotizacion: schemas.CotizacionUpdate, db: Session = Depends(get_db)):
    db_cotizacion = db.query(models.Cotizacion).filter(models.Cotizacion.id == cotizacion_id).first()
    if db_cotizacion is None:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    
    update_data = cotizacion.dict(exclude_unset=True)
    
    # Si hay un cambio de estado, convertir de enum string a enum real
    if 'estado' in update_data:
        estado_str = update_data['estado']
        if estado_str == 'pendiente':
            update_data['estado'] = models.EstadoCotizacion.PENDIENTE
        elif estado_str == 'aprobada':
            update_data['estado'] = models.EstadoCotizacion.APROBADA
        elif estado_str == 'rechazada':
            update_data['estado'] = models.EstadoCotizacion.RECHAZADA
    
    for key, value in update_data.items():
        setattr(db_cotizacion, key, value)
    
    db.commit()
    db.refresh(db_cotizacion)
    return db_cotizacion

@router.delete("/{cotizacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = db.query(models.Cotizacion).filter(models.Cotizacion.id == cotizacion_id).first()
    if cotizacion is None:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    
    db.delete(cotizacion)
    db.commit()
    return None

@router.get("/{cotizacion_id}/pdf")
def generar_pdf(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = db.query(models.Cotizacion).filter(models.Cotizacion.id == cotizacion_id).first()
    if cotizacion is None:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cotizacion.cliente_id).first()
    items = db.query(models.ItemCotizacion).filter(models.ItemCotizacion.cotizacion_id == cotizacion_id).all()
    
    pdf_path = generar_pdf_cotizacion(cotizacion, cliente, items)
    
    # Devolver el archivo PDF
    return FileResponse(
        path=pdf_path, 
        filename=f"cotizacion_{cotizacion_id}.pdf",
        media_type="application/pdf"
    )