# 🤖 Contexto del Proyecto - Sistema de Tickets (Help Desk)

> **Documento de Contexto Técnico** para comprensión por Inteligencia Artificial y desarrolladores.  
> Este archivo contiene una descripción exhaustiva de la arquitectura, tecnologías, diseño y visión del proyecto.

---

## 📋 Descripción General del Proyecto

**Sistema de Tickets de Soporte (Help Desk)** es una aplicación web completa para la gestión de tickets de soporte técnico, desarrollada con Flask (Python) y MySQL. El sistema permite a organizaciones gestionar solicitudes de soporte, asignar técnicos, comunicarse en tiempo real vía chat, y generar reportes, todo bajo un diseño moderno estilo "Glassmorphism" con experiencia de usuario fluida.

### Visión y Propósito

- **Objetivo Principal**: Centralizar y optimizar la gestión de solicitudes de soporte técnico en organizaciones.
- **Usuarios Objetivo**: Empresas pequeñas y medianas que necesitan un sistema de help desk sin complejidad excesiva.
- **Diferenciador**: Interfaz moderna con Glassmorphism, chat en tiempo real con WebSockets, y enfoque en seguridad y usabilidad.

---

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico Completo

#### Backend
- **Lenguaje**: Python 3.10+ (64-bit recomendado)
- **Framework Web**: Flask 3.0+
- **ORM**: SQLAlchemy 2.x
- **Base de Datos**: MySQL 8.0+ (UTF-8mb4)
- **Autenticación**: Flask-Login (sesiones basadas en cookies)
- **WebSockets**: Flask-SocketIO + eventlet (para chat en tiempo real)
- **Seguridad**:
  - Flask-WTF (CSRF Protection)
  - Flask-Limiter (Rate Limiting)
  - Flask-Talisman (Security Headers: CSP, HSTS)
  - Werkzeug (Password hashing con PBKDF2)
- **Email**: Flask-Mailman (soporte SMTP)
- **Exportación de Datos**:
  - pandas + openpyxl (Excel)
  - FPDF (PDF)

#### Frontend
- **CSS**: Vanilla CSS con variables CSS (`--var-name`) para tematización
- **JavaScript**: Vanilla JS (sin frameworks), uso extensivo de Fetch API
- **Diseño Visual**: Glassmorphism (fondos translúcidos, blur, gradientes)
- **Iconografía**: Font Awesome 6.5.1 (CDN)
- **Gráficos**: Chart.js 3.x (para dashboard)
- **Notificaciones**: SweetAlert2 (modales y alertas estilizadas)
- **Layout**: Sistema híbrido sidebar + topbar responsivo

#### Infraestructura de Desarrollo
- **Entorno Virtual**: venv (Python)
- **Gestión de Dependencias**: pip + requirements.txt
- **Variables de Entorno**: python-dotenv (.env file)
- **Debug Mode**: Flask debug server con auto-reload
- **Producción**: Gunicorn/uWSGI recomendados (no incluidos por defecto)

---

## 📁 Estructura de Carpetas y Archivos Clave

