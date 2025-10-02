from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

# Incluir rutas
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ppr.router, prefix="/ppr", tags=["ppr"])
app.include_router(ceplan.router, prefix="/ceplan", tags=["ceplan"])

@app.get("/")
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monitor PPR v2 - Sistema de Gestión de Programa Presupuestal por Resultado</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            .info-box {
                background-color: #ecf0f1;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }
            .links {
                margin: 20px 0;
            }
            .links a {
                display: inline-block;
                margin: 5px;
                padding: 10px 15px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }
            .links a:hover {
                background-color: #2980b9;
            }
            .footer {
                margin-top: 30px;
                text-align: center;
                color: #7f8c8d;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Monitor PPR v2</h1>
            <h2>Sistema de Gestión de Programa Presupuestal por Resultado</h2>
            
            <div class="info-box">
                <h3>Acerca del Sistema</h3>
                <p>Monitor PPR v2 es una plataforma integral para la gestión de Programas Presupuestales por Resultado (PPR) y datos CEPLAN, con roles bien definidos para diferentes actores del proceso de planificación y control.</p>
            </div>
            
            <div class="info-box">
                <h3>Características Principales</h3>
                <ul>
                    <li>Gestión de Programas Presupuestales por Resultado (PPR)</li>
                    <li>Integración de datos CEPLAN</li>
                    <li>Roles diferenciados: Administrador, Responsable de Planificación, Responsable de PPR</li>
                    <li>Seguimiento de avance físico y presupuestal</li>
                    <li>Carga de datos desde archivos Excel</li>
                </ul>
            </div>
            
            <div class="links">
                <h3>Documentación y Acceso</h3>
                <a href="/docs">Documentación de la API (Swagger)</a>
                <a href="/redoc">Documentación de la API (ReDoc)</a>
                <a href="/health">Estado del Servicio</a>
            </div>
            
            <div class="footer">
                <p>Monitor PPR v2 - Sistema de Gestión de Programa Presupuestal por Resultado</p>
                <p>Versión 2.0.0</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Monitor PPR v2 API"}