# Control Plane — Spec para Realtors (B) + control-agent (C)

Este documento define el contrato **exacto** que la sesión de **Eko-AI-RealEstate**
debe implementar para que el control plane de Automation (ya construido: componentes
A + D) lo consuma sin iteración. El cliente saliente que invoca estos endpoints vive en
`backend/app/services/control_plane_client.py` de Automation.

> Todo el tráfico va **sobre Tailscale (100.x)**. Ningún endpoint de `/admin/*` ni el
> control-agent debe exponerse públicamente. El agente debe bindearse a la interfaz
> Tailscale.

---

## B — Producto (repo Eko-AI-RealEstate)

### B1. Auth servicio-a-servicio
Añadir una dependencia `require_control_key` en `backend/app/services/auth.py` que valide
el header **`X-Control-Key`** contra una env var nueva **`CONTROL_KEY`** (por instancia).
Sólo debe gatear las rutas `/api/v1/admin/*` nuevas — **no** tocar la auth de usuarios
existente (`require_auth`).

```python
from fastapi import Header, HTTPException
from app.config import settings

async def require_control_key(x_control_key: str = Header(default="")):
    if not settings.CONTROL_KEY or x_control_key != settings.CONTROL_KEY:
        raise HTTPException(status_code=401, detail="Invalid control key")
```

Respuestas esperadas por el cliente: **401** sin/with bad key, **200** con key válida.

### B2. `GET /api/v1/admin/status`
Gateado por `require_control_key`. Readiness real (no el `/health` liviano). Forma JSON
exacta que Automation almacena en `last_health` y muestra en el panel:

```json
{
  "status": "ok",                 // "ok" | "degraded" | "error"
  "version": "1.4.2",
  "env": "production",
  "uptime_seconds": 84211,
  "checks": {
    "db":    { "ok": true,  "latency_ms": 3.1 },
    "redis": { "ok": true,  "latency_ms": 0.8 },
    "llm":   { "ok": true,  "provider": "openai", "configured": true }
  }
}
```

- `db`: `SELECT 1` contra la DB del producto.
- `redis`: `PING`.
- `llm`: que haya provider + API key configurada (no hace falta llamar al LLM).
- Códigos: **200** siempre que el endpoint responda (el estado va en el body). Si el
  servicio no puede ni arrancar, Automation lo marcará `error` por timeout/conexión.

### B2.1 `GET /api/v1/analytics`
**Ya existe** en el producto (funnel/conversión). El control plane lo consume tal cual con
el header `X-Control-Key`. Verificar únicamente que `require_control_key` (o la auth ya
presente) permita el acceso servicio-a-servicio y que devuelva JSON. Automation guarda ese
JSON bajo `last_health.metrics` y lo muestra en el detalle de instancia.

### B3. `install.sh`
`scripts/install.sh` debe **generar y persistir** dos secretos por instancia, junto a los
que ya genera:
- `CONTROL_KEY` → al `.env` del producto (consumido por `require_control_key`).
- `AGENT_KEY`   → al `.env` del control-agent (ver C).

Imprimir ambos al final del install para registrarlos manualmente en Automation
(formulario "Nueva instancia": campos *Service key* y *Agent key*).

---

## C — control-agent (sidecar por host)

Servicio FastAPI nuevo y chico, desplegado como contenedor **sidecar** con acceso a
`docker.sock` y al `docker-compose.yml` de la instancia. Reutilizable por cualquier
producto. Vivienda sugerida: carpeta `control-agent/` + un servicio extra en el
`docker-compose.yml` de cada instancia.

### Auth
Header **`X-Agent-Key`** validado contra env `AGENT_KEY`. Bind **sólo** a la interfaz
Tailscale (`100.x`), nunca `0.0.0.0` público.

### Endpoints (consumidos por `control_plane_client.agent_action` / `agent_logs`)

Automation hace:
- `POST {agent_url}/agent/{restart|migrate|redeploy}` con header `X-Agent-Key`, body `{}` (o params).
- `GET  {agent_url}/agent/logs?service=<svc>&lines=<n>` con header `X-Agent-Key`.

**Forma de respuesta de las acciones** (Automation la guarda en `InstanceActionLog.output`):

```json
{
  "exit_code": 0,
  "stdout": "...",
  "stderr": ""
}
```

Automation interpreta `exit_code == 0` como éxito; cualquier otro valor, o un HTTP no-2xx,
como fallo (status `error`).

**Forma de respuesta de logs** (Automation lee la clave `output`):

```json
{ "output": "... últimas N líneas ...", "service": "backend", "lines": 200 }
```

### Comandos por acción
| Endpoint            | Comando                                                        |
|---------------------|----------------------------------------------------------------|
| `POST /agent/restart`  | `docker compose restart` (servicio si se pasa, o stack)     |
| `POST /agent/migrate`  | `docker compose exec -T backend alembic upgrade head`       |
| `POST /agent/redeploy` | `docker compose pull && docker compose up -d --build`       |
| `GET  /agent/logs`     | `docker compose logs --tail <lines> [service]`              |

> `migrate`/`redeploy` pueden tardar minutos: Automation ya las ejecuta en una tarea
> Celery con timeout largo (`ACTION_TIMEOUT = 600s`) y hace polling del `action_id`, así
> que el agente puede responder de forma síncrona cuando el comando termina.

### Errores
- Falta/má `X-Agent-Key` → **401**.
- Acción desconocida → **400**.
- Comando que falla → **200** con `exit_code != 0` (preferido) **o** 5xx; Automation
  registra ambos como `error`.

---

## Checklist de integración (cuando B+C estén listos)
1. `curl -H "X-Control-Key: <key>" http://100.x:<port>/api/v1/admin/status` → JSON con `checks`.
2. Registrar la instancia en Automation (Control Plane → Nueva instancia) con `base_url`,
   `agent_url`, *Service key* = `CONTROL_KEY`, *Agent key* = `AGENT_KEY`.
3. Esperar un ciclo del poller (≤5 min) o pulsar "Poll ahora": el badge pasa a verde.
4. Desde el detalle, "Obtener logs" devuelve `docker compose logs`; "Reiniciar" deja una
   entrada `success` en el historial de auditoría.
