"""Landing page HTML template with placeholders for AI-generated copy."""

_LANDING_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0e1a;--surface:#111827;--text:#f1f5f9;--muted:#94a3b8;--primary:#0B4FD8;--accent:#22D3EE;--success:#10b981}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;overflow-x:hidden}
a{color:var(--accent);text-decoration:none}
@keyframes fadeInUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(11,79,216,.4)}50%{box-shadow:0 0 0 12px rgba(11,79,216,0)}}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(10,14,26,.9);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,.06)}
.nav-inner{max-width:1200px;margin:0 auto;padding:0 24px;height:60px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:20px;font-weight:700;color:var(--text);letter-spacing:-.5px}
.logo span{color:var(--primary)}
.nav-links{display:flex;gap:32px;list-style:none}
.nav-links a{color:var(--muted);font-size:14px;transition:color .2s}
.nav-links a:hover{color:var(--text)}
.nav-cta{background:var(--primary);color:#fff!important;padding:8px 18px;border-radius:8px;font-weight:500}
.hero{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:100px 24px 60px;text-align:center;background:radial-gradient(ellipse at 50% 100%,rgba(11,79,216,.15) 0%,transparent 60%)}
.hero-inner{max-width:800px;width:100%;animation:fadeInUp .8s ease both}
.badge{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:999px;background:rgba(11,79,216,.15);border:1px solid rgba(11,79,216,.25);color:var(--accent);font-size:13px;margin-bottom:24px}
.hero h1{font-size:clamp(36px,6vw,64px);font-weight:800;line-height:1.1;margin-bottom:20px;letter-spacing:-1.5px}
.hero h1 .gradient{background:linear-gradient(135deg,var(--primary),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{font-size:clamp(16px,2.5vw,20px);color:var(--muted);max-width:600px;margin:0 auto 32px}
.hero-form{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;max-width:540px;margin:0 auto 32px}
.hero-form input{flex:1 1 200px;padding:14px 18px;border-radius:10px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.05);color:var(--text);font-size:15px;outline:none;transition:border-color .2s}
.hero-form input:focus{border-color:var(--primary)}
.hero-form input::placeholder{color:var(--muted)}
.hero-form button{flex:0 0 auto;padding:14px 28px;border-radius:10px;border:none;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;font-size:16px;font-weight:600;cursor:pointer;animation:pulse 2s infinite}
.hero-form button:hover{opacity:.9}
.stats{display:flex;justify-content:center;gap:48px;margin-top:40px;flex-wrap:wrap}
.stat-num{font-size:36px;font-weight:800;color:var(--text)}
.stat-label{font-size:14px;color:var(--muted)}
.features{padding:80px 24px;max-width:1200px;margin:0 auto}
.section-header{text-align:center;margin-bottom:48px;animation:fadeInUp .8s ease both}
.section-header h2{font-size:clamp(28px,4vw,40px);font-weight:700;margin-bottom:12px}
.section-header p{color:var(--muted);font-size:18px;max-width:500px;margin:0 auto}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}
.feature-card{padding:32px;border-radius:16px;background:var(--surface);border:1px solid rgba(255,255,255,.06);transition:transform .2s,border-color .2s;animation:fadeInUp .6s ease both}
.feature-card:nth-child(2){animation-delay:.1s}
.feature-card:nth-child(3){animation-delay:.2s}
.feature-card:hover{transform:translateY(-4px);border-color:rgba(11,79,216,.3)}
.feature-icon{width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,var(--primary),var(--accent));display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:16px}
.feature-card h3{font-size:18px;font-weight:600;margin-bottom:8px}
.feature-card p{color:var(--muted);font-size:15px;line-height:1.5}
.testimonials{padding:80px 24px;background:radial-gradient(ellipse at 50% 0%,rgba(11,79,216,.08) 0%,transparent 60%)}
.testimonials-inner{max-width:1200px;margin:0 auto}
.testimonials-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;margin-top:40px}
.testimonial-card{padding:28px;border-radius:16px;background:var(--surface);border:1px solid rgba(255,255,255,.06);animation:fadeInUp .6s ease both}
.testimonial-card:nth-child(2){animation-delay:.15s}
.testimonial-stars{color:#fbbf24;font-size:18px;margin-bottom:12px}
.testimonial-card p{color:var(--muted);font-size:15px;line-height:1.6;margin-bottom:20px;font-style:italic}
.testimonial-author{display:flex;align-items:center;gap:12px}
.testimonial-avatar{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--accent));display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:600}
.testimonial-author div:last-child{font-size:14px;color:var(--muted)}
.testimonial-author strong{color:var(--text);display:block}
.footer{padding:60px 24px;text-align:center;border-top:1px solid rgba(255,255,255,.06)}
.footer h2{font-size:clamp(24px,3vw,32px);font-weight:700;margin-bottom:16px}
.footer p{color:var(--muted);margin-bottom:24px;max-width:500px;margin-left:auto;margin-right:auto}
.footer-btn{display:inline-block;padding:14px 32px;border-radius:10px;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;font-size:16px;font-weight:600}
.footer-copy{margin-top:32px;font-size:14px;color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.hero{padding-top:80px}.stats{gap:24px}.features-grid,.testimonials-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<img src="/api/v1/landing-pages/track?lp_id={{LP_ID}}" width="1" height="1" style="position:absolute;visibility:hidden;" alt="">

<nav class="nav">
  <div class="nav-inner">
    <a href="#" class="logo">eko <span>AI</span></a>
    <ul class="nav-links">
      <li><a href="#features">Features</a></li>
      <li><a href="#testimonials">Testimonials</a></li>
      <li><a href="#form" class="nav-cta">Get Started</a></li>
    </ul>
  </div>
</nav>

<section class="hero" id="form">
  <div class="hero-inner">
    <div class="badge">⚡ {{BADGE}}</div>
    <h1>{{HERO_TITLE}}</h1>
    <p>{{HERO_SUBTITLE}}</p>
    <form class="hero-form" action="/api/v1/leads/public" method="POST">
      <input type="hidden" name="source" value="landing_page">
      <input type="text" name="business_name" placeholder="Business name" required>
      <input type="email" name="email" placeholder="Email" required>
      <input type="tel" name="phone" placeholder="Phone" required>
      <input type="text" name="city" placeholder="City">
      <input type="text" name="state" placeholder="State">
      <button type="submit">{{CTA_BUTTON}}</button>
    </form>
    <div class="stats">
      <div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
      <div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
      <div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
    </div>
  </div>
</section>

<section class="features" id="features">
  <div class="section-header">
    <h2>{{FEATURES_HEADLINE}}</h2>
    <p>{{FEATURES_SUBHEADLINE}}</p>
  </div>
  <div class="features-grid">
    <div class="feature-card">
      <div class="feature-icon">{{FEATURE_1_ICON}}</div>
      <h3>{{FEATURE_1_TITLE}}</h3>
      <p>{{FEATURE_1_DESC}}</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">{{FEATURE_2_ICON}}</div>
      <h3>{{FEATURE_2_TITLE}}</h3>
      <p>{{FEATURE_2_DESC}}</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">{{FEATURE_3_ICON}}</div>
      <h3>{{FEATURE_3_TITLE}}</h3>
      <p>{{FEATURE_3_DESC}}</p>
    </div>
  </div>
</section>

<section class="testimonials" id="testimonials">
  <div class="testimonials-inner">
    <div class="section-header">
      <h2>{{TESTIMONIALS_HEADLINE}}</h2>
      <p>{{TESTIMONIALS_SUBHEADLINE}}</p>
    </div>
    <div class="testimonials-grid">
      <div class="testimonial-card">
        <div class="testimonial-stars">★★★★★</div>
        <p>"{{TESTIMONIAL_1_QUOTE}}"</p>
        <div class="testimonial-author">
          <div class="testimonial-avatar">{{TESTIMONIAL_1_INITIALS}}</div>
          <div><strong>{{TESTIMONIAL_1_NAME}}</strong>{{TESTIMONIAL_1_ROLE}}</div>
        </div>
      </div>
      <div class="testimonial-card">
        <div class="testimonial-stars">★★★★★</div>
        <p>"{{TESTIMONIAL_2_QUOTE}}"</p>
        <div class="testimonial-author">
          <div class="testimonial-avatar">{{TESTIMONIAL_2_INITIALS}}</div>
          <div><strong>{{TESTIMONIAL_2_NAME}}</strong>{{TESTIMONIAL_2_ROLE}}</div>
        </div>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <h2>{{FOOTER_HEADLINE}}</h2>
  <p>{{FOOTER_SUBHEADLINE}}</p>
  <a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
  <div class="footer-copy">© {{YEAR}} Eko AI. contact@biz.ekoaiautomation.com</div>
</footer>

</body>
</html>"""


# Default fallback values if AI fails to generate
_DEFAULT_COPY = {
    "TITLE": "Eko AI — Your 24/7 AI Agent",
    "BADGE": "AI-Powered Automation for Local Businesses",
    "HERO_TITLE": "Your Business Never Sleeps With <span class='gradient'>Eko AI</span>",
    "HERO_SUBTITLE": "Never miss a customer call again. Eko AI answers questions, books appointments, and follows up automatically—so you can focus on growing your business.",
    "CTA_BUTTON": "Get Your Free AI Analysis",
    "STAT_1_NUM": "24/7",
    "STAT_1_LABEL": "Always Available",
    "STAT_2_NUM": "500+",
    "STAT_2_LABEL": "Businesses Served",
    "STAT_3_NUM": "98%",
    "STAT_3_LABEL": "Customer Satisfaction",
    "FEATURES_HEADLINE": "Everything Your Business Needs",
    "FEATURES_SUBHEADLINE": "One AI agent that handles it all",
    "FEATURE_1_ICON": "📞",
    "FEATURE_1_TITLE": "Answer Calls 24/7",
    "FEATURE_1_DESC": "Never miss a call again. Your AI answers, qualifies leads, and transfers when needed.",
    "FEATURE_2_ICON": "💬",
    "FEATURE_2_TITLE": "Respond on WhatsApp",
    "FEATURE_2_DESC": "Instant replies to customer inquiries. Product questions, pricing, availability—all automatic.",
    "FEATURE_3_ICON": "📅",
    "FEATURE_3_TITLE": "Book Appointments",
    "FEATURE_3_DESC": "Connects directly to your calendar. Customers book, reschedule, or cancel without human help.",
    "TESTIMONIALS_HEADLINE": "Loved by Business Owners",
    "TESTIMONIALS_SUBHEADLINE": "See what our customers say",
    "TESTIMONIAL_1_QUOTE": "We went from missing 30% of calls to booking every single one. Eko AI paid for itself in the first week.",
    "TESTIMONIAL_1_INITIALS": "MR",
    "TESTIMONIAL_1_NAME": "Maria Rodriguez",
    "TESTIMONIAL_1_ROLE": "Spa Owner, Miami",
    "TESTIMONIAL_2_QUOTE": "Finally, an AI that actually sounds like me! Clients don't even know they're talking to a bot.",
    "TESTIMONIAL_2_INITIALS": "JC",
    "TESTIMONIAL_2_NAME": "James Chen",
    "TESTIMONIAL_2_ROLE": "Gym Owner, San Francisco",
    "FOOTER_HEADLINE": "Ready to never miss a customer again?",
    "FOOTER_SUBHEADLINE": "Join 500+ businesses already using Eko AI to automate their customer interactions.",
    "FOOTER_CTA": "Get Your Free AI Analysis",
}


SYSTEM_PROMPT_TEMPLATE = """You are a conversion copywriter for local businesses. Generate landing page copy for Eko AI based on the user's instructions.

Eko AI is a 24/7 AI agent for local businesses that answers calls, WhatsApp messages, emails, books appointments, and follows up with leads automatically.

Return ONLY a JSON object with these exact keys. No markdown, no explanations outside the JSON.

Required JSON structure:
{
  "TITLE": "Page title (50 chars max)",
  "BADGE": "Short badge text above headline (e.g., 'AI-Powered Automation for Local Businesses')",
  "HERO_TITLE": "Main headline with HTML span for gradient word: 'Your Business Never Sleeps With <span class=\\'gradient\\'>Eko AI</span>'",
  "HERO_SUBTITLE": "One paragraph explaining the value prop (max 200 chars)",
  "CTA_BUTTON": "Button text (e.g., 'Get Your Free AI Analysis')",
  "STAT_1_NUM": "First stat number (e.g., '24/7')",
  "STAT_1_LABEL": "First stat label (e.g., 'Always Available')",
  "STAT_2_NUM": "Second stat number",
  "STAT_2_LABEL": "Second stat label",
  "STAT_3_NUM": "Third stat number",
  "STAT_3_LABEL": "Third stat label",
  "FEATURES_HEADLINE": "Features section headline",
  "FEATURES_SUBHEADLINE": "Features section subheadline",
  "FEATURE_1_ICON": "Single emoji for feature 1",
  "FEATURE_1_TITLE": "Feature 1 title (3-4 words)",
  "FEATURE_1_DESC": "Feature 1 description (max 120 chars)",
  "FEATURE_2_ICON": "Single emoji for feature 2",
  "FEATURE_2_TITLE": "Feature 2 title",
  "FEATURE_2_DESC": "Feature 2 description",
  "FEATURE_3_ICON": "Single emoji for feature 3",
  "FEATURE_3_TITLE": "Feature 3 title",
  "FEATURE_3_DESC": "Feature 3 description",
  "TESTIMONIALS_HEADLINE": "Testimonials section headline",
  "TESTIMONIALS_SUBHEADLINE": "Testimonials subheadline",
  "TESTIMONIAL_1_QUOTE": "First testimonial quote (max 150 chars)",
  "TESTIMONIAL_1_INITIALS": "2-letter initials (e.g., 'MR')",
  "TESTIMONIAL_1_NAME": "First person name",
  "TESTIMONIAL_1_ROLE": "First person role + location",
  "TESTIMONIAL_2_QUOTE": "Second testimonial quote",
  "TESTIMONIAL_2_INITIALS": "2-letter initials",
  "TESTIMONIAL_2_NAME": "Second person name",
  "TESTIMONIAL_2_ROLE": "Second person role + location",
  "FOOTER_HEADLINE": "Footer headline",
  "FOOTER_SUBHEADLINE": "Footer subheadline (max 120 chars)",
  "FOOTER_CTA": "Footer button text"
}

USER INSTRUCTIONS:
{custom_prompt}
"""


def render_template(copy: dict, landing_page_id: int, year: int) -> str:
    """Replace placeholders in template with generated copy."""
    html = _LANDING_PAGE_TEMPLATE
    data = {**_DEFAULT_COPY, **copy, "LP_ID": str(landing_page_id), "YEAR": str(year)}
    for key, value in data.items():
        placeholder = "{{" + key + "}}"
        html = html.replace(placeholder, str(value))
    return html
