# 🎫 Sistema de Tickets de Soporte (Help Desk)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Socket.io](https://img.shields.io/badge/Socket.io-Real--Time-010101?style=for-the-badge&logo=socket.io&logoColor=white)

> **Un sistema moderno, seguro y en tiempo real para la gestión eficiente de soporte técnico.**

---

## ⚡ Instalación Rápida

> [!TIP]
> **¿Primera vez?** Usa el script de instalación automatizada:
> ```powershell
> .\setup.ps1
> ```
> O consulta la [Guía de Instalación Completa](INSTALL.md) para instalación paso a paso.

### Requisitos

- ✅ **Python 3.10+ (64-bit recomendado)**
- ✅ MySQL 8.0+
- ✅ Git

> [!WARNING]
> **Python 32-bit:** Las exportaciones a Excel/CSV (pandas) pueden no funcionar con Python de 32 bits. **Se recomienda encarecidamente usar Python 64-bit**.

### Quick Start (Windows)

```powershell
# 1. Verificar Python
py scripts/check_python.py

# 2. Crear entorno virtual
py -3.10 -m venv .venv

# 3. Activar entorno
.venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar .env
Copy-Item .env.example .env
# Edita .env y genera SECRET_KEY con: py scripts/generate_secret_key.py

# 6. Crear base de datos
py -c "import mysql.connector; conn = mysql.connector.connect(host='127.0.0.1', user='root', password=''); cursor = conn.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS ticket_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'); conn.close();"

# 7. Inicializar BD (crea tablas + admin)
py scripts/init_database.py

# 8. Ejecutar servidor
py run.py
```

📍 Accede a: **http://127.0.0.1:5000** (Usuario: `admin` / Contraseña: `admin123`)

---

## ✨ Características Principales

### 🚀 Gestión de Tickets

* **Ciclo de Vida Completo:** Crear, asignar, comentar, cerrar y reabrir tickets.
* **Prioridades y Categorías:** Clasificación inteligente para una atención eficiente.
* **Adjuntos Seguros:** Soporte para subir imágenes y documentos.
* **Exportación de Reportes:** Exportar a Excel, CSV y PDF (requiere Python 64-bit).

### 💬 Chat en Tiempo Real

* **Comunicación Instantánea:** Chat privado entre usuarios basado en WebSockets.
* **Estados de Usuario:** Indicadores visuales de **En Línea** (🟢) y **Fuera de Línea** (⚫).
* **Notificaciones:** Alertas visuales y contadores de mensajes no leídos.
* **Historial Persistente:** Los mensajes se guardan en base de datos.

### 🛡️ Seguridad Avanzada

* **Autenticación Robusta:** Login seguro con hash de contraseñas.
* **Control de Sesiones:** Timeout de 5 minutos con redirección automática.
* **Protección Total:**
  * 🔒 **CSRF Protection** en todos los formularios
  * 🛡️ **Rate Limiting** para prevenir ataques de fuerza bruta
  * 🧱 **Security Headers** (CSP, HSTS)
  * 🧹 **Sanitización HTML** para prevenir XSS

### 🎨 Experiencia de Usuario

