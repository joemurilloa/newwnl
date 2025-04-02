from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
import os
import datetime

def generar_pdf_cotizacion(cotizacion, cliente, items):
    """Genera un PDF para una cotización en inglés."""
    # Definir la ruta donde se guardará el PDF
    pdf_dir = os.path.join(os.getcwd(), "app", "static", "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"cotizacion_{cotizacion.id}.pdf")
    
    # Crear el documento
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elementos = []
    
    # Estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Heading1']
    estilo_subtitulo = estilos['Heading2']
    estilo_normal = estilos['Normal']
    
    # Título y logo (si existe)
    logo_path = os.path.join(os.getcwd(), "app", "static", "img", "logo.png")
    if os.path.exists(logo_path):
        elementos.append(Image(logo_path, width=1.5*inch, height=0.75*inch))
        elementos.append(Spacer(1, 12))
    
    # Título
    elementos.append(Paragraph("WNL Remodeling", estilo_titulo))
    elementos.append(Paragraph("Quotation", estilo_subtitulo))
    elementos.append(Spacer(1, 12))
    
    # Información de la cotización
    elementos.append(Paragraph(f"Quotation #: {cotizacion.id}", estilo_normal))
    elementos.append(Paragraph(f"Date: {cotizacion.fecha.strftime('%Y-%m-%d')}", estilo_normal))
    elementos.append(Paragraph(f"Status: {cotizacion.estado.value.capitalize()}", estilo_normal))
    elementos.append(Spacer(1, 12))
    
    # Información del cliente
    elementos.append(Paragraph("Client Information:", estilo_subtitulo))
    elementos.append(Paragraph(f"Name: {cliente.nombre} {cliente.apellido}", estilo_normal))
    elementos.append(Paragraph(f"Address: {cliente.direccion}", estilo_normal))
    elementos.append(Paragraph(f"Phone: {cliente.telefono}", estilo_normal))
    elementos.append(Paragraph(f"Email: {cliente.email}", estilo_normal))
    elementos.append(Spacer(1, 24))
    
    # Tabla de ítems
    data = [["Description", "Quantity", "Unit", "Unit Price", "Subtotal"]]
    for item in items:
        data.append([
            item.descripcion,
            str(item.cantidad),
            item.unidad,
            f"${item.precio_unitario:.2f}",
            f"${item.subtotal:.2f}"
        ])
    
    # Añadir subtotal, impuesto y total
    data.append(["", "", "", "Subtotal:", f"${cotizacion.subtotal:.2f}"])
    data.append(["", "", "", "Tax (7%):", f"${cotizacion.impuesto:.2f}"])
    data.append(["", "", "", "Total:", f"${cotizacion.total:.2f}"])
    
    # Crear tabla con estilo
    tabla = Table(data, colWidths=[3*inch, 1*inch, 0.8*inch, 1*inch, 1*inch])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -4), colors.white),
        ('GRID', (0, 0), (-1, -4), 1, colors.black),
        ('SPAN', (0, -3), (2, -3)),
        ('SPAN', (0, -2), (2, -2)),
        ('SPAN', (0, -1), (2, -1)),
        ('ALIGN', (3, -3), (4, -1), 'RIGHT'),
        ('FONTNAME', (3, -1), (4, -1), 'Helvetica-Bold'),
    ]))
    
    elementos.append(tabla)
    elementos.append(Spacer(1, 24))
    
    # Notas
    if cotizacion.notas:
        elementos.append(Paragraph("Notes:", estilo_subtitulo))
        elementos.append(Paragraph(cotizacion.notas, estilo_normal))
        
    # Términos y condiciones
    elementos.append(Spacer(1, 24))
    elementos.append(Paragraph("Terms and Conditions:", estilo_subtitulo))
    elementos.append(Paragraph("1. This quotation is valid for 30 days from the date of issue.", estilo_normal))
    elementos.append(Paragraph("2. Payment terms: 50% deposit required to begin work, 50% upon completion.", estilo_normal))
    elementos.append(Paragraph("3. Work will be scheduled upon receipt of deposit.", estilo_normal))
    elementos.append(Paragraph("4. Any additional work not specified in this quotation will be quoted separately.", estilo_normal))
    
    # Construir el PDF
    doc.build(elementos)
    
    return pdf_path

