# Eko AI Bug Fix Pipeline

## Problemas Identificados

### CRÍTICOS
1. **Pipeline Modal no aparece** — Frontend: `handleCreateLead` no ejecuta, error "Failed to find Server Action"
2. **Error Server Action** — `geocodeAddress` como async en archivo `"use client"`, Next.js 14 lo interpreta mal
3. **Disco lleno 97%** — Builds Docker fallan, logs descontrolados
4. **Repo desincronizado** — Contenedores tienen código más nuevo que el repo

### ALTOS
5. **Emails sin subject** — Se envían por Resend pero NO se persisten en `interactions`, subject vacío
6. **Worker Celery** — Necesita auditoría de estabilidad
7. **Prueba E2E** — Nunca completada exitosamente

## Workflow por Etapas

### Etapa 1 — Análisis (Paralelo)
- Leer `frontend/app/leads/page.tsx` (estructura, modal, handlers)
- Leer `frontend/lib/api.ts` (API client)
- Leer `backend/app/api/v1/leads.py` (endpoints de leads)
- Leer `backend/app/tasks/scheduled.py` (pipeline logic)
- Leer `docker-compose.yml` (config celery)

### Etapa 2 — Fixes Código (Secuencial dependiente)
- **2a**: Mover `geocodeAddress` a `frontend/lib/geocoding.ts`
- **2b**: Fix pipeline modal — verificar handlers, form submit, estado
- **2c**: Fix email persistence en `scheduled.py` + verificar subject
- **2d**: Sincronizar cambios commiteándolos

### Etapa 3 — Infra & Deploy (Paralelo independiente)
- **3a**: Script de limpieza de disco + log rotation
- **3b**: Rebuild containers con código sincronizado
- **3c**: Test E2E manual (crear lead, ver pipeline, ver email)

### Etapa 4 — Validación
- Verificar modal aparece
- Verificar email llega con subject
- Verificar worker estable
- Confirmar espacio en disco liberado

## Agentes Requeridos
- `Frontend_Fixer` — Next.js/React fixes
- `Backend_Fixer` — Python/FastAPI/Celery fixes
- `Infra_Cleaner` — Docker/disk cleanup
- `E2E_Tester` — Validación end-to-end
