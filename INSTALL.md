# 📋 Proceso de Migración UI: Bootstrap → Tailwind CSS v4 + daisyUI v5

> **Fecha de inicio**: 2025-12-29  
> **Estado actual**: ✅ **FASE 1 - ANÁLISIS COMPLETADO**  
> **Último checkpoint**: Análisis inicial y plan de implementación creados

---

## 🎯 Objetivo

Migrar el sistema de tickets de **Bootstrap 5.3.0** a **Tailwind CSS v4 + daisyUI v5** de forma incremental, manteniendo toda la funcionalidad existente del backend Flask.

> 💡 **Nota importante**: El documento de referencia `Migracion_Framework7_a_Tailwind_DaisyUI.md` menciona Framework7, pero el proyecto **actualmente usa Bootstrap 5.3.0**.

---

## 📊 Estado del Proyecto

### ✅ Completado

- [x] **Análisis de estructura del proyecto**
  - Fecha: 2025-12-29 15:07
  - Templates identificados: 9 principales, 3 de tickets, 5 de admin
  - CSS actual: Framework7 9.0.2 + Bootstrap 5.3 (híbrido) + 5 archivos CSS custom

- [x] **Identificación de dependencias**
  - Framework7 9.0.2 (CDN) - se eliminará ❌
  - Bootstrap 5.3.0 (CDN) - se eliminará ❌
  - SweetAlert2 (se mantendrá ✅)
  - Chart.js (se mantendrá ✅)
  - Socket.io (se mantendrá ✅)
  - Vortex canvas background (se mantendrá ✅)

- [x] **Plan de implementación creado**
  - Archivo: `.gemini/antigravity/brain/.../implementation_plan.md`
  - Estrategia: Migración incremental con backups `*-old.html`

- [x] **Branch de migración creado**
  - Fecha: 2025-12-29 15:31
  - Branch: `ui/tailwind-daisyui`
  - Estado: Activo

- [x] **Tailwind CSS v4 + daisyUI v5 instalados**
  - Fecha: 2025-12-29 15:31
  - Paquetes: tailwindcss ^4.0.0, @tailwindcss/cli ^4.0.0, daisyui ^5.0.0
  - Total: 34 paquetes, 0 vulnerabilidades

- [x] **Configuración CSS creada**
  - Archivo: `assets/css/app.css`
  - Tema: business (daisyUI)
  - Custom utilities: Glassmorphism, gradientes, badges

- [x] **Primera compilación exitosa**
  - Fecha: 2025-12-29 15:32
  - Output: `app/static/css/app.css`
  - Tiempo: 384ms
  - Warnings: 1 (menor, @property de daisyUI)

### ⏳ Pendiente

- [ ] **Migración de layouts base** (base_layout.html, page_shell.html)
- [ ] **Creación de UI Kit** (página de referencia)
- [ ] **Migración de templates** (0/17 archivos)

---

## 📁 Inventario de Templates

### Templates Principales (9)

| Archivo | Tamaño | Estado | Último cambio | Notas |
|---------|--------|--------|---------------|-------|
| `base.html` | 32KB | ⏳ Pendiente | - | Layout principal, navbar, chat, preloader |
| `login.html` | 13KB | ⏳ Pendiente | - | Formulario de login |
| `dashboard.html` | 5.5KB | ⏳ Pendiente | - | Página principal con gráficas |
| `profile.html` | 17KB | ⏳ Pendiente | - | Perfil de usuario |
| `search_results.html` | 3.3KB | ⏳ Pendiente | - | Resultados de búsqueda |
| `reset_password.html` | 1.5KB | ⏳ Pendiente | - | Reseteo de contraseña |
| `reset_password_request.html` | 1.1KB | ⏳ Pendiente | - | Solicitud de reset |
| `base.html.backup` | 14KB | ℹ️ Backup | - | Backup existente |
| `dashboard.html.backup` | 9.7KB | ℹ️ Backup | - | Backup existente |

