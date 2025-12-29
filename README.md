# 🎫 Sistema de Tickets de Soporte (Help Desk)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Socket.io](https://img.shields.io/badge/Socket.io-Real--Time-010101?style=for-the-badge&logo=socket.io&logoColor=white)

> **Sistema moderno, seguro y en tiempo real para gestión eficiente de soporte técnico con diseño Glassmorphism.**

---

## 📖 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Instalación Rápida](#-instalación-rápida)
- [Instalación Paso a Paso](#-instalación-paso-a-paso)
- [Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Roles de Usuario](#-roles-de-usuario)
- [Scripts de Utilidad](#-scripts-de-utilidad)
- [Troubleshooting](#-troubleshooting)
- [Documentación Adicional](#-documentación-adicional)
- [Seguridad en Producción](#-seguridad-en-producción)
- [Licencia](#-licencia)

---

## ✨ Características Principales

### 🎫 Gestión Completa de Tickets
* **Ciclo de Vida Total**: Crear, asignar, comentar, cerrar y reabrir tickets con facilidad
* **Prioridades y Estados**: Clasificación por prioridad (Alta/Media/Baja) y estados (Abierto/En Proceso/Cerrado)
* **Numeración Automática**: Formato `TKT-YYYY-NNNNN` con correlativo por año
* **Adjuntos Seguros**: Soporte para subir imágenes y documentos
* **Comentarios**: Sistema de hilos de conversación por ticket
* **Asignación Inteligente**: Asignar técnicos específicos a cada solicitud

### 💬 Chat en Tiempo Real
* **WebSockets**: Comunicación instantánea bidireccional con Socket.IO
* **Indicadores de Presencia**: Estados visuales (🟢 En Línea / ⚫ Fuera de Línea)
* **Ventanas Flotantes**: Chat privado entre usuarios con drag & drop
* **Historial Persistente**: Mensajes guardados en base de datos
* **Notificaciones Visuales**: Alertas de mensajes no leídos

### 📊 Reportes y Analítica
* **Dashboard Interactivo**: Gráficos dinámicos con Chart.js
* **Exportación Múltiple**:
  - 📗 **Excel** (.xlsx) con logo, filtros y formato profesional
  - 📄 **PDF** con logo y diseño imprimible
  - 📋 **CSV** UTF-8 para análisis de datos
* **Filtrado por Rol**: Cada usuario ve solo sus datos según permisos
* **Estadísticas en Tiempo Real**: Contadores de tickets por estado y prioridad

### 🛡️ Seguridad Avanzada
* **Autenticación Robusta**: 
  - Hash de contraseñas con PBKDF2 (Werkzeug)
  - Sesiones seguras con timeout de 5 minutos
* **Protección Completa**:
  - 🔒 **CSRF Protection** (Flask-WTF) en todos los formularios
  - 🛡️ **Rate Limiting** (2000 req/día, 500 req/hora)
  - 🧱 **Security Headers** (CSP, HSTS vía Flask-Talisman)
  - 🧹 **Sanitización HTML** para prevenir XSS
* **Auditoría Total**: Registro de todas las acciones críticas con IP y timestamp
* **Control de Acceso**: Sistema de roles (Admin/Técnico/Usuario) con permisos granulares

### 🎨 Experiencia de Usuario Premium
* **Diseño Glassmorphism**: Interfaz moderna con fondos translúcidos, blur y gradientes dinámicos
* **Dashboard Híbrido**: Sidebar colapsable + Topbar con búsqueda global
* **Modales AJAX**: Todas las operaciones sin recarga de página, flujo ultrarrápido
* **Iconografía Moderna**: Font Awesome 6 con más de 2000 iconos
* **Animaciones Fluidas**: Transiciones suaves en hover, click y navegación
* **Preloaders 3D**: Carga visual atractiva con cubos animados
* **Responsive Design**: Funcional en desktop y móvil

### ⚙️ Administración Flexible
* **Gestión de Usuarios**: CRUD completo con validación de contraseñas
* **Configuración del Sistema**:
  - Personalización de nombre del proyecto
  - Cambio de logo y favicon
  - Paleta de colores personalizable (dashboard cards)
* **Página de Perfil**: Actualización de foto de perfil con preview en tiempo real
* **Vista de Auditoría**: Registro detallado de eventos con filtros avanzados

---

## 📸 Capturas de Pantalla

> 💡 **Nota**: El sistema cuenta con un diseño moderno Glassmorphism totalmente funcional. Consulta `MIGRACION_DASHBOARD.md` para detalles técnicos del diseño.

---

## 🚀 Instalación Rápida

### Requisitos Previos

- ✅ **Python 3.10+** (64-bit **ALTAMENTE RECOMENDADO**)
- ✅ **MySQL 8.0+**
- ✅ **Git**

> [!WARNING]
> **Python 32-bit:** Las exportaciones a Excel/CSV (pandas) no funcionarán con Python de 32 bits. **Se recomienda encarecidamente usar Python 64-bit**.

### Instalación con Un Solo Comando (Windows PowerShell)

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

### Acceso Inicial

Una vez que el servidor esté corriendo:

1. Abre tu navegador en: **http://127.0.0.1:5000**
2. Inicia sesión con:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

> [!IMPORTANT]
> **Cambia la contraseña del admin** inmediatamente en producción desde tu perfil de usuario.

---

## 📋 Instalación Paso a Paso

Si prefieres hacerlo manualmente o necesitas más control:

### 1️⃣ Verificar Python

Ejecuta este script para verificar si tienes Python 64-bit:

```powershell
py scripts/check_python.py
```

Si detecta Python 32-bit, descarga **Python 64-bit** desde https://www.python.org/downloads/

### 2️⃣ Crear Entorno Virtual

```powershell
# Usar la versión 64-bit de Python
py -3.10 -m venv .venv
```

### 3️⃣ Activar Entorno Virtual

```powershell
.venv\Scripts\activate
```

Deberías ver `(.venv)` al inicio de tu línea de comandos.

### 4️⃣ Instalar Dependencias

```powershell
pip install -r requirements.txt
```

> 💡 **Nota**: La instalación puede tomar varios minutos. Si `pandas` falla, verifica que estés usando Python 64-bit.

### 5️⃣ Configurar Variables de Entorno

```powershell
# Copiar plantilla
Copy-Item .env.example .env

# Generar SECRET_KEY
py scripts/generate_secret_key.py
```

Abre el archivo `.env` en tu editor de texto favorito y:
- ✏️ Reemplaza `SECRET_KEY=your_secret_key_here` con la clave generada
- ✏️ Configura `DB_PASSWORD` si tu MySQL tiene contraseña
- ✏️ (Opcional) Configura credenciales de email para recuperación de contraseñas

**Ejemplo de .env configurado:**
```env
SECRET_KEY=tu_clave_generada_super_secreta_aqui
FLASK_ENV=development
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
DB_NAME=ticket_db
```

### 6️⃣ Crear Base de Datos

**Opción A:** Usando Python (Recomendado)
```powershell
py -c "import mysql.connector; conn = mysql.connector.connect(host='127.0.0.1', user='root', password=''); cursor = conn.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS ticket_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'); conn.close(); print('✅ Base de datos creada')"
```

**Opción B:** Usando MySQL CLI
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS ticket_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 7️⃣ Inicializar Base de Datos

Este comando crea todas las tablas y el usuario administrador:

```powershell
py scripts/init_database.py
```

Verás un mensaje confirmando que las tablas y el usuario admin fueron creados.

### 8️⃣ Ejecutar Servidor de Desarrollo

```powershell
py run.py
```

Verás un mensaje similar a:
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
```

🎉 **¡Listo!** Accede a http://127.0.0.1:5000 con **admin**/**admin123**

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Versión | Descripción |
| :--- | :--- | :---: | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | 3.10+ | Lógica del servidor y API |
| **Framework Web** | ![Flask](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white) | 3.0+ | Framework web ligero y potente |
| **Base de Datos** | ![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql&logoColor=white) | 8.0+ | Almacenamiento relacional de datos |
| **ORM** | ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white) | 2.x | Gestión de BD orientada a objetos |
| **Real-Time** | ![Socket.io](https://img.shields.io/badge/-Socket.io-010101?logo=socket.io&logoColor=white) | 5.3+ | Comunicación bidireccional (chat) |
| **Frontend CSS** | Vanilla CSS | Custom | Variables CSS + Glassmorphism |
| **Frontend JS** | Vanilla JavaScript | ES6+ | Fetch API, DOM manipulation |
| **Iconos** | ![Font Awesome](https://img.shields.io/badge/-Font_Awesome-339AF0?logo=fontawesome&logoColor=white) | 6.5.1 | 2000+ iconos vectoriales |
| **Gráficos** | Chart.js | 3.x | Gráficos interactivos del dashboard |
| **Notificaciones** | SweetAlert2 | Latest | Modales y alertas estilizadas |
| **Seguridad** | Flask-WTF, Talisman, Limiter | - | CSRF, Headers, Rate Limiting |
| **Email** | Flask-Mailman | 1.0+ | Envío de correos (recuperación pwd) |
| **Exportación** | pandas, openpyxl, FPDF | - | Excel, CSV, PDF |

---

## 📁 Estructura del Proyecto

```
sistema-tickets/
│
├── app/                              # Aplicación Flask principal
│   ├── __init__.py                  # Factory app + extensiones
│   ├── models.py                    # Modelos BD (User, Ticket, Comment, etc.)
│   │
│   ├── routes/                      # Blueprints (módulos de rutas)
│   │   ├── auth.py                 # Autenticación
│   │   ├── main.py                 # Dashboard, tickets, reportes
│   │   ├── admin.py                # Gestión de usuarios, configuración
│   │   └── chat.py                 # WebSocket handlers para chat
│   │
│   ├── templates/                   # Plantillas Jinja2 HTML
│   │   ├── layouts/                # Layouts base
│   │   ├── components/             # Componentes reutilizables (sidebar, topbar)
│   │   ├── dashboard.html          # Página principal
│   │   ├── profile.html            # Perfil de usuario
│   │   ├── tickets/                # Gestión de tickets
│   │   ├── admin/                  # Administración (users, settings, audit)
│   │   └── reports/                # Centro de reportes
│   │
│   ├── static/                      # Archivos estáticos
│   │   ├── css/
│   │   │   ├── main.css           # Estilos globales + variables CSS
│   │   │   └── tickets-page.css   # Estilos específicos
│   │   ├── js/
│   │   │   └── chat-manager.js    # Gestión de chat
│   │   ├── images/                # Imágenes estáticas
│   │   └── uploads/               # Archivos subidos por usuarios
│   │
│   └── utils/                       # Helpers y utilidades
│       ├── __init__.py             # Decoradores (admin_required, etc.)
│       ├── alerts.py               # Sistema de mensajes flash
│       └── audit.py                # log_audit() para eventos
│
├── scripts/                         # Scripts de utilidad
│   ├── init_database.py            # Crear tablas + admin
│   ├── check_python.py             # Verificar arquitectura Python
│   ├── generate_secret_key.py      # Generar SECRET_KEY
│   ├── reset_admin.py              # Resetear contraseña admin
│   └── verify_db_schema.py         # Verificar esquema BD
│
├── config.py                        # Configuración de Flask
├── run.py                           # Servidor de desarrollo
├── run_production.py                # Servidor de producción
├── wsgi.py                          # Entry point WSGI
├── requirements.txt                 # Dependencias Python
├── .env                             # Variables de entorno (NO subir a Git)
├── .env.example                     # Plantilla de .env
├── setup.ps1                        # Script de instalación automatizada
│
├── README.md                        # 👈 Este archivo
├── Context.md                       # Documentación técnica para IA/devs
└── MIGRACION_DASHBOARD.md           # Plan de migración a diseño moderno
```

---

## 👥 Roles de Usuario

| Rol | Icono | Permisos |
| :--- | :---: | :--- |
| **👑 Administrador** | 🔧 | • Acceso total al sistema<br>• Gestión de usuarios (crear, editar, eliminar)<br>• Ver todos los tickets<br>• Configuración del sistema (logos, colores)<br>• Acceso a auditoría completa<br>• Exportar reportes globales |
| **🛠️ Técnico** | 🔨 | • Ver y gestionar tickets asignados<br>• Cambiar estados de tickets<br>• Agregar comentarios<br>• Chat con usuarios<br>• Exportar reportes de sus tickets |
| **👤 Usuario** | 👨 | • Crear nuevos tickets<br>• Ver estado de sus propios tickets<br>• Comentar en sus tickets<br>• Chat con soporte<br>• Exportar reportes de sus tickets |

---

## 🔧 Scripts de Utilidad

Todos los scripts están en la carpeta `scripts/`. Ejecútalos con:

```powershell
# Verificar arquitectura de Python (32-bit vs 64-bit)
py scripts/check_python.py

# Generar SECRET_KEY aleatoria para .env
py scripts/generate_secret_key.py

# Inicializar base de datos (crear tablas + usuario admin)
py scripts/init_database.py

# Resetear contraseña del usuario admin a 'admin123'
py scripts/reset_admin.py

# Verificar esquema de base de datos
py scripts/verify_db_schema.py

# Verificar configuración completa del sistema
py scripts/check_system.py
```

---

## 🚨 Troubleshooting

### ❌ Error: Python 32-bit Detectado

**Síntoma**: `py scripts/check_python.py` muestra que tienes Python de 32 bits, o `pandas` falla al instalarse.

**Solución**:
1. Descarga **Python 64-bit** desde https://www.python.org/downloads/
2. Busca: **"Windows installer (64-bit)"**
3. Durante la instalación, marca **"Add Python to PATH"**
4. Reinstala el proyecto siguiendo los pasos de instalación

### ❌ Error: pandas no se instala

**Causa**: Python 32-bit no es compatible con pandas en versiones recientes.

**Opciones**:
- **Opción 1 (Recomendada)**: Instala Python 64-bit
- **Opción 2**: Continúa sin pandas (el sistema funcionará, pero las exportaciones Excel/CSV no estarán disponibles)

### ❌ Error: SECRET_KEY must be set

**Solución**:
1. Verifica que tu archivo `.env` exista en el directorio raíz del proyecto
2. Genera una clave ejecutando:
   ```powershell
   py scripts/generate_secret_key.py
   ```
3. Copia la clave generada y pégala en `.env`:
   ```env
   SECRET_KEY=tu_clave_generada_aqui
   ```

### ❌ Error: Cannot connect to MySQL

**Solución**:
1. Verifica que MySQL esté corriendo:
   - Abre MySQL Workbench o Administrador de Servicios de Windows
   - Busca el servicio "MySQL80" y asegúrate de que esté iniciado
2. Verifica las credenciales en `.env`:
   ```env
   DB_HOST=127.0.0.1
   DB_USER=root
   DB_PASSWORD=tu_password_aqui  # Deja vacío si no tienes contraseña
   DB_NAME=ticket_db
   ```
3. Verifica que la base de datos `ticket_db` exista:
   ```bash
   mysql -u root -p -e "SHOW DATABASES;"
   ```

### ❌ Error: ModuleNotFoundError

**Síntoma**: `ModuleNotFoundError: No module named 'flask'` (o similar)

**Solución**:
1. Asegúrate de haber activado el entorno virtual:
   ```powershell
   .venv\Scripts\activate
   ```
2. Verifica que veas `(.venv)` al inicio de tu prompt
3. Reinstala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

### ❌ El servidor no se recarga automáticamente al guardar archivos

**Solución**:
- **Backend (Python)**: El servidor con `debug=True` en `run.py` ya se recarga automáticamente cuando modificas archivos `.py`. Revisa la consola para confirmarlo.
- **Frontend (HTML/CSS/JS)**: Flask no refresca el navegador automáticamente. Debes recargar manualmente con `F5` o `Ctrl+R`, o usar una extensión de navegador como **LiveReload**.

---

## 📖 Documentación Adicional

- **[Context.md](Context.md)** - Documentación técnica completa para IA y desarrolladores (arquitectura, modelos, diseño, convenciones)
- **[MIGRACION_DASHBOARD.md](MIGRACION_DASHBOARD.md)** - Plan detallado de migración a diseño Glassmorphism, patrón de modales, endpoints JSON
- **[.env.example](.env.example)** - Plantilla de configuración con comentarios detallados

---

## 🔐 Seguridad en Producción

> [!CAUTION]
> **Antes de desplegar en producción**, realiza TODAS estas configuraciones:

### Configuración Obligatoria

1. ✅ **SECRET_KEY**: Genera una nueva clave aleatoria y **NUNCA la compartas**
   ```powershell
   py scripts/generate_secret_key.py
   ```

2. ✅ **Contraseña de Admin**: Cambia `admin123` inmediatamente desde tu perfil

3. ✅ **Variables de Entorno**: Edita `.env` y configura:
   ```env
   FLASK_ENV=production
   DB_PASSWORD=contraseña_segura_aqui
   ```

4. ✅ **Base de Datos**: Configura contraseña para MySQL y restringe acceso remoto

5. ✅ **HTTPS**: Usa certificado SSL/TLS válido (Let's Encrypt es gratuito)

6. ✅ **Servidor WSGI**: Usa Gunicorn o uWSGI detrás de Nginx:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
   ```

### Recomendaciones Adicionales

- 🔒 Habilita `force_https=True` en Talisman (archivo `app/__init__.py`)
- 🔒 Configura firewall para permitir solo puertos 80, 443
- 🔒 Implementa backups automáticos diarios de la base de datos
- 🔒 Monitorea logs de intentos de login fallidos
- 🔒 Configura Rate Limiting más estricto para producción
- 🔒 Usa variables de entorno seguras (nunca hardcodear contraseñas)

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** - siéntete libre de usarlo y modificarlo.

```
MIT License

Copyright (c) 2024 Alvaro Guerra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Agradecimientos

- Comunidad de Flask por el excelente framework
- Font Awesome por la iconografía
- Chart.js por los gráficos interactivos
- SweetAlert2 por las notificaciones elegantes
- Todos los contribuidores de las librerías open-source utilizadas

---

<div align="center">
  <sub>Desarrollado con ❤️ y mucho ☕ en colaboración con Alvaro Guerra</sub>
  <br>
  <sub>Diseño moderno implementado con asistencia de Antigravity AI</sub>
</div>
