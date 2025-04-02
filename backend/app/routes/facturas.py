from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import datetime
import uuid
from fastapi.responses import FileResponse

from .. import models, schemas
from ..database import get_db
from ..utils.pdf_generator import generar_pdf_factura

router = APIRouter()

def generar_numero_factura():
    # Genera un número de factura único basado en UUID
    return f"INV-{uuid.uuid4().hex[:8].upper()}"

@router.post("/", response_model=schemas.Factura, status_code=status.HTTP_201_CREATED)
def crear_factura(factura: schemas.FacturaCreate, db: Session = Depends(get_db)):
    # Verificar que la cotización existe
    cotizacion = db.query(models.Cotizacion).filter(models.Cotizacion.id == factura.cotizacion_id).first()
    if cotizacion is None:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    
    # Verificar que la cotización esté aprobada
    if cotizacion.estado != models.EstadoCotizacion.APROBADA:
        raise HTTPException(status_code=400, detail="La cotización debe estar aprobada para generar una factura")
    
    # Verificar que la cotización no tenga ya una factura
    factura_existente = db.query(models.Factura).filter(models.Factura.cotizacion_id == factura.cotizacion_id).first()
    if factura_existente:
        raise HTTPException(status_code=400, detail="Esta cotización ya tiene una factura asociada")
    
    # Crear la factura
    nueva_factura = models.Factura(
        cotizacion_id=factura.cotizacion_id,
        cliente_id=cotizacion.cliente_id,
        numero_factura=generar_numero_factura(),
        rtn=factura.rtn
    )
    
    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    
    return nueva_factura

@router.get("/", response_model=List[schemas.Factura])
def obtener_facturas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    facturas = db.query(models.Factura).offset(skip).limit(limit).all()
    return facturas

@router.get("/{factura_id}", response_model=schemas.Factura)
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@router.put("/{factura_id}", response_model=schemas.Factura)
def actualizar_factura(factura_id: int, factura: schemas.FacturaUpdate, db: Session = Depends(get_db)):
    db_factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if db_factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    update_data = factura.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_factura, key, value)
    
    # Si se cambia el estado a PAGADO, registrar la fecha de pago
    if factura.estado_pago and factura.estado_pago == schemas.EstadoPagoEnum.PAGADO and not db_factura.fecha_pago:
        db_factura.fecha_pago = datetime.datetime.utcnow()
    
    db.commit()
    db.refresh(db_factura)
    return db_factura

@router.get("/{factura_id}/pdf")
def generar_pdf(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if factura is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    cotizacion = db.query(models.Cotizacion).filter(models.Cotizacion.id == factura.cotizacion_id).first()
    cliente = db.query(models.Cliente).filter(models.Cliente.id == factura.cliente_id).first()
    items = db.query(models.ItemCotizacion).filter(models.ItemCotizacion.cotizacion_id == cotizacion.id).all()
    
    pdf_path = generar_pdf_factura(factura, cotizacion, cliente, items)
    
    # Devolver el archivo PDF
    return FileResponse(
        path=pdf_path, 
        filename=f"factura_{factura.numero_factura}.pdf",
        media_type="application/pdf"
    )