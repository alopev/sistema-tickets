# ====================================================================
# Script de Instalación Automatizada - Sistema de Tickets
# ====================================================================
# Este script configura automáticamente el proyecto completo
#
# Uso: .\setup.ps1
# ====================================================================

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "🎫 SISTEMA DE TICKETS - Instalación Automatizada" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# ===========================
# PASO 1: Verificar Python
# ===========================
Write-Host "📌 Paso 1/8: Verificando Python..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path "scripts/check_python.py") {
    py scripts/check_python.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        $continue = Read-Host "Python 32-bit detectado. ¿Continuar de todos modos? (S/N)"
        if ($continue -ne "S" -and $continue -ne "s") {
            Write-Host "Instalación cancelada. Instala Python 64-bit y vuelve a intentar." -ForegroundColor Red
            exit
        }
    }
} else {
    Write-Host "⚠️  Advertencia: No se pudo verificar Python" -ForegroundColor Yellow
}

Write-Host ""
$continue = Read-Host "¿Continuar con la instalación? (S/N)"
if ($continue -ne "S" -and $continue -ne "s") {
    Write-Host "Instalación cancelada." -ForegroundColor Red
    exit
}

# ===========================
# PASO 2: Crear entorno virtual
# ===========================
Write-Host ""
Write-Host "📌 Paso 2/8: Creando entorno virtual..." -ForegroundColor Yellow

if (Test-Path ".venv") {
    Write-Host "⚠️  El directorio .venv ya existe" -ForegroundColor Yellow
    $recreate = Read-Host "¿Recrear el entorno virtual? (S/N)"
    if ($recreate -eq "S" -or $recreate -eq "s") {
        Write-Host "Eliminando entorno virtual antiguo..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
        
        Write-Host "Creando nuevo entorno virtual..." -ForegroundColor Cyan
        py -3.10 -m venv .venv
    }
} else {
    Write-Host "Creando entorno virtual..." -ForegroundColor Cyan
    py -3.10 -m venv .venv
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al crear entorno virtual" -ForegroundColor Red
    Write-Host "Verifica que Python esté instalado correctamente" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Entorno virtual creado" -ForegroundColor Green

# ===========================
# PASO 3: Activar entorno
# ===========================
Write-Host ""
Write-Host "📌 Paso 3/8: Activando entorno virtual..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1
Write-Host "✅ Entorno activado" -ForegroundColor Green

# ===========================
# PASO 4: Instalar dependencias
# ===========================
Write-Host ""
Write-Host "📌 Paso 4/8: Instalando dependencias..." -ForegroundColor Yellow
Write-Host "(Esto puede tomar varios minutos...)" -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Algunas dependencias pueden haber fallado" -ForegroundColor Yellow
    Write-Host "Si pandas falló, es probable que tengas Python 32-bit" -ForegroundColor Yellow
    Write-Host "Las exportaciones Excel/CSV no funcionarán, pero el resto sí" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "¿Continuar de todos modos? (S/N)"
    if ($continue -ne "S" -and $continue -ne "s") {
        exit 1
    }
} else {
    Write-Host "✅ Dependencias instaladas" -ForegroundColor Green
}

# ===========================
# PASO 5: Configurar .env
# ===========================
Write-Host ""
Write-Host "📌 Paso 5/8: Configurando archivo .env..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Write-Host "✅ El archivo .env ya existe" -ForegroundColor Green
    $reconfigure = Read-Host "¿Quieres reconfigurarlo? (S/N)"
    if ($reconfigure -eq "S" -or $reconfigure -eq "s") {
        Copy-Item .env.example .env -Force
        Write-Host "✅ Archivo .env recreado desde plantilla" -ForegroundColor Green
    }
} else {
    Copy-Item .env.example .env
    Write-Host "✅ Archivo .env creado desde .env.example" -ForegroundColor Green
}

Write-Host ""
Write-Host "⚠️  CONFIGURACIÓN REQUERIDA:" -ForegroundColor Yellow
Write-Host "   El archivo .env necesita ser configurado antes de continuar" -ForegroundColor White
Write-Host ""

$generateKey = Read-Host "¿Generar SECRET_KEY ahora? (S/N)"
if ($generateKey -eq "S" -or $generateKey -eq "s") {
    Write-Host ""
    py scripts/generate_secret_key.py
    Write-Host ""
    Write-Host "Copia la SECRET_KEY generada arriba y pégala en el archivo .env" -ForegroundColor Cyan
    Write-Host "Presiona Enter cuando hayas terminado de editar .env" -ForegroundColor Cyan
    Read-Host
}

# ===========================
# PASO 6: Configurar MySQL
# ===========================
Write-Host ""
Write-Host "📌 Paso 6/8: Configurando base de datos MySQL..." -ForegroundColor Yellow
Write-Host ""

$dbHost = Read-Host "Host de MySQL (Enter para usar: 127.0.0.1)"
if ([string]::IsNullOrWhiteSpace($dbHost)) { $dbHost = "127.0.0.1" }

$dbUser = Read-Host "Usuario de MySQL (Enter para usar: root)"
if ([string]::IsNullOrWhiteSpace($dbUser)) { $dbUser = "root" }

$dbPassSecure = Read-Host "Contraseña de MySQL (Enter si no tiene)" -AsSecureString
$dbPass = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassSecure)
)

# Crear base de datos
Write-Host ""
Write-Host "Creando base de datos ticket_db..." -ForegroundColor Cyan
try {
    $createDbScript = @"
import mysql.connector
try:
    conn = mysql.connector.connect(host='$dbHost', user='$dbUser', password='$dbPass')
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS ticket_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
    conn.close()
    print('✅ Base de datos creada exitosamente')
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)
"@
    
    py -c $createDbScript
    
    if ($LASTEXITCODE -ne 0) {
        throw "Error al crear base de datos"
    }
    
} catch {
    Write-Host "❌ Error al crear base de datos" -ForegroundColor Red
    Write-Host "Verifica que:" -ForegroundColor Yellow
    Write-Host "  1. MySQL esté corriendo" -ForegroundColor White
    Write-Host "  2. Las credenciales sean correctas" -ForegroundColor White
    Write-Host ""
    $continue = Read-Host "¿Continuar de todos modos? (S/N)"
    if ($continue -ne "S" -and $continue -ne "s") {
        exit 1
    }
}

# ===========================
# PASO 7: Inicializar BD
# ===========================
Write-Host ""
Write-Host "📌 Paso 7/8: Inicializando base de datos (tablas + admin)..." -ForegroundColor Yellow
py scripts/init_database.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Error al inicializar base de datos" -ForegroundColor Red
    Write-Host "Revisa la configuración en .env y que MySQL esté corriendo" -ForegroundColor Yellow
    exit 1
}

# ===========================
# PASO 8: Finalización
# ===========================
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Para iniciar el servidor:" -ForegroundColor White
Write-Host "   .venv\Scripts\activate" -ForegroundColor Yellow
Write-Host "   py run.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Accede a la aplicación:" -ForegroundColor White
Write-Host "   http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Credenciales iniciales:" -ForegroundColor White
Write-Host "   Usuario:    admin" -ForegroundColor Yellow
Write-Host "   Contraseña: admin123" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  IMPORTANTE: Cambia la contraseña del admin en producción" -ForegroundColor Red
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