* **Diseño Moderno:** Interfaz limpia basada en Bootstrap 5
* **Modo Oscuro:** 🌙 Switch integrado para alternar entre temas
* **Dashboard Interactivo:** Gráficos dinámicos con Chart.js
* **Efectos Visuales:** Animaciones y transiciones suaves

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Lógica del servidor y API |
| **Framework** | ![Flask](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white) | Framework web ligero y potente |
| **Base de Datos** | ![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql&logoColor=white) | Almacenamiento relacional de datos |
| **Real-Time** | ![Socket.io](https://img.shields.io/badge/-Socket.io-010101?logo=socket.io&logoColor=white) | Comunicación bidireccional para el chat |
| **Frontend** | ![Bootstrap](https://img.shields.io/badge/-Bootstrap-7952B3?logo=bootstrap&logoColor=white) | Diseño responsivo y componentes UI |
| **ORM** | ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white) | Gestión de base de datos orientada a objetos |

---

## 📁 Estructura del Proyecto

```
sistema-tickets/
├── app/                    # Aplicación Flask
│   ├── models.py          # Modelos de base de datos
│   ├── routes/            # Rutas y vistas
│   ├── templates/         # Plantillas HTML
│   └── static/            # Archivos estáticos (CSS, JS, imágenes)
├── scripts/               # Scripts de utilidad
│   ├── check_python.py    # Verificar arquitectura de Python
│   ├── generate_secret_key.py  # Generar SECRET_KEY
│   ├── init_database.py   # Inicializar BD + crear admin
│   ├── reset_admin.py     # Resetear contraseña de admin
│   └── verify_db_schema.py  # Verificar esquema de BD
├── .env                   # Variables de entorno (NO subir a Git)
├── .env.example           # Plantilla de configuración
├── config.py              # Configuración de la aplicación
├── requirements.txt       # Dependencias de Python
├── run.py                 # Script para ejecutar el servidor
├── setup.ps1              # Script de instalación automatizada
├── INSTALL.md             # Guía de instalación detallada
└── README.md              # Este archivo
```

---

## 🔧 Scripts de Utilidad

Todos los scripts de utilidad están en la carpeta `scripts/`:

```powershell
# Verificar arquitectura de Python (32-bit vs 64-bit)
py scripts/check_python.py

# Generar SECRET_KEY aleatoria para .env
py scripts/generate_secret_key.py

# Inicializar base de datos (crear tablas + usuario admin)
py scripts/init_database.py

# Resetear contraseña del usuario admin
py scripts/reset_admin.py

# Verificar esquema de base de datos
py scripts/verify_db_schema.py

# Verificar configuración del sistema
py scripts/check_system.py
```

---

## 👥 Roles de Usuario

| Rol | Permisos |
| :--- | :--- |
| 👑 **Administrador** | Acceso total. Gestión de usuarios, ver todos los tickets, reportes globales. |
| 🛠️ **Técnico** | Ver y gestionar tickets asignados, cambiar estados, agregar comentarios. |
| 👤 **Usuario** | Crear tickets, ver estado de sus propios tickets, chatear con soporte. |

---

## 🚨 Troubleshooting

### ❌ Python 32-bit Detectado

Si `py scripts/check_python.py` muestra que tienes Python de 32 bits:

1. Descarga **Python 64-bit** desde https://www.python.org/downloads/
2. Busca: **"Windows installer (64-bit)"**
3. Durante la instalación, marca **"Add Python to PATH"**
4. Reinstala el proyecto siguiendo los pasos de instalación

### ❌ pandas no se instala

Si `pandas` falla al instalarse:

**Causa:** Python 32-bit no es compatible con pandas en versiones recientes.

**Solución:** Instala Python 64-bit (recomendado) o continúa sin pandas (las exportaciones Excel/CSV no funcionarán).

### ❌ Error: SECRET_KEY must be set

Verifica que tu archivo `.env` tenga:
```env
SECRET_KEY=tu_clave_generada_aqui
```

Genera una clave con:
```powershell
py scripts/generate_secret_key.py
```

### ❌ Error: Cannot connect to MySQL

Verifica que:
1. MySQL esté corriendo
2. Las credenciales en `.env` sean correctas
3. La base de datos `ticket_db` exista

### ❌ Error al mover archivos o permisos denegados

Si estás actualizando desde una versión anterior y algunos scripts ya están en `scripts/`, no te preocupes. El proyecto funcionará correctamente.

---

## 📖 Documentación Adicional

- **[INSTALL.md](INSTALL.md)** - Guía de instalación detallada paso a paso
- **[.env.example](.env.example)** - Plantilla de configuración con comentarios
- **Scripts de utilidad** - Todos los scripts están documentados en `scripts/`

---

## 🔐 Seguridad en Producción

> [!CAUTION]
> Antes de desplegar en producción:

1. ✅ Cambia `SECRET_KEY` por una clave aleatoria generada
2. ✅ Cambia `FLASK_ENV=production` en `.env`
3. ✅ Cambia la contraseña del usuario `admin`
4. ✅ Configura contraseña para tu base de datos MySQL
5. ✅ Usa HTTPS (no HTTP) para el servidor
6. ✅ Configura un servidor WSGI (Gunicorn, uWSGI)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - siéntete libre de usarlo y modificarlo.

---

<div align="center">
  <sub>Desarrollado con ❤️ y mucho ☕</sub>
</div>
