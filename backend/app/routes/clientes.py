from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya está registrado
    db_cliente = db.query(models.Cliente).filter(models.Cliente.email == cliente.email).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Crear el nuevo cliente
    nuevo_cliente = models.Cliente(**cliente.dict())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

@router.get("/", response_model=List[schemas.Cliente])
def obtener_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
    return clientes

@router.get("/{cliente_id}", response_model=schemas.Cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/{cliente_id}", response_model=schemas.Cliente)
def actualizar_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Actualizar solo los campos proporcionados
    update_data = cliente.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(cliente)
    db.commit()
    return None

@router.get("/buscar/", response_model=List[schemas.Cliente])
def buscar_clientes(termino: str, db: Session = Depends(get_db)):
    # Buscar clientes por nombre, apellido o email
    busqueda = f"%{termino}%"
    clientes = db.query(models.Cliente).filter(
        (models.Cliente.nombre.like(busqueda)) |
        (models.Cliente.apellido.like(busqueda)) |
        (models.Cliente.email.like(busqueda))
    ).all()
    return clientes