### Templates de Tickets (3)

| Archivo | Tamaño | Estado | Último cambio | Notas |
|---------|--------|--------|---------------|-------|
| `tickets/list.html` | 20KB | ⏳ Pendiente | - | Tabla compleja de tickets |
| `tickets/detail.html` | 6KB | ⏳ Pendiente | - | Detalle de ticket |
| `tickets/create.html` | 1.1KB | ⏳ Pendiente | - | Crear ticket |

### Templates Administrativos (5)

| Archivo | Tamaño | Estado | Último cambio | Notas |
|---------|--------|--------|---------------|-------|
| `admin/users.html` | 25KB | ⏳ Pendiente | - | Gestión de usuarios |
| `admin/system_settings.html` | 25KB | ⚠️ Revisar | [Migrado previamente](hist:541dc5ee) | Verificar compatibilidad |
| `admin/audit_logs.html` | 10KB | ⏳ Pendiente | - | Logs de auditoría |
| `admin/create_user.html` | 1KB | ⏳ Pendiente | - | Crear usuario |
| `admin/edit_user.html` | 2KB | ⏳ Pendiente | - | Editar usuario |

### Otros (2)

| Directorio | Archivos | Estado | Notas |
|------------|----------|--------|-------|
| `templates/components/` | 3 | ⏳ Pendiente | Componentes reutilizables |
| `templates/layouts/` | 2 | ⏳ Pendiente | Layouts alternativos |
| `templates/reports/` | 1 | ⚠️ Revisar | [Refinado previamente](hist:5a8d51eb) |

---

## 🔧 Archivos CSS Actuales

| Archivo | Propósito | Acción en migración |
|---------|-----------|---------------------|
| `css/main.css` | Estilos principales | ➡️ Migrar a Tailwind utilities |
| `css/tickets-page.css` | Estilos de tickets | ➡️ Migrar a componentes daisyUI |
| `css/actions-chat.css` | Chat widget | ➡️ Migrar a daisyUI + mantener JS |
| `css/f7-icons-fix.css` | Fix de iconos F7 | ❌ Eliminar (no aplica) |
| `css/ionicons-components.css` | Iconos Ionicons | ⚠️ Evaluar si mantener |

---

## 📝 Historial de Cambios

### 2025-12-29 15:25 - Corrección del análisis inicial

**Responsable**: Antigravity AI + Usuario  
**Fase**: Análisis y validación  

**Correcciones importantes**:
1. ✅ Confirmado: El proyecto **SÍ usa Framework7 9.0.2**
   - Archivo principal: `layouts/base_layout.html`
   - CDN: Framework7 9.0.2 bundle (CSS + JS)
2. ⚠️ Descubierto: Existe `base.html` con Bootstrap 5.3.0
   - Posible migración anterior no completada
   - Necesita revisión de cuál layout se usa realmente en producción
3. ✅ Decisiones del usuario confirmadas:
   - **Tema**: `business` con toque de `corporate`
   - **Rollback**: Aprobada estrategia con `*-old.html`
   - **Orden**: Seguir el propuesto en el plan

**Archivos actualizados**:
- `INSTALL.md` - Corregido el framework UI identificado
- `implementation_plan.md` - Actualizado con análisis correcto

**Próximos pasos**:
1. ⏳ Verificar qué templates usan `base_layout.html` (Framework7)
2. ⏳ Verificar qué templates usan `base.html` (Bootstrap)
3. ⏳ Crear branch `ui/tailwind-daisyui`
4. ⏳ Instalar Tailwind v4 + daisyUI v5

### 2025-12-29 15:07 - Inicialización del proceso

**Responsable**: Antigravity AI  
**Fase**: Análisis inicial  

**Acciones realizadas**:
1. ✅ Lectura de `Migracion_Framework7_a_Tailwind_DaisyUI.md`
2. ✅ Análisis de estructura de templates
3. ✅ Identificación de dependencias actuales
4. ✅ Creación de plan de implementación
5. ✅ Creación de este archivo `INSTALL.md`