```
sistema-tickets/
│
├── app/                              # Módulo principal de la aplicación Flask
│   ├── __init__.py                  # Factory app + inicialización de extensiones
│   ├── models.py                    # Modelos de base de datos (User, Ticket, Comment, etc.)
│   │
│   ├── routes/                      # Blueprints (módulos de rutas)
│   │   ├── auth.py                 # Autenticación (login, register, reset password)
│   │   ├── main.py                 # Rutas principales (dashboard, tickets, reportes)
│   │   ├── admin.py                # Rutas administrativas (users, settings, audit logs)
│   │   └── chat.py                 # WebSocket handlers para chat en tiempo real
│   │
│   ├── templates/                   # Plantillas Jinja2 HTML
│   │   ├── layouts/
│   │   │   ├── base_layout.html   # Layout HTML base (head, scripts)
│   │   │   └── page_shell.html    # Shell con sidebar + topbar
│   │   ├── components/
│   │   │   ├── sidebar.html       # Navegación lateral
│   │   │   └── topbar.html        # Barra superior
│   │   ├── dashboard.html          # Página principal con estadísticas
│   │   ├── profile.html            # Perfil de usuario
│   │   ├── tickets/
│   │   │   ├── list.html          # Lista de tickets con modales CRUD
│   │   │   └── detail.html        # Vista detallada de ticket
│   │   ├── admin/
│   │   │   ├── users.html         # Gestión de usuarios
│   │   │   ├── audit_logs.html    # Registro de auditoría
│   │   │   └── system_settings.html # Configuración del sistema
│   │   └── reports/
│   │       └── index.html         # Centro de reportes (Excel, PDF, CSV)
│   │
│   ├── static/                      # Archivos estáticos
│   │   ├── css/
│   │   │   ├── main.css           # Estilos globales + variables CSS
│   │   │   └── tickets-page.css   # Estilos específicos de tickets
│   │   ├── js/
│   │   │   ├── chat-manager.js    # Gestión de chat en tiempo real
│   │   │   └── (otros scripts inline en templates)
│   │   ├── images/                # Imágenes estáticas
│   │   └── uploads/               # Archivos subidos por usuarios
│   │
│   └── utils/                       # Utilidades y helpers
│       ├── __init__.py             # Decoradores (admin_required, tech_required)
│       ├── alerts.py               # Sistema de mensajes flash custom
│       └── audit.py                # Función log_audit() para registro de eventos
│
├── scripts/                         # Scripts de utilidad y mantenimiento
│   ├── init_database.py            # Crear tablas + usuario admin inicial
│   ├── check_python.py             # Verificar arquitectura Python (32/64 bit)
│   ├── generate_secret_key.py      # Generar SECRET_KEY para .env
│   ├── reset_admin.py              # Resetear contraseña de admin
│   └── verify_db_schema.py         # Verificar integridad del esquema BD
│
├── config.py                        # Configuración de Flask (DB, mail, uploads)
├── run.py                           # Punto de entrada para desarrollo (debug=True)
├── run_production.py                # Punto de entrada para producción
├── wsgi.py                          # Entry point para servidores WSGI
├── requirements.txt                 # Dependencias Python
├── .env                             # Variables de entorno (SECRET_KEY, DB password)
├── .env.example                     # Plantilla de .env
├── setup.ps1                        # Script de instalación automatizada (Windows PowerShell)
├── README.md                        # Documentación principal para usuarios
├── INSTALL.md                       # Guía de instalación paso a paso
├── MIGRACION_DASHBOARD.md           # Plan de migración a diseño moderno
└── Context.md                       # Este archivo (contexto para IA)
```

---

## 💾 Modelos de Base de Datos

### User
- **Campos**: `id`, `username`, `email`, `password_hash`, `role`, `profile_picture`, `active`, `fs_uniquifier`, `last_seen`, `login_count`, `current_login_at`, `current_login_ip`, `last_login_at`, `last_login_ip`
- **Roles**: `admin`, `tecnico`, `usuario`
- **Relaciones**: 
  - `tickets_created` (tickets creados por el usuario)
  - `tickets_assigned` (tickets asignados al técnico)
  - `comments` (comentarios del usuario)
  - `messages_sent`, `messages_received` (chat)
  - `audit_logs` (eventos de auditoría)

### Ticket
- **Campos**: `id`, `ticket_number` (formato: TKT-YYYY-NNNNN), `title`, `description`, `status` (abierto/en_proceso/cerrado), `priority` (alta/media/baja), `created_at`, `created_by_id`, `assigned_to_id`, `attachment`
- **Relaciones**:
  - `created_by` → User
  - `assigned_to` → User
  - `comments` → Comment (one-to-many)

### Comment
- **Campos**: `id`, `content`, `created_at`, `user_id`, `ticket_id`
- **Relaciones**: Pertenece a `User` y `Ticket`

### ChatMessage
- **Campos**: `id`, `sender_id`, `receiver_id`, `content`, `timestamp`, `read`
- **Propósito**: Mensajería privada entre usuarios vía WebSockets
- **Relaciones**: `sender` → User, `receiver` → User

### AuditLog
- **Campos**: `id`, `user_id`, `action` (ej: 'ticket_created', 'user_edited', 'profile_updated'), `details`, `timestamp`, `ip_address`
- **Propósito**: Registro de auditoría de todas las acciones críticas
- **Función Helper**: `app/utils/audit.py:log_audit(action, details, user_id)`

