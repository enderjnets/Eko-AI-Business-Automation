# Prompt para Kimi Swarm — Fix Pipeline-First UX & Lead Creation

## Contexto del Proyecto

**Eko AI** es un CRM con pipeline automatizado de leads. Stack:
- Frontend: Next.js 14 + React 18 + TypeScript + Tailwind (puerto 3001)
- Backend: FastAPI + SQLAlchemy async + PostgreSQL + pgvector (puerto 8000)
- Celery: Redis broker, worker con tareas programadas
- Deploy: Docker Compose en servidor remoto (ender-rog via SSH)

## Problemas CRÍTICOS Pendientes

### 1. PIPELINE MODAL NO APARECE EN EL FRONTEND ❌

**Síntoma**: El usuario hace clic en "+ Agregar Lead", llena el formulario, hace clic en "Guardar Lead", y NO aparece el modal de progreso del pipeline. No hay error visible. No llega request POST al backend.

**Lo que ya se intentó**:
- Sincronizar código del contenedor Docker al repo local
- Agregar `useEffect` que fuerce apertura del modal
- Cambiar condición de renderizado del modal para incluir `pipelinePhase === "tracking"`
- Mover botón "Guardar Lead" DENTRO del `<form>` (fix reciente)
- Reconstruir contenedor frontend

**Causas sospechadas**:
- Error en logs del frontend: `Failed to find Server Action "x"` — puede estar rompiendo todo el JS cliente
- La función `geocodeAddress` es `async` a nivel de módulo en un archivo `"use client"`. Next.js 14 puede interpretarla como Server Action
- Posible caché agresivo de Opera/navegador
- El build de Next.js puede tener código desincronizado entre servidor y cliente

**Archivos relevantes**:
- `frontend/app/leads/page.tsx` — contiene todo el UI de leads, modal de creación, pipeline modal
- `frontend/lib/api.ts` — API client

**Estado actual del código en contenedor**:
```bash
# Verificar
docker exec eko-frontend cat /app/app/leads/page.tsx | grep -c "showPipelineModal"
# Debería dar 4

docker exec eko-frontend cat /app/app/leads/page.tsx | grep -n "handleCreateLead"
# Línea 491: definición
# Línea 1422: onSubmit del form

docker exec eko-frontend sed -n "1528,1548p" /app/app/leads/page.tsx
# Botones deberían estar DENTRO del form
```

### 2. ERROR "Failed to find Server Action" ❌

**Síntoma**: En logs del contenedor `eko-frontend`:
```
Error: Failed to find Server Action "x". This request might be from an older or newer deployment.
Original error: Cannot read properties of undefined (reading 'workers')
```

**Causa sospechada**: La función `geocodeAddress` está definida como `async function` a nivel de módulo en `page.tsx` (archivo con `"use client"`). Next.js 14 Server Actions pueden estar interceptando esto.

**Fix propuesto**:
- Mover `geocodeAddress` a un archivo separado (ej: `frontend/lib/geocoding.ts`)
- O cambiarla a una función regular con `fetch` + `.then()` en lugar de `async/await`
- O agregar `"use server"` explícito donde corresponde y eliminar donde no

### 3. WORKER CELERY — ESTABILIDAD ⚠️

**Historial**:
- Originalmente usaba `--pool=solo` (todo en 1 hilo) → causaba "Future attached to a different loop" con asyncpg
- Se cambió a `--pool=threads` → cada tarea en hilo separado
- El fix del pipeline (`run_lead_pipeline`) verifica status del lead y envía email incluso si ya está `SCORED`

**Estado actual**: Worker estable, pipeline funciona cuando se dispara manualmente.

**Pero**: El disco del servidor está al 97% (938GB usados de 1TB). Los builds de Docker son lentos y a veces fallan por timeout.

### 4. DISCO LLENO — 97% USO ❌

**Síntoma**: `no space left on device` al copiar archivos o hacer builds.

**Ya limpiado**: 39GB liberados con `docker system prune`, pero volvió a llenarse rápido.

**Necesita**:
- Investigar qué está consumiendo espacio: logs, backups, imágenes Docker, archivos temporales
- Configurar rotación de logs
- Limpiar backups antiguos
- Verificar si hay archivos core/core dumps

### 5. CÓDIGO DESINCRONIZADO — REPO vs CONTENEDORES ⚠️

**Situación**: Los contenedores Docker tenían código más nuevo que el repo local. Se sincronizó parcialmente pero hay riesgo de que queden inconsistencias.

**Archivos que se modificaron directamente en contenedores y necesitan estar en repo**:
- `frontend/app/leads/page.tsx` (1830 líneas, Pipeline-First UX completo)
- `backend/app/api/v1/leads.py` (preview endpoint, geocodificación, pipeline queueing)
- `backend/app/tasks/scheduled.py` (pipeline logic, thread fixes)
- `frontend/lib/api.ts` (preview method, campaignsApi.delete)
- `docker-compose.yml` (celery-worker pool=threads)

**Commits pendientes**: TODO está modificado en working tree pero NO commiteado.

### 6. CLIENTE DE CORREOS — EMAILS SIN SUBJECT ❌

**Síntoma**: El usuario reporta que en los mensajes de salida (Inbox/Sent), los correos aparecen enviados pero **sin el subject (asunto)**.

**Investigación realizada**:
- El backend usa `resend.Emails.send(params)` con `"subject": subject`
- El pipeline de Celery guarda el interaction con `subject=subject`
- **PERO**: La tabla `interactions` tiene **0 registros** de tipo `email` — los emails se envían pero NO se persisten en la DB
- El entorno es `ENVIRONMENT=production` (no es mock)
- Último email enviado (lead 556): log muestra `Email sent to enderjnets@gmail.com: 7a99ce05-...` pero no aparece en `interactions`

