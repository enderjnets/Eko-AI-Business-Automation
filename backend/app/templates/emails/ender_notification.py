"""HTML email template for Ender's call summary notification."""

ENDER_NOTIFICATION_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Inbound Call — Eko AI</title>
</head>
<body style="margin:0;padding:0;background:#0B0F19;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#E2E8F0;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0B0F19;">
    <tr>
      <td align="center" style="padding:32px 16px;">
        <table width="640" cellpadding="0" cellspacing="0" border="0" style="max-width:640px;width:100%;background:#111827;border-radius:16px;border:1px solid rgba(255,255,255,0.08);overflow:hidden;">
          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#0B4FD8,#7C3AED);padding:28px 32px;text-align:left;">
              <h1 style="margin:0;font-size:22px;font-weight:700;color:#fff;letter-spacing:-0.3px;">📞 Inbound Call Completed</h1>
              <p style="margin:6px 0 0;font-size:14px;color:rgba(255,255,255,0.8);">{business_name}</p>
            </td>
          </tr>

          <!-- Summary strip -->
          <tr>
            <td style="padding:20px 32px;background:#0F172A;border-bottom:1px solid rgba(255,255,255,0.06);">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td width="25%" style="text-align:center;padding:8px;">
                    <p style="margin:0;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;color:#64748B;">Duration</p>
                    <p style="margin:4px 0 0;font-size:18px;font-weight:700;color:#E2E8F0;">{duration}</p>
                  </td>
                  <td width="25%" style="text-align:center;padding:8px;border-left:1px solid rgba(255,255,255,0.06);">
                    <p style="margin:0;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;color:#64748B;">Interest</p>
                    <p style="margin:4px 0 0;font-size:18px;font-weight:700;color:{interest_color};">{interest_level}</p>
                  </td>
                  <td width="25%" style="text-align:center;padding:8px;border-left:1px solid rgba(255,255,255,0.06);">
                    <p style="margin:0;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;color:#64748B;">Language</p>
                    <p style="margin:4px 0 0;font-size:18px;font-weight:700;color:#E2E8F0;">{language}</p>
                  </td>
                  <td width="25%" style="text-align:center;padding:8px;border-left:1px solid rgba(255,255,255,0.06);">
                    <p style="margin:0;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;color:#64748B;">Date</p>
                    <p style="margin:4px 0 0;font-size:18px;font-weight:700;color:#E2E8F0;">{call_date}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Pain points -->
          <tr>
            <td style="padding:24px 32px 12px;">
              <p style="margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:0.8px;color:#64748B;font-weight:600;">🎯 Detected Pain Points</p>
              <div style="display:flex;flex-wrap:wrap;gap:6px;">
                {pain_points_html}
              </div>
            </td>
          </tr>

          <!-- Services mentioned -->
          <tr>
            <td style="padding:12px 32px 24px;">
              <p style="margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:0.8px;color:#64748B;font-weight:600;">💡 Services Mentioned</p>
              <div style="display:flex;flex-wrap:wrap;gap:6px;">
                {services_html}
              </div>
            </td>
          </tr>

          <!-- AI Summary -->
          <tr>
            <td style="padding:0 32px 24px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0F172A;border-radius:10px;border:1px solid rgba(255,255,255,0.05);">
                <tr>
                  <td style="padding:20px;">
                    <p style="margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:0.8px;color:#64748B;font-weight:600;">🤖 AI Summary</p>
                    <p style="margin:0;font-size:14px;line-height:1.6;color:#94A3B8;">{summary}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Transcript -->
          <tr>
            <td style="padding:0 32px 24px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0F172A;border-radius:10px;border:1px solid rgba(255,255,255,0.05);">
                <tr>
                  <td style="padding:20px;">
                    <p style="margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:0.8px;color:#64748B;font-weight:600;">📝 Transcript</p>
                    <pre style="margin:0;font-size:12px;line-height:1.5;color:#CBD5E1;white-space:pre-wrap;word-break:break-word;font-family:'SF Mono',monospace;max-height:400px;overflow-y:auto;">{transcript}</pre>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Booking block (conditional) -->
          {booking_block}

          <!-- Actions -->
          <tr>
            <td style="padding:0 32px 32px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td width="50%" style="padding-right:8px;">
                    <a href="{recording_url}" style="display:block;background:linear-gradient(135deg,#0B4FD8,#7C3AED);color:#fff;text-decoration:none;padding:14px 0;border-radius:10px;font-size:14px;font-weight:600;text-align:center;">🎙 Listen to Recording</a>
                  </td>
                  <td width="50%" style="padding-left:8px;">
                    <a href="{lead_url}" style="display:block;background:transparent;color:#fff;text-decoration:none;padding:14px 0;border-radius:10px;font-size:14px;font-weight:600;text-align:center;border:2px solid rgba(255,255,255,0.15);">View Lead Profile →</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:20px 32px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;">
              <p style="margin:0;font-size:12px;color:#475569;">Eko AI Automation — Inbound Voice Agent</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def render_ender_notification(
    business_name: str,
    duration: str,
    interest_level: str,
    language: str,
    call_date: str,
    summary: str,
    transcript: str,
    recording_url: str,
    lead_url: str,
    pain_points: list = None,
    services: list = None,
    booking_block: str = "",
) -> str:
    """Render Ender's notification email."""
    interest_color = {
        "HIGH": "#22C55E",
        "MEDIUM": "#F59E0B",
        "LOW": "#EF4444",
        "NONE": "#64748B",
    }.get(interest_level, "#64748B")

    pain_points_html = ""
    if pain_points:
        for pt in pain_points:
            pain_points_html += f'<span style="display:inline-block;background:rgba(239,68,68,0.12);color:#EF4444;padding:4px 10px;border-radius:6px;font-size:12px;margin:0 4px 4px 0;">{pt}</span>'
    else:
        pain_points_html = '<span style="color:#64748B;font-size:12px;">None detected</span>'

    services_html = ""
    if services:
        for svc in services:
            services_html += f'<span style="display:inline-block;background:rgba(34,197,94,0.12);color:#22C55E;padding:4px 10px;border-radius:6px;font-size:12px;margin:0 4px 4px 0;">{svc}</span>'
    else:
        services_html = '<span style="color:#64748B;font-size:12px;">None detected</span>'

    return ENDER_NOTIFICATION_HTML.format(
        business_name=business_name,
        duration=duration,
        interest_level=interest_level,
        interest_color=interest_color,
        language=language,
        call_date=call_date,
        summary=summary,
        transcript=transcript,
        recording_url=recording_url,
        lead_url=lead_url,
        pain_points_html=pain_points_html,
        services_html=services_html,
        booking_block=booking_block,
    )


def render_booking_block(
    start_time: str,
    end_time: str,
    timezone: str,
    calendar_link: str,
) -> str:
    """Render the booking confirmation block for Ender's email."""
    return f"""<tr>
            <td style="padding:0 32px 24px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:rgba(11,79,216,0.08);border-radius:10px;border:1px solid rgba(11,79,216,0.2);">
                <tr>
                  <td style="padding:20px;">
                    <p style="margin:0 0 8px;font-size:13px;text-transform:uppercase;letter-spacing:0.8px;color:#64748B;font-weight:600;">📅 Demo Agendado</p>
                    <p style="margin:0 0 4px;font-size:16px;font-weight:600;color:#E2E8F0;">{start_time} — {end_time}</p>
                    <p style="margin:0 0 14px;font-size:13px;color:#94A3B8;">Zona horaria: {timezone}</p>
                    <a href="{calendar_link}" style="display:inline-block;background:#0B4FD8;color:#fff;text-decoration:none;padding:10px 20px;border-radius:8px;font-size:13px;font-weight:600;">➕ Añadir a Google Calendar</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>"""