### SystemSettings
- **Campos**: `id`, `project_name`, `logo_path`, `favicon_path`, `primary_color`, `secondary_color`, `card_total_color`, `card_open_color`, `card_process_color`, `card_closed_color`, `updated_at`
- **Propósito**: Configuración personalizable del sistema (nombre, colores, logos)
- **Singleton**: Solo existe una fila en esta tabla

---

## 🎨 Sistema de Diseño "Glassmorphism"

### Filosofía Visual
El proyecto migró de Bootstrap básico a un diseño custom moderno inspirado en **Glassmorphism**, caracterizado por:
- Fondos translúcidos con `backdrop-filter: blur()`
- Gradientes dinámicos (púrpura, cyan, verde)
- Sombras sutiles y profundidad visual
- Animaciones fluidas en hover y transiciones
- Background con partículas interactivas (Canvas)

### Variables CSS Globales (`main.css`)
```css
:root {
  /* Colores principales */
  --c-green: #16a34a;   /* Éxito */
  --c-purple: #a855f7;  /* Destacados */
  --c-amber: #f59e0b;   /* Advertencias */
  --c-red: #ef4444;     /* Errores */
  --c-cyan: #06b6d4;    /* Info */
  
  /* Glassmorphism */
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
  --blur-amount: 10px;
  
  /* Layout */
  --sidebar-width: 250px;
  --topbar-height: 60px;
  
  /* Tipografía */
  --font-body: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  --font-heading: 'Segoe UI', sans-serif;
}
```

### Componentes Clave

#### `.desktop-card`
Tarjeta glassmorphism principal para contenido:
```css
.desktop-card {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--blur-amount));
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

#### `.stat-mini`
Tarjetas de estadísticas pequeñas con iconos:
```html
<div class="stat-mini stat-green">
  <i class="fa-solid fa-check"></i>
  <span>Total: 42</span>
