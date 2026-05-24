# Pricing v2 — Council 2026-05-24

## TL;DR

Bajamos la barrera de entrada (Starter $99 → $249) y subimos el techo (Enterprise $299 → $1,999) para capturar valor real. Growth ($199 → $749) ahora tiene 3 sabores verticales al mismo precio. Setup fee $499 eliminado (pasa a ser add-on opcional $1,500 on-premise install). Anual con 20% off (antes 17%).

## Estructura nueva

| Plan | Mensual | Anual | Para quién |
|---|---|---|---|
| **Starter** | $249 | $199/mes ($2,388/yr) | Autónomos / freelancers / 1 persona |
| **Growth — Contable** | $749 | $599/mes ($7,188/yr) | Despacho contable 2–10 empleados |
| **Growth — Inmobiliario** | $749 | $599/mes ($7,188/yr) | Inmobiliaria 2–10 empleados |
| **Growth — Legal/Clínico** | $749 | $599/mes ($7,188/yr) | Bufete legal o clínica 2–10 empleados |
| **Enterprise** | $1,999 | $1,599/mes ($19,188/yr) | 20+ empleados, multi-oficina, o reseller white-label |

### Add-ons

- **White-label completo** — +$150/mes (tu dominio + portal)
- **Número WhatsApp adicional** — +$50/mes
- **Integración personalizada** — $500 setup + $50/mes
- **On-premise install** — $1,500 one-time (GRATIS año 1 en Enterprise)

## Justificación del Council

- **Starter $249**: el $99 actual no generaba caja real pero sí soporte y churn. El $249 cubre LTV mínimo cuando el cliente compra hardware ($1.5K-3K). El $499 original frenaba conversión.
- **Growth con verticales**: vender "automatización genérica" pierde contra Zapier/Lindy. Vender "OCR de facturas Contasol" o "WhatsApp inmobiliario" gana mercado específico. Mismo $749 baja fricción de decisión.
- **Enterprise $1,999**: market price para multi-tenant + 24/7 + on-prem. Cliente típico ya factura $50K-200K/mes — el plan paga ROI rápido.
- **Eliminar setup fee**: $499 visible bloqueaba conversión. Mantenerlo como add-on opcional ($1,500 — más caro pero opcional) reduce abandono. Enterprise lo recibe gratis año 1 como gancho.
- **Path a $20K MRR**: mix recomendado 16 Starter + 13 Growth + 3 Enterprise = 32 clientes = $19,718/mes. Costos ~$4,150/mes → rentable desde $8-10K MRR. Realista en 6-9 meses con outbound dirigido a "Socio Director" en LinkedIn.

## Arquitectura técnica

### Frontend
- `frontend/app/pricing/page.tsx` — PLANS array v2 (líneas 56-86), removed setup banner, wireado a 3 nuevos componentes + FAQ accordion 6 preguntas.
- `frontend/components/pricing/ROICalculator.tsx` — input horas + select tarifa → ahorro + ratio sobre Growth.
- `frontend/components/pricing/AddonsSection.tsx` — grid 4 add-ons.
- `frontend/components/pricing/GrowthVerticalTabs.tsx` — tabs Contable/Inmobiliario/Legal-Clínico, default Contable.
- `frontend/lib/i18n/translations.ts` — ~60 nuevas keys EN + ES (verticales, add-ons, ROI, FAQ, hardware).
- `frontend/lib/version.ts` + `CHANGELOG.md` — bump 0.7.60 → 0.8.0.

### Backend
- `backend/app/api/v1/checkout.py` — `_resolve_price_id(plan, billing_cycle, vertical)` con fallback a legacy. `CheckoutSessionRequest` extendido con `billing_cycle` + `vertical` opcionales. Setup fee line item REMOVIDO. `SETUP_FEE_CENTS=0` para no romper imports legacy.
- `backend/app/config.py` — 15 nuevas env vars `STRIPE_PRICE_*_MONTHLY/_ANNUAL` + add-ons. Legacy `STRIPE_PRICE_STARTER/GROWTH/ENTERPRISE` se mantienen como fallback.
- `.env.example` — documentadas las 15 nuevas vars.
- `scripts/create_stripe_products.py` — idempotente, dry-run mode, refuse sk_live_ sin --live.

