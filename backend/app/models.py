from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
import datetime
import enum

from .database import Base  # Usar Base desde database.py en lugar de redefinirla

class EstadoCotizacion(enum.Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"

class EstadoPago(enum.Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    PARCIAL = "parcial"

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    telefono = Column(String)
    email = Column(String, unique=True, index=True)
    direccion = Column(Text)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relaciones
    cotizaciones = relationship("Cotizacion", back_populates="cliente", cascade="all, delete-orphan")
    facturas = relationship("Factura", back_populates="cliente", cascade="all, delete-orphan")

class Cotizacion(Base):
    __tablename__ = "cotizaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
    estado = Column(Enum(EstadoCotizacion), default=EstadoCotizacion.PENDIENTE)
    subtotal = Column(Float, default=0.0)
    impuesto = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    notas = Column(Text, nullable=True)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="cotizaciones")
    items = relationship("ItemCotizacion", back_populates="cotizacion", cascade="all, delete-orphan")
    factura = relationship("Factura", back_populates="cotizacion", uselist=False)

class ItemCotizacion(Base):
    __tablename__ = "items_cotizacion"
    
    id = Column(Integer, primary_key=True, index=True)
    cotizacion_id = Column(Integer, ForeignKey("cotizaciones.id"))
    descripcion = Column(String)
    cantidad = Column(Float)
    unidad = Column(String)
    precio_unitario = Column(Float)
    subtotal = Column(Float)
    
    # Relaciones
    cotizacion = relationship("Cotizacion", back_populates="items")

class Factura(Base):
    __tablename__ = "facturas"
    
    id = Column(Integer, primary_key=True, index=True)
    cotizacion_id = Column(Integer, ForeignKey("cotizaciones.id"), unique=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    numero_factura = Column(String, unique=True, index=True)
    fecha_emision = Column(DateTime, default=datetime.datetime.utcnow)
    rtn = Column(String, nullable=True)  # Número fiscal
    estado_pago = Column(Enum(EstadoPago), default=EstadoPago.PENDIENTE)
    fecha_pago = Column(DateTime, nullable=True)
    
    # Relaciones
    cotizacion = relationship("Cotizacion", back_populates="factura")
    cliente = relationship("Cliente", back_populates="facturas")