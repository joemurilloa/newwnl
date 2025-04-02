import sys
import os

# Añadir el directorio raíz al path para importar los módulos de la aplicación
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app import models

def inicializar_datos():
    """
    Inicializa la base de datos con algunos datos de ejemplo
    """
    db = SessionLocal()
    
    # Verificar si ya hay clientes en la base de datos
    clientes_existentes = db.query(models.Cliente).first()
    if clientes_existentes:
        print("La base de datos ya contiene datos. Omitiendo inicialización.")
        db.close()
        return
    
    # Crear clientes de ejemplo
    cliente1 = models.Cliente(
        nombre="John",
        apellido="Doe",
        telefono="555-123-4567",
        email="john.doe@example.com",
        direccion="123 Main St, Miami, FL"
    )
    
    cliente2 = models.Cliente(
        nombre="Jane",
        apellido="Smith",
        telefono="555-987-6543",
        email="jane.smith@example.com",
        direccion="456 Oak Ave, Miami, FL"
    )
    
    db.add(cliente1)
    db.add(cliente2)
    db.commit()
    
    # Crear cotización de ejemplo
    cotizacion = models.Cotizacion(
        cliente_id=1,
        estado=models.EstadoCotizacion.PENDIENTE,
        notas="Cliente interesado en renovación completa de cocina"
    )
    db.add(cotizacion)
    db.commit()
    
    # Añadir ítems a la cotización
    items = [
        models.ItemCotizacion(
            cotizacion_id=cotizacion.id,
            descripcion="Kitchen cabinets installation",
            cantidad=1,
            unidad="set",
            precio_unitario=3500.00,
            subtotal=3500.00
        ),
        models.ItemCotizacion(
            cotizacion_id=cotizacion.id,
            descripcion="Countertop installation (granite)",
            cantidad=25,
            unidad="sqft",
            precio_unitario=75.00,
            subtotal=1875.00
        ),
        models.ItemCotizacion(
            cotizacion_id=cotizacion.id,
            descripcion="Backsplash tile installation",
            cantidad=30,
            unidad="sqft",
            precio_unitario=20.00,
            subtotal=600.00
        )
    ]
    
    for item in items:
        db.add(item)
    
    # Actualizar totales de la cotización
    subtotal = sum(item.subtotal for item in items)
    impuesto = subtotal * 0.07
    total = subtotal + impuesto
    
    cotizacion.subtotal = subtotal
    cotizacion.impuesto = impuesto
    cotizacion.total = total
    
    db.commit()
    
    print("Base de datos inicializada correctamente con datos de ejemplo.")
    db.close()

if __name__ == "__main__":
    inicializar_datos()