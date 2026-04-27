# Mister Contador — Documentación Técnica

> Sitio web institucional de **Mister Contador SpA** — servicios contables y financieros para Pymes chilenas.
> Identidad visual: manga/Shonen (negro, dorado, Bangers font, bordes sólidos).

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Hosting | GitHub Pages (rama `main`) |
| Frontend | HTML5 + CSS3 + JavaScript vanilla |
| CSS utility | Tailwind CSS via CDN (solo en `/triple-impacto/`) |
| Tipografías | Google Fonts — Bangers, Bebas Neue, Inter |
| Analytics | Google Analytics 4 (`G-RTB206P81H`) |
| Contacto | WhatsApp redirect (`wa.me/56940536523`) |
| Dominio | `mistercontador.cl` — apuntado via CNAME a GitHub Pages |

---

## Estructura de archivos

```
/
├── index.html              # Landing page principal
├── inventory.html          # Página Mister Inventario (SaaS)
├── socios.html             # Portal de socios
├── terminos.html           # Términos y condiciones
├── privacidad.html         # Política de privacidad
├── CNAME                   # Dominio custom para GitHub Pages
├── robots.txt              # Directivas SEO
├── sitemap.xml             # Mapa del sitio
├── img/
│   ├── logo-oficial.png    # Logo horizontal (navbar/footer)
│   ├── icon-oficial.png    # Favicon
│   └── fundador.jpg        # Foto fundador (800×640px, ~216KB)
├── triple-impacto/
│   └── index.html          # Modelo Canvas B / Sobre Nosotros
└── auth/                   # Carpeta autenticación (Supabase)
```

---

## Sistema de diseño

### Variables CSS (definidas en `index.html`)

```css
--gold:       #F5C200   /* Dorado principal */
--gold-dark:  #D4A800   /* Dorado hover */
--black:      #0a0a0a   /* Fondo de página */
--surface:    #111111   /* Cards/superficies */
--border:     #1e1e1e   /* Bordes sutiles */
--text:       #ffffff
--text-muted: #777777
```

### Tipografías

| Uso | Fuente | Clase/estilo |
|-----|--------|-------------|
| Títulos manga | Bangers | `font-family: 'Bangers', cursive; letter-spacing: 2px` |
| Headers sección | Bebas Neue | `font-family: 'Bebas Neue', sans-serif` |
| Cuerpo texto | Inter | `font-family: 'Inter', sans-serif` |

### Componentes clave

**`.btn-manga`** — Botón fantasma manga (borde blanco, hover + box-shadow)
```css
border: 2px solid white; box-shadow: 4px 4px 0 white;
hover: translate(-2px,-2px) + shadow expandido
```

**`.service-card`** — Cards de servicios con borde dorado en hover
```css
border: 2px solid rgba(245,194,0,0.2);
hover: border dorado sólido + box-shadow dorado
```

**`.testimonial-card`** — Burbuja de diálogo manga (speech bubble)
```css
background: white; border: 3px solid black;
::after → triángulo CSS (cola del bubble)
```

**`.chapter-divider`** — Separador de secciones estilo capítulo manga
```html
<div class="chapter-divider">
  <div class="ch-line"></div>
  <span class="ch-num">CAPÍTULO 01</span>
  <span class="ch-sep">—</span>
  <span class="ch-title">NOMBRE</span>
  <div class="ch-line right"></div>
</div>
```

**`.reveal` / `.reveal.visible`** — Animación de entrada por scroll
```css
.reveal { opacity: 0; transform: translateY(32px); }
.reveal.visible { opacity: 1; transform: translateY(0); }
/* Delays: .reveal-d1 a .reveal-d6 (0.1s a 0.6s) */
```

---

## JavaScript (todo vanilla, sin frameworks)

| Script | Función |
|--------|---------|
| FAQ accordion | Toggle open/close de preguntas frecuentes |
| Stats count-up | IntersectionObserver + animación numérica al entrar al viewport |
| Hero parallax | `mousemove` sobre `.hero` mueve `.hero-speedlines` |
| Scroll reveal | IntersectionObserver agrega `.visible` a elementos `.reveal` |
| Navbar activa | IntersectionObserver marca el link de nav según sección visible |
| Formulario contacto | Arma URL `wa.me` con datos del form y abre WhatsApp |

---

## Efectos visuales hero

- **Speed lines**: `repeating-conic-gradient` en `.hero-speedlines` + parallax mouse
- **Halftone**: `radial-gradient` en `.hero-halftone` con animación `breathing`
- **SFX onomatopeya**: `section[data-sfx]::after` muestra texto gigante de fondo (`¡MISIÓN!`, `¡NIVEL UP!`, etc.)

---

## Flujo de deploy

El sitio se despliega **automáticamente** con cada push a `main`.

```bash
# Clonar el repo
git clone https://github.com/mrcontadorchile-cpu/mistercontador.cl.git
cd mistercontador.cl

# Editar archivos y subir
git add .
git commit -m "descripción del cambio"
git push origin main
# → GitHub Pages despliega en ~1-2 minutos en mistercontador.cl
```

No hay proceso de build — es HTML/CSS/JS puro. Lo que está en `main` es lo que se sirve.

---

## Páginas y rutas

| URL | Archivo | Descripción |
|-----|---------|-------------|
| `mistercontador.cl/` | `index.html` | Landing principal |
| `mistercontador.cl/triple-impacto/` | `triple-impacto/index.html` | Sobre Nosotros / Canvas B |
| `mistercontador.cl/inventory.html` | `inventory.html` | Mister Inventario |
| `mistercontador.cl/socios.html` | `socios.html` | Portal socios |
| `mistercontador.cl/terminos.html` | `terminos.html` | Términos legales |
| `mistercontador.cl/privacidad.html` | `privacidad.html` | Política de privacidad |

---

## Contacto y servicios externos

| Servicio | Detalle |
|----------|---------|
| WhatsApp | `+56 9 4053 6523` |
| Email contacto | `contacto@mistercontador.cl` |
| Email soporte | `soporte@mistercontador.cl` |
| Instagram | `@mister.contador` |
| Google Analytics | GA4 — ID `G-RTB206P81H` |
| Google Search Console | Verificado (`googlea1aad062d2b4dd6e.html`) |

---

## Convenciones de commits

```
feat:  nueva funcionalidad
fix:   corrección de bug o contenido
style: cambios visuales sin lógica
refactor: restructuración sin cambio de comportamiento
```

---

*Última actualización: Abril 2026*
