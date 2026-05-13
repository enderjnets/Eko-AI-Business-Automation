"""Generate a spectacular HTML email with CSS-based visuals for lead AI analysis.

Uses dark-theme, table-based layout for maximum email client compatibility.
Replaces SVG charts with CSS inline bars and styled score circles that render
reliably in Gmail, Outlook, and Apple Mail.
"""

from typing import Optional
from app.models.lead import Lead


# ── Translation dictionary ──────────────────────────────────────────
_TRANS = {
    "es": {
        "excellent": "Excelente",
        "good": "Bueno",
        "needs_attention": "Necesita atención",
        "urgency": "Urgencia",
        "fit": "Afinidad",
        "chatbot": "Chatbot / Chat en vivo",
        "booking": "Reservas Online",
        "contact_form": "Formulario de Contacto",
        "ecommerce": "E-commerce",
        "blog": "Blog",
        "newsletter": "Newsletter",
        "online_ordering": "Pedidos Online",
        "detected": "Detectado",
        "not_detected": "No detectado",
        "no_data": "No hay datos disponibles",
        "no_gaps": "No se detectaron grandes brechas",
        "pain_points": "Puntos Débiles",
        "trigger_events": "Señales Clave",
        "tech_gaps": "Tech Gaps",
        "tech_analysis": "Análisis de Tecnología",
        "deep_analysis": "Análisis Profundo",
        "our_recommendation": "Nuestra Recomendación",
        "services_detected": "Servicios Detectados",
        "hours": "Horario",
        "team": "Equipo",
        "hero_subtitle": "Análisis Gratuito de Automatización IA",
        "cta_button": "Agenda tu demo gratis de 15 min →",
        "cta_call": "¿Prefieres llamar?",
        "default_scoring_reason": "Analizamos tu presencia online y señales de negocio para determinar cuánto podría ayudarte la automatización con IA.",
        "default_business_name": "Tu Negocio",
        # Client-facing inverted score labels
        "client_score_label_high_gap": "Mucho por mejorar",
        "client_score_label_med_gap": "Oportunidad de mejora",
        "client_score_label_low_gap": "Casi optimizado",
        "client_score_subtitle": "Puntuación de Automatización",
        "client_score_out_of": "de 100",
        "tech_gap_concrete": "Tu negocio usa solo {detected} de {total} herramientas digitales clave",
        "listen_analysis": "Escucha tu análisis",
        "listen_analysis_sub": "Prefieres escuchar en vez de leer? Dale play:",
    },
    "en": {
        "excellent": "Excellent",
        "good": "Good",
        "needs_attention": "Needs Attention",
        "urgency": "Urgency",
        "fit": "Fit",
        "chatbot": "Chatbot / Live Chat",
        "booking": "Online Booking",
        "contact_form": "Contact Form",
        "ecommerce": "E-commerce",
        "blog": "Blog",
        "newsletter": "Newsletter",
        "online_ordering": "Online Ordering",
        "detected": "Detected",
        "not_detected": "Not Detected",
        "no_data": "No data available",
        "no_gaps": "No major gaps detected",
        "pain_points": "Weaknesses",
        "trigger_events": "Key Signals",
        "tech_gaps": "Tech Gaps",
        "tech_analysis": "Technology Analysis",
        "deep_analysis": "Deep Analysis",
        "our_recommendation": "Our Recommendation",
        "services_detected": "Services Detected",
        "hours": "Hours",
        "team": "Team",
        "hero_subtitle": "Free AI Automation Analysis",
        "cta_button": "Book your free 15-min demo →",
        "cta_call": "Prefer to call?",
        "default_scoring_reason": "We analyzed your online presence and business signals to determine how much AI automation could help you.",
        "default_business_name": "Your Business",
        # Client-facing inverted score labels
        "client_score_label_high_gap": "Needs Major Improvement",
        "client_score_label_med_gap": "Improvement Opportunity",
        "client_score_label_low_gap": "Nearly Optimized",
        "client_score_subtitle": "Automation Score",
        "client_score_out_of": "out of 100",
        "tech_gap_concrete": "Your business only uses {detected} of {total} key digital tools",
        "listen_analysis": "Listen to your analysis",
        "listen_analysis_sub": "Prefer to listen instead of read? Hit play:",
    },
}


def _t(lang: str, key: str) -> str:
    return _TRANS.get(lang, _TRANS["en"]).get(key, key)


# ── Internal score colors (green=high, yellow=mid, red=low) ────────
def _score_color(score: float) -> str:
    if score >= 70:
        return "#10B981"
    if score >= 40:
        return "#F59E0B"
    return "#EF4444"


def _score_bg(score: float) -> str:
    if score >= 70:
        return "rgba(16,185,129,0.12)"
    if score >= 40:
        return "rgba(245,158,11,0.12)"
    return "rgba(239,68,68,0.12)"


