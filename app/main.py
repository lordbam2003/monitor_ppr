from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

# Importar rutas
from app.api import auth, users, ppr, ceplan

# Crear la aplicación FastAPI
app = FastAPI(
    title="Monitor PPR v2 - Sistema de Gestión de Programa Presupuestal por Resultado",
    description="API para la gestión de Programas Presupuestales por Resultado (PPR) y datos CEPLAN",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluir rutas
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ppr.router, prefix="/ppr", tags=["ppr"])
app.include_router(ceplan.router, prefix="/ceplan", tags=["ceplan"])

@app.get("/")
def read_root():
    # Servir el archivo index.html directamente
    from fastapi.responses import FileResponse
    return FileResponse("app/static/index.html")

# Importante: las rutas deben estar antes del mount de static files
# para evitar conflictos
@app.get("/dashboard")
def read_dashboard():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/dashboard.html")

@app.get("/ppr")
def read_ppr():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/ppr.html")

@app.get("/ppr-progress")
def read_ppr_progress():
    from fastapi.responses import FileResponse
    return FileResponse("app/static/ppr-progress.html")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Monitor PPR v2 API"}