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
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>{subject}</title>
  <style>
    @media only screen and (max-width: 600px) {
      .mobile-full { width: 100% !important; display: block !important; }
      .mobile-center { text-align: center !important; }
      .mobile-stack { width: 100% !important; display: block !important; padding: 8px 0 !important; }
      .mobile-hide { display: none !important; }
      .mobile-text { font-size: 16px !important; line-height: 1.6 !important; }
      .mobile-small { font-size: 14px !important; }
      .mobile-gauge { width: 100px !important; height: 100px !important; line-height: 100px !important; }
      .mobile-gauge span { font-size: 36px !important; }
    }
  </style>
</head>
<body style="margin:0;padding:0;background-color:#FFFFFF;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#333333;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF;">
    <tr>
      <td align="left" style="padding:24px 16px;">
        <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;">
          <!-- Body — plain-text style for inbox readability (matches reference design) -->
          <tr>
            <td style="padding:8px 4px 24px;">
              {email_content}
            </td>
          </tr>
          <!-- Footer — minimal, light theme -->
          <tr>
            <td style="padding:16px 4px 0;border-top:1px solid #E5E7EB;">
              <p style="margin:12px 0 4px;font-size:13px;color:#666666;line-height:1.5;">
                Eko AI Team<br>
                Denver, CO
              </p>
              <p style="margin:0;font-size:13px;color:#666666;line-height:1.5;">
                <a href="{unsubscribe_url}" style="color:#666666;text-decoration:underline;">Unsubscribe</a>
                <span> | </span>
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
    """Add inline styles to existing <p> tags that don't have them.

    Uses a neutral dark color (#333) that renders well on Gmail's white
    background. Previously used #E2E8F0 (light gray for dark-theme HTML
    wrapper), which made the body nearly invisible against an inbox in
    light mode — exactly the 'apillotado/no se ve' look reported in image
    #44.
    """
    import re

    def add_style_to_p(match):
        tag = match.group(0)
        if 'style=' in tag:
            return tag  # Already has styles, leave it
        return '<p style="margin:0 0 16px;font-size:15px;line-height:1.6;color:#333333;">'

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
                f'<p style="margin:24px 0 0;font-size:15px;line-height:1.6;color:#666666;">{para}</p>'
            )
        else:
            html_parts.append(
                f'<p style="margin:0 0 16px;font-size:15px;line-height:1.6;color:#333333;">{para}</p>'
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
    # Use .replace() instead of .format() because email_content may contain
    # CSS braces (e.g. style="display:block") which would break .format()
    return (OUTREACH_EMAIL_HTML
        .replace("{subject}", subject)
        .replace("{email_content}", email_content)
        .replace("{unsubscribe_url}", unsubscribe_url)
        .replace("{tracking_pixel}", tracking_pixel)
    )
