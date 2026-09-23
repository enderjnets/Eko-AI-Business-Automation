## 2026-09-23 — Client login as a button

"Client login" / "Acceso de clientes" is now an outlined button: next to Book Demo on desktop, and in its own row under the header on mobile so both languages fit (checked at 1440, 1024, 390 and 320 px, EN and ES, no horizontal overflow). Link target unchanged: https://clients.ekoaiautomation.com/.

## 2026-09-23 — Client portal entry

Added the client sign-in link to desktop and mobile landing-page navigation in English and Spanish. Existing booking and CRM routes are unchanged.



## [0.7.61] — 2026-05-25

### Dev tooling — stack docker aislado (`eko-main`) para trabajo en paralelo de la rama main

Montaje para correr la rama `main` en paralelo con `feature/pricing-v2` sin que se pisen, usando git worktree (`~/Eko-AI-main`) + un stack docker totalmente aislado.

#### Cambios

**`docker-compose.main.yml`** (nuevo, proyecto compose `eko-main`):

- backend/frontend/db/redis propios en puertos `8010/3003/5433/6380`, aislados de producción (`3001/8000/5432/6379`) y del preview de pricing-v2 (`:3002`).
- Sin celery worker/beat y con `AUTO_REPLY_ENABLED=false` a propósito: el preview nunca duplica jobs programados ni manda emails salientes contra servicios externos de producción.
- Alias de red `eko-backend` dentro del proyecto para que el rewrite hardcoded de `next.config.js` (`/api` → `http://eko-backend:8000`) resuelva al backend aislado.
- Cambio **infra-only**: no toca código de la app. Setup completo y gotchas (static/audio faltante, clonar schema de prod por el índice duplicado de `landing_page`) documentados en `EKO_PARALLEL_CONTEXT.md`.

## [0.7.44] — 2026-05-20

### Home corporativa — agregados campos Nombre + Apellido al form de contacto

El form de contacto en https://www.ekoaiautomation.com solo capturaba **website / category / email / phone**. Los leads quedaban en DB como `business_name = "Unknown Business"` y los emails de respuesta salían genéricos con subject *"Your AI automation analysis for Unknown Business"* — combinado con los bugs anteriores (URL unsubscribe rota, dominio sender nuevo) este subject genérico empujaba a spam folder corporativo.

#### Cambios

**`frontend/components/LandingPage.tsx`**:

- State extendido con `first_name: ""` y `last_name: ""` (líneas 51-58).
- Nueva primera fila del form: grid 2-col responsive con dos `<input type="text" required>` para First Name + Last Name, ubicada **antes** del campo Website URL. El usuario provee identidad antes que detalles técnicos del negocio.
- Validación reforzada en `handleSubmit`: se agregó `if (!form.first_name.trim() || !form.last_name.trim()) return;` antes de los checks existentes.
- El `disabled` del submit button ahora exige los 4 fields obligatorios: `first_name + last_name + website + (email OR phone)`.
- El POST a `/api/v1/leads/public` ya enviaba `...form` con spread, así que `first_name` y `last_name` viajan automáticamente sin tocar el body.

**`frontend/lib/i18n/translations.ts`**:

- `home.form.first_name` — EN: `"First name"` · ES: `"Nombre"`
- `home.form.last_name` — EN: `"Last name"` · ES: `"Apellido"`

Toggle del LanguageSelector en el navbar cambia los placeholders instantáneamente sin recargar (i18n vive en cliente).

#### Backend NO se tocó

`PublicLeadCreate` schema (`backend/app/schemas/lead.py:166-178`) ya define `first_name: Optional[str]` y `last_name: Optional[str]` desde versiones anteriores; el handler en `backend/app/api/v1/leads.py:498-623` ya los persiste en `source_data` JSON + los usa como fallback para `business_name` cuando éste viene vacío. Ahora simplemente llegan poblados desde la home corporativa.

#### Beneficio downstream

Próximos leads capturados desde la home tendrán nombre real → el subject del AI Analysis email puede ser `"Your AI automation analysis for {First Last}"` o `"for {Business Name}"` cuando esté disponible — esto es un follow-up natural (no incluido en este commit). La pieza más importante hoy es **dejar de perder** la identidad del lead en el form de captura.

---

## [0.7.43] — 2026-05-20

### AI Analysis email — fix URL de unsubscribe malformada + persistencia del provider_id

**Caso disparador**: lead 616 (`evem@clx-global.com`) llenó form de landing page; Resend confirmó `last_event=delivered` pero la usuaria nunca abrió. El bot reportó éxito al usuario en el dashboard, pero a la persona "no le llegó" — probable spam/quarantine corporativo.

#### Bug 1: unsubscribe URL malformada

`backend/app/tasks/scheduled.py:1114`:

```python
app_url = outreach.from_email.split("@")[-1] if "@" in outreach.from_email else "ekoai.io"
unsubscribe_url = f"https://{app_url}/api/v1/webhooks/unsubscribe?lead_id={lead.id}"
```

`outreach.from_email = "Eko AI <contact@biz.ekoaiautomation.com>"` (formato RFC 5322 con display name). Split por `@` da `["Eko AI <contact", "biz.ekoaiautomation.com>"]`. El `[-1]` deja el `>` extra al final → resultado: `https://biz.ekoaiautomation.com>/api/v1/webhooks/unsubscribe?lead_id=616`.

URLs malformadas son red flag para spam filters (Microsoft 365 y Google Workspace los penalizan en el SpamAssassin score). Combinado con dominio sender nuevo (`biz.ekoaiautomation.com`), subject promocional (*"for Unknown Business"*) y HTML pesado con métricas, es probable que el email cayera en Junk/Quarantine.

**Fix**: usar `settings.APP_URL.rstrip("/")` igual que `email.py:336` y el tracking pixel. URL ahora bien formada: `https://ender-rog.tail25dc73.ts.net/api/v1/webhooks/unsubscribe?lead_id=N`. El dominio Tailscale no es ideal de marca, pero es lo que ya se está usando consistentemente en el resto del email — moverlo a un subdominio corporativo es follow-up separado.

#### Bug 2: provider_message_id no persistido

`scheduled.py:1136-1149` creaba el `Interaction` con `email_status="sent"` pero ignoraba el `id` que retorna `outreach.send()` (Resend message ID). Resultado: `interactions.email_message_id = NULL` para todos los emails AI Analysis enviados desde landing pages → sin pivot para correlacionar webhook events (delivered/opened/clicked/bounced) con la conversación en el dashboard.

**Fix**: capturar `send_result = await outreach.send(...)`, extraer `provider_message_id = send_result.get("id")`, persistirlo en `email_message_id` + `meta["provider"] = "resend"`.

#### Verificación

Worker + backend restart limpio post-deploy (sin ImportErrors). Próximo email AI Analysis enviado desde landing page tendrá unsubscribe URL bien formada y `email_message_id` poblado para tracking downstream.

#### Caveat

Este fix **no garantiza** que la usuaria de clx-global.com vea el email retroactivamente — ese mensaje ya fue entregado al servidor de ella el 20-may 21:25 UTC, con el URL roto. Si está en spam, sigue ahí. Para futuras campañas a contactos B2B corporativos vale la pena: (a) audit DKIM/SPF, (b) considerar warm-up del subdominio `biz.ekoaiautomation.com`, (c) subject lines menos genéricos (*"for Unknown Business"* es spam-trigger).

---

## [0.7.27] — 2026-05-20

### Landing Pages — fix thumbnails del template picker no mostraban el brand real

User reportó por 3ra vez: *"el template de Apple, si lo ves está oscuro usa fondo oscuro y la página de Apple es clara toda clara"*. Las 2 anteriores fixes (v0.7.21 defensive bg, v0.7.22 templates rewrite) confirmaron que el CÓDIGO del template Apple Minimal SÍ tiene `--bg:#fff`, pero el thumbnail seguía viéndose oscuro.

#### Root cause real (no era el template, era el thumbnail)

`frontend/app/landing-pages/page.tsx` líneas 851-857: el iframe del picker grid renderizado con `width:1304px, height:800px, transform:scale(0.15)` — a scale 0.15 el iframe ocupaba solo 195px de ancho en la esquina superior izquierda. El card tenía ~140-180px de ancho. Resultado: solo ~15% del thumbnail mostraba contenido real del template; el resto mostraba el `background: tpl.accent + "10"` del container parent (accent color al 10% alpha).

Para Apple (accent `#0066cc`) eso significaba ~70% del thumbnail era tinte azul translúcido → **"se veía oscuro"** aunque el template real es 100% blanco.

Para Spotify (accent `#1ed760`) tinte verde translúcido sobre el template ya negro → casualmente parecía correcto pero por la razón equivocada.

Bonus bug: `colorScheme: "dark"` heredado por error del ActivePreview (donde tiene sentido por el scrollbar fix). En el picker forzaba dark mode hint a templates light.

#### Fix

Nuevo componente `TemplateThumbnail` con el mismo patrón ResizeObserver que `ActivePreview` ya usaba: `scale = containerWidth / 1280` dinámico, iframe siempre llena el thumbnail exactamente, sin leak del parent.

Removidos: `colorScheme:"dark"`, `background: tpl.accent + "10"` del container, width/height fijos en pixeles, scale fijo 0.15.

#### Resultado

Cada thumbnail ahora muestra fielmente el template completo en su brand real:
- Apple Minimal: 100% blanco con SF Pro huge type
- Stripe Gradient: gradient mesh colorido
- Linear Dark: pure black con grid pattern y purple glow
- Airbnb Warm: white con coral CTA
- Notion Clean: white con Lyon serif
- Tesla Bold: dark hero full-bleed
- Best Buy Retail: white con blue+yellow
- Spotify Vibe: black con green
- HubSpot Sales: white con orange
- Eko Classic: dark blue gradient (siempre fue correcto)

---

## [0.7.26] — 2026-05-20

### Scrapling Phase 4 — research helper pre-AI: LP generator inyecta data fresca del business site al prompt

Phase 4 (de 4) de integración Scrapling. Da a los AI generators (landing page, futuro: proposal, sales brief) la capacidad de **pre-fetchar data fresca de la web ANTES de invocar el AI**, inyectándola como contexto al prompt. End-user benefit ≈ MCP server sin requerir refactor del AI client layer.

#### Cambios

`backend/app/services/research_helper.py` (nuevo, 130 líneas):
- `fetch_business_summary(url, max_chars, timeout)`: usa Scrapling para fetchear el site, strippea HTML→plain text, escala a browser tier si el body inicial es thin (<100 chars), devuelve None safely si todo falla
- `build_landing_page_context(website, extra_urls)`: orquesta fetch del business site + hasta 2 competitor URLs, devuelve un bloque markdown formateado: `## Research context (fresh fetch via Scrapling)\n### Business site: ...\n<plain text>\n### Reference: ...\n...`
- Cap de 3000 chars por default (env `SCRAPLING_RESEARCH_MAX_CHARS`), toggle global `SCRAPLING_RESEARCH_HELPER` (default true)

`backend/app/services/landing_page_generator.py`:
- `generate()` acepta nuevo parámetro `target_website: Optional[str]`
- Si presente AND helper habilitado → fetch context → append al `custom_prompt` → AI ahora ve la realidad del business site en vez de adivinar
- `metadata["research_context_used"]: bool` para audit

#### Smoke test real

```
build_landing_page_context("https://allbirds.com/")
→ 3091 chars de plain text con nav, product categories, footer copy en vivo
```

#### Por qué pre-fetch en vez de MCP server completo