</div>
```

#### Modales
- **Overlay**: `position: fixed; inset: 0; z-index: 99999;`
- **Container**: Centrado con `backdrop-filter: blur()`
- **Tamaños**: 
  - `.modal-container` (800px) para vistas simples
  - `.modal-container-wide` (1000px) para formularios de 2 columnas

#### Badges
- **Estados de Ticket**: `.badge-abierto`, `.badge-en_proceso`, `.badge-cerrado`
- **Prioridades**: `.priority-alta`, `.priority-media`, `.priority-baja`
- **Roles**: `.role-admin`, `.role-tecnico`, `.role-usuario`

---

## 🔐 Sistema de Seguridad

### Autenticación y Autorización
1. **Login**:
   - Hash de contraseñas con `werkzeug.security.generate_password_hash()` (PBKDF2)
   - Sesiones gestionadas por Flask-Login
   - Timeout de sesión: 5 minutos de inactividad
   
2. **Decoradores de Rol**:
   - `@admin_required`: Solo administradores
   - `@tech_required`: Admin o técnicos
   - Implementados en `app/utils/__init__.py`

3. **CSRF Protection**:
   - Flask-WTF en todos los formularios
   - Tokens CSRF automáticos en templates

### Rate Limiting
- **Global**: 2000 requests/día, 500 requests/hora
- **Login**: Protección contra fuerza bruta
- Implementado con Flask-Limiter

### Security Headers (Flask-Talisman)
- **CSP (Content Security Policy)**: Restringe fuentes de scripts, estilos, fuentes
- **HSTS**: Fuerza HTTPS en producción
- **X-Frame-Options**: SAMEORIGIN (protección contra clickjacking)

### Auditoría
- Todos los cambios críticos se registran en `AuditLog`
- Eventos: login, ticket_created, user_edited, profile_updated, etc.
- IP y timestamp registrados
- Helper: `log_audit(action, details, user_id)`

---

## 🔄 Chat en Tiempo Real (WebSockets)

### Tecnologías
- **Backend**: Flask-SocketIO (eventlet)
- **Frontend**: Socket.IO client (CDN)
- **Protocolo**: WebSockets con fallback a polling

### Eventos WebSocket
1. **connect**: Usuario se conecta, se marca como online
2. **disconnect**: Usuario se desconecta, se marca como offline
3. **send_message**: Enviar mensaje privado
4. **receive_message**: Recibir mensaje privado
5. **get_online_users**: Obtener lista de usuarios en línea

### Gestión de Estado
- Estados de usuario: 🟢 Online (verde), ⚫ Offline (gris)
- `last_seen` actualizado en cada conexión/desconexión
- Ventanas de chat flotantes con drag & drop
- Notificaciones visuales de mensajes no leídos

---

## 📊 Sistema de Reportes

### Formatos de Exportación

#### Excel (.xlsx)
- **Tecnología**: pandas + openpyxl
- **Características**:
  - Logo de la empresa incrustado
  - Auto-filtros en columnas
  - Ajuste automático de ancho de columnas
  - Encabezados estilizados
- **Endpoint**: `/export/excel`
- **Requiere**: Python 64-bit

#### CSV (.csv)
- **Tecnología**: pandas
- **Encoding**: UTF-8 with BOM (compatibilidad Excel)
- **Endpoint**: `/export/csv`

#### PDF (.pdf)
- **Tecnología**: FPDF
- **Características**:
  - Logo incrustado
  - Tabla con bordes
  - Encabezados y pie de página
- **Endpoint**: `/export/pdf`

### Filtrado por Rol
- **Admin**: Ve todos los tickets
- **Técnico**: Solo tickets asignados a él
- **Usuario**: Solo tickets creados por él

---

## 🚀 Flujo de Operaciones AJAX

### Patrón de Modales CRUD
Todas las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en Tickets, Usuarios, etc., siguen este flujo:

1. **Apertura de Modal**:
   ```javascript
   function openModalName() {
       document.getElementById('modalName').classList.add('active');
       document.body.style.overflow = 'hidden';
   }
   ```

2. **Carga de Datos (para editar)**:
   ```javascript
   fetch(`/api/endpoint/${id}/details`)
       .then(res => res.json())
       .then(data => {
           // Popular campos del formulario
           document.getElementById('field').value = data.value;
       });
   ```

3. **Envío de Formulario**:
   ```javascript
   form.addEventListener('submit', (e) => {
       e.preventDefault();
       const formData = new FormData(form);
       
       fetch(endpoint, {
           method: 'POST',
           body: formData
       })
       .then(res => res.json())
       .then(data => {
           if (data.success) {
               closeModal();
               Swal.fire('Éxito!', data.message, 'success');
               setTimeout(() => location.reload(), 1500);
           } else {
               Swal.fire('Error', data.message, 'error');
           }
       });
   });
   ```

### Endpoints JSON Importantes
- `GET /tickets/<id>/details` → Detalles de ticket
- `GET /api/technicians` → Lista de técnicos disponibles
- `GET /admin/api/users/<id>/details` → Detalles de usuario
- `POST /admin/user/create` → Crear usuario (retorna JSON)
- `POST /admin/user/<id>/delete` → Eliminar usuario (retorna JSON)
- `POST /profile` (con header AJAX) → Actualizar foto de perfil

---

## 🧪 Testing y Mantenimiento

### Scripts de Mantenimiento
1. **`init_database.py`**: Crear todas las tablas y usuario admin
2. **`reset_admin.py`**: Resetear contraseña de admin a `admin123`
3. **`verify_db_schema.py`**: Verificar integridad de tablas
4. **`check_system.py`**: Verificar configuración completa
5. **`check_python.py`**: Verificar arquitectura Python

### Usuarios de Prueba Iniciales
- **Admin**: `admin` / `admin123`
- (Crear técnicos y usuarios desde panel de administración)

### Consideraciones de Testing
- **Navegadores soportados**: Chrome, Firefox, Edge (últimas versiones)
- **Responsive**: Diseñado para desktop, móvil es funcional pero no optimizado
- **Permisos**: Probar todos los flujos con diferentes roles

---

## 📦 Dependencias Clave (requirements.txt)

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-SocketIO==5.3.5
Flask-Mailman==1.0.0
Flask-WTF==1.2.1
Flask-Limiter==3.5.0
Flask-Talisman==1.1.0
mysql-connector-python==8.2.0
eventlet==0.33.3
pandas==2.1.4           # Requiere Python 64-bit
openpyxl==3.1.2
fpdf==1.7.2
python-dotenv==1.0.0
Werkzeug==3.0.1
PyJWT==2.8.0
```

