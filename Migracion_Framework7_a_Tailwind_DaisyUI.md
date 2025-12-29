# Migración UI: Framework7 ➜ Tailwind CSS v4 + daisyUI v5 (Flask/Jinja)

> Objetivo: reemplazar Framework7 por Tailwind + daisyUI **sin romper** rutas, fetch/AJAX, ni la lógica del backend.
> Estrategia: **migración incremental por plantillas**, manteniendo una versión “old” por cada página para rollback rápido.

---

## 0) Principios y reglas del juego

- **No tocar backend** al inicio: primero cambiamos **HTML/CSS** manteniendo IDs, `data-*` y endpoints.
- **Una página a la vez**: cada plantilla migrada debe quedar “lista para producción” antes de pasar a la siguiente.
- **Rollback inmediato**: cada plantilla antigua se conserva como `*-old.html` (o en `/legacy/`).
- **Contrato de JS**: si un selector JS apunta a `#ticketModal` o `.js-save`, o se mantiene, o se actualiza el JS en el mismo commit.
- **Nunca mezclar Framework7 y daisyUI en el mismo layout final**. Durante transición sí, pero con límites claros.

---

## 1) Branch / estructura recomendada

1. Crear branch:
   - `ui/tailwind-daisyui`

2. Crear carpetas (si no existen):
   - `assets/css/` (inputs de Tailwind)
   - `app/static/css/` (outputs compilados)
   - `docs/` (este archivo)

3. Convención de plantillas:
   - `templates/index-old.html`
   - `templates/index.html` (nueva)
   - (Opcional) mover todas las antiguas a `templates/legacy/` cuando termines.

---

## 2) Instalar Tailwind v4 + daisyUI v5

> Tailwind CLI v4 se instala con `tailwindcss` y `@tailwindcss/cli`. citeturn2view0  
> daisyUI v5 se añade como plugin en el CSS usando `@plugin "daisyui"`. citeturn2view1

En la raíz del proyecto:

```bash
npm init -y
npm i -D tailwindcss @tailwindcss/cli daisyui
```

Crear archivo de entrada: `assets/css/app.css`

```css
@import "tailwindcss";
@plugin "daisyui";

/* IMPORTANTE: asegura que Tailwind escanee tus templates de Flask/Jinja */
@source "../app/templates/**/*.html";
@source "../app/static/js/**/*.js";

/* Opcional: si usas templates en otra ruta, ajusta los glob */
```

> Tailwind v4 usa detección automática, pero el `@source` es la forma segura de incluir rutas específicas (por ejemplo `templates/`). citeturn3search1turn3search0

Compilar a tu `static`:

```bash
npx @tailwindcss/cli -i ./assets/css/app.css -o ./app/static/css/app.css --watch
```

> El comando base del CLI es `npx @tailwindcss/cli -i ... -o ... --watch`. citeturn2view0

### Scripts recomendados (package.json)

```json
{
  "scripts": {
    "tw:dev": "npx @tailwindcss/cli -i ./assets/css/app.css -o ./app/static/css/app.css --watch",
    "tw:build": "npx @tailwindcss/cli -i ./assets/css/app.css -o ./app/static/css/app.css --minify"
  }
}
```

---

## 3) Inyectar el CSS nuevo en tu base

En tu plantilla base (por ejemplo `base.html`):