**Código sospechoso** (`scheduled.py`, pipeline):
```python
try:
    interaction = Interaction(
        lead_id=lead.id,
        interaction_type="email",
        direction="outbound",
        subject=subject,
        content=body,
        email_status="sent",
        email_message_id=res.get("id", ""),
        meta={"auto_outreach": True, "source": "pipeline"},
    )
    db.add(interaction)
    await db.commit()
except Exception as ie:
    logger.warning(f"Failed to record interaction for lead {lead_id}: {ie}")
```

**Problemas identificados**:
1. El `except` captura el error silenciosamente — el email se envía pero no se registra
2. Puede haber un problema de sesión/transacción de SQLAlchemy que impide el commit
3. El `email_message_id` puede ser `None` si `res.get("id")` devuelve `None`, causando error en DB

**Fixes necesarios**:
- Verificar que `res.get("id")` no sea None antes de guardar
- Hacer `await db.commit()` explícito y manejar errores de DB
- Agregar log del subject enviado para debug
- Verificar en dashboard de Resend si los emails realmente llegan con subject

### 7. PRUEBA END-TO-END INCOMPLETA ❌

**Nunca se logró** una prueba manual exitosa donde:
1. Usuario hace clic en "+ Agregar Lead"
2. Llena formulario con datos reales
3. Ve el Pipeline Modal aparecer inmediatamente
4. El modal muestra pasos: preview → created → web → enrich → email
5. El pipeline se completa (~60-120s)
6. El lead aparece en la tabla con: ubicación correcta, distancia calculada, acciones visibles
7. El email llega a la bandeja con subject correcto
8. El email aparece en el Inbox de Eko AI con subject visible

## Acciones Requeridas

### Prioridad CRÍTICA

1. **Arreglar el Pipeline Modal del frontend**
   - Asegurar que `handleCreateLead` se ejecute cuando se hace clic en "Guardar Lead"
   - Verificar que no haya errores JS en consola del navegador
   - Resolver el error "Failed to find Server Action" moviendo `geocodeAddress` fuera del componente
   - Hacer hard refresh y probar manualmente

2. **Limpiar disco del servidor**
   - Encontrar y eliminar archivos grandes innecesarios
   - Configurar log rotation
   - Limpiar backups antiguos

3. **Sincronizar repo con contenedores**
   - Asegurar que todos los cambios estén commiteados
   - Hacer push al repo remoto
   - Documentar los cambios en CHANGELOG o commits descriptivos

### Prioridad ALTA

4. **Completar prueba end-to-end**
   - Crear lead manualmente con dirección real (6000 S Fraser St, Aurora, CO 80016)
   - Verificar que geocodificación funcione
   - Verificar que el modal aparezca y muestre progreso
   - Verificar que el email se envíe
   - Verificar que la tabla muestre: ubicación, distancia, acciones

5. **Auditoría de estabilidad del worker**
   - Monitorear worker por 30 minutos
   - Verificar que no haya errores "different loop"
   - Verificar que `enrich_pending_leads` no interfiera con `run_lead_pipeline`

6. **Verificación del sistema de correos**
   - Verificar que los emails se guarden en `interactions` con `subject` no vacío
   - Verificar en dashboard de Resend que los emails tengan subject
   - Probar envío manual de email y verificar subject en inbox del destinatario
   - Revisar `EmailOutreach.send()` y `generate_and_send()` para asegurar que `subject` se pasa correctamente

## Comandos Útiles

```bash
# SSH al servidor
ssh -o StrictHostKeyChecking=no ender-rog

# Verificar contenedores
docker ps

# Ver logs
 docker logs --tail 50 eko-frontend
 docker logs --tail 50 eko-backend
 docker logs --tail 50 eko-ai-bussinnes-automation-celery-worker-1

# Verificar DB
docker exec -e PGPASSWORD=eko_dev_pass eko-db psql -U eko -d eko_ai -c "SELECT * FROM leads ORDER BY id DESC LIMIT 5;"

# Verificar emails en DB
docker exec -e PGPASSWORD=eko_dev_pass eko-db psql -U eko -d eko_ai -c "SELECT id, lead_id, subject, email_status, email_message_id, created_at FROM interactions WHERE interaction_type = 'email' ORDER BY id DESC LIMIT 10;"

# Verificar logs de email en worker
docker logs --since 1h eko-ai-bussinnes-automation-celery-worker-1 2>&1 | grep -i "email sent\|subject\|resend\|outreach"

# Verificar entorno (dev vs production)
docker exec eko-backend env | grep ENVIRONMENT

# Rebuild
 cd /home/enderj/Eko-AI-Bussinnes-Automation
 docker compose build frontend backend celery-worker
 docker compose up -d

# Disk usage
 df -h
 du -sh /var/lib/docker/* 2>/dev/null | sort -rh | head -10
 du -sh /home/enderj/* 2>/dev/null | sort -rh | head -10
 du -sh /app/backups/* 2>/dev/null | sort -rh | head -10
 du -sh /tmp/* 2>/dev/null | sort -rh | head -10
 du -sh /var/log/* 2>/dev/null | sort -rh | head -10
```

## Notas Importantes

- El proyecto está en `/home/enderj/Eko-AI-Bussinnes-Automation`
- DB credentials: POSTGRES_USER=eko, POSTGRES_PASSWORD=eko_dev_pass
- JWT secret está en env del backend: `SECRET_KEY=4523b77240d00a7170f88924b316ad36559d1cb7d8edb40ca60813b4d7ff6733`
- El usuario de prueba es `dev@ekoai.com` (ID 1)
- El email de prueba del lead es `enderjnets@gmail.com`
- Nunca hacer `git push` sin confirmar con el usuario
- Nunca modificar archivos fuera del working directory sin confirmar