### Subdominios
- `app.ekoaiautomation.com/pricing` — siempre fue accesible.
- `www.ekoaiautomation.com/pricing` — accesible (rewrite solo bloquea `/`, no `/pricing`). El LandingPage component ya tiene 3 links a `/pricing` (nav, hero CTA, footer CTA).

## Deploy procedure

```bash
ssh enderj@10.0.0.240
cd ~/Eko-AI-Bussinnes-Automation

# Pre-flight ya hecho: tag v0.7.60-stable existe + branch feature/pricing-v2 activo

# 1. Crear prices en Stripe (cuando estés listo — script idempotente, se puede correr 2 veces)
docker exec -i eko-backend python - --dry-run < scripts/create_stripe_products.py  # verificar
# Cuando estés conforme, sin --dry-run:
sudo docker exec -e STRIPE_SECRET_KEY=sk_... -i eko-backend python - < scripts/create_stripe_products.py

# 2. Pegar los IDs impresos en .env (las 15 STRIPE_PRICE_*_MONTHLY/ANNUAL + add-ons)
nano .env

# 3. Rebuild frontend + restart backend
sudo docker compose build frontend
sudo docker compose up -d frontend
sudo docker compose restart eko-backend

# 4. Smoke test
curl -sI -H "Host: www.ekoaiautomation.com" http://10.0.0.240/pricing  # 200 OK
curl -sX POST http://localhost:8000/api/v1/checkout/session \
  -H "Content-Type: application/json" \
  -d '{"lead_id": 1, "plan": "starter"}'  # should still work via legacy fallback
```

## Rollback procedure

### Si frontend rompe (HTTP 500 o pricing roto)

```bash
ssh enderj@10.0.0.240
cd ~/Eko-AI-Bussinnes-Automation
git checkout v0.7.60-stable
sudo docker compose build frontend
sudo docker compose up -d frontend
# Tiempo: ~3-5 min. No toca DB ni Stripe.
```

### Si backend rompe (checkout no funciona)

```bash
git checkout v0.7.60-stable -- backend/app/api/v1/checkout.py backend/app/config.py
sudo docker compose restart eko-backend
# Tiempo: ~30s.
```

### Si Stripe products están mal seteados

No hay que rollbackear código — solo corregir env vars en `.env` y reiniciar backend. La logic de `_resolve_price_id()` siempre cae al legacy `STRIPE_PRICE_STARTER/GROWTH/ENTERPRISE` cuando una v2 var está vacía.

## Lo que NO se hace en este release

- ❌ Migrar clientes existentes del $99 al $249 — el fundador comunica manualmente.
- ❌ Sub-landings por vertical (`/pricing/contable`, etc.) — fase 2.
- ❌ Crear productos Stripe en producción automáticamente — el script existe, se corre cuando el fundador esté listo.
- ❌ Demos grabados — placeholders quedan en "agendar demo via Cal.com".

## Cosas a observar tras deploy

1. **Conversion rate** del Starter $249 vs Starter $99 — esperamos drop inicial seguido de recuperación al captar mejor ICP.
2. **CAC payback** — con Starter pagando $249 + customer paga $1.5K-3K hardware, payback debería ser ~2-3 meses.
3. **Add-on attach rate** — apuntamos a 30-40% Growth clients agregando ≥1 add-on en mes 1.
4. **Switch rate vertical Growth** — debería ser <10% año 1 si el copy de la decisión está bien hecho.

## Related

- [[feedback_eko_ai_release_tagging]] — al cerrar PR, crear tag v0.8.0 + GH release + Paperclip EKO-done
- [[project_eko_ai_landing_capability_library]] — sincronizar SYSTEM_PROMPT del generator con las nuevas features verticales para que las LPs las promocionen