def generar_pdf_factura(factura, cotizacion, cliente, items):
    """Genera un PDF para una factura en inglés."""
    # Definir la ruta donde se guardará el PDF
    pdf_dir = os.path.join(os.getcwd(), "app", "static", "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"factura_{factura.id}.pdf")
    
    # Crear el documento
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elementos = []
    
    # Estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Heading1']
    estilo_subtitulo = estilos['Heading2']
    estilo_normal = estilos['Normal']
    
    # Título y logo (si existe)
    logo_path = os.path.join(os.getcwd(), "app", "static", "img", "logo.png")
    if os.path.exists(logo_path):
        elementos.append(Image(logo_path, width=1.5*inch, height=0.75*inch))
        elementos.append(Spacer(1, 12))
    
    # Título
    elementos.append(Paragraph("WNL Remodeling", estilo_titulo))
    elementos.append(Paragraph("Invoice", estilo_subtitulo))
    elementos.append(Spacer(1, 12))
    
    # Información de la factura
    elementos.append(Paragraph(f"Invoice #: {factura.numero_factura}", estilo_normal))
    elementos.append(Paragraph(f"Date: {factura.fecha_emision.strftime('%Y-%m-%d')}", estilo_normal))
    elementos.append(Paragraph(f"Payment Status: {factura.estado_pago.value.capitalize()}", estilo_normal))
    if factura.rtn:
        elementos.append(Paragraph(f"Tax ID: {factura.rtn}", estilo_normal))
    elementos.append(Spacer(1, 12))
    
    # Información del cliente
    elementos.append(Paragraph("Client Information:", estilo_subtitulo))
    elementos.append(Paragraph(f"Name: {cliente.nombre} {cliente.apellido}", estilo_normal))
    elementos.append(Paragraph(f"Address: {cliente.direccion}", estilo_normal))
    elementos.append(Paragraph(f"Phone: {cliente.telefono}", estilo_normal))
    elementos.append(Paragraph(f"Email: {cliente.email}", estilo_normal))
    elementos.append(Spacer(1, 24))
    
    # Tabla de ítems
    data = [["Description", "Quantity", "Unit", "Unit Price", "Subtotal"]]
    for item in items:
        data.append([
            item.descripcion,
            str(item.cantidad),
            item.unidad,
            f"${item.precio_unitario:.2f}",
            f"${item.subtotal:.2f}"
        ])
    
    # Añadir subtotal, impuesto y total
    data.append(["", "", "", "Subtotal:", f"${cotizacion.subtotal:.2f}"])
    data.append(["", "", "", "Tax (7%):", f"${cotizacion.impuesto:.2f}"])
    data.append(["", "", "", "Total:", f"${cotizacion.total:.2f}"])
    
    # Crear tabla con estilo
    tabla = Table(data, colWidths=[3*inch, 1*inch, 0.8*inch, 1*inch, 1*inch])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -4), colors.white),
        ('GRID', (0, 0), (-1, -4), 1, colors.black),
        ('SPAN', (0, -3), (2, -3)),
        ('SPAN', (0, -2), (2, -2)),
        ('SPAN', (0, -1), (2, -1)),
        ('ALIGN', (3, -3), (4, -1), 'RIGHT'),
        ('FONTNAME', (3, -1), (4, -1), 'Helvetica-Bold'),
    ]))
    
    elementos.append(tabla)
    elementos.append(Spacer(1, 24))
    
    # Instrucciones de pago
    elementos.append(Paragraph("Payment Information:", estilo_subtitulo))
    elementos.append(Paragraph("Payment Methods: Check, Bank Transfer, Credit Card", estilo_normal))
    elementos.append(Paragraph("Payment Terms: Due within 30 days of invoice date", estilo_normal))
    
    if factura.estado_pago == models.EstadoPago.PAGADO and factura.fecha_pago:
        elementos.append(Spacer(1, 12))
        elementos.append(Paragraph(f"PAID ON: {factura.fecha_pago.strftime('%Y-%m-%d')}", estilo_normal))
    
    # Construir el PDF
    doc.build(elementos)
    
    return pdf_path