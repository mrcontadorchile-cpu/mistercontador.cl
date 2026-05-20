# CLAUDE.md — Mister Contador · Instrucciones de trabajo

> Sitio estático en GitHub Pages. Push a `main` = deploy automático (~1-2 min).
> Worktree: `/Users/kunga/mistercontador.cl/.claude/worktrees/zealous-mcclintock-f8ee1a/`
> Push: `git push origin claude/zealous-mcclintock-f8ee1a:main`

---

## Reglas de operación (ahorro de tokens)

1. **NUNCA leer archivos completos.** Usar `grep -n` para localizar la línea exacta antes de editar.
2. **Edición quirúrgica.** Solo el rango necesario con `sed -n 'X,Yp'` para contexto mínimo.
3. **Sin explicaciones previas.** Ejecutar directamente, explicar solo si algo falla.
4. **Commit + push siempre al final** de cada cambio, sin que el usuario lo pida.

---

## CSS Variables (definidas en `<style>` de cada HTML)

```
--gold:       #F5C200
--gold-dark:  #D4A800
--black:      #0a0a0a
--surface:    #111111
--border:     #1e1e1e
--text:       #ffffff
--text-muted: #777777
```

---

## Tipografías

| Uso | Fuente | Atributos |
|-----|--------|-----------|
| Títulos manga | Bangers | `letter-spacing: 2-4px; text-transform: uppercase` |
| Subtítulos sección | Bebas Neue | `font-size: clamp(28px,5vw,48px)` |
| Cuerpo | Inter | `font-size: 15-16px; line-height: 1.65` |

---

## Componentes reutilizables (clases clave)

| Clase | Descripción |
|-------|-------------|
| `.btn-manga` | Botón fantasma manga (borde blanco, box-shadow, hover translate) |
| `.service-card` | Card de servicio con borde dorado en hover |
| `.testimonial-card` | Speech bubble manga (fondo blanco, borde negro 3px, cola CSS) |
| `.chapter-divider` | Separador estilo capítulo manga |
| `.reveal` / `.reveal.visible` | Fade + slide-up por scroll (IntersectionObserver) |
| `.reveal-d1` … `.reveal-d6` | Delays 0.1s–0.6s para stagger |
| `.section-sfx[data-sfx]::after` | Texto gigante de fondo (onomatopeya) |
| `.manga-card` | Card con `border: 3px solid var(--gold); box-shadow: 6px 6px 0 var(--gold)` |
| `.cursor-trail` | Línea de estela del cursor (spawneada por JS) |
| `#read-progress` | Barra de progreso de lectura (gold, top fixed) |

---

## index.html — Mapa de secciones (líneas aproximadas)

```
L58    nav CSS
L99    .btn-manga CSS
L149   .hero CSS
L270   .chapter-divider CSS
L301   .service-card CSS
L317   .testimonial-card CSS
L864+  CSS: scroll reveal, progress bar, cursor, splash
L942   HTML: progress bar div
L954   HTML: Nav
L987   HTML: Hero
L1007  HTML: Stats
L1030  HTML: Servicios  (id="servicios")
L1078  HTML: Pricing    (id="planes")
L1206  HTML: Fundador
L1234  HTML: Video
L1255  HTML: Testimonios (id="testimonios")
L1308  HTML: FAQ        (id="faq")
L1349  HTML: Banner Mister Inventario
L1357  HTML: Contacto   (id="contacto")
L1397  JS: Stats count-up
L1425  JS: Hero parallax
L1461  JS: Formulario WhatsApp
L1482  JS: Navbar activa
L1507  JS: Scroll reveal
L1600  JS: Navbar glass + progress bar
L1617  JS: Cursor manga + speed lines trail
L1649  JS: Splash intro
```

---

## inventory.html — Mapa de secciones (líneas aproximadas)

```
L119   nav CSS
L167   .hero CSS
L253   .section, .section-title CSS
L283   .section-sfx, SFX ::after CSS
L290   Progress bar + cursor CSS
L696   HTML: Progress bar
L698   HTML: Nav
L729   HTML: Hero
L753   CAPÍTULO 01 divider
L763   HTML: El Problema    (id="problema",  data-sfx="¡STOCK!")
L787   CAPÍTULO 02 divider
L797   HTML: Qué Es         (id="solucion")
L825   CAPÍTULO 03 divider
L835   HTML: Impacto        (id="impacto",   data-sfx="¡CONTROL!")
L863   CAPÍTULO 04 divider
L873   HTML: Cómo Funciona  (id="como-funciona")
L902   HTML: Video demo
L915   CAPÍTULO 05 divider
L925   HTML: Funcionalidades (id="features", data-sfx="¡PYME!")
L973   CAPÍTULO 06 divider
L983   HTML: Escalabilidad  (id="escalabilidad", data-sfx="¡DIGITALIZA!")
L1007  CAPÍTULO 07 divider
L1017  HTML: Pricing        (id="pricing")
L1081  HTML: Testimonios
L1132  HTML: FAQ            (id="faq")
L1186  HTML: Ficha Proyecto (id="ficha")
L1228  HTML: CTA Final      (id="download")
L1297  JS: FAQ accordion
L1315  JS: Scroll reveal
L1340  JS: Navbar glass + progress bar
L1357  JS: Cursor manga + trail
L1385  JS: Parallax SFX
```

---

## Grep patterns más útiles

```bash
# Encontrar una sección por ID
grep -n 'id="servicios"' index.html

# Encontrar inicio de un bloque CSS
grep -n '\.service-card {' index.html

# Encontrar texto específico para cambiar copy
grep -n 'Contador Auditor' index.html

# Ver líneas alrededor de un hallazgo
sed -n '1030,1080p' index.html

# Ver CSS de un componente
grep -n '\.manga-card' inventory.html
```

---

## Patrón de capítulo manga (HTML)

```html
<div class="chapter-divider">
  <div class="ch-line"></div>
  <span class="ch-num">CAPÍTULO 0X</span>
  <span class="ch-sep">—</span>
  <span class="ch-title">NOMBRE</span>
  <div class="ch-line right"></div>
</div>
```

## Card manga dorada (CSS inline)

```html
<div style="border:3px solid var(--gold);box-shadow:6px 6px 0 var(--gold);padding:28px;background:var(--surface)">
```

## Botón WhatsApp principal

```html
<a href="https://wa.me/56940536523" target="_blank" rel="noopener" class="btn-manga">TEXTO</a>
```

---

## Deploy

```bash
git add ARCHIVO && git commit -m "tipo: descripción breve" && git push origin claude/zealous-mcclintock-f8ee1a:main
```

| Tipo | Cuándo |
|------|--------|
| `feat:` | nueva sección o funcionalidad |
| `fix:` | corrección de bug o contenido |
| `style:` | cambios visuales sin lógica |
| `refactor:` | restructuración sin cambio de comportamiento |

---

## Otros archivos

| Archivo | Propósito |
|---------|-----------|
| `triple-impacto/index.html` | Sobre Nosotros / Canvas B (usa Tailwind CDN) |
| `socios.html` | Portal socios |
| `terminos.html` / `privacidad.html` | Legales |
| `img/logo-oficial.png` | Logo horizontal (navbar/footer) |
| `img/icon-oficial.png` | Favicon |
| `img/fundador.jpg` | Foto fundador |
