# 🎫 Sistema de Tickets de Soporte (Help Desk)

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Socket.io](https://img.shields.io/badge/Socket.io-Real--Time-010101?style=for-the-badge&logo=socket.io&logoColor=white)

> **Un sistema moderno, seguro y en tiempo real para la gestión eficiente de soporte técnico.**

---

## ✨ Características Principales

### 🚀 Gestión de Tickets

* **Ciclo de Vida Completo:** Crear, asignar, comentar, cerrar y reabrir tickets.
* **Prioridades y Categorías:** Clasificación inteligente para una atención eficiente.
* **Adjuntos Seguros:** Soporte para subir imágenes y documentos.

### 💬 Chat en Tiempo Real

* **Comunicación Instantánea:** Chat privado entre usuarios basado en WebSockets.
* **Estados de Usuario:** Indicadores visuales de **En Línea** (🟢) y **Fuera de Línea** (⚫) con actualizaciones en tiempo real.
* **Notificaciones:** Alertas visuales y contadores de mensajes no leídos.
* **Historial Persistente:** Los mensajes se guardan en base de datos.

### 🛡️ Seguridad Avanzada

* **Autenticación Robusta:** Login seguro con hash de contraseñas.
* **Control de Sesiones Estricto:**
  * ⏱️ **Timeout de 5 Minutos:** Cierre de sesión automático tras 5 minutos (contador estricto).
  * 🔄 **Auto-Redirect:** Redirección automática al login al expirar el tiempo.
* **Protección Total:**
  * 🔒 **CSRF Protection** en todos los formularios.
  * 🛡️ **Rate Limiting** para prevenir fuerza bruta (50 req/min en login).
  * 🧱 **Security Headers** (CSP, HSTS) implementados.

### 🎨 Experiencia de Usuario (UI/UX)

* **Diseño Moderno:** Interfaz limpia basada en Bootstrap 5.
* **Modo Oscuro:** 🌙 Switch integrado para alternar entre tema claro y oscuro.
* **Dashboard Interactivo:** Gráficos dinámicos con Chart.js.
* **Efectos Visuales:** Fondo de vórtice interactivo y preloader animado.

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Backend** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Lógica del servidor y API. |
| **Framework** | ![Flask](https://img.shields.io/badge/-Flask-000000?logo=flask&logoColor=white) | Framework web ligero y potente. |
| **Base de Datos** | ![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql&logoColor=white) | Almacenamiento relacional de datos. |
| **Real-Time** | ![Socket.io](https://img.shields.io/badge/-Socket.io-010101?logo=socket.io&logoColor=white) | Comunicación bidireccional para el chat. |
| **Frontend** | ![Bootstrap](https://img.shields.io/badge/-Bootstrap-7952B3?logo=bootstrap&logoColor=white) | Diseño responsivo y componentes UI. |
| **ORM** | ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white) | Gestión de base de datos orientada a objetos. |

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd ticket_system
```

### 2. Configurar Entorno Virtual

```bash
# Crear entorno
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Linux/Mac)
source .venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configuración (.env)

Crea un archivo `.env` en la raíz del proyecto (puedes copiar `.env.example`) y configura tus credenciales:

```env
SECRET_KEY=tu_clave_secreta_super_segura
DATABASE_URL=mysql+mysqlconnector://usuario:password@localhost/ticket_db
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_app_password
```

### 5. Inicializar Base de Datos

El sistema creará las tablas automáticamente al iniciar, pero puedes verificarlo ejecutando:

```bash
python verify_db_schema.py
```

### 6. Ejecutar el Servidor

```bash
python run.py
```

📍 Accede a la aplicación en: `http://127.0.0.1:5000`

---

## 👥 Roles de Usuario

| Rol | Permisos |
| :--- | :--- |
| 👑 **Administrador** | Acceso total. Gestión de usuarios, ver todos los tickets, reportes globales. |
| 🛠️ **Técnico** | Ver y gestionar tickets asignados, cambiar estados, agregar comentarios técnicos. |
| 👤 **Usuario** | Crear tickets, ver estado de sus propios tickets, chatear con soporte. |

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - siéntete libre de usarlo y modificarlo.

---

<div align="center">
  <sub>Desarrollado con ❤️ y mucho ☕</sub>
</div>
