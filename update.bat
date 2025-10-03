@echo off
setlocal

:: Ruta del script + destino
set "DEST=%~dp0app\static"

echo 📁 Destino: %DEST%
echo 📦 Instalando paquetes...

npm install bootstrap @fortawesome/fontawesome-free

if errorlevel 1 (
    echo ❌ Error al instalar paquetes. Abortando.
    pause
    exit /b 1
)

:: Crear carpetas de destino
mkdir "%DEST%\css" 2>nul
mkdir "%DEST%\js" 2>nul
mkdir "%DEST%\webfonts" 2>nul

:: Copiar Bootstrap CSS
if exist "node_modules\bootstrap\dist\css\bootstrap.min.css" (
    xcopy /I /Y "node_modules\bootstrap\dist\css\bootstrap.min.css" "%DEST%\css\" >nul
    echo ✅ Bootstrap CSS copiado.
) else (
    echo ❌ No se encontró: node_modules\bootstrap\dist\css\bootstrap.min.css
)

:: Copiar Bootstrap JS
if exist "node_modules\bootstrap\dist\js\bootstrap.bundle.min.js" (
    xcopy /I /Y "node_modules\bootstrap\dist\js\bootstrap.bundle.min.js" "%DEST%\js\" >nul
    echo ✅ Bootstrap JS copiado.
) else (
    echo ❌ No se encontró: node_modules\bootstrap\dist\js\bootstrap.bundle.min.js
)

:: Copiar Font Awesome CSS
if exist "node_modules\@fortawesome\fontawesome-free\css\all.min.css" (
    xcopy /I /Y "node_modules\@fortawesome\fontawesome-free\css\all.min.css" "%DEST%\css\fontawesome.min.css" >nul
    echo ✅ Font Awesome CSS copiado.
) else (
    echo ❌ No se encontró: node_modules\@fortawesome\fontawesome-free\css\all.min.css
)

:: Copiar fuentes de Font Awesome
if exist "node_modules\@fortawesome\fontawesome-free\webfonts" (
    xcopy /I /Y "node_modules\@fortawesome\fontawesome-free\webfonts\*" "%DEST%\webfonts\" >nul
    echo ✅ Fuentes de Font Awesome copiadas.
) else (
    echo ❌ No se encontró la carpeta: node_modules\@fortawesome\fontawesome-free\webfonts
)

echo.
echo 🎯 Proceso completado. Verifica la carpeta "%DEST%".
pause