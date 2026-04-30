"""HTML email template for VAPI demo invite."""

DEMO_INVITE_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Demo Invite — Eko AI</title>
</head>
<body style="margin:0;padding:0;background:#0B0F19;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#E2E8F0;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0B0F19;">
    <tr>
      <td align="center" style="padding:40px 20px;">
        <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background:#111827;border-radius:16px;border:1px solid rgba(255,255,255,0.08);overflow:hidden;">
          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#0B4FD8,#7C3AED);padding:40px 32px 32px;text-align:center;">
              <h1 style="margin:0;font-size:28px;font-weight:700;color:#fff;letter-spacing:-0.5px;">Eko AI</h1>
              <p style="margin:8px 0 0;font-size:15px;color:rgba(255,255,255,0.85);">Automatización inteligente para tu negocio</p>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:32px;">
              <p style="margin:0 0 16px;font-size:16px;line-height:1.6;color:#E2E8F0;">
                Hola <strong>{name}</strong>,
              </p>
              <p style="margin:0 0 20px;font-size:15px;line-height:1.6;color:#94A3B8;">
                Gracias por tu interés en <strong>Eko AI</strong>. Como siguiente paso, te invitamos a una
                <strong>demo personalizada de 15 minutos</strong> donde te mostraremos cómo nuestros agentes de IA
                pueden automatizar tus llamadas, citas y seguimiento con clientes.
              </p>

              <!-- CTA Box -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0F172A;border-radius:12px;border:1px solid rgba(255,255,255,0.06);margin:24px 0;">
                <tr>
                  <td style="padding:28px;text-align:center;">
                    <p style="margin:0 0 12px;font-size:13px;text-transform:uppercase;letter-spacing:1px;color:#64748B;">Opción 1 — Llámanos ahora</p>
                    <a href="tel:{phone_number}" style="display:inline-block;background:linear-gradient(135deg,#0B4FD8,#7C3AED);color:#fff;text-decoration:none;padding:16px 36px;border-radius:10px;font-size:18px;font-weight:600;letter-spacing:-0.3px;">
                      📞 {phone_number}
                    </a>
                    <p style="margin:12px 0 0;font-size:13px;color:#64748B;">
                      Un asistente de IA te atenderá y agendará tu demo en el momento.
                    </p>
                  </td>
                </tr>
              </table>

              <p style="margin:20px 0;font-size:14px;text-align:center;color:#64748B;">
                — o si prefieres —
              </p>

              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0F172A;border-radius:12px;border:1px solid rgba(255,255,255,0.06);margin:0 0 24px;">
                <tr>
                  <td style="padding:28px;text-align:center;">
                    <p style="margin:0 0 12px;font-size:13px;text-transform:uppercase;letter-spacing:1px;color:#64748B;">Opción 2 — Agenda en línea</p>
                    <a href="{booking_url}" style="display:inline-block;background:transparent;color:#fff;text-decoration:none;padding:14px 32px;border-radius:10px;font-size:16px;font-weight:600;border:2px solid rgba(255,255,255,0.15);">
                      Seleccionar fecha y hora →
                    </a>
                  </td>
                </tr>
              </table>

              <!-- What to expect -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:8px 0 24px;">
                <tr>
                  <td style="padding:20px;background:#0F172A;border-radius:10px;border:1px solid rgba(255,255,255,0.05);">
                    <p style="margin:0 0 12px;font-size:14px;font-weight:600;color:#E2E8F0;">En la demo verás:</p>
                    <ul style="margin:0;padding-left:20px;font-size:14px;line-height:1.7;color:#94A3B8;">
                      <li>Cómo un agente de IA responde llamadas 24/7 en español e inglés</li>
                      <li>Agendamiento automático de citas en tu calendario</li>
                      <li>Recuperación de llamadas perdidas con seguimiento por SMS/email</li>
                      <li>Precios transparentes y opciones de personalización</li>
                    </ul>
                  </td>
                </tr>
              </table>

              <p style="margin:0;font-size:14px;line-height:1.6;color:#94A3B8;">
                Si tienes alguna pregunta antes de la demo, simplemente responde a este correo.
              </p>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="padding:24px 32px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;">
              <p style="margin:0;font-size:12px;color:#475569;">
                Eko AI Automation LLC · Denver, CO<br/>
                <a href="{unsubscribe_url}" style="color:#475569;text-decoration:underline;">Cancelar suscripción</a>
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def render_demo_invite(
    name: str,
    phone_number: str,
    booking_url: str,
    unsubscribe_url: str = "#",
) -> str:
    """Render the demo invite email template."""
    return DEMO_INVITE_HTML.format(
        name=name,
        phone_number=phone_number,
        booking_url=booking_url,
        unsubscribe_url=unsubscribe_url,
    )
