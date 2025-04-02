from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .routes import clientes, cotizaciones, facturas
from .database import engine
from . import models

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Crear directorio para archivos estáticos si no existe
os.makedirs(os.path.join(os.getcwd(), "app", "static", "pdfs"), exist_ok=True)
os.makedirs(os.path.join(os.getcwd(), "app", "static", "img"), exist_ok=True)

# Inicializar FastAPI
app = FastAPI(
    title="WNL Remodeling API",
    description="API para el sistema de gestión de remodelaciones WNL",
    version="1.0.0"
)

# Configurar CORS para permitir solicitudes del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173"],  # URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir routers
app.include_router(clientes.router, prefix="/api/clientes", tags=["clientes"])
app.include_router(cotizaciones.router, prefix="/api/cotizaciones", tags=["cotizaciones"])
app.include_router(facturas.router, prefix="/api/facturas", tags=["facturas"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Sistema de Gestión de Remodelaciones WNL"}

# Ejecutar con: uvicorn app.main:app --reload