# ── Client-facing inverted score colors (red=high gap, yellow=mid, green=low) ──
def _client_score_color(client_score: float) -> str:
    """Inverted: high gap = red (needs work), low gap = green (almost done)."""
    if client_score >= 70:
        return "#10B981"   # green — nearly optimized
    if client_score >= 40:
        return "#F59E0B"   # yellow — some opportunity
    return "#EF4444"       # red — major improvement needed


def _client_score_bg(client_score: float) -> str:
    if client_score >= 70:
        return "rgba(16,185,129,0.12)"
    if client_score >= 40:
        return "rgba(245,158,11,0.12)"
    return "rgba(239,68,68,0.12)"


def _client_score_label(client_score: float, lang: str) -> str:
    if client_score >= 70:
        return _t(lang, "client_score_label_low_gap")
    if client_score >= 40:
        return _t(lang, "client_score_label_med_gap")
    return _t(lang, "client_score_label_high_gap")


def _score_circle_html(score: float, label: str, size: int = 120, color_fn=None, bg_fn=None) -> str:
    """Score circle using a simple div with border-radius — universally supported."""
    color = color_fn(score) if color_fn else _score_color(score)
    bg = bg_fn(score) if bg_fn else _score_bg(score)
    font_size = size // 2
    sub_size = size // 6
    return f"""<div style="width:{size}px;height:{size}px;border-radius:50%;background:{bg};border:4px solid {color};display:inline-block;text-align:center;line-height:{size}px;margin:0 auto;" class="mobile-gauge">
  <span style="font-size:{font_size}px;font-weight:700;color:#FFFFFF;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">{int(score)}</span>
</div>
<p style="margin:8px 0 0;text-align:center;font-size:{sub_size}px;color:#94A3B8;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;">{label}</p>"""


def _mini_score_badge(score: float, label: str) -> str:
    color = _score_color(score)
    bg = _score_bg(score)
    return f"""<div style="display:inline-block;background:#111827;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:16px 24px;text-align:center;min-width:100px;">
  <p style="margin:0;font-size:28px;font-weight:700;color:{color};">{int(score)}</p>
  <p style="margin:4px 0 0;font-size:11px;color:#94A3B8;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;">{label}</p>
</div>"""


def _tech_stack_bars(lead: Lead, lang: str) -> str:
    """Generate horizontal progress bars using table cells — Gmail-safe.

    Uses boolean feature flags from the Lead model instead of searching
    technology names in tech_stack.
    """
    features = [
        (_t(lang, "chatbot"), lead.has_chatbot),
        (_t(lang, "booking"), lead.has_booking),
        (_t(lang, "contact_form"), lead.has_contact_form),
        (_t(lang, "ecommerce"), lead.has_ecommerce),
        (_t(lang, "blog"), lead.has_blog),
        (_t(lang, "newsletter"), lead.has_newsletter),
        (_t(lang, "online_ordering"), lead.has_online_ordering),
    ]

    rows = []
    for label, flag in features:
        has_it = bool(flag)
        color = "#10B981" if has_it else "#EF4444"
        emoji = "✅" if has_it else "❌"
        status = _t(lang, "detected") if has_it else _t(lang, "not_detected")
        bar_width = 85 if has_it else 20
        rows.append(
            f"""<tr>
  <td style="padding:6px 0;font-size:14px;color:#E2E8F0;white-space:nowrap;">{emoji} {label}</td>
  <td style="padding:6px 0 6px 12px;width:100%;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td width="{bar_width}%" style="background:{color};height:10px;border-radius:5px;"></td>
        <td style="background:#1F2937;height:10px;border-radius:0 5px 5px 0;"></td>
      </tr>
    </table>
  </td>
  <td style="padding:6px 0 6px 8px;font-size:12px;color:#94A3B8;white-space:nowrap;">{status}</td>
</tr>"""
        )

    return "\n".join(rows)


def _insight_card(icon: str, title: str, items: list, color: str, lang: str) -> str:
    if not items:
        items = [_t(lang, "no_data")]
    list_html = "\n".join(
        f'<li style="margin:0 0 6px;padding-left:4px;font-size:14px;line-height:1.5;color:#E2E8F0;">{item}</li>'
        for item in items[:3]
    )
    return f"""<td style="width:33.33%;padding:8px;vertical-align:top;" class="mobile-stack">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#111827;border-radius:12px;border:1px solid rgba(255,255,255,0.06);overflow:hidden;">
    <tr>
      <td style="padding:20px;">
        <p style="margin:0 0 12px;font-size:20px;">{icon}</p>
        <p style="margin:0 0 10px;font-size:13px;font-weight:700;color:{color};letter-spacing:0.5px;text-transform:uppercase;">{title}</p>
        <ul style="margin:0;padding:0 0 0 16px;list-style-type:disc;">
          {list_html}
        </ul>
      </td>
    </tr>
  </table>
</td>"""


