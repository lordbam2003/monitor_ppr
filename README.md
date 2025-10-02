# Monitor PPR v2 - Sistema de Gestión de Programa Presupuestal por Resultado

## Descripción del Proyecto

Monitor PPR v2 es un sistema web desarrollado en Python con FastAPI que permite la gestión integral de Programas Presupuestales por Resultado (PPR) y datos CEPLAN. El sistema facilita la carga, seguimiento y control de indicadores de desempeño, con roles diferenciados para administradores, responsables de planificación y responsables de PPR.

## Objetivo del Proyecto

El sistema tiene como finalidad proporcionar una plataforma unificada para el seguimiento de Programas Presupuestales por Resultado (PPR), integrando datos del PPR y CEPLAN, con roles bien definidos para diferentes actores del proceso de planificación y control.

## Convenciones de Desarrollo

### Estructura de Archivos
- Carpeta `app/` para el código principal de la aplicación
- Subcarpetas para módulos: `api/`, `models/`, `schemas/`, `database/`, `utils/`
- Carpeta `static/` para recursos estáticos (CSS, JS, imágenes)
- Carpeta `logs/` para archivos de log
- Carpeta `tests/` para pruebas unitarias e integración

### Nomenclatura
- Nombres de archivos en snake_case
- Clases en PascalCase
- Funciones y variables en snake_case
- Constantes en UPPER_SNAKE_CASE
- Prefijos de módulos en minúsculas

### Estilo de Código
- 4 espacios para indentación (no tabuladores)
- Líneas máximas de 88 caracteres
- Importaciones organizadas por estándar, terceros y locales
- Documentación de funciones y clases con docstrings en formato Google
- Tipado estático con typing

### Control de Versiones
- Commits descriptivos y atómicos
- Uso de convención de mensajes: `[tipo(scope):] descripción`
- Tipos: feature, fix, chore, docs, test, refactor, etc.

## Arquitectura del Sistema

### Tecnologías Utilizadas

- **Backend**: Python 3.8+, FastAPI
- **Frontend**: HTML5, CSS3, JavaScript puro, Bootstrap 5
- **Base de Datos**: SQLAlchemy con MariaDB
- **Autenticación**: JWT tokens
- **Documentación**: OpenAPI/Swagger

## Roles y Permisos

### 1. Administrador
- **Permisos**: Acceso total al sistema
- **Funcionalidades**:
  - Gestión de usuarios y roles
  - Configuración del sistema
  - Supervisión general
  - Acceso a todos los reportes
  - Gestión de permisos

### 2. Responsable de Planificación
- **Permisos**: Gestión de PPR y monitoreo
- **Funcionalidades**:
  - Carga de definiciones de Programas Presupuestales por Resultado desde Excel
  - Asignación de responsables a cada PPR
  - Monitoreo de avance físico y presupuestal
  - Supervisión de actualizaciones de metas
  - Generación de reportes

### 3. Responsable de PPR
- **Permisos**: Gestión de su PPR asignado
- **Funcionalidades**:
  - Actualización de metas y avances físicos de su Programa Presupuestal por Resultado
  - Visualización de su PPR asignado
  - Notificación automática al responsable de presupuesto al modificar metas
  - Visualización de su informe de avance

## Logging y Seguimiento

- **Sistema de Logging**: Implementación de logging en archivo de texto plano
- **Archivo de Log**: `logs/error.log` para seguimiento de errores
- **Formato de Log**: Fecha, hora, nivel de error, descripción y traza del error
- **Rotación de Logs**: Implementación de rotación para manejo eficiente del espacio
- **Monitoreo**: Seguimiento de errores y eventos importantes en tiempo de ejecución

## Instalación

### Para Windows (Desarrollo)

1. Ejecuta el script de configuración:
   ```
   setup_windows.bat
   ```

2. Activa el entorno virtual:
   ```
   call venv\Scripts\activate.bat
   ```

3. Inicia el servidor:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Para Linux (Desarrollo y Producción)

1. Ejecuta el script de configuración:
   ```
   ./setup_linux.sh
   ```

2. Activa el entorno virtual:
   ```
   source venv/bin/activate
   ```

3. Inicia el servidor:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Configuración Manual

1. Crea un entorno virtual:
   ```
   python -m venv venv
   ```

2. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate.bat`
   - Linux: `source venv/bin/activate`

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   ```
   cp .env.example .env
   ```
   Edita `.env` con tus credenciales de base de datos

5. Crea la base de datos:
   ```
   python create_database.py
   ```

6. Crea las tablas:
   ```
   python create_tables.py
   ```

## Configuración Requerida

Antes de ejecutar el sistema, asegúrate de:

1. Tener MariaDB instalado y en ejecución
2. Actualizar las credenciales en el archivo `.env`
3. Crear la base de datos con el script `create_database.py`

### Posibles Problemas de Conexión

Si recibes un error como "Authentication plugin '..._client' not configured", puede ser necesario configurar MariaDB para usar el plugin de autenticación compatible. Generalmente, esto se resuelve asegurando que el usuario de la base de datos esté configurado para usar el método de autenticación mysql_native_password.

## Acceso al Sistema

- La API estará disponible en: `http://localhost:8000`
- La documentación de la API en: `http://localhost:8000/docs`
- La documentación alternativa en: `http://localhost:8000/redoc`

## Prueba del Servidor

Después de la instalación, puedes verificar que el servidor esté funcionando correctamente:

1. Asegúrate de tener el entorno virtual activado
2. Ejecuta: `uvicorn app.main:app --reload`
3. Abre tu navegador en `http://localhost:8000`
4. Deberías ver un mensaje de bienvenida
5. Visita `http://localhost:8000/docs` para ver la documentación de la API

## Estructura del Proyecto

```
monitor_ppr_v2/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── ppr.py
│   │   └── ceplan.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── ppr.py
│   │   ├── ceplan.py
│   │   └── permissions.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── ppr.py
│   │   └── ceplan.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   └── models.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── logger.py
│   └── static/
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── app.js
│       └── uploads/
│           ├── ppr/
│           └── ceplan/
├── logs/
│   └── error.log
├── tests/
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

## Próximos Pasos

1. Desarrollo completo de los módulos de API
2. Implementación de autenticación y autorización
3. Desarrollo de la lógica de negocio para PPR y CEPLAN
4. Implementación del frontend con Bootstrap/JS
5. Pruebas unitarias e integración
6. Documentación del API
7. Implementación del sistema de logging
8. Pruebas de integración
9. Documentación completa