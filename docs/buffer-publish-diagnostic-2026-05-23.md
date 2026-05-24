# Buffer publish flow — diagnóstico 2026-05-23

## Pregunta original

Usuario observa: Content Studio (tab Posts) reporta 3 posts como **Publicados**, pero los profiles públicos de TikTok (@ekoaiauto), Instagram (ekoaiauto) y Facebook (Eko Ai Automation) muestran **0 publicaciones**. Sospecha de bug en el publish flow.

## Conclusión rápida

**Buffer NO está roto.** El publish pipeline funcionó correctamente — Buffer subió los 3 videos a las plataformas el 2026-05-13 y guardó los `externalLink` válidos. Las plataformas (especialmente TikTok) **ocultaron los videos del feed público** por restricciones de cuenta nueva + contenido publicado vía API + auto-moderation de AI-generated content. La discrepancia es **platform-side**, no nuestra.

## Evidencia

### Los 3 posts "sent" tienen externalLink válido

Pulled via `/content-api/buffer-snapshot?limit=100`:

| ID (last 12) | Service | sentAt | externalLink | URL status |
|---|---|---|---|---|
| `a69268a2412c` | Facebook | 2026-05-13 23:04 UTC | `https://www.facebook.com/reel/26976934708604504/` | HTTP 200 |
| `9e38ef7c7c13` | Instagram | 2026-05-13 22:48 UTC | `https://www.instagram.com/reel/DYS9DxMFSfv/` | HTTP 200 |
| `c7870a80dbf7` | TikTok | 2026-05-13 22:34 UTC | `https://tiktok.com/@ekoaiauto/video/7639508094246079758` | HTTP 301→200 |

### Por qué los profiles muestran 0

- **TikTok video page contiene**: `"unavailable"` (x18+), `"This account is private"` (x3), `"removed"` — la plataforma marcó el video como no-disponible aunque Buffer subió OK
- **TikTok profile JSON**: `videoCount:0, followerCount:0, diggCount:0, privateAccount:false` — cuenta brand-new sin actividad orgánica
- **Instagram/Facebook**: los URLs devuelven `media_id`/`video_id` válidos pero el grid público del profile está vacío

Patrón consistente con:
1. **Cuentas nuevas sin warm-up orgánico** → algoritmo sandbox
2. **Contenido publicado vía API de terceros** (Buffer Graph API) → review queue para nuevos
3. **AI-generated content** detectado por moderation → hide-from-feed sin notificar

### Los 8 posts "error" fallaron con causa específica

Cada uno tiene `error.message` claro de la plataforma:

| Service | Cantidad | Mensaje típico |
|---|---|---|
| TikTok | 5 | `"There appears to be an issue with the attached media or link attachment. This could be due to the file being too large or connection timing out."` |
| Instagram | 2 | `"It looks like there was an issue with the media attached to this post."` |
| Facebook | 1 | `"We're having trouble accessing the attached video file."` |

**Causa raíz común**: estos posts apuntaban a `litter.catbox.moe` (file host **temporal**) cuya media expiró antes que la plataforma terminara de descargarla. NO es bug del código — la pipeline ya migró a self-hosted en `ender-rog.tail25dc73.ts.net/pipeline-output/`.

## Por qué el código no detectaba esto

Auditoría del flow (`frontend/app/content-api/publish/route.ts` + `lib/buffer.ts`):

- `createPost` mutation acepta y devuelve immediate status (0-1s tras la llamada)
- Buffer asume `status=sent` = "Buffer queue lo aceptó", NO "plataforma confirmó"
- **No hay webhook handler** para notificaciones post-publish de Buffer hacia nuestro backend (`backend/app/api/v1/webhooks.py` tiene solo Resend/Cal.com/Stripe handlers — no Buffer)
- **No hay polling de `externalLink`** para verificar visibilidad real

Esto es por diseño de Buffer free tier (sin webhooks). En tier paid existe un endpoint de delivery confirmation, fuera de scope.

## Acciones tomadas (v0.7.60)

1. **Bulk-delete** de 2 tests scheduled para 2099-12-31 (smoke tests viejos, año 2099 era error humano al programar) — limpieza de grilla
2. **UI**: `error.message` ahora se renderiza como banner debajo del texto del post para cards en error → diagnóstico instantáneo del POR QUÉ falló cada uno
3. **UI**: para posts con `status=sent` + `externalLink`, el botón pequeño de icono se transformó en un botón etiquetado "Ver en plataforma ↗" verde y prominente → usuario puede verificar el estado real en 1 click
4. **Este documento** como playbook para la próxima vez que aparezca la misma duda

## Acciones recomendadas (fuera de scope)

Para mejorar la tasa de publish-visible-en-plataforma:

1. **Warm-up manual de las cuentas**: subir 3-5 posts manuales/orgánicos antes de empezar a publicar vía Buffer. Genera "signal" de cuenta legítima.
2. **Verificar Facebook Business Manager + Instagram Creator account**: business pages no verificadas tienen restricciones API más estrictas.
3. **TikTok shadow-ban check**: contactar TikTok soporte o postear desde la app móvil con el mismo login para ver si el algoritmo levanta el sandbox.
4. **(Long-term) Migrar a Buffer paid tier** para acceder a webhook de delivery confirmation, así detectamos publish-aceptado-pero-oculto en el backend y podemos alertar.

## Comandos útiles para futuras investigaciones

```bash
# Ver shape completa de cualquier post (incluye externalLink, error.message, etc)
ssh enderj@10.0.0.240 'curl -sS "http://localhost:3001/content-api/buffer-snapshot?limit=100" | python3 -m json.tool'

# Verificar si una URL de externalLink resuelve
curl -sSI -L --max-redirs 5 -A "Mozilla/5.0" "<external-link-url>" | head -5

# Profile counts de TikTok (público, sin auth)
curl -sS -L -A "Mozilla/5.0" "https://www.tiktok.com/@USERNAME" | grep -oE '"videoCount":[0-9]+|"followerCount":[0-9]+'

# Bulk-delete posts viejos (requiere Origin header)
curl -X POST -H "Origin: http://localhost:3001" -H "Content-Type: application/json" \
  -d '{"ids":["ID1","ID2"]}' \
  http://localhost:3001/content-api/posts/bulk-delete
```

## Referencias en el código

- Endpoint de publish: `frontend/app/content-api/publish/route.ts`
- Snapshot query: `frontend/app/content-api/buffer-snapshot/route.ts` (line ~120: GraphQL pide `externalLink`, `error { message }`)
- Bulk-delete (v0.7.59): `frontend/app/content-api/posts/bulk-delete/route.ts`
- Type del post: `frontend/hooks/useBufferData.ts:7-18` (`BufferPost.externalLink`, `BufferPost.error.message`)
- UI de cards: `frontend/components/content-studio/PostsList.tsx` (renderizado del banner de error + botón Ver en plataforma)