def _section_title(title: str) -> str:
    return f"""<tr>
  <td style="padding:32px 0 16px;">
    <p style="margin:0;font-size:18px;font-weight:700;color:#FFFFFF;letter-spacing:-0.3px;">{title}</p>
    <div style="width:40px;height:3px;background:linear-gradient(135deg,#0B4FD8,#7C3AED);border-radius:2px;margin-top:8px;"></div>
  </td>
</tr>"""


def _text_block(text: str, lang: str, style: str = "") -> str:
    if not text:
        text = _t(lang, "no_data") + "."
    return f"""<tr>
  <td style="padding:0 0 16px;">
    <p style="margin:0;font-size:15px;line-height:1.7;color:#E2E8F0;text-align:justify;{style}">{text}</p>
  </td>
</tr>"""


def generate_analysis_email(lead: Lead, audio_url: str = None) -> str:
    """Generate the complete HTML body for the Free AI Analysis email.

    Returns raw HTML string ready to be passed to render_outreach_email().
    """
    lang = (lead.language or "en").lower()[:2]
    if lang not in ("es", "en"):
        lang = "en"

    total_score = lead.total_score or 0
    urgency = lead.urgency_score or 0
    fit = lead.fit_score or 0
    scoring_reason = lead.scoring_reason or _t(lang, "default_scoring_reason")
    pain_points = lead.pain_points or []
    trigger_events = lead.trigger_events or []
    review_summary = lead.review_summary or ""
    proposal = lead.proposal_suggestion or ""
    services = lead.services or []
    hours = lead.business_hours or ""
    about = lead.about_text or ""
    team = lead.team_names or []
    business_name = lead.website_title or lead.business_name or _t(lang, "default_business_name")
    first_name = lead.source_data.get("first_name") if lead.source_data else None
    if not first_name:
        first_name = business_name

    # ── CLIENT-FACING INVERTED SCORE ──────────────────────────────
    # Internal 80/100  →  Client sees 20/100 (big gap = red = motivation to buy)
    client_score = 100 - total_score

    # Tech stack gap concrete metric (uses boolean feature flags)
    _FEATURES_TOTAL = 7
    _feature_flags = [
        lead.has_chatbot,
        lead.has_booking,
        lead.has_contact_form,
        lead.has_ecommerce,
        lead.has_blog,
        lead.has_newsletter,
        lead.has_online_ordering,
    ]
    detected_count = sum(1 for f in _feature_flags if f)
    gap_concrete_text = _t(lang, "tech_gap_concrete").format(detected=detected_count, total=_FEATURES_TOTAL)

    # Audio section
    if audio_url:
        audio_html = f"""<table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;background:#111827;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:16px 24px;">
  <tr>
    <td style="text-align:center;">
      <p style="margin:0 0 4px;font-size:13px;font-weight:700;color:#3B82F6;letter-spacing:0.5px;text-transform:uppercase;">{_t(lang, "listen_analysis")}</p>
      <p style="margin:0 0 10px;font-size:12px;color:#94A3B8;">{_t(lang, "listen_analysis_sub")}</p>
      <a href="{audio_url}" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#0B4FD8,#7C3AED);border-radius:50%;width:56px;height:56px;text-align:center;line-height:56px;text-decoration:none;">
        <span style="font-size:24px;">&#9658;</span>
      </a>
      <p style="margin:8px 0 0;font-size:11px;color:#64748B;">MP3 &bull; ~1 min</p>
    </td>
  </tr>
</table>"""
    else:
        audio_html = ""

    # Main score visual (inverted colors + labels)
    score_circle = _score_circle_html(
        client_score,
        _client_score_label(client_score, lang),
        size=140,
        color_fn=_client_score_color,
        bg_fn=_client_score_bg,
    )

    # Internal metrics (still shown as mini badges for transparency)
    urgency_badge = _mini_score_badge(urgency, _t(lang, "urgency"))
    fit_badge = _mini_score_badge(fit, _t(lang, "fit"))

    # Tech stack rows
    tech_rows = _tech_stack_bars(lead, lang)

    # Insight cards — missing features from boolean flags
    all_features = {
        _t(lang, "chatbot"): lead.has_chatbot,
        _t(lang, "booking"): lead.has_booking,
        _t(lang, "contact_form"): lead.has_contact_form,
        _t(lang, "ecommerce"): lead.has_ecommerce,
        _t(lang, "blog"): lead.has_blog,
        _t(lang, "newsletter"): lead.has_newsletter,
        _t(lang, "online_ordering"): lead.has_online_ordering,
    }
    missing = [name for name, flag in all_features.items() if not flag]

    pain_card = _insight_card("🚨", _t(lang, "pain_points"), pain_points, "#EF4444", lang)
    trigger_card = _insight_card("💡", _t(lang, "trigger_events"), trigger_events, "#F59E0B", lang)
    tech_card = _insight_card("🔧", _t(lang, "tech_gaps"), missing[:3] or [_t(lang, "no_gaps")], "#3B82F6", lang)

    # Services
    services_html = ""
    if services:
        services_list = "\n".join(
            f'<span style="display:inline-block;background:#1F2937;color:#E2E8F0;padding:6px 12px;border-radius:6px;font-size:13px;margin:0 6px 6px 0;">{s}</span>'
            for s in services[:8]
        )
        services_html = f"""<tr><td style="padding:0 0 16px;"><p style="margin:0 0 10px;font-size:13px;font-weight:700;color:#94A3B8;letter-spacing:0.5px;text-transform:uppercase;">{_t(lang, "services_detected")}</p><p style="margin:0;">{services_list}</p></td></tr>"""

    # Meta (hours / team)
    meta_html = ""
    if hours or team:
        meta_html = '<tr><td style="padding:0 0 16px;"><p style="margin:0;font-size:13px;color:#94A3B8;">'
        if hours:
            meta_html += f"🕐 <strong>{_t(lang, 'hours')}:</strong> {hours}<br>"
        if team:
            meta_html += f"👥 <strong>{_t(lang, 'team')}:</strong> {', '.join(team[:5])}"
        meta_html += "</p></td></tr>"

    # Proposal
    proposal_html = proposal.replace("\n", "<br>") if proposal else ""

    # CTA
    cta_html = f"""<tr>
  <td style="padding:24px 0 8px;">
    <table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
      <tr>
        <td style="background:linear-gradient(135deg,#0B4FD8,#7C3AED);border-radius:10px;text-align:center;">
          <a href="https://cal.com/ender-ocando-lfxtkn/15min" style="display:inline-block;padding:16px 40px;color:#FFFFFF;text-decoration:none;font-size:16px;font-weight:700;border-radius:10px;">{_t(lang, "cta_button")}</a>
        </td>
      </tr>
    </table>
    <p style="margin:12px 0 0;text-align:center;font-size:13px;color:#94A3B8;">{_t(lang, "cta_call")} <a href="tel:+1-256-364-1727" style="color:#3B82F6;text-decoration:none;font-weight:600;">+1-256-364-1727</a></p>
  </td>
</tr>"""

    html = f"""<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <!-- HERO -->
  <tr>
    <td align="center" style="padding:0 0 24px;">
      <p style="margin:0 0 8px;font-size:13px;font-weight:700;color:#3B82F6;letter-spacing:1px;text-transform:uppercase;">{_t(lang, "hero_subtitle")}</p>
      <h2 style="margin:0 0 12px;font-size:26px;font-weight:700;color:#FFFFFF;letter-spacing:-0.5px;">{business_name}</h2>
      {score_circle}
      <p style="margin:8px auto 0;max-width:400px;font-size:14px;line-height:1.5;color:#EF4444;font-weight:600;text-align:center;" class="mobile-small">{gap_concrete_text}</p>
      <p style="margin:12px auto 0;max-width:400px;font-size:15px;line-height:1.6;color:#94A3B8;text-align:justify;" class="mobile-text">{scoring_reason}</p>
    </td>
  </tr>

  <!-- AUDIO NOTE -->
  <tr>
    <td style="padding:0 0 24px;text-align:center;">
      {audio_html}
    </td>
  </tr>

  <!-- MINI BADGES -->
  <tr>
    <td style="padding:0 0 24px;text-align:center;" class="mobile-center">
      {urgency_badge}&nbsp;&nbsp;{fit_badge}
    </td>
  </tr>

  <!-- INSIGHT CARDS -->
  <tr>
    <td style="padding:0 0 24px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          {pain_card}
          {trigger_card}
          {tech_card}
        </tr>
      </table>
    </td>
  </tr>

  <!-- TECH STACK -->
  {_section_title(_t(lang, "tech_analysis"))}
  <tr>
    <td style="padding:0 0 8px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        {tech_rows}
      </table>
    </td>
  </tr>

  <!-- DEEP ANALYSIS -->
  {_section_title(_t(lang, "deep_analysis"))}
  {_text_block(review_summary, lang)}
  {services_html}
  {meta_html}

  <!-- PROPOSAL -->
  {_section_title(_t(lang, "our_recommendation"))}
  {_text_block(proposal_html, lang)}

  <!-- CTA -->
  {cta_html}
</table>"""

    return html
