# 🚀 Guía de Instalación Rápida - Sistema de Tickets

## Requisitos Previos

- ✅ Python 3.10+ (**64-bit recomendado**)
- ✅ MySQL 8.0+
- ✅ Git (para clonar el repositorio)

> [!WARNING]
> **Python 32-bit:** Si usas Python de 32 bits, las exportaciones a Excel/CSV pueden no funcionar. Se recomienda **Python 64-bit**.

---

## 🎯 Instalación con Un Solo Comando (Windows)

Copia y pega todo este bloque en **PowerShell**:

```powershell
# === INSTALACIÓN AUTOMÁTICA - SISTEMA DE TICKETS ===

# 1. Verificar Python (64-bit recomendado)
py scripts/check_python.py

# 2. Crear entorno virtual con Python 64-bit
py -3.10 -m venv .venv

# 3. Activar entorno virtual
.venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar archivo .env
Copy-Item .env.example .env
Write-Host "`n⚠️  IMPORTANTE: Edita el archivo .env antes de continuar" -ForegroundColor Yellow
Write-Host "  1. Abre .env en tu editor" -ForegroundColor Cyan
Write-Host "  2. Genera SECRET_KEY ejecutando: py scripts/generate_secret_key.py" -ForegroundColor Cyan
Write-Host "  3. Copia la clave generada al archivo .env" -ForegroundColor Cyan
Read-Host "`nPresiona Enter cuando hayas configurado .env"

# 6. Crear base de datos MySQL
py -c "import mysql.connector; conn = mysql.connector.connect(host='127.0.0.1', user='root', password=''); cursor = conn.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS ticket_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'); conn.close(); print('✅ Base de datos creada')"

# 7. Inicializar base de datos (crear tablas + admin)
py scripts/init_database.py

# 8. ¡Listo! Iniciar servidor
Write-Host "`n🎉 ¡Instalación completada!" -ForegroundColor Green
Write-Host "`nPara iniciar el servidor ejecuta:" -ForegroundColor Cyan
Write-Host "  py run.py" -ForegroundColor White
```

---

## 📋 Instalación Paso a Paso

Si prefieres hacerlo manualmente, sigue estos pasos:

### 1. Verificar Python

```powershell
py scripts/check_python.py
```

Este script verifica si tienes Python 64-bit instalado.

### 2. Crear Entorno Virtual

```powershell
# Usar la versión 64-bit de Python
py -3.10 -m venv .venv
```

### 3. Activar Entorno Virtual

```powershell
.venv\Scripts\activate
```

Deberías ver `(.venv)` al inicio de tu línea de comandos.

### 4. Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

```powershell
# Copiar plantilla
Copy-Item .env.example .env

# Generar SECRET_KEY
py scripts/generate_secret_key.py
```

Abre el archivo `.env` y:
- Reemplaza `SECRET_KEY` con la clave generada
- Configura `DB_PASSWORD` si tu MySQL tiene contraseña
- (Opcional) Configura credenciales de email

### 6. Crear Base de Datos

**Opción A:** Usando Python
```powershell
py -c "import mysql.connector; conn = mysql.connector.connect(host='127.0.0.1', user='root', password=''); cursor = conn.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS ticket_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'); conn.close(); print('✅ Base de datos creada')"
```

**Opción B:** Usando MySQL CLI
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS ticket_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 7. Inicializar Base de Datos

Este comando crea todas las tablas y el usuario admin:

```powershell
py scripts/init_database.py
```

### 8. Ejecutar Servidor

```powershell
py run.py
```

---

## 🌐 Acceso Inicial

Una vez que el servidor esté corriendo:

1. Abre tu navegador en: **http://127.0.0.1:5000**
2. Inicia sesión con:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

> [!IMPORTANT]
> **Cambia la contraseña del admin** inmediatamente en producción desde la configuración de perfil.

---

## 🛠️ Troubleshooting

### ❌ Error: Python 32-bit

Si ves advertencias sobre Python 32-bit:

1. Descarga **Python 64-bit** desde https://www.python.org/downloads/
2. Busca: **"Windows installer (64-bit)"**
3. Durante la instalación, marca **"Add Python to PATH"**
4. Reinstala siguiendo los pasos anteriores

### ❌ Error: pandas no se instala

Si `pandas` falla al instalarse y tienes Python 32-bit:

**Opción 1 (Recomendada):** Instala Python 64-bit

**Opción 2:** Continúa sin pandas (las exportaciones Excel/CSV no funcionarán, pero el resto del sistema sí)

### ❌ Error: No se puede conectar a MySQL

Verifica que:
1. MySQL esté corriendo (abre MySQL Workbench o Administrador de Sesiones)
2. Las credenciales en `.env` sean correctas
3. La base de datos `ticket_db` exista

### ❌ Error: SECRET_KEY must be set

Revisa que tu archivo `.env` tenga la variable `SECRET_KEY` configurada correctamente.

---

## 📞 Más Ayuda

Para más detalles, consulta el [README.md](README.md) principal del proyecto.