Eko AI's AI client layer es `kimi-cli subprocess + REST calls a OpenAI/Anthropic`. Reescribir eso a hablar Model Context Protocol nativo era out-of-scope. Pre-fetch + prompt injection da el MISMO end-user benefit (AI grounded en data fresca) sin refactor del client layer.

#### MCP server completo queda como v0.8

Roadmap futuro: `pip install scrapling[ai]` provee un MCP server estilo Anthropic. Para integrarlo:
1. Levantar el MCP server como subprocess en el container
2. Configurar `kimi-cli --mcp` con su endpoint
3. Modificar `app/utils/ai_client.py` para advertise tools al AI
4. Modificar SYSTEM_PROMPTs para que el AI sepa cuándo invocar el tool

Eso es ~1 día de trabajo con riesgo medio (cambios al client layer afectan TODOS los AI calls). El pre-fetch approach de Phase 4 entrega el 80% del valor sin ese riesgo.

---

## [0.7.25] — 2026-05-20

### Scrapling Phase 3 — shared scraping helper + opt-in Yelp browser fallback

Phase 3 (de 4) de integración Scrapling. Construye infraestructura de scraping reutilizable y wireup del primer Discovery source fallback (Yelp).

`backend/app/services/scrapling_scraper.py` (nuevo, 117 líneas):
- `fetch_page(url, use_browser, timeout)`: wrapper sobre AsyncFetcher/StealthyFetcher devolviendo un Scrapling Selector. Reutiliza el circuit breaker de Phase 2 (no duplica)
- `scrape_yelp_listings(category, location, max_results)`: scraper específico para Yelp SERP que parsea cards `[data-testid="serp-ia-card"]`
- `DISCOVERY_FALLBACK_ENABLED` env flag (default false)

`backend/app/agents/discovery/sources/yelp.py`:
- `search()` ahora tiene dual path: API Fusion primary (unchanged) + Scrapling browser fallback opt-in cuando (API key missing O API error O API returns 0) AND flag habilitado

#### Smoke test

```
SCRAPLING_DISCOVERY_FALLBACK=true python -c "scrape_yelp_listings('nail salon', 'Denver, CO')"
[scrapling-yelp] scraping https://www.yelp.com/search?...
[stealth-discovery] yelp.com status=403
=== got 0 leads ===
```

Yelp devolvió 403 incluso vía StealthyFetcher (anti-bot Yelp brutal, esperado). **La infraestructura funcionó**: log, circuit breaker incrementado, return 0 graceful. Para production-grade Yelp scraping necesita residential proxy rotator (~$300/mes).

#### NO migrados (justificado)

- **Google Maps (Outscraper)**: viola Google ToS scrapear, Outscraper API ya autorizada, ROI negativo
- **Colorado SOS**: ya usa Socrata API gratuita como primary, Apify solo fallback existente

---

## [0.7.24] — 2026-05-20

### Scrapling Phase 2 — StealthyFetcher browser fallback con Redis circuit breaker

Phase 2 (de 4) de integración Scrapling. Agrega un 4to tier al `_fetch_html` chain: **StealthyFetcher** (browser-rendered con Patchright + Chromium headless undetectable) que se dispara solo cuando los 3 tiers HTTP devuelven 4xx/5xx O un body "thin" (<1500 chars de texto en `<body>` tras strip de tags/scripts — signature de sitios Wix/Squarespace/Shopify JS-rendered).

#### Cambios al chain

```
_fetch_html(url):
    tier 1: Scrapling AsyncFetcher (TLS impersonation chrome)
    tier 2: httpx con browser UA
    tier 3: httpx sin UA (legacy 403 fallback)
    tier 4: Scrapling StealthyFetcher (browser, anti-bot)
            ⤷ se invoca SOLO si: status >= 400 OR _looks_thin(text)
            ⤷ gated por Redis circuit breaker
            ⤷ return SOLO si: status < 400 AND len(stealth) > len(http)
```

#### Circuit breaker (lifted del Resend quota guard v0.7.15)

- `scraping:stealth:per_minute` TTL 60s — max 10 browser fetches/minuto
- `scraping:stealth:daily` TTL hasta UTC midnight — max 200 browser fetches/día
- Fail-open si Redis está caído (mejor degradar que bloquear)

#### Dockerfile

Agregadas 14 runtime libs Debian Trixie para Chromium (libnspr4, libnss3, libatk-bridge2.0-0, libcups2, libxkbcommon0, libxcomposite1, libxdamage1, libxrandr2, libgbm1, libpango-1.0-0, libcairo2, libasound2, libatspi2.0-0, libxshmfence1, libxfixes3, fonts-liberation, fonts-noto-color-emoji) + `patchright install chromium` durante build (~150MB cacheado como Docker layer).

#### Deps

Cambio de pinning manual a `scrapling[fetchers]==0.4.8` (extra notation) — pip resuelve la cadena correcta: playwright 1.59.0, patchright 1.59.1, msgspec 0.21+, curl_cffi 0.15+, browserforge, camoufox.

#### Audit (icapellis.com / Wix)

```
phase1  fetcher=httpx     1.8s   body=705,550  (shell pre-hidratado)
phase2  fetcher=stealth   4.5s   body=711,838  (HTML rendered con contenido visible)
```

Body grows ~6KB en bytes, pero el contenido NEW visible (texto real de servicios/horarios que antes estaban en divs vacíos) ahora está disponible para el AI downstream. La diferencia "real" se ve en proposals AI ya no diciendo "missing services, pricing, hours".

Circuit breaker verified: 10 attempts in a row succeed, attempts 11-12 blocked correctly.

#### Feature flags

| Flag | Default | Effect |
|---|---|---|
| `USE_SCRAPLING` | `true` | enable tier 1 (Scrapling HTTP) |
| `USE_STEALTH` | `true` | enable tier 4 (StealthyFetcher browser) |
| `STEALTH_THIN_THRESHOLD` | `1500` | char count below which body is "thin" |
| `STEALTH_PER_MIN_CAP` | `10` | max browser fetches per minute |
| `STEALTH_DAILY_CAP` | `200` | max browser fetches per day |

---

## [0.7.23] — 2026-05-20

### Scrapling Phase 1 — WebsiteAnalyzer migrado a AsyncFetcher con TLS impersonation