**Hallazgos importantes**:
- El proyecto usa **Bootstrap 5.3.0**, no Framework7
- Total de templates a migrar: **17 archivos**
- 2 páginas ya migradas previamente (system_settings, reports)
- Base.html es complejo: incluye navbar, preloader 3D, chat widget, vortex background

**Próximos pasos**:
1. ⏳ Esperar confirmación del usuario sobre:
   - Tema de daisyUI preferido (corporate, business, nord, etc.)
   - Estrategia de rollback con archivos `*-old.html`
   - Orden de prioridad de migración
2. ⏳ Crear branch `ui/tailwind-daisyui`
3. ⏳ Instalar dependencias (npm init + Tailwind + daisyUI)
4. ⏳ Configurar compilación CSS

---

## 🎨 Decisiones de Diseño

### Tema daisyUI

**Estado**: ⏳ **Pendiente decisión del usuario**

**Opciones**:
- `corporate` - Profesional, neutro, ideal para sistemas empresariales
- `business` - Sobrio, alto contraste
- `nord` - Paleta nórdica, colores suaves
- `cupcake` - Colores pastel
- `dark` - Tema oscuro por defecto

**Recomendación**: `corporate` (por ser sistema de gestión)

### Estrategia de Rollback

**Estado**: ⏳ **Pendiente confirmación**

**Propuesta**:
1. Renombrar cada template: `X.html` → `X-old.html`
2. Crear nuevo `X.html` con Tailwind + daisyUI
3. Mantener ambos hasta verificación completa
4. En producción, usar variable de entorno para switch si es necesario

**Alternativa**: Crear `base-old.html` y heredar desde ahí

---

## 🚀 Fases de Migración

### Fase 1: Análisis y Configuración ✅ **COMPLETADA**

- [x] Analizar estructura del proyecto
- [x] Identificar templates y dependencias
- [x] Crear plan de implementación
- [ ] **BLOQUEADO**: Esperar confirmación de decisiones críticas
- [ ] Crear branch de migración
- [ ] Instalar Tailwind v4 + daisyUI v5
- [ ] Configurar scripts de compilación

**Progreso**: 3/7 (43%)

---

### Fase 2: UI Kit y Base ⏳ **PENDIENTE**

- [ ] Crear `assets/css/app.css` (entrada de Tailwind)
- [ ] Crear `package.json` con scripts
- [ ] Compilar CSS por primera vez
- [ ] Crear `templates/ui-kit.html` (referencia de componentes)
- [ ] Migrar `base.html` (navbar, layout, preloader, chat)
- [ ] Verificar que no se rompa nada

**Progreso**: 0/6 (0%)

---

### Fase 3: Páginas Principales ⏳ **PENDIENTE**

**Orden propuesto**:

1. **Login** (13KB)
   - [ ] Backup a `login-old.html`
   - [ ] Migrar formulario
   - [ ] Probar login exitoso/fallido

2. **Dashboard** (5.5KB)
   - [ ] Backup a `dashboard-old.html`
   - [ ] Migrar cards de estadísticas
   - [ ] Verificar Chart.js
   - [ ] Probar navegación

3. **Tickets - List** (20KB) - **CRÍTICO**
   - [ ] Backup a `tickets/list-old.html`
   - [ ] Migrar tabla compleja
   - [ ] Migrar filtros y búsqueda
   - [ ] Migrar modales (crear, editar)
   - [ ] Verificar paginación
   - [ ] Mantener todos los IDs para JS

4. **Tickets - Detail** (6KB)
   - [ ] Backup a `tickets/detail-old.html`
   - [ ] Migrar vista de detalle
   - [ ] Migrar comentarios

5. **Profile** (17KB)
   - [ ] Backup a `profile-old.html`
   - [ ] Migrar formulario de perfil

**Progreso**: 0/5 páginas (0%)

---

### Fase 4: Administración ⏳ **PENDIENTE**

