"""Professional HTML email wrapper for AI-generated outreach emails.

Uses table-based layout with inline CSS for maximum email client compatibility
(Gmail, Outlook, Apple Mail, Yahoo).
"""

from typing import Optional
import re


OUTREACH_EMAIL_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
</head>
<body style="margin:0;padding:0;background-color:#0B0F19;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#E2E8F0;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#0B0F19;">
    <tr>
      <td align="center" style="padding:32px 16px;">
        <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#111827;border-radius:16px;border:1px solid rgba(255,255,255,0.08);overflow:hidden;">
          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#0B4FD8,#7C3AED);padding:28px 32px 24px;text-align:center;">
              <h1 style="margin:0;font-size:26px;font-weight:700;color:#ffffff;letter-spacing:-0.5px;">Eko AI</h1>
              <p style="margin:6px 0 0;font-size:14px;color:rgba(255,255,255,0.85);">Automatización inteligente para tu negocio</p>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:32px;">
              {email_content}
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="padding:20px 32px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;">
              <p style="margin:0 0 6px;font-size:12px;color:#64748B;line-height:1.5;">
                [AI-generated message] — Eko AI Automation LLC, Denver, CO
              </p>
              <p style="margin:0;font-size:12px;color:#475569;line-height:1.5;">
                <a href="{unsubscribe_url}" style="color:#3B82F6;text-decoration:underline;">Unsubscribe</a>
                <span style="color:#475569;"> | </span>
                Reply STOP to opt out
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
  {tracking_pixel}
</body>
</html>"""


def _linkify_urls(text: str) -> str:
    """Convert plain URLs to styled anchor tags."""
    # Match http(s) URLs
    url_pattern = re.compile(
        r'(https?://[^\s<>"\')\]]+)',
        re.IGNORECASE
    )
    return url_pattern.sub(
        r'<a href="\1" style="color:#3B82F6;text-decoration:underline;">\1</a>',
        text
    )


def _format_booking_links(html: str) -> str:
    """Detect booking/demo links and wrap them in styled CTA buttons."""
    # Match links containing book-demo, calendar, cal.com, etc.
    booking_pattern = re.compile(
        r'(<a href="([^"]*(?:book-demo|calendar|cal\.com|scheduling)[^"]*)"[^>]*>)([^<]*)</a>',
        re.IGNORECASE
    )

    def replace_with_button(match):
        href = match.group(2)
        text = match.group(3)
        return f'''<table cellpadding="0" cellspacing="0" border="0" style="margin:20px auto;">
  <tr>
    <td style="background:linear-gradient(135deg,#0B4FD8,#7C3AED);border-radius:10px;text-align:center;">
      <a href="{href}" style="display:inline-block;padding:14px 32px;color:#ffffff;text-decoration:none;font-size:15px;font-weight:600;border-radius:10px;">{text}</a>
    </td>
  </tr>
</table>'''

    return booking_pattern.sub(replace_with_button, html)


def _style_existing_p_tags(html: str) -> str:
    """Add inline styles to existing <p> tags that don't have them."""
    import re

    def add_style_to_p(match):
        tag = match.group(0)
        if 'style=' in tag:
            return tag  # Already has styles, leave it
        return '<p style="margin:0 0 16px;font-size:15px;line-height:1.7;color:#1a1a1a;">'

    return re.sub(r'<p(?![^>]*style=)[^>]*>', add_style_to_p, html, flags=re.IGNORECASE)


def format_plain_text_to_html(text: str) -> str:
    """Convert plain text email body to professionally styled HTML paragraphs.

    Each paragraph gets inline CSS for Gmail/Outlook compatibility.
    Also handles partial HTML from LLM (<p> tags without styles).
    """
    if not text:
        return ""

    # If already has HTML tags, add inline styles to <p> tags and return
    lower_text = text.lower()
    if "<p" in lower_text or "<div" in lower_text:
        # LLM returned partial HTML — ensure all <p> tags have inline styles
        return _style_existing_p_tags(text)

    # Split into paragraphs by double newlines
    paragraphs = text.split("\n\n")
    html_parts = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Replace single newlines within a paragraph with <br>
        para = para.replace("\n", "<br>\n")

        # Linkify URLs
        para = _linkify_urls(para)

        # Check if this paragraph is ONLY a booking/demo link
        # If so, we'll render it as a CTA button (not wrapped in <p>)
        is_booking_only = bool(re.match(
            r'^\s*<a href="[^"]*"[^>]*>[^<]*</a>\s*$',
            para,
            re.IGNORECASE
        ))

        if is_booking_only:
            # Extract href and text for CTA button
            m = re.match(r'\s*<a href="([^"]*)"[^>]*>([^<]*)</a>\s*', para, re.IGNORECASE)
            if m:
                href, link_text = m.group(1), m.group(2)
                html_parts.append(
                    f'''<table cellpadding="0" cellspacing="0" border="0" style="margin:20px auto;">
  <tr>
    <td style="background:linear-gradient(135deg,#0B4FD8,#7C3AED);border-radius:10px;text-align:center;">
      <a href="{href}" style="display:inline-block;padding:14px 32px;color:#ffffff;text-decoration:none;font-size:15px;font-weight:600;border-radius:10px;">{link_text}</a>
    </td>
  </tr>
</table>'''
                )
                continue

        # Check if this paragraph looks like a sign-off (Best regards, Thanks, etc.)
        lower_para = para.lower().replace("<br>", "").strip()
        signoffs = ["best regards", "regards", "thanks", "thank you", "sincerely",
                    "saludos", "un saludo", "atentamente", "cordialmente"]
        is_signoff = any(lower_para.startswith(s) for s in signoffs)

        if is_signoff:
            html_parts.append(
                f'<p style="margin:24px 0 0;font-size:15px;line-height:1.6;color:#555555;">{para}</p>'
            )
        else:
            html_parts.append(
                f'<p style="margin:0 0 16px;font-size:15px;line-height:1.7;color:#1a1a1a;">{para}</p>'
            )

    result = "\n".join(html_parts)
    return result


def render_outreach_email(
    subject: str,
    email_content: str,
    unsubscribe_url: str = "#",
    tracking_pixel: str = "",
) -> str:
    """Render a complete professional outreach email with branding.

    Args:
        subject: Email subject line (used in <title>)
        email_content: HTML content for the body section (already styled paragraphs)
        unsubscribe_url: URL for unsubscribe link
        tracking_pixel: Tracking pixel HTML string (empty if none)

    Returns:
        Complete HTML email string ready to send via Resend
    """
    return OUTREACH_EMAIL_HTML.format(
        subject=subject,
        email_content=email_content,
        unsubscribe_url=unsubscribe_url,
        tracking_pixel=tracking_pixel,
    )
