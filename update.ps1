#Requires -Version 5.0

# Obtiene el directorio donde está este script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$DestDir = Join-Path $ScriptDir "app\static"

Write-Host "📁 Directorio del script: $ScriptDir" -ForegroundColor Cyan
Write-Host "📦 Destino: $DestDir" -ForegroundColor Cyan

# Crear estructura de destino
$Dirs = @(
    (Join-Path $DestDir "css"),
    (Join-Path $DestDir "js"),
    (Join-Path $DestDir "webfonts")
)
foreach ($dir in $Dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "✅ Creada carpeta: $dir" -ForegroundColor Green
    }
}

# Instalar paquetes
Write-Host "⬇️  Instalando Bootstrap y Font Awesome..." -ForegroundColor Yellow
npm install bootstrap @fortawesome/fontawesome-free

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al instalar paquetes. Abortando." -ForegroundColor Red
    exit 1
}

# Definir orígenes y destinos
$FilesToCopy = @(
    @{
        Source = "node_modules\bootstrap\dist\css\bootstrap.min.css"
        Dest   = Join-Path $DestDir "css\bootstrap.min.css"
    },
    @{
        Source = "node_modules\bootstrap\dist\js\bootstrap.bundle.min.js"
        Dest   = Join-Path $DestDir "js\bootstrap.bundle.min.js"
    },
    @{
        Source = "node_modules\@fortawesome\fontawesome-free\css\all.min.css"
        Dest   = Join-Path $DestDir "css\fontawesome.min.css"
    }
)

# Copiar archivos
foreach ($file in $FilesToCopy) {
    if (Test-Path $file.Source) {
        Copy-Item -Path $file.Source -Destination $file.Dest -Force
        Write-Host "✅ Copiado: $($file.Dest)" -ForegroundColor Green
    } else {
        Write-Host "❌ No encontrado: $($file.Source)" -ForegroundColor Red
    }
}

# Copiar fuentes de Font Awesome
$FontsSource = "node_modules\@fortawesome\fontawesome-free\webfonts\*"
$FontsDest = Join-Path $DestDir "webfonts"

if (Test-Path "node_modules\@fortawesome\fontawesome-free\webfonts") {
    Copy-Item -Path $FontsSource -Destination $FontsDest -Recurse -Force
    Write-Host "✅ Fuentes copiadas a: $FontsDest" -ForegroundColor Green
} else {
    Write-Host "❌ Carpeta de fuentes no encontrada: node_modules\@fortawesome\fontawesome-free\webfonts" -ForegroundColor Red
}

Write-Host "`n🎉 ¡Actualización completada!" -ForegroundColor Magenta
Write-Host "Los archivos están en: $DestDir" -ForegroundColor Cyan