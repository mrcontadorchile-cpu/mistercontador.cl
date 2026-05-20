# PRODUCT.md — Mister Contador

## Product Purpose
Mister Contador is a Chilean accounting and financial services firm for small businesses (PyMEs). The website is a landing page that converts small business owners into paying clients for accounting services, and also promotes Mister Inventario — a SaaS inventory management app for local shops.

## Register
brand — marketing landing page. Design IS the product. The aesthetic must be bold, distinctive, and memorable.

## Users
Chilean small business owners: almacenes, minimarkets, botillerías, clothing stores, local shops. Age 25–55. Not tech-savvy. They care about trust, simplicity, and whether this person will actually solve their problems. They are overwhelmed by paperwork, SII compliance, and tax obligations.

Secondary: Sercotec/Corfo fund evaluators reviewing Mister Inventario (inventory.html) for technology grants. They look for impact, scalability, and digital transformation of SMEs.

## Brand Identity
- **Aesthetic:** Manga / Shonen anime. Black pages, gold ink. Think Weekly Shonen Jump meets a financial hero story.
- **Tone:** Energetic, direct, confident. The founder is the hero. Clients are the side characters leveling up. Not corporate, not boring. Think: "your financial superhero."
- **Anti-references:** Generic blue/white accounting firms. Corporate stock-photo vibes. Pastel SaaS startups. Purple AI gradient slop.

## Design Tokens
```
--gold:       #F5C200   (primary accent — Bangers titles, borders, shadows)
--gold-dark:  #D4A800   (hover state)
--black:      #0a0a0a   (page background)
--surface:    #111111   (cards, panels)
--border:     #1e1e1e   (subtle borders)
--text:       #ffffff
--text-muted: #777777
```

## Typography
- **Display/Hero titles:** Bangers (Google Fonts) — manga impact style. `letter-spacing: 2–4px; text-transform: uppercase`
- **Section headers:** Bebas Neue — strong, editorial
- **Body:** Inter — clean, readable

## Existing Visual Motifs (preserve these)
- Chapter dividers: `.chapter-divider` — separates sections like manga chapters
- Speed lines: `repeating-conic-gradient` in hero background
- SFX onomatopoeia: giant Bangers text behind sections (¡MISIÓN!, ¡NIVEL UP!, ¡STOCK!)
- Manga cards: `border: 3px solid var(--gold); box-shadow: 6px 6px 0 var(--gold)`
- Speech bubble testimonials: white cards with black 3px border and CSS triangle tail
- Custom cursor: hand-drawn SVG arrow + gold speed lines trail on fast movement
- Scroll reveal: fade + slide-up on viewport entry
- Navbar: transparent → glassmorphism on scroll
- Progress bar: gold 3px line at top advancing with scroll

## Stack Constraints
- Pure HTML5 + CSS3 + JavaScript vanilla. Zero frameworks, zero build step.
- GitHub Pages hosting. Push to main = live in ~2 minutes.
- CDN only for Google Fonts. No npm, no bundler.
- Must work without JavaScript for basic layout.

## Pages
- `index.html` — Main landing (services, pricing, founder, testimonials, FAQ, contact)
- `inventory.html` — Mister Inventario SaaS product page
- `triple-impacto/index.html` — Sobre Nosotros / Canvas B (uses Tailwind CDN)

## What to Improve (upgrade targets)
- Hero section: can feel more visceral and impactful
- Cards: tilt 3D effect, better hover micro-interactions
- Typography scale: more dramatic contrast between display and body
- Color use: currently restrained — can push toward "committed" palette
- Motion: current easings are generic `ease` — needs custom cubic-bezier curves
- Spacing rhythm: more variation between sections for better reading flow
- Mobile: some sections feel cramped on small screens
