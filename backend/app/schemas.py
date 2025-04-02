from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Enums
class EstadoCotizacionEnum(str, Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"

class EstadoPagoEnum(str, Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    PARCIAL = "parcial"

# Cliente schemas
class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    email: EmailStr
    direccion: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None

class Cliente(ClienteBase):
    id: int
    fecha_registro: datetime
    
    class Config:
        orm_mode = True

# ItemCotizacion schemas
class ItemCotizacionBase(BaseModel):
    descripcion: str
    cantidad: float = Field(..., gt=0)
    unidad: str
    precio_unitario: float = Field(..., gt=0)

class ItemCotizacionCreate(ItemCotizacionBase):
    pass

class ItemCotizacion(ItemCotizacionBase):
    id: int
    cotizacion_id: int
    subtotal: float
    
    class Config:
        orm_mode = True

# Cotizacion schemas
class CotizacionBase(BaseModel):
    cliente_id: int
    notas: Optional[str] = None

class CotizacionCreate(CotizacionBase):
    items: List[ItemCotizacionCreate]

class CotizacionUpdate(BaseModel):
    estado: Optional[EstadoCotizacionEnum] = None
    notas: Optional[str] = None

class Cotizacion(CotizacionBase):
    id: int
    fecha: datetime
    estado: EstadoCotizacionEnum
    subtotal: float
    impuesto: float
    total: float
    items: List[ItemCotizacion] = []
    
    class Config:
        orm_mode = True

# Factura schemas
class FacturaBase(BaseModel):
    cotizacion_id: int
    rtn: Optional[str] = None

class FacturaCreate(FacturaBase):
    pass

class FacturaUpdate(BaseModel):
    estado_pago: Optional[EstadoPagoEnum] = None
    rtn: Optional[str] = None

class Factura(FacturaBase):
    id: int
    cliente_id: int
    numero_factura: str
    fecha_emision: datetime
    estado_pago: EstadoPagoEnum
    fecha_pago: Optional[datetime] = None
    
    class Config:
        orm_mode = True