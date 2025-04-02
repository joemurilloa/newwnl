# WNL Remodeling - Backend

Backend para el sistema de gestión de remodelaciones WNL.

## Tecnologías

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab (para generación de PDFs)

## Requisitos

- Python 3.8+
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/remodelaciones-app.git
cd remodelaciones-app/backend
```

2. Crear un entorno virtual:

```bash
python -m venv venv
```

3. Activar el entorno virtual:

- En Windows:
```bash
venv\Scripts\activate
```

- En macOS/Linux:
```bash
source venv/bin/activate
```

4. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

El proyecto utiliza SQLite como base de datos, lo que significa que no es necesario configurar un servidor de base de datos separado. La base de datos se creará automáticamente en la primera ejecución.

## Ejecución

1. Iniciar el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```

2. Inicializar la base de datos con datos de ejemplo (opcional):

```bash
python scripts/init_db.py
```

3. Acceder a la documentación de la API:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura del proyecto

```
backend/
├── app/
│   ├── main.py                # Punto de entrada FastAPI
│   ├── database.py            # Configuración de SQLite
│   ├── models.py              # Modelos de datos
│   ├── schemas.py             # Esquemas Pydantic
│   ├── routes/                # Rutas API
│   │   ├── clientes.py
│   │   ├── cotizaciones.py
│   │   └── facturas.py
│   ├── utils/                 # Utilidades
│   │   └── pdf_generator.py   # Generador de PDFs
│   └── static/                # Archivos estáticos
│       ├── img/               # Imágenes
│       └── pdfs/              # PDFs generados
├── scripts/                   # Scripts de utilidad
│   └── init_db.py             # Inicialización de la base de datos
├── venv/                      # Entorno virtual (ignorado por git)
├── database.db                # Base de datos SQLite (creada en tiempo de ejecución)
├── README.md                  # Este archivo
└── requirements.txt           # Dependencias del proyecto
```

## Dependencias

Las principales dependencias son:

- fastapi
- uvicorn
- sqlalchemy
- pydantic[email]
- reportlab
- python-multipart

Para instalar todas las dependencias, ejecuta:

```bash
pip install -r requirements.txt
```

## API Endpoints

### Clientes
- `GET /api/clientes/` - Obtener todos los clientes
- `POST /api/clientes/` - Crear un nuevo cliente
- `GET /api/clientes/{cliente_id}` - Obtener cliente por ID
- `PUT /api/clientes/{cliente_id}` - Actualizar cliente
- `DELETE /api/clientes/{cliente_id}` - Eliminar cliente
- `GET /api/clientes/buscar/?termino={termino}` - Buscar clientes

### Cotizaciones
- `GET /api/cotizaciones/` - Obtener todas las cotizaciones
- `POST /api/cotizaciones/` - Crear una nueva cotización
- `GET /api/cotizaciones/{cotizacion_id}` - Obtener cotización por ID
- `PUT /api/cotizaciones/{cotizacion_id}` - Actualizar cotización
- `DELETE /api/cotizaciones/{cotizacion_id}` - Eliminar cotización
- `GET /api/cotizaciones/{cotizacion_id}/pdf` - Generar PDF de cotización

### Facturas
- `GET /api/facturas/` - Obtener todas las facturas
- `POST /api/facturas/` - Crear una nueva factura
- `GET /api/facturas/{factura_id}` - Obtener factura por ID
- `PUT /api/facturas/{factura_id}` - Actualizar factura
- `GET /api/facturas/{factura_id}/pdf` - Generar PDF de factura