---

## 🔮 Estado Actual del Proyecto (Diciembre 2024)

### Completado (≈85%)
- ✅ Dashboard con estadísticas y gráficos
- ✅ Gestión completa de tickets (CRUD)
- ✅ Gestión de usuarios (CRUD)
- ✅ Configuración del sistema (logos, colores)
- ✅ Chat en tiempo real
- ✅ Reportes (Excel, PDF, CSV)
- ✅ **Auditoría** (migrado a diseño moderno, con logging de eventos)
- ✅ **Perfil de usuario** (migrado, con actualización de foto)
- ✅ Sistema de seguridad completo

### En Progreso
- 🔄 Testing completo cross-browser
- 🔄 Documentación técnica detallada
- 🔄 Optimización de performance

### Pendiente
- ❌ Página de ayuda/FAQ
- ❌ Notificaciones push
- ❌ PWA (Service Worker)
- ❌ Multi-idioma (i18n)

---

## 📝 Convenciones de Código

### Python
- **Estilo**: PEP 8
- **Naming**: snake_case para funciones y variables
- **Blueprints**: Organización por módulos (`auth`, `main`, `admin`)
- **Docstrings**: Para funciones complejas

### JavaScript
- **Estilo**: camelCase para funciones y variables
- **Uso de `const`/`let`**: No usar `var`
- **Fetch API**: Para todas las peticiones AJAX
- **Event Listeners**: Usar delegación de eventos cuando sea posible

### CSS
- **Nomenclatura**: BEM adaptado (`.component-element--modifier`)
- **Variables**: Usar variables CSS para colores y medidas
- **Mobile-first**: Media queries para pantallas grandes

### Templates (Jinja2)
- **Herencia**: Todos extienden `layouts/page_shell.html` o `layouts/base_layout.html`
- **Includes**: Componentes reutilizables en `components/`
- **Filtros**: Usar filtros de Jinja2 para formateo de datos

---

## 🌐 Despliegue en Producción

### Recomendaciones
1. **Servidor WSGI**: Gunicorn o uWSGI detrás de Nginx
2. **Base de Datos**: MySQL en servidor dedicado
3. **Variables de Entorno**:
   - `FLASK_ENV=production`
   - `SECRET_KEY` generada con script
   - `DB_PASSWORD` configurada
4. **HTTPS**: Obligatorio con certificado SSL/TLS
5. **Backups**: Automatizados diarios de la BD
6. **Logging**: Configurar logs en archivo (no consola)

### Seguridad en Producción
- Cambiar contraseña de admin
- Habilitar HSTS en Talisman
- Configurar firewall (solo puertos 80, 443, 3306 si es necesario)
- Rate limiting más estricto
- Monitoreo de intentos de login fallidos

---

## 💡 Conceptos Clave para IA

Si eres una IA leyendo esto para entender cómo contribuir al proyecto:

1. **Patrón de Templates**: Siempre extender `page_shell.html`, usar componentes de `components/`, aplicar diseño glassmorphism.

2. **Modales AJAX**: Todos los formularios en modales con overlay, envío vía fetch, respuestas JSON del backend, SweetAlert para confirmaciones.

3. **Backend JSON**: Rutas POST/PUT/DELETE deben retornar `jsonify({'success': bool, 'message': str})` para compatibilidad con frontend AJAX.

4. **Auditoría**: Llamar `log_audit(action, details)` después de operaciones críticas (crear/editar/eliminar).

5. **Seguridad**: Siempre usar decoradores `@admin_required` o `@tech_required` en rutas protegidas.

6. **Estilos**: Seguir variables CSS de `main.css`, usar clases existentes antes de crear nuevas, mantener consistencia visual.

7. **Responsive**: Priorizar desktop, asegurar funcionalidad en móvil.

---

## 📚 Referencias y Recursos

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Chart.js**: https://www.chartjs.org/docs/
- **Font Awesome**: https://fontawesome.com/icons
- **SweetAlert2**: https://sweetalert2.github.io/

---

**Documento mantenido por**: Alvaro Guerra + Antigravity AI  
**Última actualización**: Diciembre 2024  
**Versión**: 1.0
