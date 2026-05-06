# Guía de Prueba End-to-End — Eko AI Pipeline

## Objetivo
Verificar que todo el flujo de creación de lead + pipeline + email funciona correctamente después de los fixes.

## Pre-requisitos
- Servidor con Docker Compose levantado
- Repo sincronizado (git pull en `/home/enderj/Eko-AI-Bussinnes-Automation`)
- Contenedores rebuilded con `docker compose build frontend backend celery-worker`
- Acceso a navegador web (puerto 3001 del servidor)

---

## Paso 1: Preparar el entorno

```bash
# SSH al servidor
ssh -o StrictHostKeyChecking=no ender-rog

# Ir al proyecto
cd /home/enderj/Eko-AI-Bussinnes-Automation

# Traer últimos cambios del repo
git pull origin main

# Rebuild de contenedores con código nuevo
docker compose build frontend backend celery-worker

# Restart
docker compose up -d

# Verificar que todo está levantado
docker ps
```

---

## Paso 2: Verificar logs de errores previos

```bash
# Frontend — buscar "Failed to find Server Action" (NO debería aparecer)
docker logs --tail 50 eko-frontend 2>&1 | grep -i "server action\|error"

# Backend — verificar que responde
curl -s http://localhost:8000/api/v1/health || echo "Backend NO responde"

# Worker — verificar que no hay errores de loop
docker logs --tail 50 eko-ai-bussinnes-automation-celery-worker-1 2>&1 | grep -i "different loop\|error"
```

**Resultado esperado:**
- Frontend: Sin errores de "Server Action"
- Backend: Responde 200 OK
- Worker: Sin errores "different loop"

---

## Paso 3: Crear lead manualmente

1. Abrir navegador en `http://<IP_SERVIDOR>:3001`
2. Login con `dev@ekoai.com` (o usar dev-login si está disponible)
3. Ir a **Leads**
4. Clic en **"+ Agregar Lead"**
5. Llenar formulario:
   - **Nombre del negocio:** `X3nails & Spa Test`
   - **Email:** `enderjnets@gmail.com`
   - **Teléfono:** `(303) 555-0199`
   - **Website:** `https://x3nails.com` (o dejar vacío para skip de preview)
   - **Dirección:** `6000 S Fraser St`
   - **Ciudad:** `Aurora`
   - **Estado:** `CO`
   - **Categoría:** `Nail Salon`
6. Clic en **"Guardar Lead"**

**Verificaciones inmediatas:**
- [ ] Modal de crear lead se cierra
- [ ] Aparece el **Pipeline Modal** con pasos: Lead creado → Extrayendo web → Enriqueciendo con AI → Enviando email
- [ ] No hay errores en consola del navegador (F12 → Console)

---

## Paso 4: Verificar pipeline progreso

Esperar 60-120 segundos mientras el pipeline avanza.

**En el Pipeline Modal deberías ver:**
- [ ] Paso 1 "Lead creado" en verde (completado)
- [ ] Paso 2 "Extrayendo web" parpadeando en azul → luego verde
- [ ] Paso 3 "Enriqueciendo con AI" parpadeando en azul → luego verde
- [ ] Paso 4 "Enviando email" parpadeando en azul → luego verde
- [ ] Modal se cierra automáticamente después de 3 segundos de completar

**Si se queda atascado:**
```bash
# Verificar logs del worker en tiempo real
docker logs -f eko-ai-bussinnes-automation-celery-worker-1
```

---

## Paso 5: Verificar datos en la tabla

1. El lead debería aparecer en la tabla de leads
2. Verificar columnas:
   - [ ] **Ubicación:** muestra dirección correcta
   - [ ] **Score:** muestra valor numérico (ej: 72)
   - [ ] **Distancia:** si hay HQ configurada, muestra distancia en km/m
   - [ ] **Acciones:** botones "Enriquecer", "Llamar" visibles

---

## Paso 6: Verificar email enviado

### 6a. En el dashboard de Resend
- Ir a https://resend.com/emails
- Buscar email enviado a `enderjnets@gmail.com`
- [ ] Verificar que tiene **subject** no vacío (ej: "Quick question about X3nails & Spa Test")
- [ ] Verificar estado "Delivered" o "Sent"

### 6b. En la base de datos
```bash
docker exec -e PGPASSWORD=eko_dev_pass eko-db psql -U eko -d eko_ai -c "SELECT id, lead_id, subject, email_status, email_message_id, created_at FROM interactions WHERE interaction_type = 'email' ORDER BY id DESC LIMIT 5;"
```

- [ ] Debe aparecer 1 registro con `subject` no vacío
- [ ] `email_status` = `sent`
- [ ] `email_message_id` no es NULL ni vacío

### 6c. En el inbox del destinatario
- Verificar bandeja de `enderjnets@gmail.com`
- [ ] Email llegó con subject visible
- [ ] Contenido del email es coherente

---

## Paso 7: Verificar Inbox de Eko AI

1. En la app de Eko, ir a **Inbox**
2. Buscar el email recién enviado
- [ ] Aparece en la lista
- [ ] Muestra **subject** correctamente (no vacío)
- [ ] Muestra dirección "to" correcta

---

## Paso 8: Verificar estabilidad del worker (30 min)

Dejar el sistema corriendo y monitorear:

```bash
# En una terminal, monitorear logs del worker por 30 minutos
docker logs -f --since 30m eko-ai-bussinnes-automation-celery-worker-1 2>&1 | tee /tmp/worker-monitor.log
```

Buscar:
- [ ] Ningún error "Future attached to a different loop"
- [ ] Ningún error "Cannot read properties of undefined"
- [ ] Los emails se registran con `Recorded email interaction for lead N`

---

## Checklist Final

| # | Verificación | Estado |
|---|-------------|--------|
| 1 | Pipeline modal aparece al crear lead | ☐ |
| 2 | Pipeline completa 4 pasos en < 2 min | ☐ |
| 3 | Lead aparece en tabla con score > 0 | ☐ |
| 4 | Email enviado tiene subject en Resend | ☐ |
| 5 | Interaction guardada en DB con subject | ☐ |
| 6 | Email llega a inbox del destinatario | ☐ |
| 7 | Inbox de Eko AI muestra subject | ☐ |
| 8 | Worker estable 30 min sin errores | ☐ |

---

## Troubleshooting

### "Failed to find Server Action" sigue apareciendo
```bash
# Hard reload del navegador (Ctrl+Shift+R)
# O borrar caché de Next.js en el contenedor:
docker exec eko-frontend rm -rf /app/.next
docker compose restart frontend
```

### Pipeline modal NO aparece
```bash
# Verificar que handleCreateLead se ejecuta:
# 1. Abrir DevTools → Network
# 2. Crear lead
# 3. Debería ver POST /api/v1/leads con status 201
```

### Email se envía pero NO aparece en interactions
```bash
# Verificar logs del worker
docker logs --since 5m eko-ai-bussinnes-automation-celery-worker-1 2>&1 | grep -i "recorded email\|failed to record"
```

### Worker crashea con "different loop"
```bash
# Verificar que usa --pool=threads
docker exec eko-ai-bussinnes-automation-celery-worker-1 ps aux | grep celery
# Debe mostrar --pool=threads
```