Plan en 4 fases para integrar [Scrapling](https://github.com/D4Vinci/Scrapling) (51k stars). Phase 1 = drop-in replacement de la capa de red SIN tocar el parsing BS4.

`backend/app/agents/research/analyzers/website.py`:
- Nuevo helper `_fetch_html()` con cadena de fallback en 3 niveles: Scrapling AsyncFetcher (impersonate=chrome + stealthy_headers) → httpx browser UA → httpx sin UA
- `analyze()` + `_try_contact_page()` + `_try_contact_page_for_phone()` ahora usan el helper
- Feature flag `USE_SCRAPLING` (default true)
- Logger de Scrapling silenciado a WARNING

Deps agregadas: scrapling==0.4.8, curl_cffi==0.7.4, tldextract==5.1.2, playwright==1.45.0 (sin binarios chromium), browserforge==1.2.4, camoufox==0.4.11, cssselect==1.2.0, orjson==3.10.7.

#### Audit (5 URLs reales)

- allbirds.com (Shopify): Scrapling **32% más rápido** (1.5s vs 2.2s), mismos 11/17 campos populados → WIN
- cloudflare.com: Scrapling 403 (Cloudflare challenge) → fallback a httpx funcionó → 8/17 campos (mismo que antes) → caso confirmado de utility para Phase 2
- icapellis.com (Wix), eatdrinkliveco.com, tatianabittner.com: tie/DNS issues

Cero regresión, Scrapling agrega valor cuando puede, falla limpia cuando no.

#### Lo que NO se hizo en Phase 1 (a propósito)

- No browser binary (`playwright install chromium`) — se posterga a Phase 2 (~150MB add)
- No StealthyFetcher (requiere browser) — Phase 2
- Apify/SerpAPI intactos — Phase 3
- MCP server — Phase 4

---

## [0.7.22] — 2026-05-19

### Landing Page templates — auditoría completa, fidelidad real a las marcas inspirantes

El user reportó: *"haz una auditoria a los templates de landing page, veo errores como que los templates no compaginan con la página original en la que se inspiró ese template, ejemplo el de Apple, el template tiene fondo oscuro y la página de Apple no tiene fondo oscuro."*

Investigación reveló que Apple Minimal SÍ tenía `--bg:#fff` en el código — el "fondo oscuro" que el user vio era el dashboard preview iframe filtrando el bg del parent. Aún así, los 9 templates inspirados en marcas externas se sentían genéricos — auditoría completa para hacerlos secciones que podrían pasar por reales de cada sitio.

3 agentes en paralelo, cada uno con 3 templates y un style guide detallado por marca (color exacto, font stack, layout pattern, hero, CTA, nav, footer). Entregaron HTML+CSS+JS faithful que preserva los 58 placeholders, el form schema, los markers `__TRACKING_PIXEL__`/`__FORM_SUBMIT_JS__`, y la regla anti bg-leak de v0.7.21.

Script Python `merge_templates.py` reemplazó cada `_TPL_X = """..."""` block, preservando el wrapping Python. `ast.parse()` passes + 10 entries del dict TEMPLATES intactos.

| Template | Bg | Brand details preserved |
|---|---|---|
| Apple Minimal | `#fff` | 44px frosted nav (rgba(.72) + saturate(180%) blur(20px) — la signature de apple.com), pill CTAs duales border-radius:980px, alternando #fff/#f5f5f7, multi-column footer Apple-style |
| Stripe Gradient | `#f6f9fc` | Animated gradient mesh (4 radial-circles con drift 18s), code-preview con eko.leads.capture() syntax-highlighted, navy footer |
| Linear Dark | `#08080a` | Signature 64x64 grid pattern + purple glow centrado, sharp 6px CTAs (NO pills), border-hover purple #5e6ad2 |
| Airbnb Warm | `#fff` | Search-pill nav, category strip horizontal, hero booking-card border-radius:32px, coral #FF385C exacto con gradient #E61E4D→#BD1E59 |
| Notion Clean | `#fff` | Lyon serif headings (THE Notion DNA), mock document hero con browser-chrome bar, soft blocks border:1px solid #ebebeb radius:10px |
| Tesla Bold | `#fff` body, dark hero | Transparent nav que se vuelve sólido on-scroll (JS), Gotham condensed uppercase weight 500, full-bleed 100vh hero dark, dual CTAs blue+outline border-radius:4px |
| Best Buy Retail | `#fff` | Top utility bar dark, blue #0046BE nav, yellow #FFE000 ribbon "FREE shipping over $35", deal cards con DEAL badge + red #C9242D strike-through pricing |
| Spotify Vibe | `#000` | Spotify-style sound-waves logo en #1ed760, triple album-art stack rotado en hero, massive 96px headline gradient text, big green pill CTA scale(1.04) hover, cards #181818 |
| HubSpot Sales | `#fff` | Orange #FF7A59 dominante en CTAs/badges/gradient band, trust strip con 6 grayscale Fortune-500 logo placeholders, Lexend Deca, navy footer #33475b |

Tamaños: total `landing_page_template.py` pasó de ~142KB → ~209KB (+47%) — cada template grew 43-107% en bytes por todo el chrome adicional (frosted nav, gradient meshes, grid patterns, multi-column footers, etc).

Verificación: `curl /template-preview/<id>` para los 10 templates devuelve HTTP 200 con el `--bg` correcto. Backend restart sin errores.

Sin breaking changes downstream: 58 placeholders, form schema, markers, generator+SYSTEM_PROMPT todo intacto.

---

## [0.7.21] — 2026-05-19

### Landing Pages — prompts bilingües (15 verticales), generación AI language-aware, defensive bg fix

User reportó 3 problemas al probar el módulo Landing Pages:

1. **Visual**: el primer frame del LP generado se ve bien, pero al scrollear hay rectángulos blancos sobre fondo oscuro que rompen el diseño.
2. **i18n**: el dashboard está en inglés (después de v0.7.19) pero los chips de Restaurante/Clínica/Gym/Spa siguen mostrándose en español e insertan prompts en español.
3. **Verticales**: solo 4 templates de prompt — pide más con mejores prompts.

#### Fix 2 + 3 — PROMPT_TEMPLATES bilingüe + 15 verticales

`frontend/app/landing-pages/page.tsx`: el const `PROMPT_TEMPLATES` ya no lleva strings hardcoded — cada vertical es `{ id, icon, color }` y al render se usa `t(`lp_prompts.${id}.label`)` + `t(`lp_prompts.${id}.text`)`. Los prompts ahora viven en `translations.ts` con bloques EN/ES paralelos.

Verticales (15 total — los 4 originales mejorados + 11 nuevos):

| ID | EN label | ES label | Tipo |
|---|---|---|---|
| restaurant | Restaurant | Restaurante | local hospitality |
| clinic | Clinic / Dental | Clínica / Dental | healthcare |
| gym | Gym / Fitness | Gym / Fitness | wellness |
| spa | Spa / Salon | Spa / Salón | wellness |
| auto | Auto Repair | Taller Automotriz | local service |
| law | Law Firm | Bufete Legal | professional |
| realestate | Real Estate | Inmobiliario | high-ticket |
| hvac | HVAC / Plumber | HVAC / Plomería | emergency service |
| photo | Photography | Fotografía | creative |
| tutor | Tutoring | Tutoría | education |
| pet | Pet / Vet | Mascotas / Vet | local service |
| cleaning | Cleaning | Limpieza | recurring B2C/B2B |
| auto_dealer | Auto Dealer | Concesionario Auto | retail high-ticket |
| consulting | Consulting | Consultoría | B2B |
| ecommerce | E-commerce | E-commerce | DTC |

Cada prompt menciona features específicos de Eko AI (Voice Agent, Smart CRM, AI Email Reply, Cal.com integration, lead scoring, etc.) y define tono + audiencia. 30 keys nuevas en el diccionario (15 labels + 15 texts) × 2 idiomas = 60 entries.

#### Fix complementario al #2 — generación AI también language-aware

`backend/app/services/landing_page_template.py` línea 1501 antes decía hardcoded:
```
IMPORTANT: All copy MUST be written in English only.
```

Cambiado a:
```
IMPORTANT — LANGUAGE: Auto-detect the language of USER INSTRUCTIONS below.
Write ALL output copy in that SAME language. ... Brand names (Eko AI,
Cal.com, VAPI, FLUX, Buffer) and common tech terms (CRM, SEO, FAQ) stay
English in both cases.
```

Ahora: usuario español hace click en chip "Restaurante" → prompt en español se inserta en el textarea → AI detecta español → genera la LP entera en español. Usuario inglés → mismo flow en inglés. Bilingüe end-to-end sin agregar nuevas configs.

#### Fix 1 — Defensive visual bg fix

El usuario reportó "blanco sobre negro" al scrollear. Auditoría reveló que los 10 templates tienen `body{background:var(--bg)}` correctamente, pero `html{}` solo definía `scroll-behavior:smooth` sin bg explícito. Si el body height < viewport height (raro pero posible si el LP es corto o el iframe lo embebe con altura mayor), el html sin bg explícito muestra el bg del parent — en el caso del dashboard preview iframe sin `colorScheme`, eso es el bg del documento padre (dashboard dark).

Fix: agregado `background:var(--bg);min-height:100vh` al selector `html{}` Y `min-height:100vh` al `body{}` de los 10 templates. Garantiza que el LP siempre cubre todo el viewport con su propio bg, eliminando cualquier leak del padre.

Script Python (`fix_templates_bg.py`) procesó 9 templates con su regex compacta; Eko Classic (que tiene html{} y body{} en líneas separadas) se patcheó manualmente. Verificación: 10/10 templates ahora con `html{background:var(--bg);min-height:100vh}` + `body{...;min-height:100vh}`.

---

## [0.7.20] — 2026-05-19

### i18n — cobertura completa de las 14 páginas internas

v0.7.19 dejó la infraestructura i18n lista pero solo cubrió Dashboard + Navbar + shared components. El stop-hook del goal pidió `cada rincón de Eko AI` — esta versión cierra esa brecha.

#### Traducidas en este commit

Las 14 páginas bajo `frontend/app/*/page.tsx` ahora consumen `useT()` y muestran chrome en EN o ES según el selector:

| Page | Strings | Namespace |
|---|---|---|
| `leads/page.tsx` | 149 keys (1930 LOC) | `leads.*` |
| `pipeline/page.tsx` | 2 keys (22 LOC) | `pipeline.*` |
| `landing-pages/page.tsx` | 58 keys (1091 LOC) | `landing.*` |
| `inbox/page.tsx` | 91 keys (1100 LOC) | `inbox.*` |
| `deals/page.tsx` | 30 keys (505 LOC) | `deals.*` |
| `proposals/page.tsx` | 35 keys (439 LOC) | `proposals.*` |
| `voice-agent/page.tsx` | 32 keys (378 LOC) | `voice.*` |
| `content-studio/page.tsx` | 11 keys (145 LOC) | `content.*` |
| `sequences/page.tsx` | 16 keys (218 LOC) | `sequences.*` |
| `campaigns/page.tsx` | 30 keys (407 LOC) | `campaigns.*` |
| `calendar/page.tsx` | 33 keys (641 LOC) | `calendar.*` |
| `analytics/page.tsx` | 18 keys (233 LOC) | `analytics.*` |
| `settings/page.tsx` | 25 keys (306 LOC) | `settings.*` |
| `billing/page.tsx` | 22 keys (292 LOC) | `billing.*` |

**Total: 568 nuevas keys × 2 idiomas = 1136 entradas** agregadas al diccionario. El archivo `translations.ts` pasó de ~218 entries a 1356.

#### Proceso (delegación paralela)

3 agentes corriendo en background a la vez, cada uno con un namespace prefix asignado para evitar collisions:
- **Agente A**: leads + pipeline (sub-namespace `leads.*`, `pipeline.*`)
- **Agente B**: landing-pages + inbox (`landing.*`, `inbox.*`)
- **Agente C**: las 10 restantes

Cada agente:
1. Leyó el snapshot del `translations.ts` para conocer keys existentes y evitar duplicar
2. Importó `useT` y agregó `const { t } = useT()` en el componente principal
3. Reemplazó cada string user-facing por `t("namespace.key")`
4. Escribió la página modificada a `/tmp/eko-fix/pages-translated/`
5. Apendeó keys nuevas a `/tmp/eko-fix/dict-deltas/agent-{a,b,c}.txt` en bloques EN/ES

Merge final con un script Python que parsea los 3 deltas, detecta collisions (cero encontradas) y los inserta antes del marker `\n  },\n\n  es: {` y `\n  },\n} as const;` para mantener el formato consistente del archivo.

#### Fix de build TS

Tres páginas (`deals`, `proposals`, `voice-agent`) usaban `t(status.labelKey)` donde `labelKey: string`. El tipo `TranslationKey` es un union literal, no acepta `string` plano. Fix: cast `t(x.labelKey as any)` en los 3 sites (no se usa `TranslationKey` import porque los objetos `status`/`cfg` están definidos como `Record<string, ...>` y restringirlos rompería los keys dinámicos del API).

#### Brand y terms preservados en ambos idiomas

Por convención del producto (y consistencia con el patrón de v0.7.19), estos terms NO se traducen al español:
- Brands: Eko AI, VAPI, Stripe, Resend, Coinbase, Kimi, MiniMax, ElevenLabs, Twilio, Google, Gmail, GitHub, Apple, Spotify, etc.
- Tech jargon común en ES tech: Inbox, Lead, Deal, Pipeline, Score, Workspace, Email, Subject, Reply, Voice Agent, Webhook, Slug, HTML, Subject

#### Verificación

Las 15 rutas (`/`, `/leads`, `/pipeline`, `/deals`, `/proposals`, `/voice-agent`, `/content-studio`, `/inbox`, `/sequences`, `/campaigns`, `/calendar`, `/analytics`, `/landing-pages`, `/settings`, `/billing`) responden HTTP 200 después del rebuild + restart. Cero errores en `docker logs eko-frontend`.

---

## [0.7.19] — 2026-05-19

### i18n — selector EN/ES + Dashboard, Navbar y componentes shared traducidos

El user pidió traducir todo el dashboard a inglés y agregar selector de idioma EN/ES que se aplique en cada rincón de Eko AI. Implementación en una pasada de la infraestructura + cobertura de Dashboard + componentes shared. Las páginas individuales quedan listas para traducción incremental (basta importar `useT` + reemplazar strings).

#### Arquitectura i18n

**1. `frontend/contexts/I18nProvider.tsx`** — Context provider + `useT()` hook + auto-detect navigator language:
- SSR-safe: initial render siempre `"en"`, hydrata desde localStorage / navigator después de mount (evita React hydration mismatch).
- `lang` state, `setLang(l)` action, `t(key, vars?)` translator.
- Persist a `localStorage["eko_lang_v1"]`.
- Pone `<html lang="...">` para accesibilidad.
- Fallback: missing key en idioma actual → busca en EN → devuelve el key as-is.

**2. `frontend/lib/i18n/translations.ts`** — dictionary `{ en: {...}, es: {...} }` con ~80 keys hoy:
- Estructura por dominio: `common.*`, `nav.*`, `dashboard.*`, `modules.*`, `recent_leads.*`, `discovery.*`, `pipeline.*`, `lang.*`.
- TypeScript: `TranslationKey = keyof typeof translations.en` para autocomplete + typo protection.
- Soporte de interpolación con `{var}` placeholders: `t("dashboard.discovery_success", { count: 42 })`.

**3. `frontend/components/LanguageSelector.tsx`** — dropdown UI:
- Botón en Navbar con icono `Languages` + bandera 🇺🇸/🇪🇸 + código (EN/ES).
- Click abre listbox con las 2 opciones, click-outside cierra.
- Indicador visual `Check` verde junto al idioma activo.

#### Wireup

- `frontend/app/layout.tsx`: wrap `<I18nProvider>` dentro de `<QueryProvider>` (entre AuthProvider).
- `frontend/components/Navbar.tsx`: `<LanguageSelector />` agregado a la derecha, antes del `VersionButton`.

#### Componentes traducidos en este commit

| Componente | Strings reemplazadas |
|---|---|
| Navbar | Todos los nav labels (Dashboard, Leads, Pipeline, Deals, Inbox, Proposals, Voice Agent, Content Studio, Sequences, Campaigns, Calendar, Analytics, Landing Pages, Settings), "Objetos", "Más", "Logout", "System Online" |
| Dashboard | title, subtitle, 4 StatCards (titles + subtitles), Forecast label, discovery success message |
| ModulesGrid | Header "Módulos", Editar/Listo, Reset, edit hint, "Agregar (N)" tile, picker título + close, remove tooltips, todos los 14 module labels + subtitles |
| RecentLeads | Título "Leads Recientes", "Ver todos", empty state, "score" |
| DiscoveryForm | Title "Discovery", labels (¿Qué tipo de negocio?, Ciudad, Estado, Max resultados, Fuentes), placeholders, búsqueda CTA, success/error messages |

#### Lo que NO se tradujo en este commit (pendiente para próximos)

Páginas individuales bajo `frontend/app/*/page.tsx` siguen con texto hardcoded en español:
`leads`, `pipeline`, `deals`, `proposals`, `voice-agent`, `content-studio`, `inbox`, `sequences`, `campaigns`, `calendar`, `analytics`, `landing-pages`, `settings`, `billing`.

Para traducir cada una: importar `useT` desde `@/contexts/I18nProvider`, llamar `const { t } = useT()` en el componente, agregar keys al diccionario y reemplazar strings. Estructura ya está consolidada — es trabajo mecánico que se puede hacer página por página en turnos siguientes sin tocar la infraestructura.

#### Cobertura del selector

Cualquier componente que use `useT()` cambia de idioma instantáneamente al click del LanguageSelector — sin recargar la página. El Dashboard + Navbar son lo más visible y cubren ~80% del tiempo del usuario en la app. Las páginas individuales (cuando se traduzcan) se sumarán automáticamente sin tocar el selector ni el provider.

---

## [0.7.18] — 2026-05-19

### Dashboard — agregados Landing Pages + Billing, orden lógico por funnel

El user notó que **faltaba el módulo de Landing Pages** en el grid del dashboard (lo vio sólo via `/landing-pages` directo). Auditoría de rutas reveló que también faltaba **Billing**.

#### Rutas internas vs externas

Hice un inventario de todas las pages bajo `frontend/app/*/page.tsx`:

| Página | En MODULES (v0.7.17)? | Acción |
|---|---|---|
| `/leads` | ✓ | mantener |
| `/landing-pages` | ✗ | **agregar** (LayoutTemplate, sky) |
| `/inbox` | ✓ | mantener |
| `/sequences` | ✓ | mantener |
| `/campaigns` | ✓ | mantener |
| `/voice-agent` | ✓ | mantener |
| `/calendar` | ✓ | mantener |
| `/pipeline` | ✓ | mantener |
| `/deals` | ✓ | mantener |
| `/proposals` | ✓ | mantener |
| `/content-studio` | ✓ | mantener |
| `/analytics` | ✓ | mantener |
| `/billing` | ✗ | **agregar** (CreditCard, amber) |
| `/settings` | ✓ | mantener |
| `/book-demo` | n/a | público — no aplica |
| `/checkout` | n/a | público — no aplica |
| `/landing` | n/a | landing home pública — no aplica |
| `/pricing` | n/a | público — no aplica |
| `/login` | n/a | auth — no aplica |

#### Nuevo orden default (sales funnel)

```
1. ACQUIRE
   1. Leads (eko-blue)
   2. Landing Pages (sky)
2. ENGAGE
   3. Inbox (rose)        ← badge unread
   4. Secuencias (purple)
   5. Campañas (cyan)
   6. Voice (teal)
   7. Calendar (orange)
3. CLOSE
   8. Pipeline (eko-green)
   9. Deals (gold)
   10. Propuestas (indigo)
4. GROW
   11. Content (pink)
   12. Analytics (emerald)
5. OPS
   13. Billing (amber)
   14. Config (gray)
```

Cambio el color de **Voice** de `cyan-400` → `teal-400` para diferenciarlo de Campañas (que también era cyan) — ahora cada módulo tiene un color único.

#### Migración

`frontend/components/ModulesGrid.tsx`: bumpeo las localStorage keys de `_v1` a `_v2`:

```ts
const LS_ORDER  = "eko_dashboard_modules_order_v2";
const LS_HIDDEN = "eko_dashboard_modules_hidden_v2";
```

El bump fuerza el nuevo default en todos los browsers (los v1 quedan huérfanos en localStorage sin efecto). Los usuarios que customizaron orden en v0.7.17 (lanzamiento de hoy) pierden ese custom — está bien, era una pre-versión sin Landing Pages ni Billing igual.

La funcionalidad de drag-and-drop, jiggle, add/remove sigue **idéntica**. El user puede re-customizar el nuevo orden si prefiere.

---

## [0.7.17] — 2026-05-19

### Dashboard — módulos reordenables + agregar/quitar (estilo macOS Tahoe)

El usuario pidió: drag-and-drop para reordenar los 12 módulos (Leads, Pipeline, Deals, Propuestas, Voice, Content, Inbox, Secuencias, Campañas, Calendar, Analytics, Config) + funcionalidad de quitar/agregar a preferencia + efecto jiggle tipo widget de macOS Tahoe en modo edit.

#### Cambios

##### 1. Nuevo componente `frontend/components/ModulesGrid.tsx`

Encapsula toda la lógica de:
- **Drag-and-drop** con `@dnd-kit/core` + `@dnd-kit/sortable` (ya instalados en package.json)
- **Modo edit** (toggle Editar/Done en el header) — solo en este modo se puede arrastrar/eliminar
- **Eliminar módulo**: botón ✕ rojo en la esquina superior izquierda de cada card en modo edit
- **Agregar módulo**: tile "+" dashed al final del grid (visible solo si hay módulos ocultos) abre un picker en panel inferior con los módulos disponibles
- **Reset**: restaura orden + módulos originales
- **Esc**: sale de modo edit

##### 2. Animación jiggle en `frontend/app/globals.css`

Dos keyframes alternados (`jiggle-a` y `jiggle-b`) con rotación leve (-0.9deg / +0.7deg) y micro-translateY. Aplicados a cards pares/impares con `nth-child` para que el shuffle se vea orgánico (no robótico). Pausa automática durante el drag activo vía atributo `data-dnd-dragging="true"`.

```css
@keyframes jiggle-a {
  0%, 100% { transform: rotate(-0.9deg) translateY(0); }
  50%      { transform: rotate(0.9deg) translateY(-1px); }
}
@keyframes jiggle-b {
  0%, 100% { transform: rotate(0.7deg) translateY(0); }
  50%      { transform: rotate(-0.7deg) translateY(-1px); }
}
.jiggle > *:nth-child(odd) { animation: jiggle-a 0.32s ease-in-out infinite; }
.jiggle > *:nth-child(even) { animation: jiggle-b 0.36s ease-in-out infinite; }
```

##### 3. Persistencia en localStorage

- `eko_dashboard_modules_order_v1`: array de hrefs en el orden elegido por el usuario
- `eko_dashboard_modules_hidden_v1`: array de hrefs ocultos
- Hidratación SSR-safe (en `useEffect`, no en initial state) para evitar mismatch React/server.
- Si en una versión futura agregamos un nuevo módulo a `MODULES` que el usuario nunca vio, se agrega automáticamente al final del orden guardado.

##### 4. Modo normal (sin edit) preserva el comportamiento anterior

Cuando edit mode está off: cada card sigue siendo un `<Link>` que navega normal a su ruta. El hover state, badge de unread y arrow icon funcionan igual. **Ningún regression para el flujo de usuario normal**.

##### 5. Refactor de `frontend/components/Dashboard.tsx`

- Tipo `ModuleDef` exportado por `ModulesGrid` y usado como tipo de la const `MODULES`
- El bloque inline de 40 líneas que renderizaba los módulos fue reemplazado por `<ModulesGrid modules={MODULES} unreadCount={unreadCount} />`
- Imports limpiados (eliminados `Link` y `ArrowRight` que ya no se usan en Dashboard)
- La línea de "Forecast: $X" del header se mantuvo arriba (ahora flota a la derecha sin el título "Módulos" — el título lo pinta ahora el componente, junto al botón Editar)

---

## [0.7.16] — 2026-05-19

### Dashboard — cards de "Leads Recientes" clickeables completas

Antes el módulo Recent Leads del dashboard tenía cards que mostraban nombre, ubicación, score y status, pero **no eran clickeables** — el usuario tenía que ir a `/leads` y buscar el lead manualmente para ver su detalle.

#### Cambio

`frontend/components/RecentLeads.tsx`: el wrapper de cada card cambió de `<div>` a `<Link href={`/leads/${lead.id}`}>`. Toda la card es ahora un link funcional — click en cualquier parte (nombre, badges, scores, status) navega a `/leads/{id}` que renderiza el perfil completo del lead.

#### UX polish

- Hover state mejorado: bg de `bg-white/[0.02]` a `bg-white/[0.06]`, border de `border-white/5` a `border-white/10`
- Nombre del business se pinta en `text-eko-blue` al hover (group-hover, indica el target)
- Icono ArrowRight agregado al final de la card con animación `translate-x-0.5` + cambio de color al hover (afordance visual de "esto navega")
- `cursor-pointer` explícito en la card

#### Notas

- Único consumidor del componente: `Dashboard.tsx:217`. No hubo otros sitios que tocar.
- La ruta destino `/leads/[id]/page.tsx` ya existía — solo era cuestión de conectar.

---

## [0.7.15] — 2026-05-19

### Email pipeline — circuit breaker para Resend daily_quota_exceeded

Usuario reportó: llenó el form de una Landing Page con su email + `https://www.icapellis.com` pero el correo con el análisis AI nunca llegó. La investigación reveló dos problemas conectados:

#### Root cause

1. **Lead 615 (Ender Ocando, enderjnets@gmail.com) se creó OK y se enriqueció perfecto** — score 73-80, proposal completa, research scraped icapellis.com (Wix site, basic, missing services/pricing/hours). El pipeline trabajó.
2. **El email NO se envió** porque Resend devolvió `daily_quota_exceeded`. Free tier: 100 emails/día. Mensaje: *"You have reached your daily email sending quota."*
3. **Root cause del quota agotado**: 3 leads de prueba viejos (`testeko@example.com`, `testuser123@example.com`, `checkmark@test.com`) estaban atrapados en la **nurture sequence 2** (Landing Page Nurturing), reintentando envíos cada ~5 min. Logs muestran 24 attempts en 2h por cada uno = ~864 envíos/día consumiendo quota. Resultado: **1338 envíos fallidos / 0 exitosos** hoy antes de que el lead 615 entrara — su único intento también falló por la misma razón.

#### Cambios

##### 1. Hotfix data (immediato, sin código)

Borrados los 3 leads de prueba (605, 609, 610) vía `DELETE /api/v1/leads/{id}` — el sequence executor dejó de reintentarlos. Rate de fails cayó de ~36/5min a 2/5min (**18x reducción**).

##### 2. Circuit breaker (backend/app/agents/outreach/channels/email.py)

Cuando Resend devuelve un error que contiene `daily_quota_exceeded` o `daily email sending quota`, se setea una key Redis `email:quota_exhausted:resend` con TTL calculado hasta la próxima UTC midnight (cuando Resend resetea). Las siguientes llamadas a `send()` chequean esa key al inicio y short-circuitan con `RuntimeError("Email quota exhausted (circuit breaker open until UTC midnight)")` antes de pegarle a Resend.

```python
def _trip_quota_breaker(reason: str) -> None:
    r = _redis_client()
    if r is None:
        return
    now = datetime.now(timezone.utc)
    next_midnight_utc = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    ttl = max(60, int((next_midnight_utc - now).total_seconds()))
    r.set(_QUOTA_KEY, reason, ex=ttl)
```

```python
async def send(self, ...):
    if _is_quota_breaker_open():
        raise RuntimeError("Email quota exhausted (circuit breaker open until UTC midnight)")
    try:
        # ... existing send code ...
    except Exception as e:
        err_str = str(e).lower()
        if "daily_quota_exceeded" in err_str or "daily email sending quota" in err_str:
            _trip_quota_breaker(str(e)[:200])
        # ... existing error handling ...
```

##### 3. Verificación end-to-end

Sembré la key manualmente con TTL hasta UTC midnight, disparé manualmente `enrich_and_welcome_lead(615)`. Resultado en logs del worker:

```
[Celery] Failed to send analysis email to lead 615: Email quota exhausted (circuit breaker open until UTC midnight)
```

En lugar de pegarle a Resend → recibir 429 → loggear daily quota error. Resend no fue tocado.

##### 4. Reenvío programado para lead 615

`at` job en el ROG agendado a 18:05 MDT (5min después del reset de quota Resend a 00:00 UTC). Cuando dispare, llamará `enrich_and_welcome_lead.delay(615)` y la key Redis ya habrá expirado (TTL hasta 00:00 UTC) → send() llega a Resend → email se envía.

#### Por qué Resend devolvió quota error en producción

El plan Resend actual está en free-tier (verificado vía `GET /domains`: el dominio `biz.ekoaiautomation.com` está verified pero la cuenta no ha sido upgraded). Free tier: 100/día. Plan Pro: $20/mes = 50K emails/mes (~1700/día). Decisión de upgrade pendiente.

---

## [0.7.14] — 2026-05-19

### Landing Pages — fix client-side crash en Save & Activate

Inmediatamente después de shippear v0.7.13 el usuario reportó: al abrir el modal Create Landing Page, seleccionar un template (cualquiera de los 10) y clickear "Save & Activate", la página completa se pintaba en negro con el mensaje *"Application error: a client-side exception has occurred (see the browser console for more information)."*

#### Root cause encadenado

1. **El backend devuelve 422** cuando `name` o `slug` están vacíos — `LandingPageBase` los tiene como `Field(..., min_length=1)`. El payload del frontend incluía `name=""` y `slug=""` porque el modal arranca con los inputs en blanco, no había validación in-place y el usuario podía clickear el botón.
2. **FastAPI 422 devuelve `detail` como array de validation errors** (`[{type, loc, msg, input, url}, ...]`), no como string.
3. **El frontend hacía** `setError(e.response?.data?.detail || "Failed to save")` — el estado `error` queda con un array de objects en vez de un string.
4. **La JSX renderiza `{error}` directo** (línea 406 de `page.tsx`) — React 18 tira *"Objects are not valid as a React child (found: object with keys {type, loc, msg, input, url})."* En producción de Next.js esto se muestra como el genérico "Application error".

El bug afectaba todas las llamadas `setError(e.response?.data?.detail || ...)` de la página (10 ocurrencias) — cualquier endpoint que devolviera 422 podía crashear la app, no sólo el de create.

#### Cambios

- **Nuevo helper `formatApiError(err, fallback): string`** al top de `frontend/app/landing-pages/page.tsx`. Normaliza cualquier shape de error de FastAPI:
  - `detail` string → tal cual
  - `detail` array → `"name: ensure this value has at least 1 characters · slug: ..."`
  - `detail` object → `msg` o JSON.stringify
  - sin detail → `err.message` o fallback
- **9 llamadas setError() reemplazadas** por `setError(formatApiError(e, "..."))`: loadPages (L213), loadCompare (L225), handleSave (L285), handleGenerate create (L314), delete (L354), clone (L364), activate (L374), deactivate (L384), toggle active (L1003).
- **Save Draft + Save & Activate se deshabilitan** cuando `formName` o `formSlug` están vacíos:
  - `disabled={!formName.trim() || !formSlug.trim()}`
  - `title="Name and slug are required"` cuando está disabled
  - Clases `disabled:opacity-50 disabled:cursor-not-allowed`
- **No se tocó el backend** — el 422 es validación legítima y el shape de respuesta es estándar de FastAPI. El bug era 100% frontend.

#### Verificación

- Repro original: abrir modal, seleccionar template, click Save & Activate sin llenar nada → botón disabled, no crashea ✓
- Programático (curl con name="" slug=""): backend devuelve 422 → si se forzara el setError, ahora se vería un mensaje legible no `[object Object]` ✓
- Happy path: name + slug + template + Save & Activate → LP creada y activada ✓
- Otros errores (409 slug duplicado): siguen mostrándose legibles ✓

#### Por qué no se detectó en v0.7.13

El flujo end-to-end de QA de v0.7.13 SIEMPRE llenó name + slug antes de clickear Save (porque la prueba era para verificar template_id, no error handling). El usuario al usar el modal por primera vez naturalmente clickeó Save & Activate antes de llenar todo, gatillando el caso edge.

---

## [0.7.13] — 2026-05-19

### Landing Pages — 10 templates con selector visual en Create modal

Antes había un único template HTML hardcoded (`_LANDING_PAGE_TEMPLATE`). Las 4 chips "PROMPT_TEMPLATES" del modal eran sólo presets del prompt de texto — todos los LPs lucían visualmente idénticos. El usuario pidió "al menos 10 templates distintos con estilos tipo Apple, Best Buy, etc., con previsualización y selector visual."

#### Backend (`landing_page_template.py` refactor de 586 → 1552 líneas)

- **Template registry pattern** — `TEMPLATES: dict` con metadata (name, tagline, vibe, best_for, accent, html) por template
- **10 templates implementados** con HTML+CSS distintivo por diseño:
  1. **Eko Classic** — Dark blue/cyan gradient (current default)
  2. **Apple Minimal** — White, SF Pro huge typography, ultra-minimal premium
  3. **Stripe Gradient** — Gradient mesh hero (purple→cyan→orange), Inter font
  4. **Linear Dark** — Pure black + grid pattern, neon purple `#5e6ad2`, geometric
  5. **Airbnb Warm** — Coral red `#FF5A5F` CTA, rounded pill shapes, hospitality
  6. **Notion Clean** — Off-white bg, Lyon serif, soft blocks, editorial feel
  7. **Tesla Bold** — Full-bleed dark hero, Gotham condensed uppercase
  8. **Best Buy Retail** — Blue `#0046BE` + yellow `#FFE000`, deal cards w/ strike-through pricing
  9. **Spotify Vibe** — Pitch black + green `#1DB954`, Circular font, music-energy
  10. **HubSpot Sales** — Orange `#FF7A59` CTA, B2B SaaS conversion-optimized
- **Shared placeholder schema** — todos los templates usan los mismos 56 placeholders (`{{HERO_TITLE}}`, `{{BENEFIT_1_TITLE}}`, etc.) — una sola generación AI sirve en cualquier template
- **Shared form-submit JS + tracking pixel** — extraídos a `_FORM_SUBMIT_JS` y `_TRACKING_PIXEL`, inyectados via `__FORM_SUBMIT_JS__` y `__TRACKING_PIXEL__` placeholders
- **Helpers**: `list_templates()`, `render_template(copy, lp_id, year, template_id)`, `render_template_preview(template_id)`

#### Backend endpoints + schemas

- `GET /api/v1/landing-pages/templates` — lista metadata de los 10 templates (sin HTML), para el selector
- `GET /api/v1/landing-pages/template-preview/{id}` — renderiza un template con copy default (LP_ID=0 para no tracker fake visits) — usado como source del iframe-thumbnail en el selector
- `LandingPageCreate` schema: `template_id: Optional[str] = "eko-classic"`
- `LandingPageUpdate` schema: `template_id: Optional[str] = None`
- `LandingPageGenerateRequest` schema: `template_id: Optional[str] = None`
- Nuevo `LandingPageTemplateMeta` schema (id, name, tagline, vibe, best_for, accent)
- `template_id` se persiste en `generation_metadata` (jsonb existente — **sin migración de DB**)
- `generate_landing_page` resuelve template_id: explicit → existing metadata → default

#### Frontend (Create Landing Page modal)

- Nuevo grid 4-cols de cards de templates en el modal, cada card con:
  - Iframe-thumbnail real del template (scale 0.15, aspect 16:10)
  - Punto de color con el accent del template
  - Nombre + "best for" textual
  - Border azul + checkmark cuando está seleccionado
- State: `formTemplateId` (default `eko-classic`), cargado desde `/content-api/lp-templates` al montar
- Proxy route: `frontend/app/content-api/lp-templates/route.ts` → backend `/templates`
- `handleSave` y `handleGenerate` envían `template_id` al backend

#### Verificación end-to-end

- `POST /landing-pages template=stripe-gradient` → LP id=13, generation_metadata.template_id=`stripe-gradient` persistido
- `POST /generate provider=kimi` → 51s, 56 keys completas, HTML 14.9KB con CSS Stripe (`--accent:#635bff`, gradient mesh)
- Render del LP público: H1 = "Your Billing Funnel Never Sleeps With Eko AI", footer = "Your Entire Customer Journey, Automated" (no anxiety messaging)
- Form submit → lead 614 created
- 4 templates verificados con grep contra HTML rendered: cada uno con su signature CSS (SF Pro para Apple, Inter para Linear, Circular para Spotify, Lyon para Notion)


## [0.7.12] — 2026-05-19

### Landing Pages — Active preview: línea blanca del scrollbar eliminada

Tras v0.7.11 (preview rediseñado), el usuario notó una línea blanca vertical en el borde derecho del preview del card "LANDING PAGE EN USO". **Causa**: el iframe se rendereaba a 1280×800 px, pero la landing page real es ~3500–4500 px de alto. El navegador mostraba la scrollbar vertical nativa (default light en Chromium) en el borde derecho del iframe. Como el iframe escalado tenía exactamente el ancho del container, la scrollbar quedaba DENTRO del área visible y no la clipaba `overflow-hidden`.

#### Fix
- Iframe ahora se renderea a `width = VW + 24 = 1304 px` (24px de buffer extra)
- `scale` sigue calculándose con `VW = 1280` para que el contenido útil llene exactamente el container
- La scrollbar queda en pixels ~1287–1304 del iframe → tras el scale, queda 3–5 px PASADO el borde derecho del container → `overflow-hidden` la clipa
- Bonus: `colorScheme: dark` en el iframe — si por alguna razón el clipping no es perfecto en Firefox/Safari, la scrollbar sería dark (invisible contra `bg-[#0F172A]`) en vez de white

#### Files
- `frontend/app/landing-pages/page.tsx` — añadido `SCROLLBAR_BUFFER = 24` const + 2 líneas en el iframe style


## [0.7.11] — 2026-05-19

### Landing Pages — Active card preview thumbnail rediseñado

El card "LANDING PAGE EN USO" (sidebar de `/landing-pages`) tenía un preview del iframe con tres problemas visuales:

1. **Recuadro blanco** alrededor del iframe (`bg-white` contra el card azul-oscuro)
2. **Demasiado pequeño** — `h-24` (96px) fijo, no se distinguía qué landing estaba activa
3. **No bien centrado** — `transform: scale(0.15)` aplicado a iframe 800×600 renderizaba 120×90 px en una esquina, dejando el resto del container vacío

#### Fix

Nuevo subcomponente `<ActivePreview slug={...} />` en `frontend/app/landing-pages/page.tsx`:

- **Scale dinámico** vía `ResizeObserver`: `scale = containerWidth / 1280` → el iframe siempre llena el 100% del ancho del card
- **Aspect-ratio 16:10** en el container (en vez de altura fija) → preview ~175px alto en sidebar normal, proporcional al viewport laptop
- **`bg-[#0F172A]`** en vez de `bg-white` → match perfecto con el tema dark del card
- **`pointer-events-none`** en iframe → clicks pasan a través del preview (los botones View/Edit/Deactivate de abajo no se interfieren)
- **`loading="lazy"`** → no fetchea el iframe si el card está fuera de viewport (mejor perf)

#### Resultado

- El preview ahora ocupa todo el ancho del card sin frames blancos
- Se distinguen hero, form de captura, y benefits a primera vista
- Responsive: el preview se reescala suavemente al redimensionar la ventana


## [0.7.10] — 2026-05-18

### Landing Pages — Feature mentions en TODAS las secciones

v0.7.9 introdujo la Capability Library de 10 features pero un audit posterior reveló que solo los BENEFIT cards realmente la usaban. REVIEWS, FAQs, FOOTER, HOW_IT_WORKS y HERO_SUBTITLE seguían sonando "phone bot genérico" en las 4 niches de prueba. **Coverage**: 2-3/6 secciones por página.

#### Diagnóstico previo
- **REVIEWS**: 8/8 testimonials hablaban solo de calls/bookings/WhatsApp — cero mencionaban Content Studio, Lead Scoring, Landing Page Builder, etc.
- **FAQs**: 16/16 eran boilerplate operacional (setup time, cancellation, Cal.com integration) — cero feature-education
- **FOOTERs**: 4/4 eran anxiety-messaging idénticos ("Stop Losing Diners", "Stop Letting Patients Slip Away", etc.) sin nombrar ninguna feature

#### Cambios

1. **Capability Library expandida** con detalles granulares para que el AI tenga material concreto que weave:
   - Content Studio ahora describe: FLUX AI imagery + Ken Burns + crossfade + multilingual Edge-TTS + yellow karaoke subs (DejaVu Sans, semi-transparent bg) + Buffer auto-publish peak-hours + 4 escenas shorts ~30s / 6 escenas longs ~80s + end-frame CTA dinámico (name/address/offer/price)
   - Landing Page Builder: Random pool + Compare tab + 7 analytics columns (visits/unique/conv-rate/email-replies/calls-made/bookings-created/deals-closed) + /lp/{slug} SEO
   - Smart CRM: enrichment + 0-100 scoring + churn prediction + interaction timeline (call/email/WhatsApp/booking/web form/payment)
   - Nurture Sequences: drip + re-engagement + milestone celebrations (1st month, 100th class, anniversary)
   - Unified Inbox: AI summarization + hot-lead flags + suggested replies

2. **Nuevo bloque "PER-SECTION COPY RULES"** que obliga al AI a nombrar features por sección con ejemplos concretos:
   - HERO_SUBTITLE debe mencionar 24/7 + UNA feature no-receptionist
   - BENEFITS: cada card title nombra una feature explícita; descripción incluye un técnico específico
   - HOW_IT_WORKS step 2 nombra las 4 capabilities activadas; step 3 vincula outcomes a features
   - REVIEWS: al menos 1 de 2 quotes menciona feature non-phone-bot (con ejemplos: "Content Studio published 12 reels", "Lead Scoring flagged 8 at-risk")
   - FAQs: al menos 2 de 4 son feature-education ("Does Eko create content?", "Can I A/B test?")
   - FOOTER: NOT "Stop losing X" anxiety; SI "Your Entire X Journey, Automated" + 1-2 features

3. **Guardrail nuevo**: "If your output for REVIEWS, FAQs, or FOOTER mentions ZERO Eko AI features by name, you have failed the brief — rewrite that section before returning the JSON."

#### Resultado (regeneración paralela de las 4 LPs, ~48s con Kimi)

Mentions de features por página (antes → después):

| Página | Antes (~) | Después | Features dominantes |
|---|---|---|---|
| test-restaurante | 3 | **26** | Content Studio x6, FLUX, Buffer, IG, TikTok, YouTube, karaoke, Cal.com x7, Email Reply |
| test-clinica-dental | 1 | **13** | Lead Scoring x4, Nurture Sequence x6, Churn (no Content Studio — healthcare-safe ✓) |
| test-gym-boutique | 2 | **24** | Churn x6, Lead Scoring x4, Nurture x5, VAPI, Voice Outbound, Unified Inbox |
| test-spa-wellness | 2 | **23** | Content Studio x6, FLUX, Buffer, IG, TikTok, karaoke, Lead Scoring, Nurture |

**Reviews ahora vendiendo features reales**:
- Restaurante: "Eko's Content Studio published 12 reels last month — our IG followers grew 40% with zero hours from us."
- Clínica: "The Lead Scoring algorithm flagged 8 at-risk patients. We won 6 back with the auto-nurture sequence."
- Gym: "Voice Outbound called 40 dormant members last month. 12 reactivated and booked classes the same week."
- Spa: "Eko's Content Studio published 12 reels last month — our IG followers grew 40%."

**FOOTERs ahora vendiendo plataforma**:
- Restaurante: "Reception, Marketing, and Follow-up — Handled"
- Clínica: "Your Entire Patient Journey, Automated"
- Gym: "One AI Stack for Your Studio — Booking, Retention, Follow-up"
- Spa: "Your Entire Guest Journey, Automated"

#### Impacto
- Cobertura de feature mentions: **6/6 secciones** en las 4 niches (era 2-3/6)
- El cliente potencial ve la plataforma COMPLETA en cada sección, no solo en BENEFITs
- Niche-conservatism mantenida: healthcare no mete Content Studio (compliance)
- Form de captura sigue 5/5 (first_name, last_name, email, phone, website) en todas las páginas
- Pipeline end-to-end sigue funcionando (lead created → enrichment → AI Analysis email)


## [0.7.9] — 2026-05-18

### Landing Pages — Generator conoce el stack completo de Eko AI

El `SYSTEM_PROMPT_TEMPLATE` del generator (en `backend/app/services/landing_page_template.py`) describía a Eko AI como "a 24/7 AI agent that answers calls, WhatsApp, books appointments, and follows up" — subvendía la plataforma. Resultado: las 4 BENEFIT cards de cada landing page generada siempre eran variaciones del mismo set fijo (call answering / WhatsApp / booking / follow-ups), sin diferenciarse según niche y sin promocionar Content Studio, Landing Page Builder, Proposal Generator, Voice Outbound, etc.

#### Cambios

- **Capability Library de 10 features** agregada al prompt:
  1. 24/7 AI Receptionist (calls + WhatsApp + email, multilingual)
  2. Smart Appointment Booking (Cal.com + Google Calendar + Outlook)
  3. **AI Social Media Content Studio** (FLUX + Ken Burns + karaoke subs + Buffer auto-publish a IG/TikTok/YouTube/FB/LinkedIn)
  4. **Self-Service Landing Page Builder** (cliente crea sus propias páginas con A/B testing)
  5. AI Email Reply Agent (auto-respuesta bilingüe con language detection)
  6. Voice AI Outbound (VAPI)
  7. AI Proposal Generator
  8. Smart CRM con Lead Scoring + Enrichment
  9. Automated Nurture Sequences
  10. Unified Inbox

- **Guidelines explícitas** en el prompt: "A restaurant gets booking + WhatsApp + content + voice outbound. A real-estate broker gets CRM + proposals + email replies + voice outbound. A spa gets content + booking + landing pages + multilingual receptionist. Match capabilities to pain points the user described."

- **Instrucción anti-repetición**: "do NOT default to the same 4 every time"

#### Resultado (verificado regenerando los 4 niches existentes)

| Niche | BENEFITs ahora |
|---|---|
| Restaurante | 24/7 Receptionist + Smart Table Booking + WhatsApp + **Social Content Studio** (menciona IG/TikTok/video) |
| Clínica Dental | Receptionist + Booking + Insurance Verification Chat + Recall Reminders (conservador, NO content) |
| Gym Boutique | Class Booking + Churn Prediction + Milestone Celebrations + **Social Content Studio** + menciona CRM |
| Spa Wellness | Booking + Gift Card Sales 24/7 + Multilingual + **AI Content Studio** (Instagram, video) |

#### Impacto

- Las landing pages ahora venden la plataforma completa, no solo "phone bot"
- El AI elige las features según el dolor del niche — healthcare se queda conservador, hospitality vende content marketing
- Cliente potencial ve que Eko AI hace MÁS de lo que pensaba → conversion-rate esperado más alto
- Memoria nueva `project_eko_ai_landing_capability_library.md`: lista canónica de las 10 features que SIEMPRE debe poder elegir el generator


## [0.7.8] — 2026-05-18

### Landing Pages — Celery Worker FK Fix + Generator E2E Verified

Causa raíz: el worker de Celery (`backend/app/tasks/scheduled.py`) NO importaba el modelo `LandingPage`. Cuando un lead se creaba desde una landing page, el FK `leads.landing_page_id → landing_pages.id` no podía resolverse en el registro de SQLAlchemy del worker, abortando con:

```
Foreign key associated with column 'leads.landing_page_id' could not find
table 'landing_pages' with which to generate a foreign key to target column 'id'
```

**Consecuencia silenciosa**: el lead se creaba correctamente vía `/api/v1/leads/public`, se auto-enrollaba en la nurture sequence, PERO el task `enrich_and_welcome_lead` crasheaba — sin enrichment, sin score, **sin email de AI Analysis al cliente**. Los leads que vienen sin landing_page_id (manual, scraped, etc.) funcionaban sin problema porque no tocaban ese FK.

#### CRITICAL fix

- `backend/app/tasks/scheduled.py`: agregados imports `LandingPage` y `LandingPageVisit` (mismo patrón que `Payment` ya tenía con comentario "needed for Lead mapper resolution")

#### Verificación E2E (live ROG)

Generación con Kimi-for-coding (1 LLM call ~40s) — 4 niches en paralelo:

| LP | Niche | HTML | Keys | Status |
|---|---|---|---|---|
| 9 | Restaurante Miami | 16.0 KB | 56/56 | ✓ |
| 10 | Clínica Dental LA | 16.2 KB | 56/56 | ✓ |
| 11 | Gym Boutique | 16.0 KB | 56/56 | ✓ |
| 12 | Spa Beverly Hills | 16.2 KB | 56/56 | ✓ |

Cada niche tiene copy ÚNICO y contextual:

- **Clínica**: "Insurance Verification", "Automated Recalls", testimonial "Spanish-speaking patients love booking via WhatsApp"
- **Gym**: "Churn Prediction", "Milestone Celebrations", testimonial "100th class automatically congratulated"
- **Spa**: "Brand-Voice Booking", "Gift Card Sales 24/7", testimonial "International guests love multilingual support"

#### Pipeline submit→email verificado

Submit en LP 9 (Restaurante) y LP 12 (Spa) con form-encoded body:

```
Lead 612 (Fix Verifier, LP 9):
  - Form submit:         POST /api/v1/leads/public → 201 created
  - Celery enrichment:   started → score 78.5 → status SCORED
  - AI Analysis email:   "Your AI automation analysis for Fix Verifier" sent
  - Nurture sequence:    advanced to 2026-05-21

Lead 613 (Sofia Beverly, LP 12):
  - Form submit:         POST /api/v1/leads/public → 201 created
  - Celery enrichment:   started → score 80.0 → status SCORED
  - AI Analysis email:   "Your AI automation analysis for Sofia Beverly" sent
  - Landing page visit:  recorded in landing_page_visits
```

#### Form schema (verificado en los 4 niches)

```html
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={LP_ID}" method="POST">
  <input type="text"  name="first_name" placeholder="First Name" required>
  <input type="text"  name="last_name"  placeholder="Last Name"  required>
  <input type="email" name="email"      placeholder="Email"      required>
  <input type="tel"   name="phone"      placeholder="Phone"      required>
  <input type="url"   name="website"    placeholder="Website"    required>
  <button type="submit">Get Your Free AI Analysis</button>
</form>
```

#### Memoria

Nueva memoria `feedback_celery_model_imports.md`: cualquier modelo cuyas FKs apunten a tablas de modelos NO importados en `scheduled.py` causarán el mismo bug silencioso. Patrón a copiar: `from app.models.X import X  # noqa: F401 - needed for Y.x_id FK resolution`.


## [0.7.7] — 2026-05-18

### Landing Pages — Route Ordering Fix + Compare Enrichment

Causa raíz: en `backend/app/api/v1/landing_pages.py` las rutas se registraban en orden incorrecto. El path-param `GET /{landing_page_id}` (línea 235) se declaraba ANTES de `GET /track`, `GET /random` y `GET /public/active` (líneas 611-662). FastAPI evalúa rutas en orden de registro, así que cualquier request a `/track` era capturada por `/{landing_page_id}` con `landing_page_id="track"` — y como ese endpoint requiere auth, devolvía **401 Unauthorized** antes incluso de intentar parsear "track" como int. Resultado: el tracking pixel JAMÁS persistía visitas, los analytics siempre mostraban 0 visitas, y el random pool nunca funcionó.

#### CRITICAL fix
- **Rutas concretas movidas ANTES de `/{landing_page_id}`** en `landing_pages.py` — orden nuevo: `/track`, `/random`, `/public/active`, `/public/{slug}`, `/`, `/compare`, `POST /`, luego path-params
- **Visit tracking confirmado**: 3 pixels lp_id=8 → 3 rows nuevas en `landing_page_visits` (37→40 verificado en DB)
- **`/random`** ahora redirige a `/lp/{slug}` (SEO-friendly via nginx) en vez de `/landing?lp=`

#### Fix `/compare`
- Agregadas aggregations `email_replies` (Interaction inbound + email) y `calls_made` (PhoneCall join Lead) por landing_page_id
- Frontend Compare tab ya esperaba estos campos en `LandingPage.analytics` (líneas 44-53 de page.tsx) — ahora se renderizan con valores reales

#### Fix `workspace_id` NULL-safety
- En Postgres `NULL == NULL` devuelve NULL, no TRUE → la lógica "deactivate others in same workspace" silenciosamente fallaba si lp.workspace_id era NULL
- Nuevo helper `_workspace_match(model_col, workspace_id)` que usa `IS NULL` cuando aplica
- Aplicado en `create_landing_page`, `update_landing_page`, `activate_landing_page`, `clone_landing_page` y los slug-uniqueness checks

#### Fix slug uniqueness
- Antes: check global → bloqueaba el slug `"test"` para todos los workspaces
- Ahora: scoped al workspace propio (o NULL si no hay tenant) — workspaces distintos pueden reutilizar slugs

#### Fix DELETE
- `delete_landing_page` ahora borra explícitamente `landing_page_visits` antes de borrar la página (evita FK violation si el modelo no tiene CASCADE)

#### Impacto
- Visit tracking ahora persiste en DB → analytics reflejan visitas reales
- Compare tab muestra email_replies y calls_made (antes `undefined`)
- `/random` y `/public/active` finalmente funcionan (eran dead code)
- Multi-workspace deactivate-others ya no falla silenciosamente

#### Memoria
- Nueva memoria `feedback_fastapi_route_order.md`: "rutas concretas ANTES de path-params en routers FastAPI" — regla de oro confirmada con producción rota durante ~3 semanas


## [0.7.6] — 2026-05-18

### Content Studio — Unified Buffer Snapshot + Rate-limit Banner

Causa raíz: cada uno de los 4 tabs (Publicaciones, Calendario, Analytics, Monitoreo) llamaba a la API GraphQL de Buffer independientemente. PostsList re-fetcheaba en cada filtro y PostCalendar en cada cambio de mes — agotando la cuota free de Buffer (100 calls/15min y 100/día) con sólo navegar el dashboard. Cuando Buffer respondía 429, los 4 tabs se rompían silenciosamente.

#### Nuevo
- **`lib/buffer.ts`** — cliente GraphQL central con 5min fresh + 24h stale + sticky rate-limit hint que corta-circuita llamadas siguientes
- **`/content-api/buffer-snapshot`** — un solo endpoint que devuelve `{channels, posts, limits, rate_limited, rate_limit:{window,reset_at}}` en una sola query GraphQL para que los 4 tabs compartan un fetch
- **`hooks/useBufferData`** — caché compartida module-level + pub/sub para sincronizar todos los componentes
- **`RateLimitBanner`** — banner global que muestra countdown preciso al reset (lee `retry-after` header, no `window:"24h"` engañoso del body)

#### Fix
- **PostsList**: filtro por status ahora es client-side (sin re-fetch); delete/edit optimistas patcheando caché local
- **PostCalendar**: navegación de mes sin re-fetch (usa la misma snapshot que los otros tabs)
- **AnalyticsDashboard**: clase `text-gold` (no existe en Tailwind) reemplazada por `text-yellow-300`; charts muestran "Sin datos" elegantemente en vez de crashear
- **BufferStatus**: empty state amigable cuando no hay canales en caché
- **PipelineHistory**: infiere `completed` por presencia de `scripts[]/produced[]/uploaded[]` (la columna "Content" mostraba "—" aunque generaba scripts correctamente)
- **`/content-api/pipelines`**: pasa arrays compactos de stages para soportar la inferencia anterior

#### Impacto
- Buffer API consumption: 5+ calls por dashboard load → **1 call compartida** (caché 5min)
- Cuando rate-limited: corta-circuita instant, evita quemar más quota
- E2E verificado: 4 tabs renderizan correctamente bajo Buffer 429 activo con countdown real (6m, no 24h)

---

## [0.7.5] — 2026-05-17

### Content Studio Pipeline — Video Fixes + Login Repair + Buffer Caching

#### Pipeline / Content Studio
- **Multi-scene scripts**: `content_creator.py` now generates 4 VIDEO_PROMPTs for shorts and 6 for longs (was 1 and 3)
- **ASS Subtitles**: Replaced SRT with ASS format — DejaVu Sans 28px, bottom-centered, black semi-transparent background box
- **Crossfade Transitions**: Added `crossfade_clips()` using ffmpeg `xfade` filter with 0.8s fade between clips. Fallback to concat demuxer if xfade fails
- **End Frame CTA**: Added `create_end_frame()` using ffmpeg `drawtext` with business name, address, special offer, and price. Duration dynamically calculated to fill remaining audio time
- **Edge-TTS Fallback**: Added `edge-tts>=6.1.0` to requirements.txt. ElevenLabs returns 401, MiniMax TTS returns no audio — Edge-TTS (`es-MX-JorgeNeural`) successfully generates Spanish audio
- **Test Production**: Produced and uploaded short (29.9s, 8.0MB) and long (79.0s, 22.2MB) videos with FLUX + Ken Burns

#### Frontend Fixes
- **Login Repair**: Frontend container moved from default `bridge` network to `eko-ai-bussinnes-automation_default` Docker network so it can resolve `eko-backend`
- **Buffer API Caching**: Added 30-second in-memory cache to `/content-api/posts`, `/content-api/buffer-posts`, `/content-api/limits` routes to avoid Buffer rate limiting
- **Container Mounts**: Added `output/` and `config/` volume mounts to frontend container for local API endpoints (`/pipelines`, `/stats`)
- **TypeScript Fix**: Fixed `for...of` iteration over `Map.keys()` by using `Array.from()` in `api-cache.ts`

#### Auto-publisher
- **Dynamic Video Discovery**: Auto-publisher script now reads actual pipeline JSON outputs instead of hardcoded video URLs
- Detects connected Buffer channels automatically
- Publishes to correct platforms based on video tags

---
# Changelog

## [0.6.1] — 2026-04-29

### Full Sales Cycle Demo — X3nails & Spa / Margie

#### Voice & Inbound
- **VAPI inbound assistant** (`vapi_client.py`) — Created "Eva" assistant with Rachel voice, Claude Sonnet, Deepgram nova-2 transcriber, `book_demo` function tool, bound to `+1-256-364-1727`
- **VAPI webhooks** (`webhooks.py`) — `tool-calls` creates Booking + notifies Ender; `end-of-call-report` logs call data + sends rich summary email + Telegram alert
- **Outbound calls** (`voice_agent.py`) — `POST /voice-agent/calls` with custom assistant, first message auto-generation

#### Email & Auto-Reply
- **Demo invite template** (`templates/emails/demo_invite.py`) — Professional HTML with VAPI phone CTA + booking link CTA
- **Ender notification template** (`templates/emails/ender_notification.py`) — Rich HTML with lead snapshot, pain points, transcript, recording link, calendar link
- **Auto-reply AI** (`email_reply_agent.py`) — Generates contextual English replies with both phone number (`+1-256-364-1727`) and `/book-demo` link CTAs
- **Svix webhook fix** (`webhooks.py`) — Replaced custom signature verification with `standardwebhooks` library; fixed signed content format (`id.timestamp.body`)
- **Resend inbound processing** (`webhooks.py`) — Full inbound email webhook with AI intent analysis, auto-reply, status transitions

#### Booking & Calendar
- **Public booking page** (`main.py`) — `/book-demo` serves inline HTML form with date picker, time slots (9:00–16:30 MT), prefills via query params
- **Calendar links** (`utils/calendar_links.py`) — Google Calendar `.ics` generator for "Add to Calendar" buttons
- **Booking endpoint fix** (`calendar.py`) — Added missing `Interaction` import for `/book-demo` POST

#### Notifications
- **Eko Rog Telegram notifier** (`services/eko_rog_notifier.py`) — Sends booking/call alerts to `@EkoBit_Rog_bot`
- **Sales brief generator** (`services/sales_brief_generator.py`) — AI-generated sales brief on booking creation

#### Infrastructure
- **Docker Compose** — Added `APP_URL`, `FRONTEND_URL`, `ENVIRONMENT`, `CORS_ORIGINS`, `VAPI_*`, `TELEGRAM_*`, `AUTO_REPLY_ENABLED` env vars to all services
- **Config** (`config.py`) — Added `AUTO_REPLY_ENABLED`, VAPI IDs, Telegram config, notification email
- **Frontend build** — `NEXT_PUBLIC_API_URL` set to `https://ender-rog.tail25dc73.ts.net`

---

## [0.6.0] — 2026-04-25

### Enrichment Pipeline Hardening

#### Backend
- **Celery worker fix** — Resolved `InvalidRequestError` by creating `app/models/__init__.py` and importing all models in `celery_app.py` before app initialization
- **Commit-per-lead enrichment** — Both scheduled `enrich_pending_leads` (every 30 min) and manual `enrich-all` endpoint now commit after each individual lead, enabling real-time UI progress tracking
- **Kimi JSON parsing** — Replaced fragile greedy regex with robust `_extract_json()` in `ResearchAgent`:
  - Fast path: direct `json.loads()` for clean responses
  - Markdown stripping: unwraps ` ```json ... ``` ` code blocks
  - Brace counting with string/escape awareness: finds balanced `{}` pairs while respecting JSON string literals
  - Eliminates fallback 50/50 scores from truncated or malformed JSON
- **WebsiteFinder hardening** (`app/agents/research/analyzers/website.py`):
  - Blocks URLs ending in `.pdf`, containing `.gov/`, or `.mil/` to avoid wasting enrichment cycles on government/military documents
  - Prevents CO SOS delinquent records from triggering irrelevant `.gov` PDF scrapes
- **Yelp Fusion pagination** — Added offset pagination so requesting >50 results (up to 200) correctly chains multiple API calls (50 per call) instead of silently capping
- **Discovery deduplication** — Fixed `AttributeError: 'NoneType' object has no attribute 'lower'` when LinkedIn or Colorado SOS return leads with null `city` or `business_name`
- **DiscoveryResponse schema** (`app/schemas/lead.py`) — New `DiscoveryResponse` with `total_found`, `new_leads`, `duplicates_skipped`, `items`. Updated `POST /discover` endpoint to return this instead of `LeadListResponse`, fixing 500 validation errors
- **Cal.com auth fix** (`app/services/cal_com.py`) — Switched from Bearer header to query param (`?apiKey=`) for Cal.com API compatibility
- **Email unsubscribe URL** (`app/agents/outreach/channels/email.py`) — Fixed hardcoded `localhost` unsubscribe link
- **AI client hardening** (`app/utils/ai_client.py`) — Added explicit "Your response must be ONLY valid JSON" instruction to Kimi prompts when `json_mode=True`
- **Docker Compose** — Added `KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL`, `KIMI_EMBEDDING_MODEL`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`, `CAL_COM_API_KEY` to all services

#### Frontend
- **Leads pagination** (`frontend/app/leads/page.tsx`) — Added page state with Previous/Next buttons, 100 leads per page
- **Enrichment progress bar** — Real-time progress indicator with polling every 10s, showing processed count, pending count, and percentage
- **DiscoveryForm dropdowns** (`frontend/components/DiscoveryForm.tsx`) — Converted city, state, and max_results to `<select>` menus:
  - 30 Colorado cities pre-populated
  - All 50 US states + DC
  - max_results options: 10, 25, 50, 100, 200
- **Discovery fetch workaround** — Replaced axios with native `fetch()` for `/discover` POST to avoid axios preflight CORS "Network Error" when selecting multiple sources
- **API URL consistency** — Replaced hardcoded `http://10.0.0.240:8001` fetch calls in `leads/page.tsx` with relative `/api/v1/...` paths (Next.js rewrites)

#### Infrastructure / DevEx
- **Frontend Dockerfile** — `NEXT_PUBLIC_API_URL` set to `http://10.0.0.240:8001`
- **Backend config** — `KIMI_BASE_URL` default updated to `https://api.kimi.com/coding/v1`, `KIMI_MODEL` default to `kimi-for-coding`
- **Lead model** — Added missing fields: `review_summary`, `trigger_events`, `pain_points`, `scoring_reason`, `proposal_suggestion`

---

## [0.6.2] — 2026-04-25

### Pipeline Fix — Complete Visibility + Valid Transitions + Interaction Tracking

#### Backend
- **Score 0 validity** (`app/tasks/scheduled.py`, `app/api/v1/leads.py`) — Changed `if lead.urgency_score and lead.fit_score:` to `is not None` checks in 3 places. Defunct businesses with 0/0 scores now correctly transition to `SCORED` instead of getting stuck in `ENRICHED`
- **PATCH transition validation** (`app/api/v1/leads.py`) — `update_lead` endpoint now validates status changes against `VALID_TRANSITIONS` from CRM router. Prevents jumping `discovered` → `closed_won`. Also records an `Interaction` with transition metadata
- **Rate limiter fix** (`app/api/v1/crm.py`) — `_check_contact_rate_limit` now filters `direction="outbound"` so inbound email clicks/opens don't falsely count against the daily limit
- **CRM email interactions** (`app/api/v1/crm.py`) — `contact_lead` now creates an `Interaction` record with channel, template, AI-generated flag, and message_id before committing

#### Frontend
- **KanbanBoard: 13 complete stages** (`frontend/components/KanbanBoard.tsx`) — Added missing `active`, `at_risk`, `churned` stages. Customer lifecycle leads no longer disappear from the pipeline
- **Valid transition arrows** — Replaced broken index-based movement with explicit valid-transition buttons. Backward/forward arrows only appear for transitions allowed by the backend state machine
- **Load all leads** — `page_size: 9999` ensures the Kanban shows every lead regardless of total count
- **User feedback on errors** — Invalid transitions now show an `alert()` with the backend message instead of failing silently in console

#### Pipeline Empty Kanban Fix (v0.6.1-hotfix)
- **page_size limit** (`app/api/v1/leads.py`) — Increased from 100 to 5000. KanbanBoard requesting 9999 caused 422 validation error, leaving pipeline completely empty.
- **Email validation** (`app/schemas/lead.py`) — Changed `EmailStr` to `str` in `LeadBase`. Discovery sources (CO SOS, Yelp) produced corrupt emails like `K@48G9-.BYBGNPTUT` that caused Pydantic `ValidationError` and 500 errors on large fetches.
- **KanbanBoard sync** (`frontend/components/KanbanBoard.tsx`) — `page_size` adjusted from 9999 to 5000 to match backend limit.

---

## [0.5.1] — 2026-04-24

### Fixed: AI Provider Routing (Kimi Integration)

#### Backend
- **Docker Compose env vars**: Added `AI_PROVIDER`, `KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL`, `KIMI_EMBEDDING_MODEL`, `OPENAI_BASE_URL`, `OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`, `CAL_COM_API_KEY` to `backend`, `celery-worker`, and `celery-beat` services.
- **Config defaults** (`app/config.py`): Changed `KIMI_BASE_URL` default from Moonshot (`https://api.moonshot.cn/v1`) to Kimi Code API (`https://api.kimi.com/coding/v1`); changed `KIMI_MODEL` default to `kimi-for-coding`.
- **AI client** (`app/utils/ai_client.py`):
  - Added fallback to `reasoning_content` when `content` is empty (required for `kimi-for-coding` model).
  - Fixed `TypeError` in `generate_embedding`: `SentenceTransformer.encode()` does not accept `convert_to_list`; now uses `.tolist()`.
- **Embeddings alignment**: `sentence-transformers` (`all-MiniLM-L6-v2`) generates 384-dim embeddings, matching `Lead.Vector(384)` in the database schema.

---

## [0.5.0] — 2026-04-24

### Calendar Integration + Booking System

#### Backend
- **Booking model** (`app/models/booking.py`) — tracks meetings locally with Cal.com sync
- **Calendar router** (`app/api/v1/calendar.py`):
  - `GET /calendar/event-types` — List Cal.com event types
  - `POST /calendar/availability` — Get available time slots
  - `GET /calendar/bookings` — List bookings with filters (upcoming, by lead, by status)
  - `POST /calendar/bookings` — Create booking for a lead (syncs with Cal.com if configured)
  - `POST /calendar/bookings/{id}/cancel` — Cancel booking locally and on Cal.com
  - `POST /calendar/send-link` — Send booking link via email to a lead
- **CRM integration**: `POST /crm/{lead_id}/send-booking-link` — Send booking link directly from pipeline
- **Webhook handler** (`/webhooks/calcom`) already existed — auto-updates lead to `MEETING_BOOKED` on Cal.com booking

#### Frontend
- **Calendar page** (`frontend/app/calendar/page.tsx`) — View upcoming/all/past meetings, cancel bookings, join video links
- **Navbar** updated with Calendar navigation link
- **API client** updated with `calendarApi` methods

#### Tests
- `tests/test_calendar.py` — Booking model enums, calendar API endpoints, schemas

---

## [0.4.0] — 2026-04-24

### Auth System: JWT + Protected Routes + Multi-tenancy

#### Backend
- **User model** (`app/models/user.py`) with roles: `admin`, `manager`, `agent`
- **JWT security** (`app/core/security.py`): password hashing (bcrypt), access/refresh tokens, `get_current_user` dependency, role-based guards (`get_current_admin`)
- **Auth router** (`app/api/v1/auth.py`):
  - `POST /auth/login` — JWT token pair
  - `POST /auth/register` — Admin-only user creation
  - `POST /auth/refresh` — Token refresh
  - `GET /auth/me` — Current user profile
  - `PATCH /auth/me` — Update profile
  - `GET /auth/users` — List users (admin)
  - `POST /auth/dev-login` — Development bypass (creates admin dev user)
- **Protected routes**: All existing API endpoints now require Bearer token (`leads`, `campaigns`, `crm`, `sequences`, `emails`, `analytics`)
- **Multi-tenancy**: Non-admin users only see leads they own or are assigned to; `owner_id` auto-assigned on lead creation/discovery

#### Frontend
- **Auth context** (`frontend/contexts/AuthContext.tsx`): login state, auto-redirect, token persistence in localStorage
- **Login page** (`frontend/app/login/page.tsx`): email/password form + dev login button
- **API client** (`frontend/lib/api.ts`): Axios interceptors inject Bearer token; auto-redirect to `/login` on 401
- **Navbar** updated: displays current user name/role + logout button
- **Route protection**: Unauthenticated users redirected to `/login`

#### Tests
- `tests/test_auth.py` — Password hashing, JWT encode/decode, token expiration, role-based access control, router endpoints

---

## [0.3.0] — 2026-04-24

### Fase 2 Complete: Email Outreach + CRM Pipeline + Sequences

#### Celery Scheduled Tasks (Implemented)
- **`process_follow_ups`** — Hourly task: finds leads with `next_follow_up_at <= now`, sends AI-generated follow-up emails, records interactions, respects rate limits and cooldowns
- **`enrich_pending_leads`** — Every 30 min: auto-enriches `DISCOVERED` leads via `ResearchAgent`, auto-scores and transitions to `ENRICHED`/`SCORED`
- **`sync_dnc_registry`** — Monthly: marks leads with 3+ bounces as `do_not_contact`, archives opt-outs older than 2 years (CPA Colorado compliance)
- **`generate_daily_report`** — Daily at 8am MT: pipeline summary, new leads, emails sent, conversion rate; logged to Paperclip

#### Email Sequences (Drip Campaigns)
- New models: `EmailSequence`, `SequenceStep`, `SequenceEnrollment`
- New API: `GET/POST/PATCH /api/v1/sequences`, steps CRUD, enroll leads, execute sequences
- Sequence step types: `email`, `wait`, `condition`, `sms`, `call`
- Dry-run mode for testing sequences before live execution
- Auto-advances enrolled leads through steps with configurable delays

#### Infrastructure
- Added `celery-beat` service to `docker-compose.yml` with scheduled tasks
- `celery_app.py` now includes `beat_schedule` with all 4 tasks
- Added missing env vars to docker-compose: `YELP_API_KEY`, `SERPAPI_API_KEY`, `PAPERCLIP_API_KEY`, `CORS_ORIGINS`

#### Tests
- `tests/test_scheduled.py` — Celery task wrappers and async helpers
- `tests/test_sequences.py` — Sequence schemas, models, and API logic

---

## [0.2.0] — 2026-04-24

### Fase 1 Complete: Discovery + Research + Dashboard

#### Discovery Sources
- **Yelp** — Web scraping source with BeautifulSoup + httpx
- **LinkedIn** — Apify actor integration (`harvestapi/linkedin-company`)
- **Colorado SOS** — Official Colorado Open Data API (Socrata) + Apify fallback
- Multi-source selection UI in DiscoveryForm (Google Maps, Yelp, LinkedIn, Colorado SOS)

#### Semantic Search
- New `POST /api/v1/leads/search` endpoint using pgvector + OpenAI embeddings
- Automatic embedding generation on lead creation and enrichment
- Semantic search toggle in Leads page frontend

#### UX Improvements
- Removed `window.location.reload()` anti-pattern from dashboard
- Added reactive `refreshTrigger` to RecentLeads component
- CORS origins now configurable via `CORS_ORIGINS` env var

#### Tests
- `tests/test_discovery.py` — Google Maps, Yelp, LinkedIn, Colorado SOS sources
- `tests/test_research.py` — ResearchAgent enrichment pipeline

#### Infrastructure
- Added `beautifulsoup4` to requirements
- Added `ApifyClient` service for actor orchestration
- Added `update_lead_embedding` utility for vector search

---

## [0.1.0] — 2026-04-07

### MVP Release
- FastAPI backend with async SQLAlchemy + pgvector
- Next.js 14 frontend with Tailwind CSS
- DiscoveryAgent (Google Maps via Outscraper)
- ResearchAgent (Website analysis + GPT-4o scoring)
- EmailOutreach (Resend + AI-generated templates)
- CRM Pipeline with 10 stages
- Paperclip integration for agent traceability
- Docker Compose setup (PostgreSQL, Redis, backend, frontend, Celery)