1. **System Settings** (25KB) - ⚠️ **REVISAR**
   - [ ] Verificar migración previa (conversación 541dc5ee)
   - [ ] Adaptar a nueva estructura si es necesario

2. **Users** (25KB)
   - [ ] Backup a `admin/users-old.html`
   - [ ] Migrar tabla de usuarios
   - [ ] Migrar modales de edición

3. **Audit Logs** (10KB)
   - [ ] Backup a `admin/audit_logs-old.html`
   - [ ] Migrar tabla de logs

4. **Create/Edit User** (1KB + 2KB)
   - [ ] Migrar formularios

**Progreso**: 0/4 secciones (0%)

---

### Fase 5: Verificación y Limpieza ⏳ **PENDIENTE**

- [ ] Smoke tests de todas las funcionalidades
- [ ] Pruebas responsive (móvil, tablet, desktop)
- [ ] Pruebas de dark mode
- [ ] Pruebas en Chrome, Firefox
- [ ] Eliminar archivos `*-old.html` (opcional, después de verificación)
- [ ] Eliminar CSS de Bootstrap
- [ ] Actualizar documentación

**Progreso**: 0/7 (0%)

---

## 📈 Progreso Global

```
Total de archivos a migrar: 17
Archivos completados:        0
Archivos en progreso:        0
Archivos pendientes:        17

Progreso: ▱▱▱▱▱▱▱▱▱▱ 0%
```

**Fase actual**: 1. Análisis y Configuración  
**Próximo checkpoint**: Configuración de Tailwind + daisyUI

---

## 🔗 Referencias

- **Plan de implementación**: [implementation_plan.md](file:///.gemini/antigravity/brain/d7794032-0715-4a41-a816-6d7ffbb1c1e2/implementation_plan.md)
- **Guía de migración**: [Migracion_Framework7_a_Tailwind_DaisyUI.md](file:///c:/Users/alvaro.guerra/Desktop/sistema-tickets/Migracion_Framework7_a_Tailwind_DaisyUI.md)
- **Documentación Tailwind v4**: https://tailwindcss.com/docs/v4-beta
- **Documentación daisyUI v5**: https://daisyui.com/
- **Migración anterior (System Settings)**: Conversación 541dc5ee-03e9-4df2-b757-7562aa22784b
- **Refinamiento Reports**: Conversación 5a8d51eb-f5cd-414c-9359-09b157a14406

---

## 🆘 Rollback en Caso de Emergencia

### Rollback Inmediato (1 minuto)

1. Cambiar render en Flask views:
   ```python
   return render_template('base-old.html')  # en vez de 'base.html'
   ```

2. Reiniciar servidor Flask

### Rollback por Git (5 minutos)

```bash
git log --oneline  # Ver últimos commits
git revert <commit-hash>  # Revertir commit específico
git push
```

### Switch Condicional (para testing)

```python
# config.py
USE_NEW_UI = os.getenv('USE_NEW_UI', 'true') == 'true'

# En cada route:
template = 'login.html' if USE_NEW_UI else 'login-old.html'
return render_template(template)
```

---

## 📌 Notas y Recordatorios

- ⚠️ **CRÍTICO**: Mantener todos los IDs y atributos `data-*` en elementos interactivos (JS depende de ellos)
- ✅ **SweetAlert2, Chart.js, Socket.io** se mantienen sin cambios
- ✅ **Preloader 3D boxes** se mantiene (migrar CSS a Tailwind)
- ✅ **Vortex background** canvas se mantiene sin cambios
- ⚠️ Verificar `system_settings.html` y `reports/index.html` (posiblemente ya migrados)
- 💡 Crear commits granulares (uno por página migrada)

---

## ✍️ Última actualización

**Fecha**: 2025-12-29 15:07  
**Autor**: Antigravity AI  
**Acción**: Inicialización del proceso de migración y análisis completo

---

_Este archivo se actualizará con cada cambio en el proceso de migración._