- Quitar (o comentar) CSS de Framework7 en la versión “new”.
- Agregar:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
```

---

## 4) Elegir y fijar un tema daisyUI

daisyUI funciona por temas y se activa con `data-theme` en el `<html>`. citeturn1search13turn1search0

Ejemplo (en `base.html`):

```html
<html lang="es" data-theme="corporate">
```

Opciones:
- Si solo usarás 1 tema, puedes limitarlo desde el CSS: citeturn1search6

```css
@import "tailwindcss";
@plugin "daisyui" {
  themes: corporate --default;
}
```

---

## 5) Estrategia de migración por página (tu idea, mejorada)

### Opción A (tu enfoque): renombrar y reconstruir
Para cada página:

1. Renombrar:
   - `X.html` ➜ `X-old.html`
2. Crear nuevo:
   - `X.html` (Tailwind/daisyUI)

✅ Pros: clarísimo, rollback fácil.  
⚠️ Contras: hay que cuidar includes/extends.

### Opción B (aún más segura): layouts paralelos
Mantén ambos layouts:

- `base-old.html` (Framework7)
- `base.html` (Tailwind/daisyUI)

Luego cada página decide:

- `X-old.html` hace `{% extends "base-old.html" %}`
- `X.html` hace `{% extends "base.html" %}`

✅ Pros: no mezclas dependencias, transición limpia.

---

## 6) “UI Kit” (recomendado antes de migrar páginas reales)

Crea una página `templates/ui-kit.html` que tenga:

- Botones (primary/secondary/ghost)
- Inputs (normal + error)
- Badges + alerts
- Tabla
- Modal
- Dropdown/menu
- Paginación

Esto reduce el riesgo de “migrar sin sistema”.

---

## 7) Mapeo rápido: Framework7 ➜ daisyUI/Tailwind

| Necesidad | Framework7 | daisyUI / Tailwind |
|---|---|---|
| Layout dashboard | Panels/Views | `drawer`, `navbar`, `menu`, `card` |
| Buttons | `button` variants | `btn`, `btn-primary`, `btn-ghost` |
| Forms | list inputs | `input`, `select`, `textarea`, `form-control` |
| Tables | custom/table | `table`, `table-zebra`, `overflow-x-auto` |
| Alerts | F7 notifications | `alert`, `toast` (o mantener SweetAlert2) |
| Modal | F7 popup | `modal` con `<dialog>` (recomendado) citeturn0search0 |
| Badges | chips | `badge`, `badge-success`, etc. |

---

## 8) Patrón recomendado para modales (HTML <dialog>)

daisyUI tiene 3 métodos; el `<dialog>` es el más accesible y permite cerrar con `Esc`. citeturn0search0

Ejemplo base:

```html
<button class="btn btn-primary" onclick="ticketModal.showModal()">Nuevo ticket</button>

<dialog id="ticketModal" class="modal">
  <div class="modal-box">
    <h3 class="font-bold text-lg">Crear ticket</h3>

    <form method="dialog" class="space-y-3 mt-4">
      <input class="input input-bordered w-full" placeholder="Asunto">
      <textarea class="textarea textarea-bordered w-full" placeholder="Descripción"></textarea>

      <div class="modal-action">
        <button class="btn">Cerrar</button>
        <button class="btn btn-primary" type="button" id="btnGuardarTicket">Guardar</button>
      </div>
    </form>
  </div>
</dialog>
```

Regla: mantén IDs que ya use tu JS (`#btnGuardarTicket`, etc.) para no reescribir lógica.

---

## 9) Orden sugerido de migración (impacto vs riesgo)

1. `base` (layout principal: sidebar/topbar)
2. Login
3. Listado de tickets (tabla + filtros)
4. Detalle de ticket (badges/estado, comentarios)
5. Dashboards (cards + Chart.js)
6. Páginas administrativas (usuarios, categorías, etc.)

---

## 10) Checklist por página (Definition of Done)

Cada página migrada cumple:

- [ ] Compila Tailwind sin errores
- [ ] Sin dependencias de Framework7 en esa plantilla
- [ ] IDs y `data-*` requeridos por JS existen
- [ ] Responsive mínimo: móvil/tablet/desktop
- [ ] Estados: hover, focus, disabled, loading (si aplica)
- [ ] Accesibilidad básica: focus visible, labels, modal con Esc
- [ ] Sin “saltos” de layout al cargar
- [ ] Revisión visual rápida en 2 navegadores modernos

---

## 11) QA / smoke tests

- Crear ticket
- Editar estado / asignación
- Buscar / filtrar
- Paginación (si aplica)
- Abrir/cerrar modales
- Confirmaciones (SweetAlert2 o daisyUI)
- Charts renderizan ok
- Errores del backend se muestran (alerts)

---

## 12) Rollback plan

Si algo falla:

- Cambiar render a `*-old.html` temporalmente **o**
- Revertir el commit de la plantilla migrada (por página)

Opcional: “switch” por variable de entorno en Flask:

```python
# idea (opcional):
# template = "index.html" if os.getenv("UI_VERSION","new") == "new" else "index-old.html"
```

---

## 13) Notas / ideas extra (para que no se sienta genérico)

- Define 1 tema fijo al inicio (`corporate`, `business`, `nord`, etc.) y luego lo ajustas.
- Crea 5 utilidades propias (poquitas) para tu identidad:
  - `btn-brand`, `card-glass`, `text-muted`, `border-soft`, `shadow-soft`
- Mantén SweetAlert2 para confirmaciones críticas; usa daisyUI para UI “estructural”.
- Si tu UI anterior era glassmorphism, úsalo solo en cards principales para no “lavar” el contraste.

---

## 14) Próximo paso inmediato

1) Crear `ui-kit.html`  
2) Migrar `base.html` (layout principal)  
3) Migrar “Tickets list” como primera página real

