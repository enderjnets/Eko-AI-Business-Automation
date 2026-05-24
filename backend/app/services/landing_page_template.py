"""Landing page HTML templates with placeholders for AI-generated copy.

Multiple visual designs share the same 56-key placeholder vocabulary so the
AI generates one copy that renders against any chosen template.
"""

from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# Shared form-submit JS — same logic across all templates. Inserted at the
# bottom of every template's body. Targets the form by action attribute so
# templates can use any class name they want.
# ─────────────────────────────────────────────────────────────────────────────
_FORM_SUBMIT_JS = """<script>
(function(){
  var form = document.querySelector('form[action*="/api/v1/leads/public"]');
  if(!form) return;
  var msg = document.createElement('div');
  msg.style.cssText='display:none;margin-top:14px;padding:12px 16px;border-radius:8px;font-size:14px;font-weight:500;text-align:center;';
  form.appendChild(msg);
  form.addEventListener('submit', function(e){
    e.preventDefault();
    msg.style.display='none';
    var btn = form.querySelector('button[type="submit"], button');
    var orig = btn.textContent;
    btn.textContent='Sending...'; btn.disabled=true;
    fetch(form.action, {method:'POST', body:new URLSearchParams(new FormData(form)), headers:{'Accept':'application/json'}})
      .then(function(r){return r.json().catch(function(){return {};});})
      .then(function(res){
        if(res.status==='created'){
          msg.textContent="Thanks! We'll send your AI analysis to your email within 24 hours.";
          msg.style.background='rgba(16,185,129,0.15)'; msg.style.color='#10b981'; msg.style.border='1px solid rgba(16,185,129,0.3)';
          form.reset();
        } else if(res.status==='existing'){
          msg.textContent="You're already on our list! We'll reach out soon.";
          msg.style.background='rgba(251,191,36,0.15)'; msg.style.color='#fbbf24'; msg.style.border='1px solid rgba(251,191,36,0.3)';
        } else {
          msg.textContent="Something went wrong. Please try again.";
          msg.style.background='rgba(239,68,68,0.15)'; msg.style.color='#ef4444';
        }
        msg.style.display='block';
      })
      .catch(function(){ msg.textContent="Error. Please try again."; msg.style.display='block'; })
      .finally(function(){ btn.textContent=orig; btn.disabled=false; });
  });
})();
</script>"""


# ─────────────────────────────────────────────────────────────────────────────
# Shared tracking pixel — Eko AI visit tracking, hidden 1×1 gif. Same across
# all templates; injected via placeholder substitution.
# ─────────────────────────────────────────────────────────────────────────────
_TRACKING_PIXEL = '<img src="/api/v1/landing-pages/track?lp_id={{LP_ID}}" width="1" height="1" style="position:absolute;visibility:hidden;" alt="">'


# ─────────────────────────────────────────────────────────────────────────────
# Shared lead-capture form — 5 inputs + submit button. Each template wraps it
# with its own .hero-form / .lead-form class for styling. The form action and
# field names are identical across all templates so the backend works the same.
# ─────────────────────────────────────────────────────────────────────────────
_FORM_FIELDS_HTML = """<form action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
  <input type="text" name="first_name" placeholder="First Name" required>
  <input type="text" name="last_name" placeholder="Last Name" required>
  <input type="email" name="email" placeholder="Email" required>
  <input type="tel" name="phone" placeholder="Phone" required>
  <input type="url" name="website" placeholder="Website" required>
  <button type="submit">{{CTA_BUTTON}}</button>
</form>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 1: EKO CLASSIC — Dark blue/cyan gradient, the original signature look
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_EKO_CLASSIC = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TITLE}}</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0e1a;--surface:#111827;--text:#f1f5f9;--muted:#94a3b8;--primary:#0B4FD8;--accent:#22D3EE}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;overflow-x:hidden;min-height:100vh}
a{color:var(--accent);text-decoration:none}
@keyframes fadeInUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(11,79,216,.4)}50%{box-shadow:0 0 0 12px rgba(11,79,216,0)}}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(10,14,26,.9);backdrop-filter:blur(12px);border-bottom:1px solid rgba(255,255,255,.06)}
.nav-inner{max-width:1200px;margin:0 auto;padding:0 24px;height:60px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:20px;font-weight:700;color:var(--text)}.logo span{color:var(--primary)}
.nav-links{display:flex;gap:28px;list-style:none;align-items:center}
.nav-links a{color:var(--muted);font-size:14px;transition:color .2s}.nav-links a:hover{color:var(--text)}
.nav-cta{background:var(--primary);color:#fff!important;padding:8px 18px;border-radius:8px;font-weight:500}
.hero{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:100px 24px 60px;text-align:center;background:radial-gradient(ellipse at 50% 100%,rgba(11,79,216,.15) 0%,transparent 60%)}
.hero-inner{max-width:800px;width:100%;animation:fadeInUp .8s ease both}
.badge{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:999px;background:rgba(11,79,216,.15);border:1px solid rgba(11,79,216,.25);color:var(--accent);font-size:13px;margin-bottom:24px}
.hero h1{font-size:clamp(36px,6vw,64px);font-weight:800;line-height:1.1;margin-bottom:20px;letter-spacing:-1.5px}
.hero h1 .gradient{background:linear-gradient(135deg,var(--primary),var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{font-size:clamp(16px,2.5vw,20px);color:var(--muted);max-width:600px;margin:0 auto 32px}
.hero-form{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;max-width:540px;margin:0 auto 32px}
.hero-form input{flex:1 1 200px;padding:14px 18px;border-radius:10px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.05);color:var(--text);font-size:15px;outline:none}
.hero-form input:focus{border-color:var(--primary)}.hero-form input::placeholder{color:var(--muted)}
.hero-form button{flex:0 0 auto;padding:14px 28px;border-radius:10px;border:none;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;font-size:16px;font-weight:600;cursor:pointer;animation:pulse 2s infinite}
.stats{display:flex;justify-content:center;gap:48px;margin-top:40px;flex-wrap:wrap}
.stat-num{font-size:36px;font-weight:800;color:var(--text)}.stat-label{font-size:14px;color:var(--muted)}
.section{padding:80px 24px;max-width:1200px;margin:0 auto}
.section-alt{background:radial-gradient(ellipse at 50% 0%,rgba(11,79,216,.06) 0%,transparent 60%)}
.section-header{text-align:center;margin-bottom:56px}
.section-header h2{font-size:clamp(28px,4vw,40px);font-weight:700;margin-bottom:12px}
.section-header p{color:var(--muted);font-size:18px;max-width:500px;margin:0 auto}
.features-grid,.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature-card{padding:32px;border-radius:16px;background:var(--surface);border:1px solid rgba(255,255,255,.06);transition:transform .2s,border-color .2s}
.feature-card:hover{transform:translateY(-4px);border-color:rgba(11,79,216,.3)}
.feature-icon{width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,var(--primary),var(--accent));display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:16px}
.feature-card h3{font-size:18px;font-weight:600;margin-bottom:8px}.feature-card p{color:var(--muted);font-size:15px}
.step-card{text-align:center;padding:32px}
.step-num{width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--accent));display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;margin:0 auto 20px;color:#fff}
.step-card h3{font-size:20px;font-weight:600;margin-bottom:10px}.step-card p{color:var(--muted);font-size:15px}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px;margin-top:40px}
.review-card{padding:28px;border-radius:16px;background:var(--surface);border:1px solid rgba(255,255,255,.06)}
.review-stars{color:#fbbf24;font-size:18px;margin-bottom:12px}
.review-card p{color:var(--muted);font-size:15px;font-style:italic;margin-bottom:20px}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--accent));display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:600;color:#fff}
.review-author strong{color:var(--text);display:block}.review-author div:last-child{font-size:14px;color:var(--muted)}
.faq-list{max-width:800px;margin:40px auto 0}
.faq-item{border-bottom:1px solid rgba(255,255,255,.08)}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;padding:20px 0;background:none;border:none;color:var(--text);font-size:17px;font-weight:500;text-align:left;cursor:pointer}
.faq-q::after{content:'+';font-size:22px;color:var(--accent);transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .3s ease,padding .3s ease;color:var(--muted);font-size:15px}
.faq-item.active .faq-a{max-height:200px;padding-bottom:20px}
.footer{padding:60px 24px;text-align:center;border-top:1px solid rgba(255,255,255,.06)}
.footer h2{font-size:clamp(24px,3vw,32px);font-weight:700;margin-bottom:16px}
.footer p{color:var(--muted);margin-bottom:24px;max-width:500px;margin:0 auto 24px}
.footer-btn{display:inline-block;padding:14px 32px;border-radius:10px;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;font-weight:600}
.footer-copy{margin-top:32px;font-size:14px;color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.stats{gap:24px}.features-grid,.steps-grid,.reviews-grid{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner"><a href="#" class="logo">eko <span>AI</span></a>
<ul class="nav-links"><li><a href="#benefits">Benefits</a></li><li><a href="#how-it-works">How It Works</a></li><li><a href="#reviews">Reviews</a></li><li><a href="#faq">FAQ</a></li><li><a href="#form" class="nav-cta">Get Started</a></li></ul></div></nav>
<section class="hero" id="form"><div class="hero-inner">
<div class="badge">⚡ {{BADGE}}</div><h1>{{HERO_TITLE}}</h1><p>{{HERO_SUBTITLE}}</p>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button></form>
<div class="stats"><div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div></div></div></section>
<section class="section" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature-card"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature-card"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature-card"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature-card"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section section-alt" id="how-it-works"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step-card"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step-card"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step-card"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review-card"><div class="review-stars">★★★★★</div><p>"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><strong>{{REVIEW_1_NAME}}</strong>{{REVIEW_1_ROLE}}</div></div></div>
<div class="review-card"><div class="review-stars">★★★★★</div><p>"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><strong>{{REVIEW_2_NAME}}</strong>{{REVIEW_2_ROLE}}</div></div></div></div></section>
<section class="section section-alt" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq-list">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
<div class="footer-copy">© {{YEAR}} Eko AI. contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 2: APPLE MINIMAL — White, huge typography, lots of whitespace, premium
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_APPLE_MINIMAL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--text:#1d1d1f;--muted:#6e6e73;--accent:#0066cc;--accent-h:#0051a4;--light:#f5f5f7;--hairline:#d2d2d7;--dark:#000}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:'SF Pro Display','SF Pro Text',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.47059;-webkit-font-smoothing:antialiased;font-weight:400;letter-spacing:-.022em;min-height:100vh}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}

/* GLOBAL NAV — frosted, 44px, full product menu (Apple signature) */
.nav{position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(255,255,255,.72);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid rgba(0,0,0,.06)}
.nav-inner{max-width:1024px;margin:0 auto;padding:0 22px;height:44px;display:flex;align-items:center;gap:0}
.nav-logo{width:14px;height:18px;display:inline-block;color:var(--text);opacity:.88;flex-shrink:0}
.nav-logo svg{width:100%;height:100%;display:block;fill:currentColor}
.nav-links{display:flex;list-style:none;flex:1;justify-content:center;margin:0;padding:0;gap:0}
.nav-links li{padding:0 11px}
.nav-links a{color:var(--text);font-size:12px;font-weight:400;opacity:.88;letter-spacing:-.01em;transition:opacity .2s}
.nav-links a:hover{opacity:1;text-decoration:none}
.nav-utility{display:flex;gap:18px;align-items:center;flex-shrink:0}
.nav-utility a{font-size:12px;color:var(--text);opacity:.88}
.nav-utility .icon{width:14px;height:14px;opacity:.88}
.nav-hamburger{display:none;background:none;border:none;color:var(--text);font-size:18px;cursor:pointer;padding:8px}

/* MINI-PROMO STRIP — Apple's "Education Store Home" tiny ribbon */
.mini-strip{background:var(--light);padding:11px 22px;text-align:center;font-size:14px;color:var(--text);margin-top:44px;border-bottom:1px solid rgba(0,0,0,.04);font-weight:400;letter-spacing:-.014em}
.mini-strip strong{font-weight:500}
.mini-strip a{color:var(--accent);font-weight:400;margin-left:6px}
.mini-strip a::after{content:' \203A'}

/* SHOWCASE SECTION — Apple's product page pattern (~60vh, alt bg, centered, dual CTA, image area below) */
.showcase{min-height:62vh;padding:54px 22px 24px;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;text-align:center;overflow:hidden;position:relative}
.showcase-bg-light{background:var(--bg);color:var(--text)}
.showcase-bg-gray{background:var(--light);color:var(--text)}
.showcase-bg-dark{background:var(--dark);color:#f5f5f7}
.showcase-bg-blue{background:#dbe6f7;color:var(--text)}
.showcase-bg-peach{background:#fdf1e8;color:var(--text)}
.showcase-bg-mint{background:#e5f2e8;color:var(--text)}
.showcase .eyebrow{font-size:21px;font-weight:600;letter-spacing:-.016em;margin-bottom:5px;display:block;line-height:1.19;opacity:.88}
.showcase-bg-dark .eyebrow{color:#f5f5f7}
.showcase h2{font-size:clamp(40px,5.6vw,80px);font-weight:600;letter-spacing:-.015em;line-height:1.05;margin-bottom:6px;max-width:980px}
.showcase .sub{font-size:clamp(19px,1.8vw,28px);font-weight:400;line-height:1.14;letter-spacing:.004em;max-width:680px;margin-bottom:18px;opacity:.94}
.showcase-bg-dark .sub{color:#a1a1a6}
.showcase .cta-row{display:flex;gap:24px;flex-wrap:wrap;justify-content:center;margin-bottom:42px}
.showcase .price{font-size:17px;margin-top:4px;margin-bottom:10px;opacity:.78}

/* PILL CTAs — Apple's exact pattern */
.btn-pill{display:inline-flex;align-items:center;padding:12px 22px;border-radius:980px;font-size:17px;line-height:1.17648;font-weight:400;letter-spacing:-.022em;transition:background .2s,opacity .2s,color .2s;cursor:pointer;border:none;font-family:inherit;text-decoration:none;white-space:nowrap}
.btn-primary{background:var(--accent);color:#fff}
.btn-primary:hover{background:#0077ed;text-decoration:none;color:#fff}
.btn-link{color:var(--accent);background:transparent;padding:12px 0;display:inline-flex;align-items:center;gap:1px}
.btn-link:hover{text-decoration:underline}
.btn-link::after{content:'\00a0\203A';font-size:18px;line-height:1}
.showcase-bg-dark .btn-link{color:#2997ff}

/* PRODUCT-IMAGE PLACEHOLDER (the gradient block Apple uses) */
.product-stage{width:100%;max-width:1024px;aspect-ratio:16/9;border-radius:24px;margin-top:auto;position:relative;overflow:hidden;box-shadow:0 30px 60px -28px rgba(0,0,0,.25)}
.stage-blue{background:linear-gradient(180deg,#dbe6f7 0%,#fff 100%)}
.stage-gray{background:linear-gradient(160deg,#e8eaed 0%,#c9d2dd 100%)}
.stage-dark{background:radial-gradient(circle at 50% 40%,#3a3a3c 0%,#1d1d1f 60%,#000 100%)}
.stage-peach{background:linear-gradient(180deg,#fdf1e8 0%,#f7d9c2 100%)}
.stage-mint{background:linear-gradient(180deg,#e5f2e8 0%,#b8d9c0 100%)}
.product-stage::before{content:'';position:absolute;inset:16% 18%;border-radius:16px;background:rgba(255,255,255,.55);box-shadow:inset 0 0 0 2px rgba(255,255,255,.7),0 18px 36px -16px rgba(0,0,0,.18);backdrop-filter:blur(4px)}
.product-stage.stage-dark::before{background:rgba(40,40,42,.85);box-shadow:inset 0 0 0 2px rgba(80,80,82,.6)}

/* HERO is just the first showcase with a small badge */
.hero-badge{display:inline-block;font-size:17px;color:var(--accent);font-weight:400;margin-bottom:4px;letter-spacing:-.022em}

/* STATS — Apple uses thin hairline-bordered band */
.stats-band{background:var(--bg);padding:54px 22px;border-top:1px solid var(--hairline);border-bottom:1px solid var(--hairline)}
.stats-inner{max-width:980px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:32px;text-align:center}
.stat-num{font-size:clamp(40px,5vw,64px);font-weight:600;letter-spacing:-.015em;color:var(--text);line-height:1}
.stat-label{font-size:14px;color:var(--muted);margin-top:8px;letter-spacing:-.016em}

/* HOW IT WORKS — single section, 3-col grid */
.how-section{padding:120px 22px;background:var(--light);text-align:center}
.how-inner{max-width:980px;margin:0 auto}
.how-eyebrow{display:block;font-size:17px;color:var(--accent);font-weight:400;margin-bottom:12px;letter-spacing:-.022em}
.how-section h2{font-size:clamp(40px,5vw,72px);font-weight:600;letter-spacing:-.015em;line-height:1.06;margin-bottom:14px}
.how-section .sub{font-size:clamp(19px,2vw,24px);color:var(--text);max-width:680px;margin:0 auto 72px;line-height:1.21;letter-spacing:.009em;opacity:.92}
.how-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;text-align:left}
.how-step{background:#fff;border-radius:18px;padding:40px 32px;min-height:240px;position:relative}
.how-step-num{font-size:14px;color:var(--accent);font-weight:500;letter-spacing:-.01em;margin-bottom:14px;text-transform:none}
.how-step h3{font-size:24px;font-weight:600;letter-spacing:-.012em;margin-bottom:10px;line-height:1.16}
.how-step p{font-size:17px;color:var(--muted);line-height:1.4;letter-spacing:-.014em}

/* REVIEWS — Apple-style cards, 2-col */
.reviews-section{padding:120px 22px;background:var(--bg);text-align:center}
.reviews-inner{max-width:980px;margin:0 auto}
.reviews-section h2{font-size:clamp(40px,5vw,72px);font-weight:600;letter-spacing:-.015em;line-height:1.06;margin-bottom:14px}
.reviews-section .sub{font-size:clamp(19px,2vw,24px);color:var(--text);max-width:680px;margin:0 auto 72px;line-height:1.21;letter-spacing:.009em;opacity:.92}
.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;text-align:left}
.review-card{background:var(--light);border-radius:18px;padding:40px 36px}
.review-quote{font-size:21px;font-weight:500;letter-spacing:-.016em;line-height:1.33;margin-bottom:28px;color:var(--text)}
.review-author{display:flex;align-items:center;gap:14px}
.review-initials{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#5ac8fa);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:500;letter-spacing:0}
.review-name{font-size:15px;font-weight:500;color:var(--text);letter-spacing:-.014em}
.review-role{font-size:13px;color:var(--muted);letter-spacing:-.012em}

/* FAQ — Apple-style accordion, centered single column */
.faq-section{padding:120px 22px;background:var(--light)}
.faq-inner{max-width:760px;margin:0 auto;text-align:center}
.faq-section h2{font-size:clamp(40px,5vw,72px);font-weight:600;letter-spacing:-.015em;line-height:1.06;margin-bottom:14px}
.faq-section .sub{font-size:clamp(19px,2vw,24px);color:var(--text);max-width:680px;margin:0 auto 60px;line-height:1.21;letter-spacing:.009em;opacity:.92}
.faq-list{text-align:left;border-top:1px solid var(--hairline)}
.faq-item{border-bottom:1px solid var(--hairline)}
.faq-q{width:100%;text-align:left;background:none;border:none;padding:24px 40px 24px 0;font-size:19px;font-weight:500;letter-spacing:-.016em;color:var(--text);cursor:pointer;font-family:inherit;display:flex;justify-content:space-between;align-items:center;line-height:1.3}
.faq-q::after{content:'+';font-size:22px;font-weight:300;color:var(--accent);transition:transform .25s;flex-shrink:0;margin-left:24px}
.faq-item.active .faq-q::after{content:'\2013'}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .25s;font-size:17px;color:var(--muted);line-height:1.5;letter-spacing:-.014em;padding:0 60px 0 0}
.faq-item.active .faq-a{max-height:600px;padding:0 60px 24px 0}

/* CTA FORM SECTION — minimal Apple-style */
.cta-section{padding:120px 22px;background:var(--bg);text-align:center}
.cta-inner{max-width:680px;margin:0 auto}
.cta-section h2{font-size:clamp(40px,5vw,64px);font-weight:600;letter-spacing:-.015em;line-height:1.06;margin-bottom:14px}
.cta-section .sub{font-size:clamp(19px,2vw,24px);color:var(--muted);max-width:560px;margin:0 auto 40px;line-height:1.21;letter-spacing:.009em}
.cta-form{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:32px}
.cta-form input{padding:13px 18px;border-radius:980px;border:1px solid var(--hairline);background:#fff;color:var(--text);font-size:15px;font-family:inherit;outline:none;transition:border-color .2s,box-shadow .2s;letter-spacing:-.014em}
.cta-form input:focus{border-color:var(--accent);box-shadow:0 0 0 4px rgba(0,102,204,.15)}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:1/-1}
.cta-form button{grid-column:1/-1;padding:13px 28px;border-radius:980px;border:none;background:var(--accent);color:#fff;font-size:17px;font-weight:400;letter-spacing:-.022em;cursor:pointer;font-family:inherit;transition:background .2s;margin-top:8px}
.cta-form button:hover{background:#0077ed}

/* FOOTER — Apple's multi-column text-only on light gray */
.footer{background:var(--light);color:var(--muted);padding:24px 22px 22px;font-size:12px;line-height:1.33;letter-spacing:-.01em;border-top:1px solid var(--hairline)}
.footer-inner{max-width:1024px;margin:0 auto}
.footer-disclaimer{padding-bottom:18px;border-bottom:1px solid var(--hairline);margin-bottom:18px;color:var(--muted)}
.footer-cols{display:grid;grid-template-columns:repeat(7,1fr);gap:32px;padding-bottom:22px;border-bottom:1px solid var(--hairline)}
.footer-col h4{font-size:12px;font-weight:600;color:var(--text);margin-bottom:10px;letter-spacing:-.01em}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:6px}
.footer-col a{color:var(--muted);font-size:12px;letter-spacing:-.01em}
.footer-col a:hover{text-decoration:underline;color:var(--text)}
.footer-bottom{padding-top:18px;display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;color:var(--muted)}
.footer-bottom a{color:var(--muted)}
.footer-bottom a:hover{text-decoration:underline}

@media(max-width:900px){
.footer-cols{grid-template-columns:repeat(3,1fr)}
.how-grid,.reviews-grid{grid-template-columns:1fr}
.stats-inner{grid-template-columns:1fr;gap:40px}
}
@media(max-width:640px){
.nav-links,.nav-utility{display:none}
.nav-hamburger{display:block}
.nav-inner{padding:0 16px}
.mini-strip{font-size:12px;padding:9px 14px}
.showcase{padding:42px 16px 18px;min-height:auto}
.showcase h2{font-size:34px}
.showcase .sub{font-size:18px}
.showcase .cta-row{gap:16px;margin-bottom:30px}
.cta-form{grid-template-columns:1fr}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:auto}
.product-stage{aspect-ratio:4/3;border-radius:16px}
.how-section,.reviews-section,.faq-section,.cta-section{padding:72px 16px}
.faq-q{font-size:17px;padding:20px 0}
.footer-cols{grid-template-columns:repeat(2,1fr);gap:22px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<span class="nav-logo" aria-label="Eko"><svg viewBox="0 0 14 17" xmlns="http://www.w3.org/2000/svg"><path d="M11.6 12.2c0 .9-.3 1.7-.9 2.5-.7.9-1.5 1.4-2.5 1.3-.9-.1-1.4-.4-2.1-.4-.7 0-1.3.4-2 .4-1 0-1.9-.6-2.5-1.4-1.3-1.8-2-5-.7-7.3.6-1.1 1.8-1.9 3-1.9.9 0 1.7.5 2.3.5.5 0 1.6-.6 2.7-.5.5 0 1.8.2 2.7 1.5-.1 0-1.6.9-1.6 2.8-.1 2.1 1.7 2.8 1.6 2.5zM8.4 3.4c.5-.5.8-1.3.7-2-.7 0-1.4.4-1.9.9-.4.5-.8 1.3-.7 2 .7.1 1.4-.4 1.9-.9z"/></svg></span>
<ul class="nav-links">
<li><a href="#">Store</a></li>
<li><a href="#">Mac</a></li>
<li><a href="#">iPad</a></li>
<li><a href="#">iPhone</a></li>
<li><a href="#">Watch</a></li>
<li><a href="#">Vision</a></li>
<li><a href="#">AirPods</a></li>
<li><a href="#">TV</a></li>
<li><a href="#">Entertainment</a></li>
<li><a href="#">Accessories</a></li>
<li><a href="#">Support</a></li>
</ul>
<div class="nav-utility">
<a href="#" aria-label="Search"><svg class="icon" viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M6 0a6 6 0 1 1 0 12 6 6 0 0 1 0-12zm0 1.5a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9zM10.5 9.5l3 3-1 1-3-3 1-1z"/></svg></a>
<a href="#" aria-label="Bag"><svg class="icon" viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M4 4V3a3 3 0 0 1 6 0v1h2v9H2V4h2zm1 0h4V3a2 2 0 0 0-4 0v1z"/></svg></a>
</div>
<button class="nav-hamburger" aria-label="Menu">&#9776;</button>
</div></nav>

<div class="mini-strip">{{BADGE}} <a href="#form">Get started</a></div>

<!-- HERO showcase (light) -->
<section class="showcase showcase-bg-light" id="hero">
<span class="hero-badge">{{BADGE}}</span>
<h2>{{HERO_TITLE}}</h2>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="cta-row">
<a href="#form" class="btn-pill btn-primary">{{CTA_BUTTON}}</a>
<a href="#benefits" class="btn-pill btn-link">Learn more</a>
</div>
<div class="product-stage stage-blue"></div>
</section>

<!-- Stats hairline band -->
<div class="stats-band"><div class="stats-inner">
<div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></div>

<!-- BENEFITS — 4 full-bleed Apple-style product showcase sections (alt bg) -->
<section class="showcase showcase-bg-gray" id="benefits">
<span class="eyebrow">{{BENEFIT_1_ICON}} &nbsp; {{BENEFITS_HEADLINE}}</span>
<h2>{{BENEFIT_1_TITLE}}</h2>
<p class="sub">{{BENEFIT_1_DESC}}</p>
<div class="cta-row">
<a href="#form" class="btn-pill btn-primary">{{CTA_BUTTON}}</a>
<a href="#how" class="btn-pill btn-link">Learn more</a>
</div>
<div class="product-stage stage-gray"></div>
</section>

<section class="showcase showcase-bg-dark">
<span class="eyebrow">{{BENEFIT_2_ICON}}</span>
<h2>{{BENEFIT_2_TITLE}}</h2>
<p class="sub">{{BENEFIT_2_DESC}}</p>
<div class="cta-row">
<a href="#form" class="btn-pill btn-primary">{{CTA_BUTTON}}</a>
<a href="#how" class="btn-pill btn-link">Learn more</a>
</div>
<div class="product-stage stage-dark"></div>
</section>

<section class="showcase showcase-bg-peach">
<span class="eyebrow">{{BENEFIT_3_ICON}}</span>
<h2>{{BENEFIT_3_TITLE}}</h2>
<p class="sub">{{BENEFIT_3_DESC}}</p>
<div class="cta-row">
<a href="#form" class="btn-pill btn-primary">{{CTA_BUTTON}}</a>
<a href="#how" class="btn-pill btn-link">Learn more</a>
</div>
<div class="product-stage stage-peach"></div>
</section>

<section class="showcase showcase-bg-mint">
<span class="eyebrow">{{BENEFIT_4_ICON}}</span>
<h2>{{BENEFIT_4_TITLE}}</h2>
<p class="sub">{{BENEFIT_4_DESC}}</p>
<p class="sub" style="font-size:17px;margin-top:-8px;opacity:.75">{{BENEFITS_SUBHEADLINE}}</p>
<div class="cta-row">
<a href="#form" class="btn-pill btn-primary">{{CTA_BUTTON}}</a>
<a href="#how" class="btn-pill btn-link">Learn more</a>
</div>
<div class="product-stage stage-mint"></div>
</section>

<!-- HOW IT WORKS — single light-gray section with 3-col grid -->
<section class="how-section" id="how"><div class="how-inner">
<span class="how-eyebrow">How it works</span>
<h2>{{HOW_HEADLINE}}</h2>
<p class="sub">{{HOW_SUBHEADLINE}}</p>
<div class="how-grid">
<div class="how-step"><div class="how-step-num">Step 01</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="how-step"><div class="how-step-num">Step 02</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="how-step"><div class="how-step-num">Step 03</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>

<!-- REVIEWS -->
<section class="reviews-section" id="reviews"><div class="reviews-inner">
<h2>{{REVIEWS_HEADLINE}}</h2>
<p class="sub">{{REVIEWS_SUBHEADLINE}}</p>
<div class="reviews-grid">
<div class="review-card"><div class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-initials">{{REVIEW_1_INITIALS}}</div><div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div></div></div>
<div class="review-card"><div class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-initials">{{REVIEW_2_INITIALS}}</div><div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div></div></div>
</div>
</div></section>

<!-- FAQ -->
<section class="faq-section" id="faq"><div class="faq-inner">
<h2>{{FAQ_HEADLINE}}</h2>
<p class="sub">{{FAQ_SUBHEADLINE}}</p>
<div class="faq-list">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<!-- CTA FORM -->
<section class="cta-section" id="form"><div class="cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p class="sub">{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div></section>

<!-- FOOTER — Apple 7-column text-only -->
<footer class="footer"><div class="footer-inner">
<div class="footer-disclaimer">More ways to shop: <a href="#form" style="color:var(--accent)">Find a partner</a> or <a href="#form" style="color:var(--accent)">talk to a specialist</a>. Or call contact@biz.ekoaiautomation.com.</div>
<div class="footer-cols">
<div class="footer-col"><h4>Shop &amp; Learn</h4><ul><li><a href="#benefits">Store</a></li><li><a href="#benefits">Features</a></li><li><a href="#how">How it works</a></li><li><a href="#reviews">Customers</a></li><li><a href="#faq">Support</a></li></ul></div>
<div class="footer-col"><h4>Services</h4><ul><li><a href="#form">Eko AI Cloud</a></li><li><a href="#form">Eko AI Pay</a></li><li><a href="#form">AI Care</a></li><li><a href="#form">Trade In</a></li></ul></div>
<div class="footer-col"><h4>Eko Store</h4><ul><li><a href="#form">Find a Store</a></li><li><a href="#form">Genius Bar</a></li><li><a href="#form">Today at Eko</a></li><li><a href="#form">Group Reservations</a></li></ul></div>
<div class="footer-col"><h4>For Business</h4><ul><li><a href="#">Eko and Business</a></li><li><a href="#">Shop for Business</a></li></ul></div>
<div class="footer-col"><h4>For Education</h4><ul><li><a href="#">Eko and Education</a></li><li><a href="#">Shop for K-12</a></li><li><a href="#">Shop for University</a></li></ul></div>
<div class="footer-col"><h4>For Healthcare</h4><ul><li><a href="#">Eko in Healthcare</a></li><li><a href="#">Health Records</a></li><li><a href="#">AI Watch in Healthcare</a></li></ul></div>
<div class="footer-col"><h4>Eko Values</h4><ul><li><a href="#">Accessibility</a></li><li><a href="#">Education</a></li><li><a href="#">Environment</a></li><li><a href="#">Privacy</a></li><li><a href="#">Supply Chain</a></li></ul></div>
</div>
<div class="footer-bottom">
<div>Copyright &copy; {{YEAR}} Eko AI Inc. All rights reserved.</div>
<div><a href="#">Privacy Policy</a> &nbsp;|&nbsp; <a href="#">Terms of Use</a> &nbsp;|&nbsp; <a href="#">Sales and Refunds</a> &nbsp;|&nbsp; <a href="#">Legal</a> &nbsp;|&nbsp; <a href="#">Site Map</a></div>
</div>
</div></footer>
__FORM_SUBMIT_JS__
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 3: STRIPE GRADIENT — Gradient mesh hero, technical/clean, sophisticated
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_STRIPE_GRADIENT = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#f6f9fc;
  --bg-white:#fff;
  --text:#0a2540;
  --text-soft:#425466;
  --text-muted:#697386;
  --hair:#e3e8ee;
  --brand:#635bff;
  --brand-h:#5851ec;
  --cyan:#00d4ff;
  --pink:#ff80bf;
  --mint:#a3f7bf;
  --orange:#ffb340;
  --navy:#0a2540;
}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:'Sohne','Inter','-apple-system',BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;font-weight:425;min-height:100vh}
a{color:var(--brand);text-decoration:none}
a:hover{text-decoration:underline}

/* NAV — white sticky, sharp bottom shadow */
.nav{position:sticky;top:0;z-index:9999;background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(12px);-webkit-backdrop-filter:saturate(180%) blur(12px);box-shadow:0 1px 0 rgba(0,0,0,.05)}
.nav-inner{max-width:1080px;margin:0 auto;padding:0 24px;height:64px;display:flex;align-items:center;gap:36px}
.brand{display:flex;align-items:center;gap:6px;font-weight:600;font-size:22px;letter-spacing:-.02em;color:var(--text);font-family:'Sohne','Inter',sans-serif;font-style:italic}
.brand svg{width:60px;height:25px;display:block}
.nav-links{display:flex;list-style:none;gap:24px;flex:1}
.nav-links a{color:var(--text);font-size:15px;font-weight:500;letter-spacing:-.005em;padding:6px 0;position:relative}
.nav-links a:hover{color:var(--brand);text-decoration:none}
.nav-utility{display:flex;gap:18px;align-items:center}
.nav-utility a{color:var(--text);font-size:15px;font-weight:500}
.nav-utility .signin{color:var(--text)}
.btn-dark{background:var(--navy);color:#fff;padding:8px 16px;border-radius:9999px;font-size:15px;font-weight:500;letter-spacing:-.005em;display:inline-flex;align-items:center;gap:6px;transition:background .15s,transform .15s;border:none;cursor:pointer;font-family:inherit}
.btn-dark:hover{background:#1c3556;text-decoration:none;color:#fff;transform:translateY(-1px)}
.btn-dark::after{content:'\2192';margin-left:2px;font-size:16px}
.nav-hamburger{display:none;background:none;border:none;color:var(--text);font-size:22px;cursor:pointer;padding:8px}

/* HERO with ANIMATED GRADIENT MESH (Stripe signature) */
.hero-wrap{position:relative;overflow:hidden;background:var(--bg);padding-bottom:60px}
.mesh{position:absolute;inset:0;overflow:hidden;z-index:0;pointer-events:none}
.mesh::before,.mesh::after,.mesh-blob1,.mesh-blob2,.mesh-blob3{content:'';position:absolute;border-radius:50%;filter:blur(120px);opacity:.7;mix-blend-mode:multiply}
.mesh::before{width:560px;height:560px;background:#635bff;top:-120px;left:-80px;animation:drift1 26s ease-in-out infinite alternate}
.mesh::after{width:520px;height:520px;background:#00d4ff;top:-40px;right:-100px;animation:drift2 30s ease-in-out infinite alternate}
.mesh-blob1{width:480px;height:480px;background:#ff80bf;top:240px;left:35%;opacity:.55;animation:drift3 28s ease-in-out infinite alternate}
.mesh-blob2{width:440px;height:440px;background:#a3f7bf;bottom:-80px;left:8%;opacity:.55;animation:drift4 32s ease-in-out infinite alternate}
.mesh-blob3{width:420px;height:420px;background:#ffb340;bottom:-120px;right:5%;opacity:.5;animation:drift5 24s ease-in-out infinite alternate}
@keyframes drift1{0%{transform:translate(0,0) scale(1)}100%{transform:translate(80px,60px) scale(1.1)}}
@keyframes drift2{0%{transform:translate(0,0) scale(1)}100%{transform:translate(-60px,40px) scale(1.05)}}
@keyframes drift3{0%{transform:translate(0,0) scale(1)}100%{transform:translate(-100px,80px) scale(.95)}}
@keyframes drift4{0%{transform:translate(0,0) scale(1)}100%{transform:translate(120px,-40px) scale(1.08)}}
@keyframes drift5{0%{transform:translate(0,0) scale(1)}100%{transform:translate(-80px,-60px) scale(.95)}}

.hero{position:relative;z-index:1;padding:88px 24px 40px;max-width:1080px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.hero-left{max-width:560px}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.6);backdrop-filter:blur(8px);border:1px solid rgba(99,91,255,.2);color:var(--brand);padding:6px 14px;border-radius:9999px;font-size:13px;font-weight:500;letter-spacing:-.005em;margin-bottom:24px}
.hero-badge::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--brand)}
.hero h1{font-size:clamp(40px,5.5vw,72px);font-weight:600;line-height:1.05;letter-spacing:-.025em;margin-bottom:24px;color:var(--text);font-family:'Sohne','Inter',sans-serif}
.hero h1 .grad{background:linear-gradient(135deg,#635bff 0%,#00d4ff 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero p.sub{font-size:20px;color:var(--text-soft);line-height:1.45;margin-bottom:32px;font-weight:425;letter-spacing:-.005em}
.hero-cta-row{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:18px}
.btn-grad{background:linear-gradient(135deg,#635bff 0%,#00d4ff 100%);color:#fff;padding:14px 26px;border-radius:9999px;font-size:16px;font-weight:500;letter-spacing:-.005em;display:inline-flex;align-items:center;gap:6px;transition:transform .15s,box-shadow .2s;border:none;cursor:pointer;font-family:inherit;box-shadow:0 4px 14px rgba(99,91,255,.35)}
.btn-grad:hover{transform:translateY(-1px);box-shadow:0 8px 22px rgba(99,91,255,.45);text-decoration:none;color:#fff}
.btn-grad::after{content:'\2192';margin-left:2px}
.btn-outline{background:rgba(255,255,255,.7);backdrop-filter:blur(8px);color:var(--text);padding:14px 26px;border-radius:9999px;font-size:16px;font-weight:500;letter-spacing:-.005em;border:1px solid rgba(10,37,64,.12);display:inline-flex;align-items:center;gap:6px;cursor:pointer;font-family:inherit;transition:background .15s,transform .15s}
.btn-outline:hover{background:#fff;text-decoration:none;color:var(--text);transform:translateY(-1px)}

/* CODE PREVIEW BLOCK — Stripe signature */
.code-card{background:#0a2540;border-radius:14px;box-shadow:0 50px 100px -20px rgba(50,50,93,.25),0 30px 60px -30px rgba(0,0,0,.3);overflow:hidden;font-family:'Sohne Mono','SF Mono','Roboto Mono',Menlo,monospace;font-size:13px;line-height:1.6;position:relative;transform:rotate(-1deg)}
.code-tabs{display:flex;background:#1a2f4e;padding:0 4px;border-bottom:1px solid rgba(255,255,255,.06)}
.code-tab{padding:11px 16px;color:#8da6c5;font-size:12px;font-weight:500;border-bottom:2px solid transparent;cursor:pointer}
.code-tab.active{color:#fff;border-bottom-color:var(--cyan)}
.code-dots{display:flex;gap:6px;padding:11px 14px;border-right:1px solid rgba(255,255,255,.06)}
.code-dot{width:10px;height:10px;border-radius:50%;background:#ff5f57}
.code-dot:nth-child(2){background:#ffbd2e}
.code-dot:nth-child(3){background:#28ca42}
.code-body{padding:22px 24px;color:#cdd9e8;overflow-x:auto}
.code-line{display:block;white-space:nowrap}
.tk-comment{color:#7a8ca9;font-style:italic}
.tk-key{color:#a3f7bf}
.tk-str{color:#ff80bf}
.tk-num{color:#ffb340}
.tk-fn{color:#00d4ff}
.tk-kw{color:#c4a8ff}
.tk-prop{color:#cdd9e8}

/* TRUSTED-BY LOGO STRIP */
.trust-strip{background:var(--bg);padding:40px 24px 0;position:relative;z-index:1}
.trust-inner{max-width:1080px;margin:0 auto;text-align:center}
.trust-label{font-size:13px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:22px;font-weight:500}
.trust-logos{display:flex;justify-content:space-between;align-items:center;gap:32px;flex-wrap:wrap;opacity:.55}
.trust-logo{font-family:'Sohne','Inter',sans-serif;font-size:22px;font-weight:700;color:var(--text);letter-spacing:-.02em}
.trust-logo.italic{font-style:italic;font-weight:600}

/* STATS BAND */
.stats-band{background:var(--bg-white);padding:72px 24px;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);position:relative;z-index:1}
.stats-inner{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:48px;text-align:left}
.stat-num{font-size:clamp(40px,5vw,56px);font-weight:600;letter-spacing:-.025em;color:var(--text);line-height:1;margin-bottom:8px;font-family:'Sohne','Inter',sans-serif}
.stat-num .grad{background:linear-gradient(135deg,#635bff,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.stat-label{font-size:13px;color:var(--text-muted);text-transform:uppercase;letter-spacing:.08em;font-weight:500}

/* SECTION generic */
.section{padding:96px 24px;background:var(--bg-white)}
.section-alt{background:var(--bg)}
.section-inner{max-width:1080px;margin:0 auto}
.section-head{max-width:680px;margin:0 auto 56px;text-align:center}
.section-eyebrow{display:inline-block;font-size:13px;color:var(--brand);text-transform:uppercase;letter-spacing:.1em;font-weight:600;margin-bottom:16px}
.section-head h2{font-size:clamp(34px,4.5vw,52px);font-weight:600;letter-spacing:-.025em;line-height:1.08;color:var(--text);margin-bottom:18px;font-family:'Sohne','Inter',sans-serif}
.section-head p{font-size:19px;color:var(--text-soft);line-height:1.5;font-weight:425}

/* BENEFITS — Stripe-style cards w/ gradient icon circles */
.benefits-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.benefit-card{background:#fff;border:1px solid var(--hair);border-radius:16px;padding:36px 32px;box-shadow:0 1px 2px rgba(0,0,0,.04);transition:box-shadow .25s,transform .25s,border-color .25s;position:relative;overflow:hidden}
.benefit-card:hover{box-shadow:0 18px 36px -16px rgba(50,50,93,.18);transform:translateY(-2px);border-color:rgba(99,91,255,.25)}
.benefit-icon{width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,#635bff,#00d4ff);color:#fff;display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:24px;box-shadow:0 6px 16px -6px rgba(99,91,255,.5)}
.benefit-card:nth-child(2) .benefit-icon{background:linear-gradient(135deg,#ff80bf,#ffb340)}
.benefit-card:nth-child(3) .benefit-icon{background:linear-gradient(135deg,#a3f7bf,#00d4ff)}
.benefit-card:nth-child(4) .benefit-icon{background:linear-gradient(135deg,#635bff,#ff80bf)}
.benefit-card h3{font-size:21px;font-weight:600;letter-spacing:-.012em;margin-bottom:10px;color:var(--text);line-height:1.25}
.benefit-card p{font-size:16px;color:var(--text-soft);line-height:1.55;font-weight:425}

/* HOW — numbered step row */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;position:relative}
.steps::before{content:'';position:absolute;top:32px;left:12%;right:12%;height:1px;background:linear-gradient(90deg,transparent,var(--hair) 20%,var(--hair) 80%,transparent);z-index:0}
.step{position:relative;z-index:1;text-align:center;padding:0 12px}
.step-num{width:64px;height:64px;border-radius:50%;background:#fff;border:1px solid var(--hair);color:var(--brand);font-size:22px;font-weight:600;display:flex;align-items:center;justify-content:center;margin:0 auto 24px;box-shadow:0 6px 16px -6px rgba(50,50,93,.12);font-family:'Sohne Mono','SF Mono',monospace}
.step h3{font-size:19px;font-weight:600;letter-spacing:-.01em;margin-bottom:8px;color:var(--text)}
.step p{font-size:15px;color:var(--text-soft);line-height:1.5}

/* REVIEWS — white cards w/ rating, quote, author */
.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.review{background:#fff;border:1px solid var(--hair);border-radius:16px;padding:36px 32px;box-shadow:0 1px 2px rgba(0,0,0,.04);position:relative}
.review .stars{color:#ffb340;font-size:14px;margin-bottom:16px;letter-spacing:2px}
.review-quote{font-size:18px;color:var(--text);line-height:1.5;font-weight:425;margin-bottom:24px;letter-spacing:-.005em}
.review-author{display:flex;align-items:center;gap:14px;border-top:1px solid var(--hair);padding-top:20px}
.review-avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#635bff,#00d4ff);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:600}
.review:nth-child(2) .review-avatar{background:linear-gradient(135deg,#ff80bf,#ffb340)}
.review-name{font-size:15px;font-weight:600;color:var(--text);letter-spacing:-.005em}
.review-role{font-size:13px;color:var(--text-muted)}

/* FAQ — Stripe-style left-aligned w/ + toggle */
.faq{max-width:760px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--hair)}
.faq-q{width:100%;text-align:left;background:none;border:none;padding:24px 0;font-size:18px;font-weight:600;letter-spacing:-.005em;color:var(--text);cursor:pointer;font-family:inherit;display:flex;justify-content:space-between;align-items:center;line-height:1.4;gap:24px}
.faq-q::after{content:'+';font-size:22px;color:var(--brand);transition:transform .25s;flex-shrink:0;font-weight:500}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .25s;font-size:16px;color:var(--text-soft);line-height:1.55}
.faq-item.active .faq-a{max-height:600px;padding:0 0 24px}

/* CTA section — gradient bg */
.cta-block{background:linear-gradient(135deg,#635bff 0%,#00d4ff 100%);padding:88px 24px;color:#fff;text-align:center;position:relative;overflow:hidden}
.cta-block::before{content:'';position:absolute;top:-100px;left:-50px;width:300px;height:300px;background:#ff80bf;filter:blur(100px);opacity:.4;border-radius:50%}
.cta-block::after{content:'';position:absolute;bottom:-100px;right:-50px;width:300px;height:300px;background:#a3f7bf;filter:blur(100px);opacity:.4;border-radius:50%}
.cta-inner{max-width:680px;margin:0 auto;position:relative;z-index:1}
.cta-inner h2{font-size:clamp(36px,5vw,56px);font-weight:600;letter-spacing:-.025em;line-height:1.08;margin-bottom:18px;color:#fff}
.cta-inner p{font-size:19px;line-height:1.5;margin-bottom:36px;opacity:.92}
.cta-form{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;max-width:520px;margin:0 auto}
.cta-form input{padding:14px 18px;border-radius:8px;border:none;background:rgba(255,255,255,.95);color:var(--text);font-size:15px;font-family:inherit;outline:none;font-weight:425}
.cta-form input::placeholder{color:var(--text-muted)}
.cta-form input:focus{box-shadow:0 0 0 3px rgba(255,255,255,.4)}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:1/-1}
.cta-form button{grid-column:1/-1;padding:14px 28px;border-radius:8px;border:none;background:var(--navy);color:#fff;font-size:16px;font-weight:600;cursor:pointer;font-family:inherit;letter-spacing:-.005em;transition:background .15s,transform .15s;margin-top:6px}
.cta-form button:hover{background:#1c3556;transform:translateY(-1px)}

/* FOOTER — navy w/ white text, 5-col */
.footer{background:var(--navy);color:#adbdcc;padding:72px 24px 32px}
.footer-inner{max-width:1080px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px;border-bottom:1px solid rgba(255,255,255,.08)}
.footer-brand{display:flex;align-items:center;gap:8px;font-size:24px;font-weight:600;font-style:italic;color:#fff;letter-spacing:-.02em;margin-bottom:12px;font-family:'Sohne','Inter',sans-serif}
.footer-tag{font-size:14px;color:#7c8da0;line-height:1.55;max-width:280px}
.footer-col h4{font-size:13px;font-weight:600;color:#fff;margin-bottom:18px;text-transform:uppercase;letter-spacing:.1em}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:10px}
.footer-col a{color:#adbdcc;font-size:14px;transition:color .15s}
.footer-col a:hover{color:#fff;text-decoration:none}
.footer-bot{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding-top:32px;font-size:13px;color:#7c8da0}
.footer-bot a{color:#7c8da0}
.footer-bot a:hover{color:#fff;text-decoration:none}

@media(max-width:900px){
.hero{grid-template-columns:1fr;gap:36px;padding:60px 20px 30px}
.code-card{transform:rotate(0deg)}
.benefits-grid,.reviews-grid{grid-template-columns:1fr}
.stats-inner{grid-template-columns:1fr;gap:36px;text-align:center}
.steps{grid-template-columns:1fr;gap:48px}
.steps::before{display:none}
.footer-top{grid-template-columns:1fr 1fr;gap:36px}
.trust-logos{justify-content:center;gap:24px}
}
@media(max-width:640px){
.nav-links,.nav-utility{display:none}
.nav-hamburger{display:block;margin-left:auto}
.nav-inner{padding:0 18px;gap:0}
.hero{padding:48px 18px 24px}
.hero h1{font-size:36px}
.hero p.sub{font-size:17px}
.section{padding:60px 18px}
.cta-block{padding:60px 18px}
.cta-form{grid-template-columns:1fr}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:auto}
.code-body{font-size:11px;padding:18px}
.section-head h2{font-size:28px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="brand"><svg viewBox="0 0 60 25" xmlns="http://www.w3.org/2000/svg"><text x="0" y="20" font-family="Sohne, Inter, sans-serif" font-weight="700" font-style="italic" font-size="22" fill="#0a2540">eko</text></svg></a>
<ul class="nav-links">
<li><a href="#benefits">Products</a></li>
<li><a href="#how">Solutions</a></li>
<li><a href="#">Developers</a></li>
<li><a href="#reviews">Resources</a></li>
<li><a href="#">Pricing</a></li>
</ul>
<div class="nav-utility">
<a href="#form" class="signin">Sign in</a>
<a href="#form" class="btn-dark">Contact sales</a>
</div>
<button class="nav-hamburger" aria-label="Menu">&#9776;</button>
</div></nav>

<!-- HERO with animated gradient mesh -->
<div class="hero-wrap">
<div class="mesh"><div class="mesh-blob1"></div><div class="mesh-blob2"></div><div class="mesh-blob3"></div></div>
<section class="hero">
<div class="hero-left">
<span class="hero-badge">{{BADGE}}</span>
<h1>{{HERO_TITLE}} <span class="grad">automation infrastructure</span> for the modern business.</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="hero-cta-row">
<a href="#form" class="btn-grad">{{CTA_BUTTON}}</a>
<a href="#benefits" class="btn-outline">Contact sales &#8594;</a>
</div>
</div>
<div class="hero-right">
<div class="code-card">
<div style="display:flex;align-items:center">
<div class="code-dots"><span class="code-dot"></span><span class="code-dot"></span><span class="code-dot"></span></div>
<div class="code-tabs">
<span class="code-tab active">eko.js</span>
<span class="code-tab">automate.py</span>
<span class="code-tab">.curl</span>
</div>
</div>
<div class="code-body">
<span class="code-line"><span class="tk-comment">// Automate any business workflow in seconds</span></span>
<span class="code-line"><span class="tk-kw">const</span> <span class="tk-prop">eko</span> <span class="tk-kw">=</span> <span class="tk-fn">require</span><span class="tk-prop">(</span><span class="tk-str">'eko-ai'</span><span class="tk-prop">)(</span><span class="tk-str">'sk_live_***'</span><span class="tk-prop">);</span></span>
<span class="code-line">&nbsp;</span>
<span class="code-line"><span class="tk-kw">const</span> <span class="tk-prop">workflow</span> <span class="tk-kw">=</span> <span class="tk-kw">await</span> <span class="tk-prop">eko.workflows.</span><span class="tk-fn">create</span><span class="tk-prop">({</span></span>
<span class="code-line">&nbsp;&nbsp;<span class="tk-key">name</span><span class="tk-prop">:</span> <span class="tk-str">'lead-followup-sequence'</span><span class="tk-prop">,</span></span>
<span class="code-line">&nbsp;&nbsp;<span class="tk-key">trigger</span><span class="tk-prop">:</span> <span class="tk-str">'form.submit'</span><span class="tk-prop">,</span></span>
<span class="code-line">&nbsp;&nbsp;<span class="tk-key">model</span><span class="tk-prop">:</span> <span class="tk-str">'eko-pro-v3'</span><span class="tk-prop">,</span></span>
<span class="code-line">&nbsp;&nbsp;<span class="tk-key">channels</span><span class="tk-prop">: [</span><span class="tk-str">'email'</span><span class="tk-prop">,</span> <span class="tk-str">'sms'</span><span class="tk-prop">,</span> <span class="tk-str">'whatsapp'</span><span class="tk-prop">],</span></span>
<span class="code-line">&nbsp;&nbsp;<span class="tk-key">cadence</span><span class="tk-prop">: {</span> <span class="tk-key">days</span><span class="tk-prop">:</span> <span class="tk-num">14</span><span class="tk-prop">,</span> <span class="tk-key">touches</span><span class="tk-prop">:</span> <span class="tk-num">7</span> <span class="tk-prop">},</span></span>
<span class="code-line"><span class="tk-prop">});</span></span>
<span class="code-line">&nbsp;</span>
<span class="code-line"><span class="tk-prop">console.</span><span class="tk-fn">log</span><span class="tk-prop">(</span><span class="tk-str">`Workflow live: </span><span class="tk-prop">${</span><span class="tk-prop">workflow.id</span><span class="tk-prop">}</span><span class="tk-str">`</span><span class="tk-prop">);</span></span>
<span class="code-line"><span class="tk-comment">// > Workflow live: wf_3RX9pK7Jh2Lq</span></span>
</div>
</div>
</div>
</section>
<div class="trust-strip"><div class="trust-inner">
<div class="trust-label">Trusted by forward-thinking businesses worldwide</div>
<div class="trust-logos">
<span class="trust-logo italic">amazon</span>
<span class="trust-logo">SHOPIFY</span>
<span class="trust-logo italic">salesforce</span>
<span class="trust-logo">NOTION</span>
<span class="trust-logo">FIGMA</span>
<span class="trust-logo italic">slack</span>
</div>
</div></div>
</div>

<!-- STATS -->
<div class="stats-band"><div class="stats-inner">
<div><div class="stat-num"><span class="grad">{{STAT_1_NUM}}</span></div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num"><span class="grad">{{STAT_2_NUM}}</span></div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num"><span class="grad">{{STAT_3_NUM}}</span></div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></div>

<!-- BENEFITS -->
<section class="section" id="benefits"><div class="section-inner">
<div class="section-head">
<span class="section-eyebrow">Products</span>
<h2>{{BENEFITS_HEADLINE}}</h2>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>
<div class="benefits-grid">
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div>
</div></section>

<!-- HOW IT WORKS -->
<section class="section section-alt" id="how"><div class="section-inner">
<div class="section-head">
<span class="section-eyebrow">How it works</span>
<h2>{{HOW_HEADLINE}}</h2>
<p>{{HOW_SUBHEADLINE}}</p>
</div>
<div class="steps">
<div class="step"><div class="step-num">01</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">02</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">03</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>

<!-- REVIEWS -->
<section class="section" id="reviews"><div class="section-inner">
<div class="section-head">
<span class="section-eyebrow">Customers</span>
<h2>{{REVIEWS_HEADLINE}}</h2>
<p>{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-grid">
<div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><div class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div></div></div>
<div class="review"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><div class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div></div></div>
</div>
</div></section>

<!-- FAQ -->
<section class="section section-alt" id="faq"><div class="section-inner">
<div class="section-head">
<span class="section-eyebrow">FAQs</span>
<h2>{{FAQ_HEADLINE}}</h2>
<p>{{FAQ_SUBHEADLINE}}</p>
</div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<!-- CTA BLOCK -->
<section class="cta-block" id="form"><div class="cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Work email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Company website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div></section>

<!-- FOOTER navy -->
<footer class="footer"><div class="footer-inner">
<div class="footer-top">
<div>
<div class="footer-brand">eko</div>
<div class="footer-tag">Automation infrastructure for ambitious businesses, powered by AI.</div>
</div>
<div class="footer-col"><h4>Products</h4><ul><li><a href="#benefits">Automate</a></li><li><a href="#benefits">Sequences</a></li><li><a href="#benefits">Inbox</a></li><li><a href="#benefits">Reports</a></li></ul></div>
<div class="footer-col"><h4>Solutions</h4><ul><li><a href="#how">SaaS</a></li><li><a href="#how">Agencies</a></li><li><a href="#how">E-commerce</a></li><li><a href="#how">Enterprise</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#reviews">Customers</a></li><li><a href="#faq">Support</a></li><li><a href="#">Docs</a></li><li><a href="#">API</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Jobs</a></li><li><a href="#">Newsroom</a></li><li><a href="#">Privacy</a></li></ul></div>
</div>
<div class="footer-bot">
<div>&copy; {{YEAR}} Eko AI Inc. &nbsp;|&nbsp; <a href="#">Privacy &amp; terms</a> &nbsp;|&nbsp; <a href="#">Cookie settings</a></div>
<div>contact@biz.ekoaiautomation.com</div>
</div>
</div></footer>
__FORM_SUBMIT_JS__
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 4: LINEAR DARK — Pure black bg, neon purple accents, sharp geometric
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_LINEAR_DARK = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#08080a;
  --bg-1:#0d0e10;
  --bg-2:#131418;
  --text:#f7f8f8;
  --text-soft:#b4bcd0;
  --text-muted:#8a8f98;
  --border:rgba(255,255,255,.08);
  --border-soft:rgba(255,255,255,.06);
  --border-hover:rgba(94,106,210,.45);
  --purple:#5e6ad2;
  --purple-soft:rgba(94,106,210,.15);
  --purple-glow:rgba(94,106,210,.35);
}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:'Inter Display','Inter','-apple-system',BlinkMacSystemFont,'SF Pro Display','Helvetica Neue',Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;font-weight:400;min-height:100vh;font-feature-settings:'ss01','cv11'}
a{color:var(--text);text-decoration:none;transition:color .15s}
a:hover{color:var(--text)}
.mono{font-family:'Berkeley Mono','SF Mono','JetBrains Mono','Roboto Mono',Menlo,monospace}

/* GRID PATTERN BACKGROUND (Linear signature) */
.grid-bg{position:fixed;inset:0;z-index:0;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:64px 64px;mask-image:radial-gradient(ellipse 80% 60% at 50% 30%,#000 50%,transparent 100%);-webkit-mask-image:radial-gradient(ellipse 80% 60% at 50% 30%,#000 50%,transparent 100%)}
.purple-glow{position:absolute;top:0;left:0;right:0;height:800px;z-index:0;pointer-events:none;background:radial-gradient(ellipse 60% 50% at 50% 25%,var(--purple-glow) 0%,transparent 60%)}

/* NAV — translucent dark, sharp, sparse */
.nav{position:sticky;top:0;z-index:9999;background:rgba(8,8,10,.7);backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);border-bottom:1px solid var(--border-soft)}
.nav-inner{max-width:1280px;margin:0 auto;padding:0 32px;height:60px;display:flex;align-items:center;gap:40px}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);font-weight:500;font-size:15px;letter-spacing:-.02em}
.brand .mark{width:24px;height:24px;border-radius:6px;background:linear-gradient(135deg,#5e6ad2 0%,#7c89e6 100%);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:13px;box-shadow:0 0 12px rgba(94,106,210,.4);font-family:'Berkeley Mono',monospace}
.nav-links{display:flex;list-style:none;gap:28px;flex:1}
.nav-links a{color:var(--text-soft);font-size:14px;font-weight:400;letter-spacing:-.005em;transition:color .15s}
.nav-links a:hover{color:var(--text)}
.nav-utility{display:flex;gap:16px;align-items:center}
.nav-utility a{color:var(--text-soft);font-size:14px;font-weight:400}
.nav-utility a:hover{color:var(--text)}
.btn-sharp{background:#fff;color:#08080a;padding:7px 14px;border-radius:6px;font-size:14px;font-weight:500;letter-spacing:-.005em;display:inline-flex;align-items:center;gap:4px;transition:background .15s,transform .15s;border:none;cursor:pointer;font-family:inherit}
.btn-sharp:hover{background:#e6e6e6;color:#08080a;text-decoration:none;transform:translateY(-1px)}
.btn-sharp-outline{background:transparent;color:var(--text);padding:7px 14px;border-radius:6px;font-size:14px;font-weight:500;letter-spacing:-.005em;display:inline-flex;align-items:center;gap:4px;border:1px solid var(--border);cursor:pointer;font-family:inherit;transition:border-color .15s,background .15s}
.btn-sharp-outline:hover{border-color:rgba(255,255,255,.18);background:rgba(255,255,255,.04);color:var(--text);text-decoration:none}
.nav-hamburger{display:none;background:none;border:none;color:var(--text);font-size:20px;cursor:pointer;padding:6px}

/* HERO — compact centered, NEW pill badge, sharp CTAs */
.hero{position:relative;z-index:1;padding:120px 32px 80px;text-align:center;max-width:1280px;margin:0 auto;overflow:hidden}
.new-pill{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.04);border:1px solid var(--border);padding:5px 5px 5px 14px;border-radius:9999px;font-size:13px;color:var(--text-soft);letter-spacing:-.005em;margin-bottom:32px;transition:border-color .15s,background .15s;cursor:pointer}
.new-pill:hover{border-color:rgba(94,106,210,.4);background:rgba(94,106,210,.05);color:var(--text)}
.new-pill .new-tag{background:var(--purple-soft);color:#a4afff;font-size:11px;font-weight:500;padding:2px 8px;border-radius:9999px;margin-left:0;text-transform:uppercase;letter-spacing:.04em}
.new-pill .new-arrow{margin-left:0;color:var(--text-muted);font-size:14px;padding-right:8px}
.hero-h1{font-size:clamp(40px,5.5vw,72px);font-weight:560;line-height:1.05;letter-spacing:-.045em;color:var(--text);max-width:840px;margin:0 auto 24px;font-family:'Inter Display','Inter',sans-serif}
.hero-sub{font-size:20px;color:var(--text-soft);line-height:1.45;max-width:600px;margin:0 auto 40px;font-weight:400;letter-spacing:-.005em}
.hero-cta-row{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:80px}

/* APP SCREENSHOT MOCKUP — Linear signature dark window with subtle glow */
.app-mockup{max-width:1100px;margin:0 auto;background:linear-gradient(180deg,#16181d 0%,#0b0c0e 100%);border:1px solid var(--border);border-radius:14px;overflow:hidden;box-shadow:0 0 0 1px rgba(255,255,255,.02),0 30px 60px -30px rgba(94,106,210,.4),0 60px 120px -40px rgba(0,0,0,.8);position:relative}
.app-mockup::before{content:'';position:absolute;inset:-1px;border-radius:14px;padding:1px;background:linear-gradient(180deg,rgba(94,106,210,.35),transparent 30%);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.app-titlebar{height:34px;background:#0d0e10;border-bottom:1px solid var(--border-soft);display:flex;align-items:center;padding:0 14px;gap:8px}
.app-titlebar .dots{display:flex;gap:6px}
.app-titlebar .dot{width:11px;height:11px;border-radius:50%;background:#383a40}
.app-titlebar .url{flex:1;text-align:center;color:var(--text-muted);font-size:11px;font-family:'Berkeley Mono',monospace;letter-spacing:-.01em}
.app-body{display:grid;grid-template-columns:200px 1fr 280px;min-height:440px}
.app-side{background:#0a0b0d;border-right:1px solid var(--border-soft);padding:16px 12px;font-size:13px}
.app-side-section{margin-bottom:18px}
.app-side-title{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--text-muted);margin-bottom:8px;font-weight:500;padding:0 8px}
.app-side-item{display:flex;align-items:center;gap:8px;padding:5px 8px;border-radius:5px;color:var(--text-soft);cursor:pointer;font-size:13px;letter-spacing:-.005em}
.app-side-item.active{background:rgba(94,106,210,.12);color:#fff}
.app-side-item .ic{width:14px;height:14px;border-radius:3px;background:rgba(255,255,255,.08);flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:9px;color:var(--text-muted)}
.app-side-item.active .ic{background:var(--purple);color:#fff}
.app-main{padding:18px 22px;background:#0b0c0e}
.app-main-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid var(--border-soft)}
.app-main-title{font-size:14px;font-weight:500;color:var(--text)}
.app-main-actions{display:flex;gap:6px}
.app-action-btn{background:rgba(255,255,255,.04);border:1px solid var(--border-soft);color:var(--text-soft);padding:4px 10px;border-radius:5px;font-size:11px;font-family:'Berkeley Mono',monospace;letter-spacing:.02em}
.app-issue{display:grid;grid-template-columns:auto 1fr auto auto auto;gap:12px;align-items:center;padding:9px 8px;border-bottom:1px solid var(--border-soft);font-size:13px;cursor:pointer}
.app-issue:hover{background:rgba(255,255,255,.02)}
.app-issue .pri{width:14px;height:14px;border-radius:3px;background:transparent;border:1px solid var(--text-muted)}
.app-issue.urgent .pri{background:#eb5757;border-color:#eb5757}
.app-issue.high .pri{background:#f2994a;border-color:#f2994a}
.app-issue .id{font-family:'Berkeley Mono',monospace;color:var(--text-muted);font-size:12px;letter-spacing:-.01em;min-width:60px}
.app-issue .title{color:var(--text);letter-spacing:-.005em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.app-issue .tag{font-size:11px;background:var(--purple-soft);color:#a4afff;padding:2px 8px;border-radius:9999px;font-family:'Berkeley Mono',monospace}
.app-issue .tag.bug{background:rgba(235,87,87,.15);color:#ff8b8b}
.app-issue .tag.feature{background:rgba(75,184,166,.15);color:#7eddc9}
.app-issue .assignee{width:18px;height:18px;border-radius:50%;background:linear-gradient(135deg,#5e6ad2,#7c89e6);font-size:9px;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600}
.app-issue .due{color:var(--text-muted);font-size:11px;font-family:'Berkeley Mono',monospace}
.app-detail{background:#0a0b0d;border-left:1px solid var(--border-soft);padding:18px;font-size:13px}
.app-detail h4{font-size:13px;font-weight:500;color:var(--text);margin-bottom:14px;letter-spacing:-.005em}
.app-detail-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border-soft);font-size:12px;color:var(--text-muted)}
.app-detail-row span:last-child{color:var(--text-soft);font-family:'Berkeley Mono',monospace}

/* CUSTOMER LOGO STRIP — sparse mono logos like Linear */
.trust-strip{padding:60px 32px 40px;text-align:center;position:relative;z-index:1}
.trust-label{font-size:13px;color:var(--text-muted);letter-spacing:-.005em;margin-bottom:32px}
.trust-logos{display:flex;justify-content:center;gap:48px;flex-wrap:wrap;align-items:center;opacity:.65;max-width:1080px;margin:0 auto}
.trust-logos span{font-family:'Inter Display','Inter',sans-serif;font-size:18px;font-weight:600;color:var(--text-soft);letter-spacing:-.02em}
.trust-logos span.mono{font-family:'Berkeley Mono',monospace;font-weight:400}

/* STATS — minimal, mono-numbers */
.stats-band{padding:80px 32px;border-top:1px solid var(--border-soft);border-bottom:1px solid var(--border-soft);position:relative;z-index:1}
.stats-inner{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:48px;text-align:left}
.stat-num{font-size:clamp(40px,5vw,64px);font-weight:500;letter-spacing:-.04em;color:var(--text);line-height:1;margin-bottom:10px;font-family:'Inter Display','Inter',sans-serif}
.stat-label{font-size:13px;color:var(--text-muted);letter-spacing:-.005em;line-height:1.4}

/* SECTION */
.section{padding:120px 32px;position:relative;z-index:1}
.section-inner{max-width:1080px;margin:0 auto}
.section-head{max-width:680px;margin:0 auto 64px;text-align:center}
.section-eyebrow{display:inline-block;font-size:13px;color:#a4afff;font-family:'Berkeley Mono',monospace;letter-spacing:-.005em;margin-bottom:18px}
.section-head h2{font-size:clamp(34px,4.5vw,52px);font-weight:560;letter-spacing:-.04em;line-height:1.08;color:var(--text);margin-bottom:18px;font-family:'Inter Display','Inter',sans-serif}
.section-head p{font-size:18px;color:var(--text-soft);line-height:1.5;font-weight:400;letter-spacing:-.005em}

/* BENEFITS — 3x2 grid (4 used), sharp 12px corners, hover purple border */
.benefits-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--border-soft);border:1px solid var(--border-soft);border-radius:12px;overflow:hidden}
.benefit-card{background:#0a0b0d;padding:40px 36px;transition:background .2s;position:relative;cursor:pointer}
.benefit-card:hover{background:#0e0f12}
.benefit-card::after{content:'';position:absolute;inset:0;border:1px solid transparent;border-radius:inherit;transition:border-color .2s;pointer-events:none}
.benefit-card:hover::after{border-color:var(--border-hover)}
.benefit-icon{width:36px;height:36px;border-radius:8px;background:rgba(94,106,210,.1);border:1px solid var(--border);color:#a4afff;display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:24px}
.benefit-card h3{font-size:18px;font-weight:500;letter-spacing:-.012em;margin-bottom:8px;color:var(--text);line-height:1.3}
.benefit-card p{font-size:15px;color:var(--text-soft);line-height:1.55;letter-spacing:-.005em}

/* HOW — vertical numbered list, mono numbers */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid var(--border-soft);border-bottom:1px solid var(--border-soft)}
.step{padding:40px 32px;border-left:1px solid var(--border-soft);position:relative}
.step:first-child{border-left:none}
.step-num{font-family:'Berkeley Mono',monospace;font-size:13px;color:#a4afff;letter-spacing:-.005em;margin-bottom:32px}
.step h3{font-size:18px;font-weight:500;letter-spacing:-.012em;margin-bottom:8px;color:var(--text);line-height:1.3}
.step p{font-size:15px;color:var(--text-soft);line-height:1.55;letter-spacing:-.005em}

/* REVIEWS — text-forward, no card decoration, 2 cols */
.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:48px}
.review{padding:36px 0}
.review-quote{font-size:21px;color:var(--text);line-height:1.45;font-weight:400;margin-bottom:24px;letter-spacing:-.012em;font-family:'Inter Display','Inter',sans-serif}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#5e6ad2,#7c89e6);color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:500}
.review-name{font-size:14px;font-weight:500;color:var(--text);letter-spacing:-.005em}
.review-role{font-size:13px;color:var(--text-muted);letter-spacing:-.005em}

/* FAQ — accordion white-on-black, sharp */
.faq{max-width:760px;margin:0 auto;border-top:1px solid var(--border-soft)}
.faq-item{border-bottom:1px solid var(--border-soft)}
.faq-q{width:100%;text-align:left;background:none;border:none;padding:24px 0;font-size:17px;font-weight:500;letter-spacing:-.012em;color:var(--text);cursor:pointer;font-family:inherit;display:flex;justify-content:space-between;align-items:center;line-height:1.4;gap:24px;transition:color .15s}
.faq-q:hover{color:#a4afff}
.faq-q::after{content:'+';font-size:20px;color:var(--text-muted);transition:transform .25s,color .15s;flex-shrink:0;font-weight:400}
.faq-item.active .faq-q::after{transform:rotate(45deg);color:#a4afff}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .25s;font-size:15px;color:var(--text-soft);line-height:1.6;letter-spacing:-.005em}
.faq-item.active .faq-a{max-height:600px;padding:0 0 24px}

/* CTA SECTION — centered, dark glowing */
.cta-block{padding:120px 32px;text-align:center;position:relative;z-index:1;overflow:hidden}
.cta-block::before{content:'';position:absolute;top:50%;left:50%;width:600px;height:600px;background:radial-gradient(circle,rgba(94,106,210,.18) 0%,transparent 60%);transform:translate(-50%,-50%);pointer-events:none}
.cta-inner{max-width:560px;margin:0 auto;position:relative;z-index:1}
.cta-inner h2{font-size:clamp(36px,5vw,56px);font-weight:560;letter-spacing:-.04em;line-height:1.08;margin-bottom:18px;color:var(--text);font-family:'Inter Display','Inter',sans-serif}
.cta-inner p{font-size:18px;color:var(--text-soft);line-height:1.5;margin-bottom:40px;letter-spacing:-.005em}
.cta-form{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:480px;margin:0 auto}
.cta-form input{padding:11px 14px;border-radius:6px;border:1px solid var(--border);background:rgba(255,255,255,.03);color:var(--text);font-size:14px;font-family:inherit;outline:none;letter-spacing:-.005em;transition:border-color .15s,background .15s}
.cta-form input::placeholder{color:var(--text-muted)}
.cta-form input:focus{border-color:var(--purple);background:rgba(94,106,210,.05)}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:1/-1}
.cta-form button{grid-column:1/-1;padding:11px 24px;border-radius:6px;border:none;background:#fff;color:#08080a;font-size:14px;font-weight:500;cursor:pointer;font-family:inherit;letter-spacing:-.005em;transition:background .15s,transform .15s;margin-top:6px}
.cta-form button:hover{background:#e6e6e6;transform:translateY(-1px)}

/* FOOTER — dark, sparse */
.footer{padding:80px 32px 40px;border-top:1px solid var(--border-soft);position:relative;z-index:1;background:var(--bg)}
.footer-inner{max-width:1280px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px;border-bottom:1px solid var(--border-soft)}
.footer-brand-block{max-width:280px}
.footer-brand-block .brand{font-size:15px;margin-bottom:14px}
.footer-tag{font-size:13px;color:var(--text-muted);line-height:1.55;letter-spacing:-.005em}
.footer-col h4{font-size:13px;font-weight:500;color:var(--text);margin-bottom:14px;letter-spacing:-.005em}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:8px}
.footer-col a{color:var(--text-muted);font-size:13px;letter-spacing:-.005em;transition:color .15s}
.footer-col a:hover{color:#a4afff;text-decoration:none}
.footer-bot{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding-top:32px;font-size:12px;color:var(--text-muted)}
.footer-bot a{color:var(--text-muted)}
.footer-bot a:hover{color:#a4afff;text-decoration:none}
.footer-soc{display:flex;gap:14px}

@media(max-width:900px){
.app-body{grid-template-columns:1fr}
.app-side,.app-detail{display:none}
.benefits-grid{grid-template-columns:1fr}
.reviews-grid{grid-template-columns:1fr;gap:24px}
.steps{grid-template-columns:1fr}
.step{border-left:none;border-top:1px solid var(--border-soft)}
.step:first-child{border-top:none}
.stats-inner{grid-template-columns:1fr;gap:36px;text-align:center}
.footer-top{grid-template-columns:1fr 1fr;gap:36px}
.trust-logos{gap:24px}
}
@media(max-width:640px){
.nav-links,.nav-utility{display:none}
.nav-hamburger{display:block;margin-left:auto}
.nav-inner{padding:0 18px;gap:0}
.hero{padding:60px 20px 40px}
.hero-h1{font-size:32px}
.hero-sub{font-size:16px}
.section,.cta-block{padding:72px 20px}
.cta-form{grid-template-columns:1fr}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:auto}
.app-issue{grid-template-columns:auto 1fr auto;gap:8px}
.app-issue .tag,.app-issue .due{display:none}
.section-head h2{font-size:28px}
.benefit-card{padding:28px 22px}
}
</style></head>
<body>__TRACKING_PIXEL__

<div class="grid-bg"></div>
<div class="purple-glow"></div>

<nav class="nav"><div class="nav-inner">
<a href="#" class="brand"><span class="mark">L</span> Eko</a>
<ul class="nav-links">
<li><a href="#benefits">Features</a></li>
<li><a href="#how">Method</a></li>
<li><a href="#reviews">Customers</a></li>
<li><a href="#">Changelog</a></li>
<li><a href="#">Pricing</a></li>
<li><a href="#faq">Company</a></li>
</ul>
<div class="nav-utility">
<a href="#form">Log in</a>
<a href="#form" class="btn-sharp-outline">Contact</a>
<a href="#form" class="btn-sharp">Sign up</a>
</div>
<button class="nav-hamburger" aria-label="Menu">&#9776;</button>
</div></nav>

<!-- HERO -->
<section class="hero">
<a href="#benefits" class="new-pill"><span class="new-tag">New</span> {{BADGE}} <span class="new-arrow">&rarr;</span></a>
<h1 class="hero-h1">{{HERO_TITLE}}</h1>
<p class="hero-sub">{{HERO_SUBTITLE}}</p>
<div class="hero-cta-row">
<a href="#form" class="btn-sharp">{{CTA_BUTTON}}</a>
<a href="#benefits" class="btn-sharp-outline">Open Eko &rarr;</a>
</div>

<!-- APP SCREENSHOT MOCKUP -->
<div class="app-mockup">
<div class="app-titlebar">
<div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
<div class="url">eko.app/team/EKO/active</div>
<div style="width:50px"></div>
</div>
<div class="app-body">
<aside class="app-side">
<div class="app-side-section">
<div class="app-side-title">Workspace</div>
<div class="app-side-item"><span class="ic">&#9737;</span> Inbox</div>
<div class="app-side-item"><span class="ic">&#9728;</span> My issues</div>
<div class="app-side-item active"><span class="ic">&#9650;</span> Active</div>
<div class="app-side-item"><span class="ic">&#9711;</span> Backlog</div>
</div>
<div class="app-side-section">
<div class="app-side-title">Teams</div>
<div class="app-side-item"><span class="ic">E</span> Engineering</div>
<div class="app-side-item"><span class="ic">D</span> Design</div>
<div class="app-side-item"><span class="ic">G</span> Growth</div>
<div class="app-side-item"><span class="ic">O</span> Operations</div>
</div>
<div class="app-side-section">
<div class="app-side-title">Cycles</div>
<div class="app-side-item"><span class="ic">&#9737;</span> Cycle 47</div>
<div class="app-side-item"><span class="ic">&#9737;</span> Cycle 48</div>
</div>
</aside>
<main class="app-main">
<div class="app-main-head">
<div class="app-main-title">Active &middot; 24 issues</div>
<div class="app-main-actions">
<span class="app-action-btn">Filter</span>
<span class="app-action-btn">Group: Priority</span>
<span class="app-action-btn">+ New</span>
</div>
</div>
<div class="app-issue urgent"><span class="pri"></span><span class="id">EKO-204</span><span class="title">Add multi-channel sequence triggers</span><span class="tag feature">feature</span><span class="assignee">JM</span><span class="due">May 28</span></div>
<div class="app-issue urgent"><span class="pri"></span><span class="id">EKO-198</span><span class="title">Webhook delivery retries past 24h fail silently</span><span class="tag bug">bug</span><span class="assignee">SL</span><span class="due">May 24</span></div>
<div class="app-issue high"><span class="pri"></span><span class="id">EKO-191</span><span class="title">Inbox view should group by thread</span><span class="tag">design</span><span class="assignee">RK</span><span class="due">May 30</span></div>
<div class="app-issue high"><span class="pri"></span><span class="id">EKO-187</span><span class="title">Improve LLM cold-start latency &lt;200ms</span><span class="tag">perf</span><span class="assignee">JM</span><span class="due">Jun 02</span></div>
<div class="app-issue"><span class="pri"></span><span class="id">EKO-184</span><span class="title">Workflow export to JSON</span><span class="tag feature">feature</span><span class="assignee">RK</span><span class="due">Jun 04</span></div>
<div class="app-issue"><span class="pri"></span><span class="id">EKO-179</span><span class="title">Add OAuth for HubSpot integration</span><span class="tag">api</span><span class="assignee">SL</span><span class="due">Jun 08</span></div>
<div class="app-issue"><span class="pri"></span><span class="id">EKO-176</span><span class="title">Onboarding tooltips inconsistent</span><span class="tag bug">bug</span><span class="assignee">JM</span><span class="due">Jun 10</span></div>
</main>
<aside class="app-detail">
<h4>EKO-198 &middot; Webhook retries</h4>
<div class="app-detail-row"><span>Status</span><span>In Progress</span></div>
<div class="app-detail-row"><span>Priority</span><span>Urgent</span></div>
<div class="app-detail-row"><span>Assignee</span><span>SL</span></div>
<div class="app-detail-row"><span>Cycle</span><span>Cycle 47</span></div>
<div class="app-detail-row"><span>Due</span><span>May 24</span></div>
<div class="app-detail-row"><span>Labels</span><span>bug, infra</span></div>
<div class="app-detail-row"><span>Branch</span><span>fix/webhook-retry</span></div>
<div class="app-detail-row"><span>Created</span><span>3d ago</span></div>
</aside>
</div>
</div>
</section>

<!-- TRUST -->
<div class="trust-strip">
<div class="trust-label">Trusted by the fastest growing companies in the world</div>
<div class="trust-logos">
<span>Vercel</span>
<span class="mono">Ramp</span>
<span>Loom</span>
<span class="mono">Cash App</span>
<span>Mercury</span>
<span class="mono">Retool</span>
<span>Arc</span>
</div>
</div>

<!-- STATS -->
<div class="stats-band"><div class="stats-inner">
<div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></div>

<!-- BENEFITS -->
<section class="section" id="benefits"><div class="section-inner">
<div class="section-head">
<span class="section-eyebrow">// features</span>
<h2>{{BENEFITS_HEADLINE}}</h2>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>
<div class="benefits-grid">
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div>
</div></section>

<!-- HOW -->
<section class="section" id="how"><div class="section-inner">
<div class="section-head">
<span class="section-eyebrow">// method</span>
<h2>{{HOW_HEADLINE}}</h2>
<p>{{HOW_SUBHEADLINE}}</p>
</div>
<div class="steps">
<div class="step"><div class="step-num">01 / Setup</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">02 / Build</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">03 / Ship</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>

<!-- REVIEWS -->
<section class="section" id="reviews"><div class="section-inner">
<div class="section-head">
<span class="section-eyebrow">// customers</span>
<h2>{{REVIEWS_HEADLINE}}</h2>
<p>{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-grid">
<div class="review"><div class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div></div></div>
<div class="review"><div class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div></div></div>
</div>
</div></section>

<!-- FAQ -->
<section class="section" id="faq"><div class="section-inner">
<div class="section-head">
<span class="section-eyebrow">// faq</span>
<h2>{{FAQ_HEADLINE}}</h2>
<p>{{FAQ_SUBHEADLINE}}</p>
</div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<!-- CTA -->
<section class="cta-block" id="form"><div class="cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Work email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Company URL" required>
<button type="submit">{{FOOTER_CTA}} &rarr;</button>
</form>
</div></section>

<!-- FOOTER -->
<footer class="footer"><div class="footer-inner">
<div class="footer-top">
<div class="footer-brand-block">
<a href="#" class="brand"><span class="mark">L</span> Eko</a>
<div class="footer-tag" style="margin-top:14px">A purpose-built automation system for ambitious operators. Designed and built with care.</div>
</div>
<div class="footer-col"><h4>Product</h4><ul><li><a href="#benefits">Features</a></li><li><a href="#how">Method</a></li><li><a href="#">Changelog</a></li><li><a href="#">Integrations</a></li><li><a href="#">Pricing</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#reviews">Customers</a></li><li><a href="#">Careers</a></li><li><a href="#">Brand</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#">Documentation</a></li><li><a href="#">API reference</a></li><li><a href="#faq">Support</a></li><li><a href="#">Status</a></li></ul></div>
<div class="footer-col"><h4>Connect</h4><ul><li><a href="#">Twitter</a></li><li><a href="#">GitHub</a></li><li><a href="#">YouTube</a></li><li><a href="#form">Contact</a></li></ul></div>
</div>
<div class="footer-bot">
<div>&copy; {{YEAR}} Eko AI Inc. &nbsp; &middot; &nbsp; <a href="#">Privacy</a> &nbsp; &middot; &nbsp; <a href="#">Terms</a> &nbsp; &middot; &nbsp; <a href="#">Security</a></div>
<div>contact@biz.ekoaiautomation.com</div>
</div>
</div></footer>
__FORM_SUBMIT_JS__
</body></html>
"""


# Continued in next file part — templates 5-10


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 5: AIRBNB WARM — Coral red, rounded corners, friendly hospitality vibe
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_AIRBNB_WARM = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--coral:#FF385C;--coral-hover:#E31C5F;--coral-dark:#BD1E59;--text:#222222;--muted:#717171;--bg:#fff;--surface:#f7f7f7;--border:#ebebeb;--border-hi:#dddddd;--star:#FF385C;--success:#008A05}
html{scroll-behavior:smooth;background:#fff;min-height:100vh}
body{font-family:"Cereal","Circular","Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#fff!important;color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh}
a{color:var(--text);text-decoration:none}
img{max-width:100%;display:block}

/* TOP NAV */
.nav{position:sticky;top:0;z-index:200;background:#fff;border-bottom:1px solid var(--border)}
.nav-inner{max-width:1760px;margin:0 auto;padding:18px 40px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.logo{display:flex;align-items:center;gap:8px;font-size:22px;font-weight:800;color:var(--coral);letter-spacing:-.6px;flex-shrink:0}
.logo svg{width:30px;height:32px;display:block}
.logo-text{font-family:inherit;font-weight:800;font-size:21px;letter-spacing:-.6px}
.nav-center{display:flex;gap:0;align-items:center}
.nav-tab{position:relative;padding:14px 16px;font-size:15px;font-weight:500;color:var(--muted);cursor:pointer;transition:color .15s}
.nav-tab:hover{color:var(--text)}
.nav-tab.active{color:var(--text);font-weight:600}
.nav-tab.active::after{content:'';position:absolute;left:50%;bottom:-1px;transform:translateX(-50%);width:36px;height:2px;background:var(--text);border-radius:1px}
.nav-right{display:flex;align-items:center;gap:4px;flex-shrink:0}
.nav-host{padding:12px 14px;border-radius:24px;font-size:14px;font-weight:600;color:var(--text);transition:background .15s}
.nav-host:hover{background:var(--surface)}
.nav-globe{padding:12px;border-radius:50%;font-size:16px;color:var(--text);transition:background .15s;cursor:pointer;border:none;background:transparent}
.nav-globe:hover{background:var(--surface)}
.nav-profile{display:flex;align-items:center;gap:12px;padding:5px 6px 5px 12px;border:1px solid var(--border);border-radius:24px;cursor:pointer;transition:box-shadow .15s;background:#fff}
.nav-profile:hover{box-shadow:0 2px 8px rgba(0,0,0,.18)}
.nav-profile .lines{display:flex;flex-direction:column;gap:3px}
.nav-profile .lines span{width:14px;height:2px;background:var(--text);border-radius:2px}
.nav-profile .avatar{width:30px;height:30px;border-radius:50%;background:var(--muted);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px}

/* SEARCH PILL (separate row, Airbnb style) */
.search-row{background:#fff;border-bottom:1px solid var(--border);padding:8px 40px 16px;display:flex;justify-content:center}
.search-pill{display:flex;align-items:stretch;background:#fff;border:1px solid var(--border);border-radius:40px;box-shadow:0 1px 2px rgba(0,0,0,.08),0 4px 12px rgba(0,0,0,.05);overflow:hidden;max-width:850px;width:100%;transition:box-shadow .2s}
.search-pill:hover{box-shadow:0 2px 6px rgba(0,0,0,.1),0 6px 20px rgba(0,0,0,.07)}
.sp-cell{padding:14px 24px;cursor:pointer;border-right:1px solid var(--border);flex:1;min-width:0;transition:background .15s;border-radius:32px}
.sp-cell:hover{background:#ebebeb}
.sp-cell:last-of-type{border-right:none}
.sp-label{font-size:12px;font-weight:700;color:var(--text);letter-spacing:.2px;display:block;margin-bottom:2px}
.sp-value{font-size:14px;color:var(--muted);font-weight:400;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sp-submit{display:flex;align-items:center;padding:7px 7px 7px 18px}
.sp-btn{width:48px;height:48px;border-radius:50%;background:var(--coral);color:#fff;border:none;display:flex;align-items:center;justify-content:center;font-size:16px;cursor:pointer;transition:background .15s,width .25s ease}
.sp-btn:hover{background:var(--coral-hover)}
.sp-btn::before{content:'\01F50D';font-size:14px}

/* CATEGORY STRIP */
.cat-strip{background:#fff;border-bottom:1px solid var(--border);overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:8px 0}
.cat-strip::-webkit-scrollbar{display:none}
.cat-inner{max-width:1760px;margin:0 auto;padding:8px 40px;display:flex;gap:36px;align-items:flex-end;width:max-content;min-width:100%}
.cat{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:8px;color:var(--muted);font-size:12px;font-weight:600;cursor:pointer;padding:8px 0 14px;border-bottom:2px solid transparent;flex-shrink:0;opacity:.7;transition:color .15s,border-color .15s,opacity .15s;text-align:center;min-width:56px}
.cat:hover{color:var(--text);opacity:1;border-bottom-color:#dddddd}
.cat.active{color:var(--text);border-bottom-color:var(--text);opacity:1}
.cat-icon{font-size:24px;line-height:1;filter:grayscale(20%)}
.cat-label{font-size:12px;line-height:1.2;white-space:nowrap}

/* HERO */
.hero{padding:48px 40px 8px;text-align:center;background:#fff}
.hero-inner{max-width:1024px;margin:0 auto}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:24px;background:#fff;border:1px solid var(--border);color:var(--text);font-size:13px;font-weight:600;margin-bottom:24px;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.badge::before{content:'\2605';color:var(--coral);font-size:14px}
h1{font-size:clamp(36px,5vw,60px);font-weight:700;line-height:1.05;letter-spacing:-1.6px;margin-bottom:18px;color:var(--text)}
.hero p.sub{font-size:clamp(16px,2vw,20px);color:var(--muted);max-width:600px;margin:0 auto 32px;line-height:1.45;font-weight:400}

/* BOOKING CARD (search-bar style) */
.booking-card{max-width:850px;margin:0 auto;background:#fff;border-radius:32px;border:1px solid var(--border);box-shadow:0 8px 28px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.04);display:flex;align-items:stretch;text-align:left;transition:box-shadow .2s}
.booking-card:hover{box-shadow:0 12px 36px rgba(0,0,0,.12),0 1px 2px rgba(0,0,0,.04)}
.bc-cell{flex:1;padding:14px 24px;border-right:1px solid var(--border);min-width:0;cursor:pointer;border-radius:32px;transition:background .15s}
.bc-cell:hover{background:#ebebeb}
.bc-cell:last-of-type{border-right:none}
.bc-cell label{display:block;font-size:12px;font-weight:700;color:var(--text);letter-spacing:.2px;margin-bottom:4px;cursor:pointer}
.bc-cell input{width:100%;border:none;outline:none;background:transparent;font-size:14px;font-family:inherit;color:var(--text)}
.bc-cell input::placeholder{color:var(--muted)}
.bc-submit{display:flex;align-items:center;padding:7px}
.bc-btn{padding:0;width:48px;height:48px;border:none;border-radius:50%;background:var(--coral);color:#fff;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-weight:700;transition:background .15s,width .25s,padding .25s ease}
.bc-btn:hover{background:var(--coral-hover);width:auto;padding:0 18px}
.bc-btn::before{content:'\01F50D';margin-right:0;transition:margin .25s ease}
.bc-btn:hover::before{margin-right:8px}
.bc-btn .label{display:none;font-size:14px;font-weight:600;letter-spacing:.2px}
.bc-btn:hover .label{display:inline}

.hero-meta{margin-top:24px;font-size:14px;color:var(--muted);font-weight:400}
.hero-meta::before{content:'\2605 ';color:var(--coral)}

/* STATS strip */
.stats{display:flex;justify-content:center;gap:64px;margin:48px auto 0;max-width:920px;flex-wrap:wrap;padding:32px 24px;border-top:1px solid var(--border)}
.stat{text-align:center;min-width:140px}
.stat-num{font-size:clamp(36px,4vw,48px);font-weight:800;color:var(--coral);letter-spacing:-1.2px;line-height:1}
.stat-label{font-size:14px;color:var(--muted);margin-top:8px;font-weight:500}

/* SECTION layout */
.section{padding:72px 40px;max-width:1760px;margin:0 auto;background:#fff}
.section-alt{background:#fff;max-width:none;border-top:1px solid var(--border)}
.section-alt-inner{max-width:1760px;margin:0 auto;padding:72px 40px}
.section-header{margin-bottom:36px}
.section-header h2{font-size:clamp(22px,2.6vw,32px);font-weight:600;letter-spacing:-.6px;margin-bottom:8px;color:var(--text)}
.section-header p{color:var(--muted);font-size:15px;max-width:640px;line-height:1.5;font-weight:400}

/* INSPIRATION CARDS (Airbnb listing style) */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px 24px}
.feature{background:transparent;cursor:pointer;border:none;padding:0;transition:transform .2s}
.feature:hover{transform:translateY(-2px)}
.feature-media{aspect-ratio:1/1;border-radius:24px;background:linear-gradient(135deg,#FFE5EA 0%,#FFB3C1 100%);position:relative;overflow:hidden;margin-bottom:12px;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.feature:nth-child(2) .feature-media{background:linear-gradient(135deg,#E8F4E5 0%,#A4D8A0 100%)}
.feature:nth-child(3) .feature-media{background:linear-gradient(135deg,#FFF0D6 0%,#FFD082 100%)}
.feature:nth-child(4) .feature-media{background:linear-gradient(135deg,#DDEEFF 0%,#88B9F0 100%)}
.feature-icon{font-size:72px;line-height:1;filter:drop-shadow(0 6px 12px rgba(0,0,0,.18))}
.feature-heart{position:absolute;top:14px;right:14px;width:24px;height:24px;color:rgba(255,255,255,.95);text-shadow:0 1px 2px rgba(0,0,0,.4);font-size:22px;line-height:1;cursor:pointer}
.feature-heart::before{content:'\2661'}
.feature-meta{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;padding:0 4px}
.feature-title-row{flex:1;min-width:0}
.feature h3{font-size:15px;font-weight:600;color:var(--text);letter-spacing:-.1px;line-height:1.3;margin-bottom:2px;display:flex;justify-content:space-between;align-items:center;gap:8px}
.feature-rating{font-size:14px;color:var(--text);font-weight:500;display:inline-flex;align-items:center;gap:4px;flex-shrink:0}
.feature-rating::before{content:'\2605';color:var(--text);font-size:13px}
.feature p{color:var(--muted);font-size:14px;line-height:1.4;font-weight:400;margin-top:2px}
.feature-price{margin-top:8px;font-size:14px;color:var(--text);font-weight:600;padding:0 4px}
.feature-price span{font-weight:400;color:var(--muted)}

/* "LIVE ANYWHERE" big cards */
.live-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:8px}
.live-card{aspect-ratio:1.1/1;border-radius:16px;overflow:hidden;position:relative;cursor:pointer;background:linear-gradient(180deg,#FFC1CB 0%,#FF7A87 100%);transition:transform .2s,box-shadow .2s;box-shadow:0 2px 8px rgba(0,0,0,.08)}
.live-card:nth-child(2){background:linear-gradient(180deg,#C5E1A5 0%,#7CB342 100%)}
.live-card:nth-child(3){background:linear-gradient(180deg,#BBDEFB 0%,#42A5F5 100%)}
.live-card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(0,0,0,.18)}
.live-icon{position:absolute;top:24px;right:24px;font-size:64px;opacity:.4;filter:drop-shadow(0 4px 8px rgba(0,0,0,.2))}
.live-label{position:absolute;left:24px;bottom:24px;color:#fff;font-size:24px;font-weight:700;text-shadow:0 2px 6px rgba(0,0,0,.35);letter-spacing:-.4px;line-height:1.1}

/* STEPS */
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:48px;max-width:1100px;margin:0 auto}
.step{text-align:center;padding:16px}
.step-circle{width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#FF385C 0%,#E61E4D 100%);color:#fff;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:800;margin:0 auto 20px;box-shadow:0 8px 20px rgba(255,56,92,.28)}
.step h3{font-size:18px;font-weight:600;margin-bottom:8px;color:var(--text);letter-spacing:-.2px}
.step p{color:var(--muted);font-size:15px;line-height:1.5}

/* REVIEWS — Airbnb style */
.reviews-header-row{display:flex;align-items:center;flex-wrap:wrap;gap:14px;margin-bottom:28px}
.reviews-rating{display:flex;align-items:center;gap:8px;font-size:22px;font-weight:700;color:var(--text)}
.reviews-rating .star{color:var(--text);font-size:22px}
.reviews-rating .dot{color:var(--muted);font-size:14px;font-weight:500;margin:0 4px}
.reviews-rating .ct{font-weight:500;text-decoration:underline;cursor:pointer}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:32px 48px}
.review{padding:0;background:transparent;border:none}
.review-stars{color:var(--text);font-size:11px;margin-bottom:14px;letter-spacing:1px;display:flex;align-items:center;gap:10px}
.review-stars .stars::before{content:'\2605\2605\2605\2605\2605';color:var(--text);font-size:11px;letter-spacing:1.5px}
.review-stars .date{color:var(--text);font-weight:500;font-size:13px;border-left:1px solid var(--border-hi);padding-left:10px}
.review-quote{font-size:16px;color:var(--text);margin-bottom:18px;line-height:1.55;font-weight:400;font-style:normal}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,var(--coral),var(--coral-dark));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;flex-shrink:0}
.review-name{font-weight:600;font-size:14px;display:block;color:var(--text)}
.review-role{font-size:13px;color:var(--muted);display:block;margin-top:2px}

/* FAQ */
.faq{max-width:920px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--border)}
.faq-item:first-child{border-top:1px solid var(--border)}
.faq-q{width:100%;padding:24px 0;background:none;border:none;text-align:left;font-size:18px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit;letter-spacing:-.2px;transition:color .15s;gap:24px}
.faq-q:hover{color:var(--text);opacity:.7}
.faq-q::after{content:'\02C5';font-size:24px;color:var(--text);transition:transform .3s;flex-shrink:0;line-height:.5}
.faq-item.active .faq-q::after{transform:rotate(180deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;line-height:1.6}
.faq-item.active .faq-a{max-height:380px;padding:0 0 28px}

/* FOOTER CTA */
.footer-cta{padding:88px 40px;background:linear-gradient(135deg,#FF385C 0%,#E61E4D 50%,#BD1E59 100%);text-align:center;color:#fff}
.footer-cta-inner{max-width:780px;margin:0 auto}
.footer-cta h2{font-size:clamp(32px,4vw,48px);font-weight:700;letter-spacing:-1.2px;margin-bottom:16px;color:#fff;line-height:1.1}
.footer-cta p{font-size:18px;color:rgba(255,255,255,.95);margin-bottom:32px;max-width:560px;margin-left:auto;margin-right:auto;line-height:1.5}
.cta-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;max-width:680px;margin:0 auto;background:#fff;padding:14px;border-radius:32px;box-shadow:0 12px 40px rgba(0,0,0,.22)}
.cta-form input{padding:14px 18px;border:1px solid var(--border);border-radius:24px;font-size:14px;font-family:inherit;outline:none;background:#fff;color:var(--text);transition:border-color .15s,box-shadow .15s}
.cta-form input::placeholder{color:var(--muted)}
.cta-form input:focus{border-color:var(--coral);box-shadow:0 0 0 2px rgba(255,56,92,.18)}
.cta-form button{grid-column:1/-1;padding:16px 28px;border:none;border-radius:24px;background:linear-gradient(135deg,#FF385C 0%,#BD1E59 100%);color:#fff;font-size:15px;font-weight:700;cursor:pointer;letter-spacing:.2px;transition:filter .15s,transform .15s}
.cta-form button:hover{filter:brightness(.96);transform:translateY(-1px)}

/* FOOTER */
.footer{padding:48px 40px 24px;background:var(--surface);color:var(--text);border-top:1px solid var(--border)}
.footer-cols{max-width:1760px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;padding-bottom:32px;border-bottom:1px solid var(--border-hi)}
.footer-col h4{font-size:14px;font-weight:700;margin-bottom:16px;color:var(--text)}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.footer-col a{font-size:14px;color:var(--text);font-weight:400}
.footer-col a:hover{text-decoration:underline}
.footer-bottom{max-width:1760px;margin:0 auto;padding-top:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;font-size:14px;color:var(--text)}
.footer-bottom-left{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.footer-bottom-left .sep{color:var(--muted)}
.footer-bottom-right{display:flex;gap:20px;flex-wrap:wrap;align-items:center}
.footer-bottom-right span{display:flex;align-items:center;gap:6px;font-weight:600;cursor:pointer}
.footer-bottom-right span:hover{text-decoration:underline}

@media(max-width:1024px){.nav-center{display:none}}
@media(max-width:900px){.search-pill{flex-wrap:wrap}.sp-cell{flex:1 1 50%;border-right:none;border-bottom:1px solid var(--border)}.booking-card{flex-wrap:wrap}.bc-cell{flex:1 1 50%;border-right:none;border-bottom:1px solid var(--border)}}
@media(max-width:640px){.nav-inner{padding:14px 20px;gap:8px}.nav-host,.nav-globe{display:none}.search-row{padding:8px 16px 12px}.cat-inner{gap:24px;padding:8px 20px}.hero{padding:32px 20px 8px}.section,.section-alt-inner{padding:48px 20px}.footer-cta,.footer{padding-left:20px;padding-right:20px}.footer-cta{padding-top:64px;padding-bottom:64px}.features-grid,.reviews-grid,.steps-grid,.live-grid{grid-template-columns:1fr}.stats{gap:32px;padding:24px 16px}}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="logo">
<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="#FF385C" d="M16 1C7.7 1 1 7.7 1 16s6.7 15 15 15 15-6.7 15-15S24.3 1 16 1zm6.3 22.8c-.5.4-1.2.4-1.7-.1l-3.9-3.9c-.6.4-1.3.6-2 .6-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5c0 .8-.3 1.5-.7 2.1l3.8 3.8c.5.5.5 1.2.1 1.7z"/></svg>
<span class="logo-text">eko</span>
</a>
<div class="nav-center">
<div class="nav-tab active">Stays</div>
<div class="nav-tab">Experiences</div>
<div class="nav-tab">Online Experiences</div>
</div>
<div class="nav-right">
<a href="#form" class="nav-host">Become a host</a>
<button class="nav-globe" type="button" aria-label="Language">&#127760;</button>
<div class="nav-profile" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})"><div class="lines"><span></span><span></span><span></span></div><div class="avatar">E</div></div>
</div>
</div></nav>

<div class="search-row">
<div class="search-pill" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">
<div class="sp-cell"><span class="sp-label">Where</span><div class="sp-value">Search destinations</div></div>
<div class="sp-cell"><span class="sp-label">Check in</span><div class="sp-value">Add dates</div></div>
<div class="sp-cell"><span class="sp-label">Check out</span><div class="sp-value">Add dates</div></div>
<div class="sp-cell"><span class="sp-label">Who</span><div class="sp-value">Add guests</div></div>
<div class="sp-submit"><button class="sp-btn" type="button" aria-label="Search"></button></div>
</div>
</div>

<div class="cat-strip"><div class="cat-inner">
<div class="cat active"><span class="cat-icon">&#127968;</span><span class="cat-label">Featured</span></div>
<div class="cat"><span class="cat-icon">&#127958;</span><span class="cat-label">Beachfront</span></div>
<div class="cat"><span class="cat-icon">&#127956;</span><span class="cat-label">Mountain</span></div>
<div class="cat"><span class="cat-icon">&#128561;</span><span class="cat-label">OMG!</span></div>
<div class="cat"><span class="cat-icon">&#127795;</span><span class="cat-label">Treehouses</span></div>
<div class="cat"><span class="cat-icon">&#127957;</span><span class="cat-label">Cabins</span></div>
<div class="cat"><span class="cat-icon">&#127963;</span><span class="cat-label">Mansions</span></div>
<div class="cat"><span class="cat-icon">&#127984;</span><span class="cat-label">Castles</span></div>
<div class="cat"><span class="cat-icon">&#128293;</span><span class="cat-label">Trending</span></div>
<div class="cat"><span class="cat-icon">&#128507;</span><span class="cat-label">Off-the-grid</span></div>
<div class="cat"><span class="cat-icon">&#127946;</span><span class="cat-label">Pools</span></div>
<div class="cat"><span class="cat-icon">&#9968;</span><span class="cat-label">Skiing</span></div>
</div></div>

<section class="hero"><div class="hero-inner">
<div class="badge">{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="booking-card">
<div class="bc-cell"><label>Where</label><input type="text" placeholder="Search destinations" readonly></div>
<div class="bc-cell"><label>Check in</label><input type="text" placeholder="Add dates" readonly></div>
<div class="bc-cell"><label>Check out</label><input type="text" placeholder="Add dates" readonly></div>
<div class="bc-cell"><label>Who</label><input type="text" placeholder="Add guests" readonly></div>
<div class="bc-submit"><button class="bc-btn" type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})"><span class="label">{{CTA_BUTTON}}</span></button></div>
</div>
<div class="hero-meta">Superhost &middot; 4.92 average rating &middot; 12,439 verified reviews</div>
<div class="stats">
<div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</div></section>

<section class="section" id="benefits">
<div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature">
<div class="feature-media"><span class="feature-icon">{{BENEFIT_1_ICON}}</span><span class="feature-heart" aria-hidden="true"></span></div>
<div class="feature-meta"><div class="feature-title-row"><h3>{{BENEFIT_1_TITLE}}<span class="feature-rating">4.97</span></h3><p>{{BENEFIT_1_DESC}}</p></div></div>
<div class="feature-price">From $129 <span>/ night</span></div>
</div>
<div class="feature">
<div class="feature-media"><span class="feature-icon">{{BENEFIT_2_ICON}}</span><span class="feature-heart" aria-hidden="true"></span></div>
<div class="feature-meta"><div class="feature-title-row"><h3>{{BENEFIT_2_TITLE}}<span class="feature-rating">4.91</span></h3><p>{{BENEFIT_2_DESC}}</p></div></div>
<div class="feature-price">From $184 <span>/ night</span></div>
</div>
<div class="feature">
<div class="feature-media"><span class="feature-icon">{{BENEFIT_3_ICON}}</span><span class="feature-heart" aria-hidden="true"></span></div>
<div class="feature-meta"><div class="feature-title-row"><h3>{{BENEFIT_3_TITLE}}<span class="feature-rating">4.95</span></h3><p>{{BENEFIT_3_DESC}}</p></div></div>
<div class="feature-price">From $212 <span>/ night</span></div>
</div>
<div class="feature">
<div class="feature-media"><span class="feature-icon">{{BENEFIT_4_ICON}}</span><span class="feature-heart" aria-hidden="true"></span></div>
<div class="feature-meta"><div class="feature-title-row"><h3>{{BENEFIT_4_TITLE}}<span class="feature-rating">4.88</span></h3><p>{{BENEFIT_4_DESC}}</p></div></div>
<div class="feature-price">From $98 <span>/ night</span></div>
</div>
</div>
</section>

<section class="section-alt"><div class="section-alt-inner" id="how">
<div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="live-grid">
<div class="live-card"><span class="live-icon">&#127958;</span><span class="live-label">Outdoor<br>getaways</span></div>
<div class="live-card"><span class="live-icon">&#127968;</span><span class="live-label">Unique<br>stays</span></div>
<div class="live-card"><span class="live-icon">&#127757;</span><span class="live-label">Entire<br>homes</span></div>
</div>
<div class="steps-grid" style="margin-top:64px">
<div class="step"><div class="step-circle">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-circle">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-circle">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>

<section class="section" id="reviews">
<div class="reviews-header-row">
<div style="flex:1;min-width:240px">
<h2 style="font-size:clamp(22px,2.6vw,32px);font-weight:600;letter-spacing:-.6px;color:var(--text)">{{REVIEWS_HEADLINE}}</h2>
<p style="color:var(--muted);font-size:15px;margin-top:6px;line-height:1.5">{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-rating"><span class="star">&#9733;</span>4.92 <span class="dot">&middot;</span> <span class="ct">12,439 reviews</span></div>
</div>
<div class="reviews-grid">
<div class="review"><div class="review-stars"><span class="stars"></span><span class="date">May 2026</span></div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars"><span class="stars"></span><span class="date">Apr 2026</span></div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div>
</div>
</section>

<section class="section-alt"><div class="section-alt-inner" id="faq">
<div class="section-header" style="text-align:center;max-width:780px;margin-left:auto;margin-right:auto"><h2>{{FAQ_HEADLINE}}</h2><p style="margin:0 auto">{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<section class="footer-cta" id="form"><div class="footer-cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div></section>

<footer class="footer">
<div class="footer-cols">
<div class="footer-col"><h4>Support</h4><ul><li><a href="#">Help Center</a></li><li><a href="#">AirCover</a></li><li><a href="#">Anti-discrimination</a></li><li><a href="#">Disability support</a></li><li><a href="#">Cancellation options</a></li><li><a href="#">Report neighborhood concern</a></li></ul></div>
<div class="footer-col"><h4>Hosting</h4><ul><li><a href="#">Eko your home</a></li><li><a href="#">AirCover for Hosts</a></li><li><a href="#">Hosting resources</a></li><li><a href="#">Community forum</a></li><li><a href="#">Hosting responsibly</a></li><li><a href="#">Eko-friendly tools</a></li></ul></div>
<div class="footer-col"><h4>Eko</h4><ul><li><a href="#">Newsroom</a></li><li><a href="#">New features</a></li><li><a href="#">Careers</a></li><li><a href="#">Investors</a></li><li><a href="#">Gift cards</a></li><li><a href="#">Eko.org emergency stays</a></li></ul></div>
</div>
<div class="footer-bottom">
<div class="footer-bottom-left">&copy; {{YEAR}} eko, Inc. <span class="sep">&middot;</span> <a href="#">Privacy</a> <span class="sep">&middot;</span> <a href="#">Terms</a> <span class="sep">&middot;</span> <a href="#">Sitemap</a></div>
<div class="footer-bottom-right"><span>&#127760; English (US)</span><span>$ USD</span></div>
</div>
</footer>
__FORM_SUBMIT_JS__
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 6: NOTION CLEAN — Off-white, serif, playful, blocks, soft shadows
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_NOTION_CLEAN = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--cream:#f7f6f3;--cream-2:#f1f1ef;--text:#191919;--ink:#37352f;--muted:#787774;--muted-2:#9b9a97;--blue:#2eaadc;--red:#e03e3e;--orange:#d9730d;--green:#0f7b6c;--purple:#9065b0;--pink:#cb6bc0;--border:#ebebeb;--border-soft:#f1f1ef}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:'Inter','Segoe UI','Helvetica Neue',Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;font-feature-settings:'ss01','cv11';min-height:100vh}
.serif{font-family:'Lyon','Lyon Display','Charter','Iowan Old Style','Apple Garamond','Baskerville','Times New Roman',Georgia,serif;font-feature-settings:'liga','dlig'}
a{color:var(--text);text-decoration:none}

/* ── NAV ── */
.nav{position:sticky;top:0;z-index:9999;background:rgba(255,255,255,.97);backdrop-filter:saturate(180%) blur(10px);border-bottom:1px solid var(--border-soft)}
.nav-inner{max-width:1280px;margin:0 auto;padding:0 32px;height:64px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.logo{display:flex;align-items:center;gap:8px;font-family:'Inter',sans-serif;font-size:17px;font-weight:600;color:var(--text);letter-spacing:-.01em}
.logo .glyph{width:22px;height:22px;background:var(--text);color:#fff;border-radius:4px;font-family:'Inter',sans-serif;font-weight:900;font-size:14px;display:inline-flex;align-items:center;justify-content:center;letter-spacing:0}
.nav-links{display:flex;gap:0;list-style:none;flex:1;justify-content:center}
.nav-links li{padding:0 6px}
.nav-links a{color:var(--text);font-size:14px;font-weight:500;padding:8px 12px;border-radius:6px;transition:background .15s,opacity .15s;display:inline-flex;align-items:center;gap:4px}
.nav-links a::after{content:'';display:inline-block}
.nav-links a.with-chev::after{content:'⌄';font-size:12px;margin-left:2px;opacity:.6;font-weight:600}
.nav-links a:hover{background:var(--cream)}
.nav-utility{display:flex;align-items:center;gap:6px}
.nav-utility .link{font-size:14px;font-weight:500;color:var(--text);padding:8px 12px;border-radius:6px;transition:background .15s}
.nav-utility .link:hover{background:var(--cream)}
.nav-cta{padding:8px 16px;border-radius:6px;background:var(--text);color:#fff!important;font-size:14px;font-weight:600;border:1px solid var(--text);transition:background .15s,transform .1s}
.nav-cta:hover{background:#000;transform:translateY(-1px)}

/* ── HERO ── */
.hero{padding:88px 32px 48px;max-width:1100px;margin:0 auto;text-align:center}
.hero-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:6px;background:var(--cream);border:1px solid var(--border);color:var(--text);font-size:13.5px;font-weight:500;margin-bottom:36px;font-family:'Inter',sans-serif}
.hero-badge .dot{width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block}
.hero h1{font-family:'Lyon','Lyon Display','Charter','Iowan Old Style','Baskerville','Georgia',serif;font-size:clamp(48px,7vw,96px);font-weight:700;line-height:.95;letter-spacing:-3px;margin:0 auto 28px;max-width:1000px;color:var(--text)}
.hero h1 em{font-style:italic;font-weight:400;color:var(--ink)}
.hero .sub{font-family:'Inter',sans-serif;font-size:clamp(18px,1.4vw,21px);color:var(--muted);max-width:660px;margin:0 auto 36px;line-height:1.45;font-weight:400}
.hero-ctas{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:18px}
.btn-primary{display:inline-flex;align-items:center;justify-content:center;padding:13px 24px;border-radius:6px;background:var(--text);color:#fff!important;font-family:'Inter',sans-serif;font-weight:600;font-size:15px;border:1px solid var(--text);transition:background .15s,transform .1s;cursor:pointer}
.btn-primary:hover{background:#000;transform:translateY(-1px)}
.btn-outline{display:inline-flex;align-items:center;justify-content:center;padding:13px 24px;border-radius:6px;background:#fff;color:var(--text)!important;font-family:'Inter',sans-serif;font-weight:600;font-size:15px;border:1px solid var(--border);transition:background .15s,border-color .15s;cursor:pointer}
.btn-outline:hover{background:var(--cream);border-color:var(--muted-2)}
.hero-meta{font-family:'Inter',sans-serif;font-size:13.5px;color:var(--muted);margin-top:8px}

/* ── MOCK NOTION DOCUMENT SCREENSHOT ── */
.hero-screenshot{margin:56px auto 0;max-width:1080px;border-radius:12px;border:1px solid var(--border);background:#fff;overflow:hidden;box-shadow:0 24px 60px rgba(15,15,15,.08),0 4px 12px rgba(15,15,15,.04)}
.hs-bar{display:flex;align-items:center;gap:8px;padding:11px 14px;border-bottom:1px solid var(--border-soft);background:var(--cream)}
.hs-bar .d{width:12px;height:12px;border-radius:50%;display:inline-block}
.hs-bar .d.r{background:#fc615d}
.hs-bar .d.y{background:#fdbc40}
.hs-bar .d.g{background:#34c84a}
.hs-bar .t{margin-left:14px;font-size:12px;color:var(--muted);font-family:'Inter',sans-serif}
.hs-body{display:grid;grid-template-columns:220px 1fr;min-height:380px;background:#fff;text-align:left}

/* sidebar */
.hs-sb{background:var(--cream);padding:18px 12px;border-right:1px solid var(--border-soft);font-family:'Inter',sans-serif;font-size:13px;color:var(--ink);display:flex;flex-direction:column;gap:2px}
.hs-sb-user{display:flex;align-items:center;gap:8px;padding:6px 8px;font-weight:600;margin-bottom:12px}
.hs-sb-user .av{width:20px;height:20px;border-radius:4px;background:linear-gradient(135deg,#cb6bc0,#9065b0);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700}
.hs-sb-section{font-size:11.5px;color:var(--muted-2);font-weight:600;text-transform:uppercase;letter-spacing:.04em;padding:14px 8px 6px}
.hs-sb-item{display:flex;align-items:center;gap:8px;padding:5px 8px;border-radius:4px;cursor:default;color:var(--ink)}
.hs-sb-item:hover{background:var(--cream-2)}
.hs-sb-item.active{background:rgba(35,131,226,.07);color:var(--text);font-weight:500}
.hs-sb-item .ic{width:18px;text-align:center;font-size:13px}

/* main doc area */
.hs-doc{padding:28px 40px 36px;background:#fff;display:flex;flex-direction:column;gap:10px;position:relative}
.hs-doc-emoji{font-size:32px;line-height:1;margin-bottom:8px}
.hs-h{font-family:'Lyon','Charter','Georgia',serif;font-size:36px;font-weight:700;letter-spacing:-1px;color:var(--text);line-height:1.1}
.hs-meta{font-family:'Inter',sans-serif;font-size:12.5px;color:var(--muted-2);margin-bottom:14px;display:flex;gap:12px;flex-wrap:wrap}
.hs-block{display:flex;gap:10px;align-items:flex-start;padding:4px 0;color:var(--ink);font-size:14.5px;font-family:'Inter',sans-serif;line-height:1.6}
.hs-block .b{flex-shrink:0;color:var(--muted-2);font-size:14px;margin-top:1px}
.hs-callout{display:flex;gap:12px;padding:14px 16px;border-radius:6px;background:#f8f6f2;border:1px solid #ebe6dc;color:var(--ink);font-family:'Inter',sans-serif;font-size:14px;line-height:1.55;margin-top:6px}
.hs-callout .ce{font-size:18px;line-height:1.2}
.hs-callout strong{color:var(--text);font-weight:600}

/* slash menu (Notion signature) */
.hs-slash{position:absolute;bottom:36px;left:60px;width:260px;background:#fff;border:1px solid var(--border);border-radius:8px;box-shadow:0 10px 32px rgba(15,15,15,.18),0 2px 6px rgba(15,15,15,.05);padding:6px;font-family:'Inter',sans-serif;font-size:13.5px;color:var(--ink)}
.hs-slash-h{padding:6px 10px 4px;font-size:11.5px;color:var(--muted-2);font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.hs-slash-item{display:flex;align-items:center;gap:10px;padding:6px 10px;border-radius:4px}
.hs-slash-item:first-of-type{background:var(--cream-2)}
.hs-slash-item .si{width:24px;height:24px;border-radius:4px;background:var(--cream-2);display:inline-flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0}
.hs-slash-item .sl{display:block;font-weight:500;line-height:1.15}
.hs-slash-item .ss{display:block;font-size:11.5px;color:var(--muted)}

/* ── STATS STRIP ── */
.stats{display:flex;justify-content:center;gap:96px;margin:96px auto 0;max-width:1100px;flex-wrap:wrap}
.stat{text-align:center}
.stat-num{font-family:'Lyon','Charter','Georgia',serif;font-size:52px;font-weight:700;color:var(--text);letter-spacing:-1.5px;line-height:1}
.stat-label{font-family:'Inter',sans-serif;font-size:13px;color:var(--muted);margin-top:10px;font-weight:500}

/* ── SECTIONS ── */
.section{padding:120px 32px}
.section-inner{max-width:1180px;margin:0 auto}
.section-alt{background:var(--cream)}
.section-header{text-align:center;margin-bottom:64px}
.section-eyebrow{display:block;font-family:'Inter',sans-serif;font-size:13px;font-weight:600;color:var(--green);text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px}
.section-header h2{font-family:'Lyon','Charter','Georgia',serif;font-size:clamp(34px,4.5vw,60px);font-weight:700;letter-spacing:-1.5px;line-height:1.05;margin-bottom:18px;color:var(--text)}
.section-header h2 em{font-style:italic;font-weight:400;color:var(--ink)}
.section-header p{font-family:'Inter',sans-serif;color:var(--muted);font-size:18px;max-width:620px;margin:0 auto;line-height:1.5}

/* ── SOFT BLOCKS ── */
.features-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.feature{padding:28px 26px;border-radius:10px;background:#fff;border:1px solid var(--border);transition:transform .2s,box-shadow .2s,border-color .2s;display:flex;flex-direction:column;gap:6px}
.feature:hover{transform:translateY(-2px);box-shadow:0 10px 28px rgba(15,15,15,.06);border-color:#dcdcdc}
.section-alt .feature{background:#fff}
.feature-icon{font-size:28px;line-height:1;margin-bottom:14px;display:inline-block}
.feature h3{font-family:'Lyon','Charter','Georgia',serif;font-size:20px;font-weight:700;color:var(--text);letter-spacing:-.3px;line-height:1.2;margin-bottom:4px}
.feature p{font-family:'Inter',sans-serif;color:var(--muted);font-size:14.5px;line-height:1.55}

.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.step{padding:28px 26px;border-radius:10px;background:#fff;border:1px solid var(--border);display:flex;flex-direction:column;gap:6px}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:6px;background:var(--text);color:#fff;font-family:'Inter',sans-serif;font-weight:700;font-size:13.5px;margin-bottom:14px}
.step h3{font-family:'Lyon','Charter','Georgia',serif;font-size:20px;font-weight:700;letter-spacing:-.3px;line-height:1.2;margin-bottom:4px}
.step p{font-family:'Inter',sans-serif;color:var(--muted);font-size:14.5px;line-height:1.55}

.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.review{padding:32px;border-radius:10px;background:#fff;border:1px solid var(--border);transition:box-shadow .2s}
.review:hover{box-shadow:0 10px 28px rgba(15,15,15,.06)}
.review-stars{color:#f5a623;font-size:14px;margin-bottom:16px;letter-spacing:2px}
.review-quote{font-family:'Lyon','Charter','Georgia',serif;font-size:20px;color:var(--text);margin-bottom:22px;line-height:1.4;letter-spacing:-.3px;font-weight:400}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:40px;height:40px;border-radius:6px;background:linear-gradient(135deg,var(--blue),var(--green));color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Inter',sans-serif;font-weight:700;font-size:14px}
.review-name{font-family:'Inter',sans-serif;font-weight:600;font-size:14.5px;display:block;color:var(--text)}
.review-role{font-family:'Inter',sans-serif;font-size:13px;color:var(--muted)}

.faq{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:10px}
.faq-item{border:1px solid var(--border);border-radius:10px;background:#fff;overflow:hidden;transition:box-shadow .2s,border-color .2s}
.faq-item:hover{border-color:#dcdcdc}
.faq-q{width:100%;padding:20px 22px;background:none;border:none;text-align:left;font-family:'Lyon','Charter','Georgia',serif;font-size:18px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);letter-spacing:-.3px;gap:24px;line-height:1.3}
.faq-q::after{content:'⌄';font-size:18px;color:var(--muted);transition:transform .25s;font-family:'Inter',sans-serif;flex-shrink:0;font-weight:600}
.faq-item.active .faq-q::after{transform:rotate(180deg);color:var(--text)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;font-family:'Inter',sans-serif;color:var(--muted);font-size:15px;line-height:1.6;padding:0 22px}
.faq-item.active .faq-a{max-height:320px;padding:0 22px 20px}

/* ── FOOTER CTA (form lives here) ── */
.footer-cta{padding:120px 32px;text-align:center;background:var(--cream)}
.footer-cta-inner{max-width:780px;margin:0 auto}
.footer-cta h2{font-family:'Lyon','Charter','Georgia',serif;font-size:clamp(40px,5.5vw,68px);font-weight:700;letter-spacing:-2px;margin-bottom:18px;color:var(--text);line-height:1}
.footer-cta h2 em{font-style:italic;font-weight:400}
.footer-cta p{font-family:'Inter',sans-serif;font-size:18px;color:var(--muted);max-width:580px;margin:0 auto 32px;line-height:1.5}
.cta-form{display:flex;flex-wrap:wrap;gap:8px;max-width:680px;margin:0 auto 18px;justify-content:center;padding:14px;background:#fff;border:1px solid var(--border);border-radius:10px;box-shadow:0 6px 20px rgba(15,15,15,.04)}
.cta-form input{flex:1 1 200px;padding:12px 14px;border:1px solid var(--border);border-radius:6px;background:#fff;color:var(--text);font-size:14px;font-family:inherit;outline:none;transition:border-color .15s,box-shadow .15s}
.cta-form input::placeholder{color:var(--muted-2)}
.cta-form input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(46,170,220,.16)}
.cta-form button{flex:0 0 auto;padding:12px 24px;border:none;border-radius:6px;background:var(--text);color:#fff;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit;transition:background .15s}
.cta-form button:hover{background:#000}

/* ── FOOTER: BLACK bg ── */
.footer{background:#000;color:#fff;padding:64px 32px 32px;font-family:'Inter',sans-serif}
.footer-inner{max-width:1180px;margin:0 auto}
.footer-cta-top{text-align:center;padding-bottom:48px;border-bottom:1px solid #2a2a2a;margin-bottom:48px}
.footer-cta-top a{display:inline-block;padding:11px 22px;border-radius:6px;background:#fff;color:#000!important;font-weight:600;font-size:14px;transition:background .15s}
.footer-cta-top a:hover{background:#f0f0f0}
.footer-top{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px;border-bottom:1px solid #2a2a2a}
.footer-brand{display:flex;flex-direction:column;gap:14px;max-width:260px}
.footer-brand .logo{color:#fff;font-family:'Inter',sans-serif;font-size:18px;font-weight:600}
.footer-brand .logo .glyph{background:#fff;color:#000}
.footer-brand p{color:#9a9a9a;font-size:13px;line-height:1.55}
.footer-col h4{font-size:12px;font-weight:700;color:#fff;margin-bottom:16px;text-transform:uppercase;letter-spacing:.06em}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:10px}
.footer-col a{font-size:13.5px;color:#9a9a9a;text-decoration:none;transition:color .15s}.footer-col a:hover{color:#fff;text-decoration:underline}
.footer-bottom{display:flex;justify-content:space-between;align-items:center;padding-top:32px;flex-wrap:wrap;gap:16px}
.copy{font-size:12px;color:#777}
.footer-legal{display:flex;gap:18px;font-size:12px;list-style:none}
.footer-legal a{color:#777;text-decoration:none}
.footer-legal a:hover{color:#fff}

@media(max-width:900px){.nav-links{display:none}.features-grid,.steps-grid,.reviews-grid{grid-template-columns:1fr}.stats{gap:40px}.section,.footer-cta{padding:80px 24px}.footer-top{grid-template-columns:1fr 1fr;gap:32px}.hs-body{grid-template-columns:1fr;min-height:auto}.hs-sb{display:none}.hs-doc{padding:24px 24px 32px}.hs-h{font-size:28px}.hs-slash{display:none}}
@media(max-width:640px){.nav-inner{padding:0 18px;gap:12px}.hero{padding:64px 18px 40px}.hero h1{font-size:48px;letter-spacing:-2px}.hero-ctas{flex-direction:column;align-items:stretch;max-width:340px;margin-left:auto;margin-right:auto}.btn-primary,.btn-outline{width:100%}.cta-form input,.cta-form button{flex:1 1 100%}.footer-top{grid-template-columns:1fr}.footer{padding:48px 18px 28px}.section,.footer-cta{padding:64px 18px}.section-header h2{font-size:32px;letter-spacing:-1px}}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="logo"><span class="glyph">N</span>Eko</a>
<ul class="nav-links">
<li><a href="#benefits">Eko AI</a></li>
<li><a href="#benefits" class="with-chev">Product</a></li>
<li><a href="#how">Download</a></li>
<li><a href="#how" class="with-chev">Solutions</a></li>
<li><a href="#reviews" class="with-chev">Resources</a></li>
<li><a href="#faq">Pricing</a></li>
</ul>
<div class="nav-utility">
<a href="#form" class="link">Sign in</a>
<a href="#form" class="nav-cta">Try Eko free</a>
</div>
</div></nav>

<section class="hero" id="form">
<div class="hero-badge"><span class="dot"></span>{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="hero-ctas">
<a href="#cta-form" class="btn-primary">{{CTA_BUTTON}}</a>
<a href="#how" class="btn-outline">Request demo</a>
</div>
<div class="hero-meta">Free to try. No credit card required.</div>

<div class="hero-screenshot" aria-hidden="true">
<div class="hs-bar"><span class="d r"></span><span class="d y"></span><span class="d g"></span><span class="t">eko.so / workspace / Welcome</span></div>
<div class="hs-body">
<aside class="hs-sb">
<div class="hs-sb-user"><span class="av">E</span>Eko Workspace</div>
<div class="hs-sb-item"><span class="ic">🔍</span>Search</div>
<div class="hs-sb-item"><span class="ic">🏠</span>Home</div>
<div class="hs-sb-item"><span class="ic">📥</span>Inbox</div>
<div class="hs-sb-section">Private</div>
<div class="hs-sb-item active"><span class="ic">👋</span>Welcome</div>
<div class="hs-sb-item"><span class="ic">📚</span>Reading list</div>
<div class="hs-sb-item"><span class="ic">🎯</span>Goals 2026</div>
<div class="hs-sb-section">Shared</div>
<div class="hs-sb-item"><span class="ic">🚀</span>Launch plan</div>
<div class="hs-sb-item"><span class="ic">📋</span>Tasks</div>
<div class="hs-sb-item"><span class="ic">💡</span>Ideas DB</div>
</aside>
<div class="hs-doc">
<div class="hs-doc-emoji">👋</div>
<div class="hs-h">Welcome to your workspace</div>
<div class="hs-meta">Last edited just now &middot; 3 collaborators</div>
<div class="hs-block"><span class="b">✓</span><span>Organize everything &mdash; notes, docs, projects, tasks &mdash; in one place.</span></div>
<div class="hs-block"><span class="b">✓</span><span>Drag-and-drop blocks: text, tables, databases, kanban boards, embeds.</span></div>
<div class="hs-block"><span class="b">✓</span><span>Real-time collaboration that scales from solo to your whole team.</span></div>
<div class="hs-callout"><span class="ce">💡</span><span><strong>Tip:</strong> Type <strong>/</strong> anywhere to insert any block instantly &mdash; from headings to inline databases.</span></div>
<div class="hs-slash">
<div class="hs-slash-h">Basic blocks</div>
<div class="hs-slash-item"><span class="si">¶</span><span><span class="sl">Text</span><span class="ss">Just start writing with plain text.</span></span></div>
<div class="hs-slash-item"><span class="si">H</span><span><span class="sl">Heading 1</span><span class="ss">Big section heading.</span></span></div>
<div class="hs-slash-item"><span class="si">▦</span><span><span class="sl">Table</span><span class="ss">A simple table.</span></span></div>
<div class="hs-slash-item"><span class="si">☐</span><span><span class="sl">To-do list</span><span class="ss">Track tasks with a checkbox.</span></span></div>
</div>
</div>
</div>
</div>

<div class="stats">
<div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</section>

<section class="section section-alt" id="benefits"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">Why teams choose Eko</span><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div></div></section>

<section class="section" id="how"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">Get started</span><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div></div></section>

<section class="section section-alt" id="reviews"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">Stories</span><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div>
</div></div></section>

<section class="section" id="faq"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">FAQ</span><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div></div></section>

<section class="footer-cta">
<div class="footer-cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form id="cta-form" class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Enter your email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div>
</section>

<footer class="footer">
<div class="footer-inner">
<div class="footer-cta-top"><a href="#cta-form">Get started &mdash; it's free</a></div>
<div class="footer-top">
<div class="footer-brand">
<div class="logo"><span class="glyph">N</span>Eko</div>
<p>One connected workspace for your notes, docs, projects, and team.</p>
</div>
<div class="footer-col"><h4>Product</h4><ul><li><a href="#benefits">Features</a></li><li><a href="#how">Templates</a></li><li><a href="#form">Pricing</a></li><li><a href="#">Integrations</a></li><li><a href="#">What's new</a></li></ul></div>
<div class="footer-col"><h4>Download</h4><ul><li><a href="#">iOS &amp; Android</a></li><li><a href="#">Mac &amp; Windows</a></li><li><a href="#">Calendar</a></li><li><a href="#">Web Clipper</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#faq">Help center</a></li><li><a href="#">Eko Academy</a></li><li><a href="#">Community</a></li><li><a href="#reviews">Customers</a></li><li><a href="#">Guides</a></li></ul></div>
<div class="footer-col"><h4>Eko Made Simple</h4><ul><li><a href="#">For Students</a></li><li><a href="#">For Startups</a></li><li><a href="#">For Enterprise</a></li><li><a href="#">For Personal Use</a></li></ul></div>
</div>
<div class="footer-bottom">
<div class="copy">&copy; {{YEAR}} Eko AI &middot; contact@biz.ekoaiautomation.com</div>
<ul class="footer-legal"><li><a href="#">Privacy</a></li><li><a href="#">Terms</a></li><li><a href="#">Security</a></li><li><a href="#">Cookies</a></li><li><a href="#">Contact</a></li></ul>
</div>
</div>
</footer>
__FORM_SUBMIT_JS__
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 7: TESLA BOLD — Full-bleed dark hero, minimal nav, huge CTA
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_TESLA_BOLD = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--surface:#f4f4f4;--surface-2:#ebebeb;--text:#171a20;--ink:#393c41;--muted:#5c5e62;--muted-2:#86888c;--blue:#3457b8;--blue-hover:#2c4ba0;--border:#d0d1d2}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:'Inter','Gotham','Helvetica Neue',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh;font-weight:400}
a{color:var(--text);text-decoration:none}

/* ── NAV: transparent → solid white on scroll ── */
.nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:14px 40px;display:flex;align-items:center;justify-content:space-between;background:transparent;transition:background .3s ease,box-shadow .3s ease}
.nav.scrolled{background:#fff;box-shadow:0 1px 0 rgba(0,0,0,.06)}
.nav .logo{font-size:18px;font-weight:700;color:#fff;letter-spacing:.18em;font-family:'Inter',sans-serif;transition:color .3s}
.nav.scrolled .logo{color:var(--text)}
.nav-links{display:flex;gap:0;list-style:none;flex:1;justify-content:center;flex-wrap:wrap}
.nav-links li{padding:0}
.nav-links a{color:#fff;font-size:14px;font-weight:500;padding:8px 14px;border-radius:8px;transition:background .2s,color .3s;white-space:nowrap}
.nav-links a:hover{background:rgba(255,255,255,.1)}
.nav.scrolled .nav-links a{color:var(--text)}
.nav.scrolled .nav-links a:hover{background:rgba(0,0,0,.05)}
.nav-right{display:flex;gap:0;align-items:center}
.nav-right a{color:#fff;font-size:14px;font-weight:500;padding:8px 14px;border-radius:8px;transition:background .2s,color .3s}
.nav-right a:hover{background:rgba(255,255,255,.1)}
.nav.scrolled .nav-right a{color:var(--text)}
.nav.scrolled .nav-right a:hover{background:rgba(0,0,0,.05)}

/* ── HERO: full-bleed 100vh, content anchored BOTTOM-CENTER ── */
.hero{position:relative;height:100vh;min-height:640px;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;padding:120px 24px 56px;background:linear-gradient(180deg,#1a2233 0%,#0e1726 45%,#06090f 100%);overflow:hidden;color:#fff}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 90% 55% at 50% 70%,rgba(70,100,180,.32) 0%,transparent 65%),radial-gradient(circle at 50% 100%,rgba(140,170,220,.18) 0%,transparent 45%);pointer-events:none}
.hero::after{content:'';position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:80%;max-width:1200px;height:140px;background:radial-gradient(ellipse at 50% 100%,rgba(180,200,240,.22) 0%,transparent 70%);pointer-events:none;filter:blur(20px)}
.hero-inner{position:relative;z-index:2;text-align:center;max-width:1100px;width:100%}
.badge{display:inline-block;color:rgba(255,255,255,.78);font-size:13px;font-weight:500;letter-spacing:.04em;margin-bottom:18px}
h1{font-size:clamp(40px,5.8vw,64px);font-weight:500;line-height:1.05;letter-spacing:-1px;margin-bottom:14px;color:#fff}
.hero p.sub{font-size:13px;color:rgba(255,255,255,.85);max-width:680px;margin:0 auto 36px;line-height:1.55;font-weight:400}
.hero p.sub a{color:#fff;text-decoration:underline;text-underline-offset:3px}

/* ── DUAL CTA PILLS: identical width, 18px radius (Tesla signature) ── */
.hero-cta-row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin:0 auto}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:12px 100px;border-radius:18px;font-size:14px;font-weight:500;letter-spacing:.02em;cursor:pointer;text-align:center;transition:all .15s ease;font-family:inherit}
.btn-primary{background:var(--blue);color:#fff!important;border:2px solid var(--blue)}
.btn-primary:hover{background:var(--blue-hover);border-color:var(--blue-hover)}
.btn-outline{background:rgba(255,255,255,0);color:#fff!important;border:2px solid #fff}
.btn-outline:hover{background:rgba(255,255,255,.1)}
.btn-dark{background:var(--text);color:#fff!important;border:2px solid var(--text)}
.btn-dark:hover{background:#000;border-color:#000}

.scroll-cue{position:absolute;bottom:18px;left:50%;transform:translateX(-50%);color:rgba(255,255,255,.6);font-size:11px;z-index:2}
.scroll-cue::after{content:'⌄';display:block;font-size:22px;font-weight:300;text-align:center;line-height:1;margin-top:4px;animation:bob 2s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(6px)}}

/* ── LINEUP: product grid (Model 3/Y/S/X) ── */
.lineup-section{background:#fff;padding:96px 0 80px;text-align:center}
.lineup-head{max-width:900px;margin:0 auto 48px;padding:0 24px}
.lineup-head h2{font-size:clamp(28px,3.5vw,40px);font-weight:500;letter-spacing:-.5px;color:var(--text);margin-bottom:12px}
.lineup-head p{color:var(--muted);font-size:16px;line-height:1.55}
.lineup{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1px;background:#ebebeb;max-width:1500px;margin:0 auto;border-top:1px solid #ebebeb;border-bottom:1px solid #ebebeb}
.lineup-card{background:#fff;padding:40px 24px 48px;text-align:center;display:flex;flex-direction:column;align-items:center}
.lineup-img{width:100%;height:200px;border-radius:6px;background:linear-gradient(135deg,#e8ecf2 0%,#c5cdd8 100%);margin-bottom:28px;display:flex;align-items:center;justify-content:center;font-size:54px;color:rgba(255,255,255,.7);box-shadow:inset 0 -40px 80px rgba(0,0,0,.12)}
.lineup-name{font-size:32px;font-weight:500;color:var(--text);letter-spacing:-.5px;margin-bottom:8px;line-height:1.1}
.lineup-tag{color:var(--muted);font-size:14px;margin-bottom:18px;line-height:1.4}
.lineup-tag strong{font-weight:600;color:var(--text)}
.lineup-actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;width:100%}
.lineup-actions .btn{padding:9px 0;font-size:13px;min-width:170px;flex:1 1 170px;max-width:200px;border-radius:14px}

/* ── STATS STRIP: white bg, big DARK numbers ── */
.stats-strip{background:#fff;padding:88px 40px;border-top:1px solid var(--surface-2)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:48px;max-width:1280px;margin:0 auto}
.stat{text-align:center}
.stat-num{font-size:clamp(44px,5.2vw,68px);font-weight:500;color:var(--text);letter-spacing:-1.5px;line-height:1}
.stat-label{font-size:12px;color:var(--muted);margin-top:14px;text-transform:uppercase;letter-spacing:.16em;font-weight:500}

/* ── SECTIONS (white, minimalist) ── */
.section{padding:96px 32px;background:#fff}
.section-surface{background:var(--surface)}
.section-inner{max-width:1280px;margin:0 auto;text-align:center}
.section-header{margin-bottom:64px;max-width:780px;margin-left:auto;margin-right:auto}
.section-header h2{font-size:clamp(30px,4vw,46px);font-weight:500;letter-spacing:-.5px;color:var(--text);margin-bottom:14px;line-height:1.1}
.section-header p{color:var(--muted);font-size:16px;max-width:640px;margin:0 auto;line-height:1.55}

.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:56px}
.feature{text-align:center;padding:0 12px}
.feature-icon{font-size:42px;margin-bottom:20px;line-height:1}
.feature h3{font-size:16px;font-weight:600;color:var(--text);letter-spacing:-.1px;margin-bottom:12px;line-height:1.25}
.feature p{color:var(--muted);font-size:14.5px;line-height:1.6}

.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:48px}
.step{text-align:center;padding:0 12px}
.step-num{display:inline-block;font-size:clamp(48px,6vw,72px);font-weight:500;color:var(--text);letter-spacing:-2px;line-height:1;margin-bottom:14px}
.step h3{font-size:18px;font-weight:600;color:var(--text);margin-bottom:12px;letter-spacing:-.1px;line-height:1.25}
.step p{color:var(--muted);font-size:14.5px;line-height:1.6}

/* ── REVIEWS: clean white cards, italic quote ── */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:32px}
.review{padding:36px 32px;background:#fff;border:1px solid var(--surface-2);border-radius:6px;text-align:left}
.review-stars{color:var(--text);font-size:13px;margin-bottom:18px;letter-spacing:2px;font-weight:500}
.review-quote{font-family:Georgia,'Times New Roman',serif;font-size:18px;color:var(--text);margin-bottom:24px;line-height:1.45;font-style:italic;font-weight:400}
.review-author{display:flex;align-items:center;gap:14px;font-size:13px;color:var(--muted);letter-spacing:.02em}
.review-avatar{width:40px;height:40px;border-radius:50%;background:var(--text);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:600;font-size:13px;flex-shrink:0}
.review-name{font-weight:600;color:var(--text);display:block;font-size:14px;margin-bottom:2px}
.review-role{font-size:12.5px;color:var(--muted)}

/* ── FAQ ── */
.faq{max-width:820px;margin:0 auto;text-align:left}
.faq-item{border-bottom:1px solid var(--border)}
.faq-item:first-child{border-top:1px solid var(--border)}
.faq-q{width:100%;padding:24px 8px;background:none;border:none;text-align:left;font-size:16px;font-weight:500;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit;gap:24px;line-height:1.4}
.faq-q::after{content:'+';font-size:22px;color:var(--text);transition:transform .3s;font-weight:300;flex-shrink:0;line-height:1}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:14.5px;line-height:1.65;padding:0 8px}
.faq-item.active .faq-a{max-height:320px;padding:0 8px 24px}

/* ── FOOTER CTA (still light) ── */
.footer-cta{padding:120px 32px;text-align:center;background:var(--surface)}
.footer-cta-inner{max-width:880px;margin:0 auto}
.footer-cta h2{font-size:clamp(36px,5vw,56px);font-weight:500;letter-spacing:-1px;margin-bottom:20px;color:var(--text);line-height:1.05}
.footer-cta p{font-size:17px;color:var(--muted);max-width:600px;margin:0 auto 36px;line-height:1.55}
.cta-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px;max-width:720px;margin:0 auto;padding:16px;background:#fff;border-radius:10px;border:1px solid var(--border);box-shadow:0 10px 30px rgba(0,0,0,.05)}
.cta-form input{padding:13px 16px;border:1px solid var(--border);background:#fff;color:var(--text);font-size:14px;font-family:inherit;outline:none;border-radius:6px;transition:border-color .15s,box-shadow .15s}
.cta-form input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(52,87,184,.15)}
.cta-form input::placeholder{color:var(--muted-2)}
.cta-form button{grid-column:1/-1;padding:14px 32px;border:none;background:var(--blue);color:#fff;font-size:14px;font-weight:500;cursor:pointer;letter-spacing:.02em;border-radius:18px;transition:background .15s;font-family:inherit}
.cta-form button:hover{background:var(--blue-hover)}

/* ── FOOTER: WHITE bg, small muted links, 5 columns ── */
.footer{background:#fff;padding:48px 40px 32px;border-top:1px solid var(--surface-2);color:var(--muted)}
.footer-inner{max-width:1500px;margin:0 auto}
.footer-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:24px;padding-bottom:32px}
.footer-col h4{font-size:12px;font-weight:600;color:var(--text);text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:8px}
.footer-col a{font-size:12px;color:var(--muted);font-weight:500;line-height:1.5}
.footer-col a:hover{color:var(--text);text-decoration:underline}
.footer-bottom{padding-top:24px;border-top:1px solid var(--surface-2);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px}
.footer-bottom-links{display:flex;gap:18px;flex-wrap:wrap;list-style:none}
.footer-bottom-links a{color:var(--muted);font-size:12px;font-weight:500}
.footer-bottom-links a:hover{color:var(--text)}
.copy{font-size:12px;color:var(--muted)}

@media(max-width:900px){.nav-links{display:none}}
@media(max-width:640px){.nav{padding:14px 18px}.nav-right a{padding:8px 10px;font-size:13px}.hero{padding:100px 18px 48px;min-height:560px}.hero-cta-row{flex-direction:column;align-items:stretch;width:100%;max-width:340px;margin:0 auto}.btn{padding:12px 24px;width:100%;min-width:0}.section,.footer-cta,.stats-strip,.lineup-section{padding-left:18px;padding-right:18px;padding-top:64px;padding-bottom:64px}.lineup{grid-template-columns:1fr}.lineup-card{padding:36px 20px 40px}.features-grid,.steps-grid,.reviews-grid{grid-template-columns:1fr;gap:36px}.cta-form input,.cta-form button{grid-column:1/-1}.footer{padding:36px 18px 24px}.footer-cols{grid-template-columns:1fr 1fr}.footer-bottom{flex-direction:column;text-align:center}}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav" id="nav">
<a href="#" class="logo">EKO</a>
<ul class="nav-links">
<li><a href="#benefits">Model S</a></li>
<li><a href="#benefits">Model 3</a></li>
<li><a href="#benefits">Model X</a></li>
<li><a href="#benefits">Model Y</a></li>
<li><a href="#how">Cybertruck</a></li>
<li><a href="#how">Powerwall</a></li>
<li><a href="#how">Solar Panels</a></li>
<li><a href="#reviews">Solar Roof</a></li>
<li><a href="#form">Existing Inventory</a></li>
<li><a href="#form">Used Inventory</a></li>
<li><a href="#form">Demo Drive</a></li>
</ul>
<div class="nav-right">
<a href="#form">Account</a>
<a href="#form">Menu</a>
</div>
</nav>

<section class="hero" id="top">
<div class="hero-inner">
<div class="badge">{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="hero-cta-row">
<a href="#form" class="btn btn-primary">{{CTA_BUTTON}}</a>
<a href="#benefits" class="btn btn-outline">Custom Order</a>
</div>
</div>
<div class="scroll-cue">Scroll</div>
</section>

<section class="lineup-section" id="benefits">
<div class="lineup-head">
<h2>{{BENEFITS_HEADLINE}}</h2>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>
<div class="lineup">
<div class="lineup-card">
<div class="lineup-img">{{BENEFIT_1_ICON}}</div>
<div class="lineup-name">{{BENEFIT_1_TITLE}}</div>
<div class="lineup-tag">{{BENEFIT_1_DESC}}<br><strong>$48,990</strong> After Federal Tax Credit</div>
<div class="lineup-actions">
<a href="#form" class="btn btn-primary">Custom Order</a>
<a href="#form" class="btn btn-dark">Demo Drive</a>
</div>
</div>
<div class="lineup-card">
<div class="lineup-img">{{BENEFIT_2_ICON}}</div>
<div class="lineup-name">{{BENEFIT_2_TITLE}}</div>
<div class="lineup-tag">{{BENEFIT_2_DESC}}<br><strong>$54,990</strong> After Federal Tax Credit</div>
<div class="lineup-actions">
<a href="#form" class="btn btn-primary">Custom Order</a>
<a href="#form" class="btn btn-dark">Demo Drive</a>
</div>
</div>
<div class="lineup-card">
<div class="lineup-img">{{BENEFIT_3_ICON}}</div>
<div class="lineup-name">{{BENEFIT_3_TITLE}}</div>
<div class="lineup-tag">{{BENEFIT_3_DESC}}<br><strong>$79,990</strong> After Federal Tax Credit</div>
<div class="lineup-actions">
<a href="#form" class="btn btn-primary">Custom Order</a>
<a href="#form" class="btn btn-dark">Demo Drive</a>
</div>
</div>
<div class="lineup-card">
<div class="lineup-img">{{BENEFIT_4_ICON}}</div>
<div class="lineup-name">{{BENEFIT_4_TITLE}}</div>
<div class="lineup-tag">{{BENEFIT_4_DESC}}<br><strong>$89,990</strong> After Federal Tax Credit</div>
<div class="lineup-actions">
<a href="#form" class="btn btn-primary">Custom Order</a>
<a href="#form" class="btn btn-dark">Demo Drive</a>
</div>
</div>
</div>
</section>

<div class="stats-strip">
<div class="stats">
<div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</div>

<section class="section section-surface" id="how">
<div class="section-inner">
<div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><span class="step-num">01</span><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><span class="step-num">02</span><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><span class="step-num">03</span><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div>
</section>

<section class="section" id="reviews">
<div class="section-inner">
<div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review">
<div class="review-stars">★★★★★</div>
<p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author">
<div class="review-avatar">{{REVIEW_1_INITIALS}}</div>
<div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div>
</div>
</div>
<div class="review">
<div class="review-stars">★★★★★</div>
<p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author">
<div class="review-avatar">{{REVIEW_2_INITIALS}}</div>
<div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div>
</div>
</div>
</div>
</div>
</section>

<section class="section section-surface" id="faq">
<div class="section-inner">
<div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div>
</section>

<section class="footer-cta" id="form">
<div class="footer-cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div>
</section>

<footer class="footer">
<div class="footer-inner">
<div class="footer-cols">
<div class="footer-col"><h4>Vehicles</h4><ul><li><a href="#">Model S</a></li><li><a href="#">Model 3</a></li><li><a href="#">Model X</a></li><li><a href="#">Model Y</a></li><li><a href="#">Cybertruck</a></li></ul></div>
<div class="footer-col"><h4>Energy</h4><ul><li><a href="#">Solar Roof</a></li><li><a href="#">Solar Panels</a></li><li><a href="#">Powerwall</a></li><li><a href="#">Megapack</a></li></ul></div>
<div class="footer-col"><h4>Charging</h4><ul><li><a href="#">Charging</a></li><li><a href="#">Trip Planner</a></li><li><a href="#">Supercharger</a></li><li><a href="#">Find Us</a></li></ul></div>
<div class="footer-col"><h4>Shop</h4><ul><li><a href="#">Vehicle Accessories</a></li><li><a href="#">Apparel</a></li><li><a href="#">Lifestyle</a></li><li><a href="#">Charging</a></li></ul></div>
<div class="footer-col"><h4>EKO Account</h4><ul><li><a href="#">Sign In</a></li><li><a href="#">Manage Order</a></li><li><a href="#">Refer and Earn</a></li><li><a href="mailto:contact@biz.ekoaiautomation.com">Contact</a></li></ul></div>
</div>
<div class="footer-bottom">
<div class="copy">EKO &copy; {{YEAR}} &middot; contact@biz.ekoaiautomation.com</div>
<ul class="footer-bottom-links"><li><a href="#">Privacy &amp; Legal</a></li><li><a href="#">Vehicle Recalls</a></li><li><a href="#">Locations</a></li><li><a href="#">Careers</a></li><li><a href="#">News</a></li></ul>
</div>
</div>
</footer>

<script>
(function(){var n=document.getElementById('nav');function s(){if(window.scrollY>40)n.classList.add('scrolled');else n.classList.remove('scrolled')}window.addEventListener('scroll',s,{passive:true});s();})();
</script>
__FORM_SUBMIT_JS__
</body></html>
"""



# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 8: BEST BUY RETAIL — White bg, blue+yellow, deal cards, pricing emphasis
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_BESTBUY_RETAIL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--blue:#0046BE;--blue-dark:#003494;--blue-hover:#001E73;--blue-light:#e6efff;--yellow:#FFE000;--yellow-dark:#FFD200;--red:#C9242D;--red-dark:#A41C24;--green:#0d6e2a;--green-bg:#e8f4ec;--text:#1d252c;--text-light:#2d3640;--muted:#6f7780;--bg:#fff;--surface:#f0f2f4;--surface-2:#e7eaee;--border:#d2d8df;--border-soft:#e3e7eb;--star:#FFB300}
html{scroll-behavior:smooth;background:#fff;min-height:100vh}
body{font-family:"Human BBY","Inter","Arial",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#fff!important;color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;display:block}

/* TOP UTILITY BAR */
.utility-bar{background:#1d252c;color:#fff;padding:6px 24px;font-size:12px;display:flex;align-items:center;justify-content:flex-end;gap:0}
.utility-bar .util-inner{max-width:1500px;width:100%;margin:0 auto;display:flex;align-items:center;justify-content:flex-end;gap:24px}
.utility-bar a{color:#fff;font-weight:500;display:inline-flex;align-items:center;gap:6px;font-size:12px;transition:color .15s}
.utility-bar a:hover{color:var(--yellow);text-decoration:none}
.utility-bar .pipe{color:rgba(255,255,255,.3)}

/* MAIN NAV — BLUE BAR */
.nav{background:var(--blue);padding:18px 24px;color:#fff}
.nav-inner{max-width:1500px;margin:0 auto;width:100%;display:flex;align-items:center;gap:18px}
.logo{display:flex;align-items:center;flex-shrink:0;transition:transform .15s}
.logo:hover{transform:translateY(-1px)}
.logo .tag{background:var(--yellow);color:var(--text);padding:9px 12px 9px 12px;border-radius:0;font-size:13px;font-weight:900;letter-spacing:.4px;display:inline-flex;align-items:center;gap:2px;line-height:1;position:relative;clip-path:polygon(0 0,100% 0,calc(100% - 12px) 100%,0 100%)}
.logo .tag-text{font-family:inherit;font-weight:900;letter-spacing:.6px;font-size:14px}

.search{flex:1;display:flex;align-items:stretch;max-width:760px;background:#fff;border-radius:30px;overflow:hidden;height:44px;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.search input{flex:1;padding:0 22px;border:none;outline:none;font-size:14px;font-family:inherit;color:var(--text);background:#fff}
.search input::placeholder{color:var(--muted)}
.search button{padding:0 22px;border:none;background:var(--blue);color:#fff;font-size:13px;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:8px;border-radius:0 30px 30px 0;font-family:inherit;transition:background .15s}
.search button:hover{background:var(--blue-hover)}
.search button::before{content:'\01F50D';font-size:14px}

.nav-right{display:flex;align-items:center;gap:18px;flex-shrink:0;font-size:12px;font-weight:500}
.nav-right a{color:#fff;display:flex;flex-direction:column;align-items:center;gap:3px;line-height:1.1;text-align:center;padding:4px 6px;border-radius:4px;transition:background .15s;font-weight:500}
.nav-right a:hover{background:rgba(255,255,255,.1);text-decoration:none}
.nav-icon{font-size:20px;display:block;margin-bottom:2px}
.cart-link{position:relative}
.cart-link .badge{position:absolute;top:-2px;right:-2px;background:var(--yellow);color:var(--text);font-size:10px;font-weight:900;width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;line-height:1}

/* YELLOW SHIPPING RIBBON */
.shipping-ribbon{background:var(--yellow);color:var(--text);text-align:center;padding:8px 24px;font-size:13px;font-weight:600;letter-spacing:.1px}
.shipping-ribbon::before{content:'\1F69A  ';font-size:14px;margin-right:4px}
.shipping-ribbon strong{font-weight:900}
.shipping-ribbon a{color:var(--blue);text-decoration:underline;margin-left:6px;font-weight:700}

/* SUBNAV — white with red HOT items */
.subnav{background:#fff;border-bottom:1px solid var(--border);padding:0 24px}
.subnav-inner{max-width:1500px;margin:0 auto;display:flex;align-items:center;gap:0;overflow-x:auto;padding:10px 0;-webkit-overflow-scrolling:touch}
.subnav-inner::-webkit-scrollbar{display:none}
.subnav a{color:var(--text);font-size:13px;font-weight:700;white-space:nowrap;padding:4px 14px;border-right:1px solid var(--border);transition:color .15s}
.subnav a:first-child{padding-left:0}
.subnav a:last-child{border-right:none}
.subnav a:hover{color:var(--blue);text-decoration:none}
.subnav .hot{color:var(--red)}
.subnav .hot:hover{color:var(--red-dark)}

/* HERO — SPLIT product spotlight + deals grid */
.hero{background:linear-gradient(180deg,#fff 0%,#fafbfc 100%);padding:32px 24px 48px}
.hero-inner{max-width:1500px;margin:0 auto;display:grid;grid-template-columns:1.3fr 1fr;gap:32px;align-items:stretch}
.hero-left{background:#fff;border:1px solid var(--border);border-radius:6px;padding:36px;display:flex;flex-direction:column;gap:18px;box-shadow:0 2px 8px rgba(0,0,0,.04);position:relative}
.deal-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 12px;background:var(--yellow);color:var(--text);font-weight:900;font-size:12px;letter-spacing:.5px;text-transform:uppercase;border-radius:3px;align-self:flex-start;box-shadow:0 2px 4px rgba(0,0,0,.12)}
.deal-badge::before{content:'\26A1'}
.hero-product-row{display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:center}
.product-image{width:200px;height:200px;border-radius:6px;background:linear-gradient(135deg,#f0f2f4 0%,#e7eaee 100%);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:84px;border:1px solid var(--border);position:relative;overflow:hidden}
.product-image::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.6),transparent 60%)}
h1{font-size:clamp(28px,4vw,42px);font-weight:900;line-height:1.05;letter-spacing:-1.3px;color:var(--text);margin-bottom:8px}
h1 .accent{color:var(--blue)}
.product-name{font-size:14px;color:var(--muted);font-weight:500;margin-bottom:10px;text-transform:uppercase;letter-spacing:.5px}
.hero p.sub{font-size:15px;color:var(--text-light);line-height:1.55;margin-bottom:12px}
.rating-line{display:inline-flex;align-items:center;gap:8px;font-size:14px;color:var(--muted);margin-bottom:4px}
.rating-line .stars{color:var(--star);font-size:18px;letter-spacing:1.5px}
.rating-line .num{font-weight:700;color:var(--text)}
.rating-line a{color:var(--blue);text-decoration:underline;font-weight:500}
.price-block{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin:8px 0 4px}
.price-was{text-decoration:line-through;color:var(--red);font-size:15px;font-weight:600}
.price-now{font-size:38px;font-weight:900;color:var(--text);letter-spacing:-1.5px;line-height:1}
.price-save{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;background:var(--green-bg);color:var(--green);font-size:13px;font-weight:800;border-radius:3px;text-transform:uppercase;letter-spacing:.4px}
.cta-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:14px 28px;border-radius:4px;font-size:15px;font-weight:700;cursor:pointer;border:none;font-family:inherit;text-decoration:none;transition:all .15s;letter-spacing:.1px}
.btn-primary{background:var(--blue);color:#fff!important;flex:1;min-width:180px}
.btn-primary:hover{background:var(--blue-hover);text-decoration:none}
.btn-outline{background:#fff;color:var(--blue)!important;border:2px solid var(--blue);flex:1;min-width:180px}
.btn-outline:hover{background:var(--blue-light);text-decoration:none}

/* HERO RIGHT: Today's Top Deals mini-grid */
.hero-right{display:flex;flex-direction:column;gap:12px}
.deals-header{display:flex;justify-content:space-between;align-items:center;padding:0 4px}
.deals-header h2{font-size:18px;font-weight:900;color:var(--text);letter-spacing:-.4px}
.deals-header a{color:var(--blue);font-size:13px;font-weight:700}
.deals-mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;flex:1}
.mini-deal{background:#fff;border:1px solid var(--border);border-radius:4px;padding:14px;display:flex;flex-direction:column;gap:6px;cursor:pointer;transition:box-shadow .15s,transform .15s;position:relative}
.mini-deal:hover{box-shadow:0 4px 12px rgba(0,70,190,.12);transform:translateY(-2px)}
.mini-deal-corner{position:absolute;top:0;left:0;background:var(--yellow);color:var(--text);font-size:10px;font-weight:900;padding:3px 9px 3px 8px;letter-spacing:.4px;text-transform:uppercase;border-radius:4px 0 6px 0;line-height:1.1}
.mini-deal-img{width:100%;height:80px;border-radius:3px;background:linear-gradient(135deg,#f0f2f4,#e7eaee);display:flex;align-items:center;justify-content:center;font-size:36px;margin-top:14px}
.mini-deal-name{font-size:12px;color:var(--text);font-weight:600;line-height:1.3;min-height:32px}
.mini-deal-price{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap}
.mini-deal-price .now{color:var(--text);font-size:16px;font-weight:900}
.mini-deal-price .was{color:var(--red);text-decoration:line-through;font-size:11px;font-weight:600}

/* TRUST STRIP */
.trust-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:0;max-width:1500px;margin:0 auto 0;background:#fff;border:1px solid var(--border);border-radius:6px;overflow:hidden;margin-top:0}
.trust-wrap{padding:0 24px;background:#fff}
.trust{padding:18px 16px;text-align:center;border-right:1px solid var(--border);display:flex;flex-direction:column;align-items:center;gap:4px}
.trust:last-child{border-right:none}
.trust-icon{font-size:22px;line-height:1}
.trust-text{font-size:13px;font-weight:800;color:var(--text);line-height:1.3}
.trust-sub{font-size:11px;color:var(--muted);font-weight:500}

.stats-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:24px;max-width:1500px;margin-left:auto;margin-right:auto;padding:0 24px}
.stat-tile{padding:24px;border-radius:6px;background:#fff;border:1px solid var(--border);border-top:4px solid var(--yellow);text-align:left;box-shadow:0 2px 6px rgba(0,0,0,.04)}
.stat-num{font-size:36px;font-weight:900;color:var(--blue);letter-spacing:-1px;line-height:1}
.stat-label{font-size:12px;color:var(--muted);margin-top:6px;text-transform:uppercase;letter-spacing:.5px;font-weight:700}

/* SECTIONS */
.section{padding:56px 24px;max-width:1500px;margin:0 auto;background:#fff}
.section-alt{background:var(--surface);max-width:none}
.section-alt-inner{max-width:1500px;margin:0 auto;padding:56px 24px}
.section-header{margin-bottom:28px;text-align:left;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
.section-header-text{flex:1;min-width:240px}
.section-header h2{font-size:clamp(24px,3vw,32px);font-weight:900;letter-spacing:-1px;margin-bottom:6px;color:var(--text);line-height:1.15}
.section-header h2 .accent{color:var(--blue)}
.section-header p{color:var(--muted);font-size:15px;max-width:680px;line-height:1.5}
.section-header .see-all{color:var(--blue);font-size:13px;font-weight:700;white-space:nowrap}
.section-header .see-all:hover{text-decoration:underline}

/* DEAL CARDS — featured grid */
.deals-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.deal-card{position:relative;padding:18px;border:1px solid var(--border);border-radius:4px;background:#fff;transition:box-shadow .15s,transform .15s;display:flex;flex-direction:column;gap:6px}
.deal-card:hover{box-shadow:0 6px 18px rgba(0,70,190,.12);transform:translateY(-2px)}
.deal-corner{position:absolute;top:0;left:0;background:var(--yellow);color:var(--text);padding:5px 12px 5px 10px;font-size:11px;font-weight:900;letter-spacing:.5px;text-transform:uppercase;border-radius:4px 0 6px 0;z-index:2;line-height:1.1}
.deal-corner-red{background:var(--red);color:#fff}
.deal-icon{width:100%;height:140px;border-radius:4px;background:linear-gradient(135deg,#f0f2f4,#e7eaee);display:flex;align-items:center;justify-content:center;font-size:56px;margin:16px 0 12px;border:1px solid var(--border-soft);position:relative;overflow:hidden}
.deal-icon::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.5),transparent 60%)}
.deal-stars{color:var(--star);font-size:13px;letter-spacing:1.2px;margin-bottom:2px}
.deal-stars .ct{color:var(--muted);margin-left:4px;font-size:12px;font-weight:500}
.deal-card h3{font-size:14px;font-weight:600;color:var(--text);line-height:1.35;margin-bottom:2px}
.deal-card p{color:var(--muted);font-size:13px;line-height:1.45;flex:1;font-weight:400}
.deal-price-row{display:flex;align-items:baseline;gap:8px;margin-top:8px;flex-wrap:wrap}
.deal-was{text-decoration:line-through;color:var(--red);font-size:12px;font-weight:600}
.deal-price{color:var(--text);font-size:22px;font-weight:900;letter-spacing:-.6px;line-height:1}
.deal-save{display:inline-block;padding:2px 8px;background:var(--green-bg);color:var(--green);font-size:11px;font-weight:800;border-radius:2px;text-transform:uppercase;letter-spacing:.3px;margin-top:2px}
.deal-add{width:100%;padding:11px 16px;border:none;border-radius:4px;background:var(--blue);color:#fff;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit;letter-spacing:.2px;margin-top:10px;transition:background .15s}
.deal-add:hover{background:var(--blue-hover)}

/* STEPS */
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
.step{padding:28px;border-radius:4px;background:#fff;border:1px solid var(--border);border-top:4px solid var(--blue);position:relative;padding-top:56px}
.step:nth-child(2){border-top-color:var(--yellow)}
.step:nth-child(3){border-top-color:var(--red)}
.step-num{position:absolute;top:20px;left:20px;width:38px;height:38px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:17px}
.step:nth-child(2) .step-num{background:var(--yellow);color:var(--text)}
.step:nth-child(3) .step-num{background:var(--red)}
.step h3{font-size:17px;font-weight:700;margin-bottom:8px;color:var(--text);letter-spacing:-.2px}
.step p{color:var(--muted);font-size:14px;line-height:1.55}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}
.review{padding:22px;border:1px solid var(--border);border-radius:4px;background:#fff}
.review-verified{display:inline-flex;align-items:center;gap:6px;background:var(--green-bg);color:var(--green);padding:3px 8px;border-radius:3px;font-size:11px;font-weight:800;margin-bottom:12px;text-transform:uppercase;letter-spacing:.3px}
.review-verified::before{content:'\2713'}
.review-stars{color:var(--yellow);font-size:18px;margin-bottom:8px;letter-spacing:1px;-webkit-text-stroke:0;text-shadow:0 0 0 var(--yellow-dark)}
.review-title{font-size:14px;font-weight:800;color:var(--text);margin-bottom:6px;letter-spacing:-.1px}
.review-quote{font-size:14px;color:var(--text);margin-bottom:14px;line-height:1.55;font-weight:400}
.review-author{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.review-avatar{width:34px;height:34px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;flex-shrink:0}
.review-name{font-weight:700;font-size:13px;display:block;color:var(--text)}
.review-role{font-size:11px;color:var(--muted)}
.review-helpful{padding-top:12px;border-top:1px solid var(--border);font-size:12px;color:var(--muted);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.review-helpful .helpful-text{font-weight:500}
.review-helpful .thumbs{display:flex;gap:6px}
.review-helpful button{padding:5px 12px;border:1px solid var(--border);background:#fff;color:var(--text);font-size:12px;font-weight:700;border-radius:3px;cursor:pointer;font-family:inherit;display:inline-flex;align-items:center;gap:4px;transition:background .15s,border-color .15s}
.review-helpful button:hover{background:var(--blue-light);border-color:var(--blue)}

/* FAQ */
.faq{max-width:920px;margin:0 auto}
.faq-item{border:1px solid var(--border);border-radius:4px;background:#fff;margin-bottom:8px;overflow:hidden;transition:border-color .15s}
.faq-item:hover{border-color:var(--blue)}
.faq-q{width:100%;padding:18px 20px;background:none;border:none;text-align:left;font-size:15px;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit;gap:16px;transition:background .15s}
.faq-q:hover{background:var(--surface)}
.faq-q::after{content:'\02C5';font-size:20px;color:var(--blue);transition:transform .3s;font-weight:900;line-height:.5;flex-shrink:0}
.faq-item.active .faq-q::after{transform:rotate(180deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:14px;padding:0 20px;line-height:1.6}
.faq-item.active .faq-a{max-height:300px;padding:0 20px 18px}

/* FOOTER CTA */
.footer-cta-block{background:var(--blue);padding:48px 24px;text-align:center;color:#fff;position:relative;overflow:hidden}
.footer-cta-block::before{content:'';position:absolute;top:-50px;left:-50px;width:300px;height:300px;background:radial-gradient(circle,rgba(255,224,0,.1),transparent 70%);border-radius:50%;pointer-events:none}
.footer-cta-inner{max-width:880px;margin:0 auto;position:relative;z-index:1}
.footer-cta-inner h2{font-size:clamp(28px,4vw,40px);font-weight:900;letter-spacing:-1px;margin-bottom:14px;color:#fff;line-height:1.15}
.footer-cta-inner h2 .accent{color:var(--yellow)}
.footer-cta-inner p{font-size:16px;margin-bottom:24px;color:rgba(255,255,255,.95);max-width:600px;margin-left:auto;margin-right:auto;line-height:1.55}
.cta-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px;max-width:760px;margin:0 auto;padding:16px;background:#fff;border:3px solid var(--yellow);border-radius:8px;box-shadow:0 12px 30px rgba(0,0,0,.25)}
.cta-form input{padding:12px 14px;border:1px solid var(--border);border-radius:4px;font-size:14px;font-family:inherit;outline:none;background:#fff;color:var(--text);transition:border-color .15s,box-shadow .15s}
.cta-form input:focus{border-color:var(--blue);box-shadow:0 0 0 2px rgba(0,70,190,.18)}
.cta-form button{grid-column:1/-1;padding:16px 28px;border:none;border-radius:4px;background:var(--blue);color:#fff;font-size:15px;font-weight:900;cursor:pointer;letter-spacing:.4px;text-transform:uppercase;font-family:inherit;transition:background .15s;display:inline-flex;align-items:center;justify-content:center;gap:8px}
.cta-form button::before{content:'\26A1'}
.cta-form button:hover{background:var(--blue-hover)}

/* GEEK SQUAD BADGE ROW */
.geek-row{background:#fff;padding:32px 24px;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.geek-inner{max-width:1500px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:24px;text-align:center}
.geek-badge{display:flex;flex-direction:column;align-items:center;gap:6px}
.geek-badge .ic{font-size:30px;line-height:1}
.geek-badge .ti{font-weight:800;font-size:13px;color:var(--text);letter-spacing:.2px}
.geek-badge .sb{font-size:11px;color:var(--muted);font-weight:500}

/* FOOTER — DARK */
.footer{background:#1d252c;color:#fff;padding:48px 24px 24px}
.footer-cols{max-width:1500px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:32px;padding-bottom:32px;border-bottom:1px solid rgba(255,255,255,.15)}
.footer-col h4{font-size:13px;font-weight:900;margin-bottom:14px;color:var(--yellow);text-transform:uppercase;letter-spacing:.6px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:8px}
.footer-col a{font-size:13px;color:#fff;font-weight:400;opacity:.85;transition:opacity .15s,color .15s}
.footer-col a:hover{color:var(--yellow);text-decoration:none;opacity:1}
.footer-bottom{max-width:1500px;margin:0 auto;padding-top:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;font-size:12px;color:rgba(255,255,255,.7)}
.footer-bottom-links{display:flex;gap:14px;flex-wrap:wrap}
.footer-bottom-links a{color:rgba(255,255,255,.85);font-size:12px}
.footer-bottom-links a:hover{color:var(--yellow)}

@media(max-width:1024px){.hero-inner{grid-template-columns:1fr}.hero-product-row{grid-template-columns:1fr;text-align:center}.product-image{margin:0 auto}}
@media(max-width:900px){.search{display:none}.deals-mini-grid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.utility-bar{display:none}.nav{padding:12px 16px}.nav-right{gap:12px}.nav-right a span:not(.badge){display:none}.subnav,.shipping-ribbon{padding-left:16px;padding-right:16px;font-size:12px}.section,.section-alt-inner,.footer-cta-block,.footer{padding-left:16px;padding-right:16px}.section{padding-top:40px;padding-bottom:40px}.deals-grid,.reviews-grid,.steps-grid,.trust-strip,.stats-row,.deals-mini-grid{grid-template-columns:1fr}.trust{border-right:none;border-bottom:1px solid var(--border)}.btn{min-width:0;width:100%}.hero-left{padding:24px}.section-header{flex-direction:column;align-items:flex-start}}
</style></head>
<body>__TRACKING_PIXEL__

<div class="utility-bar"><div class="util-inner">
<a href="#">Order Status</a><span class="pipe">|</span>
<a href="#">Saved Items</a><span class="pipe">|</span>
<a href="#">My Eko account</a><span class="pipe">|</span>
<a href="#">Sign in</a>
</div></div>

<nav class="nav"><div class="nav-inner">
<a href="#" class="logo"><span class="tag"><span class="tag-text">EKO BUY</span></span></a>
<div class="search"><input type="text" placeholder="What can we help you find today?"><button type="button" aria-label="Search">Search</button></div>
<div class="nav-right">
<a href="#"><span class="nav-icon">&#128205;</span><span>Stores</span></a>
<a href="#"><span class="nav-icon">&#10084;</span><span>Saved</span></a>
<a href="#" class="cart-link"><span class="nav-icon">&#128722;</span><span>Cart</span><span class="badge">0</span></a>
</div>
</div></nav>

<div class="shipping-ribbon"><strong>FREE shipping</strong> on orders $35+ &nbsp;|&nbsp; Eko Plus members get free 2-day shipping every day <a href="#">Learn more</a></div>

<nav class="subnav"><div class="subnav-inner">
<a href="#benefits" class="hot">Top Deals</a>
<a href="#" class="hot">Deal of the Day</a>
<a href="#">Eko Buy Outlet</a>
<a href="#">Eko Buy Business</a>
<a href="#">Yes, Eko Buy Sells That</a>
<a href="#">Find a Store</a>
<a href="#">Recently Viewed</a>
<a href="#">Credit Cards</a>
<a href="#">Gift Cards</a>
</div></nav>

<section class="hero"><div class="hero-inner">
<div class="hero-left">
<span class="deal-badge">{{BADGE}}</span>
<div class="hero-product-row">
<div class="product-image">&#128241;</div>
<div>
<div class="product-name">Featured Deal &middot; Limited time</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="rating-line"><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span><span class="num">4.8</span> <a href="#reviews">(12,439 reviews)</a></div>
<div class="price-block">
<span class="price-was">$299.99</span>
<span class="price-now">FREE</span>
<span class="price-save">Save $299</span>
</div>
</div>
</div>
<div class="cta-row">
<a href="#form" class="btn btn-primary">{{CTA_BUTTON}}</a>
<a href="#benefits" class="btn btn-outline">Shop deals</a>
</div>
</div>
<div class="hero-right">
<div class="deals-header"><h2>Today's Top Deals</h2><a href="#benefits">See all &rsaquo;</a></div>
<div class="deals-mini-grid">
<div class="mini-deal"><span class="mini-deal-corner">DEAL</span><div class="mini-deal-img">&#128247;</div><div class="mini-deal-name">Smart device with full HD display</div><div class="mini-deal-price"><span class="now">$149</span><span class="was">$249</span></div></div>
<div class="mini-deal"><span class="mini-deal-corner">DEAL</span><div class="mini-deal-img">&#127911;</div><div class="mini-deal-name">Wireless audio with noise cancel</div><div class="mini-deal-price"><span class="now">$79</span><span class="was">$129</span></div></div>
<div class="mini-deal"><span class="mini-deal-corner">DEAL</span><div class="mini-deal-img">&#128187;</div><div class="mini-deal-name">Compact pro-grade workstation</div><div class="mini-deal-price"><span class="now">$899</span><span class="was">$1199</span></div></div>
<div class="mini-deal"><span class="mini-deal-corner">DEAL</span><div class="mini-deal-img">&#127918;</div><div class="mini-deal-name">Console bundle with extras</div><div class="mini-deal-price"><span class="now">$399</span><span class="was">$499</span></div></div>
</div>
</div>
</div></section>

<div class="trust-wrap">
<div class="trust-strip">
<div class="trust"><span class="trust-icon">&#11088;</span><span class="trust-text">4.8 / 5</span><span class="trust-sub">50,000+ shoppers</span></div>
<div class="trust"><span class="trust-icon">&#128666;</span><span class="trust-text">Free Shipping</span><span class="trust-sub">on orders $35+</span></div>
<div class="trust"><span class="trust-icon">&#8617;</span><span class="trust-text">60-Day Returns</span><span class="trust-sub">no questions asked</span></div>
<div class="trust"><span class="trust-icon">&#128176;</span><span class="trust-text">Price Match</span><span class="trust-sub">we'll match it</span></div>
<div class="trust"><span class="trust-icon">&#128737;</span><span class="trust-text">Geek Squad Setup</span><span class="trust-sub">expert install</span></div>
</div>
</div>

<div class="stats-row">
<div class="stat-tile"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat-tile"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat-tile"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>

<section class="section" id="benefits">
<div class="section-header"><div class="section-header-text"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div><a href="#form" class="see-all">See all deals &rsaquo;</a></div>
<div class="deals-grid">
<div class="deal-card"><div class="deal-corner">DEAL</div><div class="deal-icon">{{BENEFIT_1_ICON}}</div><div class="deal-stars">&#9733;&#9733;&#9733;&#9733;&#9733; <span class="ct">(2,341)</span></div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p><div class="deal-price-row"><span class="deal-was">$149.99</span><span class="deal-price">FREE</span></div><span class="deal-save">Save $149</span><button class="deal-add" type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">Add to Cart</button></div>
<div class="deal-card"><div class="deal-corner deal-corner-red">HOT</div><div class="deal-icon">{{BENEFIT_2_ICON}}</div><div class="deal-stars">&#9733;&#9733;&#9733;&#9733;&#9733; <span class="ct">(1,892)</span></div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p><div class="deal-price-row"><span class="deal-was">$199.99</span><span class="deal-price">FREE</span></div><span class="deal-save">Save $199</span><button class="deal-add" type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">Add to Cart</button></div>
<div class="deal-card"><div class="deal-corner">DEAL</div><div class="deal-icon">{{BENEFIT_3_ICON}}</div><div class="deal-stars">&#9733;&#9733;&#9733;&#9733;&#9733; <span class="ct">(3,108)</span></div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p><div class="deal-price-row"><span class="deal-was">$249.99</span><span class="deal-price">FREE</span></div><span class="deal-save">Save $249</span><button class="deal-add" type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">Add to Cart</button></div>
<div class="deal-card"><div class="deal-corner">DEAL</div><div class="deal-icon">{{BENEFIT_4_ICON}}</div><div class="deal-stars">&#9733;&#9733;&#9733;&#9733;&#9733; <span class="ct">(2,567)</span></div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p><div class="deal-price-row"><span class="deal-was">$179.99</span><span class="deal-price">FREE</span></div><span class="deal-save">Save $179</span><button class="deal-add" type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">Add to Cart</button></div>
</div>
</section>

<section class="section-alt"><div class="section-alt-inner" id="how">
<div class="section-header"><div class="section-header-text"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div></div>
<div class="steps-grid">
<div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>

<section class="section" id="reviews">
<div class="section-header"><div class="section-header-text"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div><a href="#form" class="see-all">See all reviews &rsaquo;</a></div>
<div class="reviews-grid">
<div class="review"><div class="review-verified">Verified Purchase</div><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><div class="review-title">Absolutely worth every penny</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div>
<div class="review-helpful"><span class="helpful-text">Was this helpful? <strong>142 of 158</strong></span><div class="thumbs"><button type="button">&#128077; Yes</button><button type="button">&#128078; No</button></div></div></div>
<div class="review"><div class="review-verified">Verified Purchase</div><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><div class="review-title">Exceeded my expectations</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div>
<div class="review-helpful"><span class="helpful-text">Was this helpful? <strong>98 of 104</strong></span><div class="thumbs"><button type="button">&#128077; Yes</button><button type="button">&#128078; No</button></div></div></div>
</div>
</section>

<section class="section-alt"><div class="section-alt-inner" id="faq">
<div class="section-header"><div class="section-header-text"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<section class="footer-cta-block" id="form"><div class="footer-cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div></section>

<div class="geek-row"><div class="geek-inner">
<div class="geek-badge"><span class="ic">&#128737;</span><span class="ti">Geek Squad</span><span class="sb">Tech support 24/7</span></div>
<div class="geek-badge"><span class="ic">&#128666;</span><span class="ti">Free Shipping</span><span class="sb">Orders over $35</span></div>
<div class="geek-badge"><span class="ic">&#127978;</span><span class="ti">In-Store Pickup</span><span class="sb">Ready in 1 hour</span></div>
<div class="geek-badge"><span class="ic">&#128179;</span><span class="ti">Flexible Payments</span><span class="sb">My Eko Buy Card</span></div>
<div class="geek-badge"><span class="ic">&#9851;</span><span class="ti">Recycling</span><span class="sb">Trade-in program</span></div>
</div></div>

<footer class="footer">
<div class="footer-cols">
<div class="footer-col"><h4>Customer Service</h4><ul><li><a href="#">Contact Us</a></li><li><a href="#">Help Center</a></li><li><a href="#">Order Status</a></li><li><a href="#">Returns & Exchanges</a></li><li><a href="#">Shipping & Delivery</a></li><li><a href="#">Product Recalls</a></li></ul></div>
<div class="footer-col"><h4>About Eko Buy</h4><ul><li><a href="#">Corporate Information</a></li><li><a href="#">Careers</a></li><li><a href="#">Corporate Responsibility</a></li><li><a href="#">Sustainability</a></li><li><a href="#">Diversity & Inclusion</a></li><li><a href="#">Newsroom</a></li></ul></div>
<div class="footer-col"><h4>Investors</h4><ul><li><a href="#">Investor Relations</a></li><li><a href="#">Financial Reports</a></li><li><a href="#">Governance</a></li><li><a href="#">Stock Information</a></li></ul></div>
<div class="footer-col"><h4>Partnerships</h4><ul><li><a href="#">Affiliate Program</a></li><li><a href="#">Become a Vendor</a></li><li><a href="#">Developers</a></li><li><a href="#">Advertise</a></li></ul></div>
<div class="footer-col"><h4>Eko Buy Accounts</h4><ul><li><a href="#">My Eko Buy Card</a></li><li><a href="#">Rewards Program</a></li><li><a href="#">Gift Cards</a></li><li><a href="#">Membership</a></li><li><a href="#">Manage Account</a></li></ul></div>
</div>
<div class="footer-bottom">
<div>&copy; {{YEAR}} eko Buy &middot; contact@biz.ekoaiautomation.com</div>
<div class="footer-bottom-links"><a href="#">Privacy Policy</a><a href="#">Terms of Service</a><a href="#">Accessibility</a><a href="#">CA Privacy Rights</a><a href="#">Interest-Based Ads</a></div>
</div>
</footer>
__FORM_SUBMIT_JS__
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 9: SPOTIFY VIBE — Pitch black bg, vibrant green accent, music-energy
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_SPOTIFY_VIBE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#000;--surface:#121212;--surface-2:#181818;--surface-3:#1f1f1f;--surface-hi:#282828;--text:#fff;--muted:#a7a7a7;--muted-2:#737373;--green:#1ed760;--green-bright:#1fdf64;--green-dark:#169c46;--pink:#ff4632;--blue:#4f9eff;--purple:#c44dff}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:'Spotify Circular','CircularSp',Montserrat,'Helvetica Neue',Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh;font-weight:400}
a{color:var(--text);text-decoration:none}

/* ── NAV: SOLID BLACK (Spotify never goes transparent) ── */
.nav{position:fixed;top:0;left:0;right:0;z-index:9999;background:#000;padding:0;height:72px;display:flex;align-items:center;border-bottom:1px solid transparent}
.nav-inner{max-width:1568px;margin:0 auto;padding:0 32px;width:100%;display:flex;align-items:center;justify-content:space-between;gap:24px}
.logo{display:inline-flex;align-items:center;gap:8px;font-size:24px;font-weight:900;color:#fff;letter-spacing:-.5px}
.logo svg{width:32px;height:32px;flex-shrink:0;color:#1ed760}
.nav-links{display:flex;gap:8px;list-style:none;align-items:center;margin-left:24px}
.nav-links a{color:#fff;font-size:14px;font-weight:700;padding:8px 14px;border-radius:4px;transition:color .15s,transform .15s;display:inline-block}
.nav-links a:hover{color:#fff;transform:scale(1.04)}
.nav-utility{display:flex;align-items:center;gap:18px;margin-left:auto}
.nav-divider{width:1px;height:26px;background:#3a3a3a}
.nav-utility .link{color:var(--muted);font-size:14px;font-weight:700;transition:color .15s,transform .15s}
.nav-utility .link:hover{color:#fff;transform:scale(1.04)}
.nav-cta{padding:14px 32px;border-radius:500px;background:#fff;color:#000!important;font-weight:700;font-size:14px;letter-spacing:.1px;transition:transform .15s,background .15s;display:inline-block}
.nav-cta:hover{transform:scale(1.04);background:#f0f0f0}

/* ── HERO: split layout, text left + rotated album stack right ── */
.hero{position:relative;padding:140px 32px 96px;background:linear-gradient(135deg,#1a3d2e 0%,#0a1f17 40%,#000 100%);overflow:hidden;min-height:92vh;display:flex;align-items:center}
.hero::before{content:'';position:absolute;top:-200px;right:-150px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(30,215,96,.28) 0%,transparent 65%);filter:blur(40px);pointer-events:none}
.hero::after{content:'';position:absolute;bottom:-150px;left:-100px;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(79,158,255,.18) 0%,transparent 70%);filter:blur(60px);pointer-events:none}
.hero-inner{position:relative;z-index:2;max-width:1240px;margin:0 auto;width:100%;display:grid;grid-template-columns:1.15fr .85fr;gap:80px;align-items:center}
.hero-text{text-align:left}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:500px;background:rgba(30,215,96,.14);border:1px solid rgba(30,215,96,.4);color:var(--green);font-size:12px;font-weight:700;margin-bottom:28px;letter-spacing:.3px;text-transform:uppercase}
.badge .pulse{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 0 0 rgba(30,215,96,.7);animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(30,215,96,.7)}70%{box-shadow:0 0 0 12px rgba(30,215,96,0)}100%{box-shadow:0 0 0 0 rgba(30,215,96,0)}}

.hero h1{font-size:clamp(56px,8vw,104px);font-weight:900;line-height:.9;letter-spacing:-3.5px;margin-bottom:24px;color:#fff;font-family:inherit}
.hero h1 .grad{background:linear-gradient(135deg,#1ed760 0%,#3be477 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;display:inline}
.hero .sub{font-size:clamp(17px,1.4vw,20px);color:var(--muted);max-width:520px;margin:0 0 36px;line-height:1.5;font-weight:400}

/* ── SIGNATURE GLOWING GREEN PILL ── */
.hero-ctas{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:28px;align-items:center}
.btn-pill-green{display:inline-flex;align-items:center;justify-content:center;padding:16px 48px;border-radius:500px;background:var(--green);color:#000!important;font-size:15px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;border:none;cursor:pointer;transition:transform .15s,background .15s,box-shadow .2s;font-family:inherit;box-shadow:0 4px 24px rgba(30,215,96,.4)}
.btn-pill-green:hover{transform:scale(1.04);background:var(--green-bright);box-shadow:0 6px 32px rgba(30,215,96,.55)}
.btn-pill-outline{display:inline-flex;align-items:center;justify-content:center;padding:16px 36px;border-radius:500px;background:transparent;color:#fff;font-size:15px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;border:2px solid #fff;cursor:pointer;transition:transform .15s,background .15s;font-family:inherit}
.btn-pill-outline:hover{transform:scale(1.04);background:rgba(255,255,255,.08);color:#fff}
.hero-meta{font-size:12.5px;color:var(--muted);font-weight:500;letter-spacing:.2px}

/* ── ROTATED ALBUM STACK (Spotify signature) ── */
.hero-visual{position:relative;display:flex;align-items:center;justify-content:center;min-height:460px}
.album-stack{position:relative;width:100%;max-width:420px;aspect-ratio:1}
.album{position:absolute;width:62%;aspect-ratio:1;border-radius:10px;box-shadow:0 24px 64px rgba(0,0,0,.7),0 0 0 1px rgba(255,255,255,.08) inset;overflow:hidden}
.album-1{top:6%;left:0;background:linear-gradient(135deg,#1ed760 0%,#0a5d2a 100%);transform:rotate(-10deg);z-index:1}
.album-2{top:18%;left:19%;background:linear-gradient(135deg,#ff4632 0%,#7d1b10 100%);transform:rotate(0deg);z-index:3}
.album-3{top:6%;right:0;background:linear-gradient(135deg,#4f9eff 0%,#1a3d8e 100%);transform:rotate(10deg);z-index:2}
.album::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at 28% 28%,rgba(255,255,255,.22),transparent 60%)}
.album::before{content:'';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:32%;aspect-ratio:1;border-radius:50%;background:rgba(0,0,0,.4);box-shadow:0 0 0 2px rgba(255,255,255,.12) inset,0 0 0 18px rgba(255,255,255,.02) inset}

/* ── form (inline-stack pills) ── */
.cta-form{display:flex;flex-wrap:wrap;gap:10px;max-width:560px;margin:24px 0 0;justify-content:flex-start}
.cta-form input{flex:1 1 200px;padding:14px 22px;border:1px solid #2a2a2a;border-radius:500px;background:rgba(20,20,20,.85);color:#fff;font-size:14px;font-family:inherit;outline:none;transition:all .2s;font-weight:500}
.cta-form input::placeholder{color:#6a6a6a}
.cta-form input:focus{border-color:var(--green);background:#1a1a1a}
.cta-form button{flex:0 0 auto;padding:14px 36px;border:none;border-radius:500px;background:var(--green);color:#000;font-size:14px;font-weight:700;cursor:pointer;letter-spacing:.8px;text-transform:uppercase;transition:transform .15s,background .15s,box-shadow .2s;font-family:inherit;box-shadow:0 4px 18px rgba(30,215,96,.35)}
.cta-form button:hover{background:var(--green-bright);transform:scale(1.04);box-shadow:0 6px 26px rgba(30,215,96,.5)}

/* ── STATS STRIP ── */
.stats-strip{background:var(--surface);padding:56px 32px;border-top:1px solid #1a1a1a;border-bottom:1px solid #1a1a1a}
.stats{display:flex;justify-content:center;gap:96px;max-width:1240px;margin:0 auto;flex-wrap:wrap}
.stat{text-align:center}
.stat-num{font-size:clamp(42px,5vw,68px);font-weight:900;color:var(--green);letter-spacing:-2px;line-height:1;font-family:inherit}
.stat-label{font-size:12px;color:var(--muted);margin-top:12px;text-transform:uppercase;letter-spacing:1.6px;font-weight:700}

/* ── SECTIONS ── */
.section{padding:120px 32px}
.section-inner{max-width:1240px;margin:0 auto}
.section-alt{background:var(--surface)}
.section-dark{background:linear-gradient(180deg,#000 0%,#0a0a0a 100%)}
.section-header{margin-bottom:56px;text-align:left;max-width:820px}
.section-header.center{text-align:center;margin-left:auto;margin-right:auto}
.section-eyebrow{display:inline-block;font-size:12px;color:var(--green);font-weight:700;text-transform:uppercase;letter-spacing:1.8px;margin-bottom:18px}
.section-header h2{font-size:clamp(40px,6vw,80px);font-weight:900;letter-spacing:-2.5px;line-height:.98;margin-bottom:20px;color:#fff;font-family:inherit}
.section-header h2 .grad{background:linear-gradient(135deg,var(--green),var(--green-bright));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.section-header p{color:var(--muted);font-size:17px;max-width:620px;line-height:1.5;font-weight:400}

/* ── FEATURES (Spotify card grid with 80px gradient album-art) ── */
.features-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.feature{padding:20px 18px 24px;border-radius:8px;background:var(--surface-2);transition:background .25s,transform .15s;cursor:pointer;position:relative;display:flex;flex-direction:column}
.feature:hover{background:var(--surface-hi);transform:translateY(-2px)}
.feature-art{width:80px;height:80px;border-radius:6px;margin-bottom:18px;display:flex;align-items:center;justify-content:center;font-size:36px;box-shadow:0 8px 24px rgba(0,0,0,.55);position:relative;overflow:hidden;flex-shrink:0}
.feature:nth-child(1) .feature-art{background:linear-gradient(135deg,#1ed760,#0a5d2a)}
.feature:nth-child(2) .feature-art{background:linear-gradient(135deg,#ff4632,#7d1b10)}
.feature:nth-child(3) .feature-art{background:linear-gradient(135deg,#4f9eff,#1a3d8e)}
.feature:nth-child(4) .feature-art{background:linear-gradient(135deg,#c44dff,#5a1d8e)}
.feature-art::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at 28% 28%,rgba(255,255,255,.22),transparent 65%)}
.feature-icon{position:relative;z-index:2;font-size:36px;line-height:1}
.feature h3{font-size:18px;font-weight:700;margin-bottom:6px;color:#fff;letter-spacing:-.3px;line-height:1.2}
.feature p{color:var(--muted);font-size:14px;line-height:1.45;font-weight:400}

/* ── STEPS ── */
.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.step{padding:32px 28px;border-radius:8px;background:var(--surface-2);position:relative;transition:background .25s,transform .15s}
.step:hover{background:var(--surface-hi);transform:translateY(-2px)}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;background:var(--green);color:#000;font-size:14px;font-weight:900;margin-bottom:20px;font-family:inherit}
.step h3{font-size:22px;font-weight:900;margin-bottom:10px;letter-spacing:-.5px;color:#fff;line-height:1.15}
.step p{color:var(--muted);font-size:15px;line-height:1.5;font-weight:400}

/* ── REVIEWS ── */
.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.review{padding:36px;border-radius:8px;background:var(--surface-2);transition:background .25s;border:1px solid transparent}
.review:hover{background:var(--surface-hi);border-color:rgba(30,215,96,.2)}
.review-stars{color:var(--green);font-size:14px;margin-bottom:18px;letter-spacing:3px}
.review-quote{font-size:19px;color:#fff;margin-bottom:28px;line-height:1.45;font-weight:500;letter-spacing:-.3px}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,var(--green),var(--green-bright));color:#000;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:16px;flex-shrink:0}
.review-name{font-weight:900;font-size:15px;display:block;color:#fff;letter-spacing:-.2px}
.review-role{font-size:13px;color:var(--muted);font-weight:500;margin-top:2px}

/* ── FAQ ── */
.faq{max-width:820px;margin:0 auto}
.faq-item{border-bottom:1px solid #1f1f1f}
.faq-item:first-child{border-top:1px solid #1f1f1f}
.faq-q{width:100%;padding:28px 8px;background:none;border:none;text-align:left;font-size:19px;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:#fff;letter-spacing:-.3px;gap:24px;font-family:inherit;transition:color .15s}
.faq-q:hover{color:var(--green)}
.faq-q::after{content:'+';font-size:28px;color:var(--green);transition:transform .25s;font-weight:300;flex-shrink:0;line-height:1}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;line-height:1.6;padding:0 8px;font-weight:400}
.faq-item.active .faq-a{max-height:320px;padding:0 8px 28px}

/* ── FOOTER CTA ── */
.footer-cta{padding:140px 32px;text-align:center;background:linear-gradient(180deg,#000 0%,#0a3d22 100%);border-top:1px solid #0a1a12;position:relative;overflow:hidden}
.footer-cta::before{content:'';position:absolute;top:50%;left:50%;width:680px;height:680px;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(30,215,96,.22) 0%,transparent 60%);filter:blur(50px);pointer-events:none}
.footer-cta-inner{position:relative;z-index:1;max-width:820px;margin:0 auto}
.footer-cta h2{font-size:clamp(40px,6vw,80px);font-weight:900;letter-spacing:-2.5px;margin-bottom:24px;line-height:.95;color:#fff;font-family:inherit}
.footer-cta p{font-size:19px;color:var(--muted);max-width:600px;margin:0 auto 40px;line-height:1.45;font-weight:400}
.footer-btn{display:inline-block;padding:18px 56px;border-radius:500px;background:var(--green);color:#000;font-weight:900;font-size:15px;text-transform:uppercase;letter-spacing:1.4px;transition:transform .15s,background .15s,box-shadow .2s;font-family:inherit;border:none;cursor:pointer;box-shadow:0 6px 32px rgba(30,215,96,.45)}
.footer-btn:hover{background:var(--green-bright);transform:scale(1.04);color:#000;box-shadow:0 8px 40px rgba(30,215,96,.6)}

/* ── FOOTER (multi-column, black, social pills) ── */
.footer{background:#000;padding:80px 32px 40px;border-top:1px solid #1a1a1a}
.footer-inner{max-width:1280px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px}
.footer-brand{display:flex;flex-direction:column;gap:16px}
.footer-brand .logo{color:#fff;font-size:24px}
.footer-brand p{color:var(--muted);font-size:13px;line-height:1.55;max-width:280px;font-weight:400}
.footer-col h4{font-size:11px;font-weight:700;color:#fff;margin-bottom:20px;text-transform:uppercase;letter-spacing:1.5px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.footer-col a{font-size:14px;color:var(--muted);font-weight:500;transition:color .15s}
.footer-col a:hover{color:#fff;text-decoration:underline}
.footer-bottom{padding-top:32px;border-top:1px solid #1a1a1a;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
.copy{font-size:12px;color:#6a6a6a;font-weight:500}
.footer-socials{display:flex;gap:12px}
.footer-socials a{width:40px;height:40px;border-radius:50%;background:#fff;color:#000;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:13px;transition:transform .15s,background .15s}
.footer-socials a:hover{transform:scale(1.08);background:#eaeaea}

@media(max-width:960px){.hero-inner{grid-template-columns:1fr;gap:48px;text-align:center}.hero-text{text-align:center}.hero-ctas{justify-content:center}.cta-form{justify-content:center}.nav-links{display:none}.features-grid{grid-template-columns:repeat(2,1fr)}.steps-grid,.reviews-grid{grid-template-columns:1fr}.stats{gap:48px}.section{padding:80px 24px}.footer-top{grid-template-columns:1fr 1fr;gap:32px}.section-header{text-align:center;margin-left:auto;margin-right:auto}.hero-visual{min-height:340px}.album-stack{max-width:320px}}
@media(max-width:640px){.features-grid{grid-template-columns:1fr}.footer-top{grid-template-columns:1fr}.cta-form input,.cta-form button{flex:1 1 100%}.album-stack{max-width:260px}.hero{padding:120px 18px 72px}.footer-cta{padding:96px 18px}.section{padding:64px 18px}.footer{padding:48px 18px 24px}.footer-bottom{flex-direction:column;text-align:center}}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="logo">
<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></svg>
Eko
</a>
<ul class="nav-links">
<li><a href="#benefits">Premium</a></li>
<li><a href="#faq">Support</a></li>
<li><a href="#how">Download</a></li>
</ul>
<div class="nav-utility">
<a href="#form" class="link">Sign up</a>
<span class="nav-divider"></span>
<a href="#form" class="link">Log in</a>
<a href="#form" class="nav-cta">Get Premium</a>
</div>
</div></nav>

<section class="hero" id="form"><div class="hero-inner">
<div class="hero-text">
<div class="badge"><span class="pulse"></span>{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="hero-ctas">
<a href="#cta-form" class="btn-pill-green">{{CTA_BUTTON}}</a>
<a href="#how" class="btn-pill-outline">Learn more</a>
</div>
<form id="cta-form" class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Email address" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button>
</form>
<div class="hero-meta" style="margin-top:20px">Free forever. Upgrade anytime. Cancel whenever.</div>
</div>
<div class="hero-visual" aria-hidden="true">
<div class="album-stack">
<div class="album album-1"></div>
<div class="album album-3"></div>
<div class="album album-2"></div>
</div>
</div>
</div></section>

<div class="stats-strip">
<div class="stats">
<div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</div>

<section class="section section-dark" id="benefits"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">Why Eko</span><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-art"><span class="feature-icon">{{BENEFIT_1_ICON}}</span></div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-art"><span class="feature-icon">{{BENEFIT_2_ICON}}</span></div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-art"><span class="feature-icon">{{BENEFIT_3_ICON}}</span></div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-art"><span class="feature-icon">{{BENEFIT_4_ICON}}</span></div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div></div></section>

<section class="section section-alt" id="how"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">Get started</span><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><span class="step-num">1</span><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><span class="step-num">2</span><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><span class="step-num">3</span><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div></div></section>

<section class="section section-dark" id="reviews"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">Loved by listeners</span><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div>
</div></div></section>

<section class="section section-alt" id="faq"><div class="section-inner">
<div class="section-header center"><span class="section-eyebrow">FAQ</span><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div></div></section>

<section class="footer-cta">
<div class="footer-cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
</div>
</section>

<footer class="footer">
<div class="footer-inner">
<div class="footer-top">
<div class="footer-brand">
<div class="logo"><svg width="32" height="32" viewBox="0 0 24 24" fill="#1ed760" aria-hidden="true"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></svg>Eko</div>
<p>Sound for everyone. Discover, create, and share the music that moves you.</p>
</div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Jobs</a></li><li><a href="#">For the Record</a></li></ul></div>
<div class="footer-col"><h4>Communities</h4><ul><li><a href="#">For Artists</a></li><li><a href="#">Developers</a></li><li><a href="#">Advertising</a></li><li><a href="#">Investors</a></li><li><a href="#">Vendors</a></li></ul></div>
<div class="footer-col"><h4>Useful links</h4><ul><li><a href="#faq">Support</a></li><li><a href="#form">Free Mobile App</a></li><li><a href="#">Popular Cities</a></li></ul></div>
<div class="footer-col"><h4>Eko Plans</h4><ul><li><a href="#form">Premium Individual</a></li><li><a href="#form">Premium Duo</a></li><li><a href="#form">Premium Family</a></li><li><a href="#form">Premium Student</a></li><li><a href="#form">Eko Free</a></li></ul></div>
</div>
<div class="footer-bottom">
<div class="copy">&copy; {{YEAR}} Eko AI &middot; contact@biz.ekoaiautomation.com</div>
<div class="footer-socials">
<a href="#" aria-label="Instagram">IG</a>
<a href="#" aria-label="Twitter">X</a>
<a href="#" aria-label="Facebook">FB</a>
</div>
</div>
</div>
</footer>
__FORM_SUBMIT_JS__
</body></html>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 10: HUBSPOT SALES — Orange CTA, B2B SaaS feel, conversion-optimized
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_HUBSPOT_SALES = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--text:#33475b;--text-dark:#2d3e50;--muted:#516f90;--soft:#7c98b6;--brand:#FF7A59;--brand-dark:#ff5c35;--brand-soft:#fdf3f0;--teal:#0098d4;--teal-dark:#00709b;--green:#00bda5;--purple:#6a78d1;--red:#ec4f48;--bg:#fff;--surface:#f5f8fa;--surface-2:#eaf0f6;--border:#cbd6e2;--border-soft:#dfe3eb}
html{scroll-behavior:smooth;background:#fff;min-height:100vh}
body{font-family:'Lexend Deca','Lexend','Avenir Next',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#fff!important;color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased;min-height:100vh}
a{color:var(--teal);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;display:block}
.container{max-width:1180px;margin:0 auto;padding:0 24px}

/* NAV */
.nav{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid var(--border-soft);box-shadow:0 1px 0 rgba(0,0,0,.02)}
.nav-inner{max-width:1240px;margin:0 auto;padding:0 24px;height:72px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.logo{font-size:22px;font-weight:700;color:var(--text);letter-spacing:-.4px;display:flex;align-items:center;gap:8px;flex-shrink:0}
.logo-mark{width:32px;height:32px;flex-shrink:0;display:inline-block}
.logo-mark svg{display:block;width:100%;height:100%}
.nav-links{display:flex;gap:0;list-style:none;align-items:center;flex:1;justify-content:center}
.nav-links li{position:relative}
.nav-links a{color:var(--text);font-size:15px;font-weight:500;transition:color .15s;padding:24px 14px;display:inline-flex;align-items:center;gap:5px}
.nav-links a:hover{color:var(--brand);text-decoration:none}
.nav-links a.has-caret::after{content:'\02C5';color:var(--soft);font-size:14px;line-height:.5;transition:transform .15s}
.nav-links a:hover.has-caret::after{transform:rotate(180deg);color:var(--brand)}
.nav-actions{display:flex;align-items:center;gap:14px;flex-shrink:0}
.nav-signin{color:var(--text);font-size:14px;font-weight:500;padding:8px 12px;transition:color .15s}
.nav-signin:hover{color:var(--brand);text-decoration:none}
.nav-cta{padding:11px 22px;border-radius:60px;background:var(--brand);color:#fff!important;font-size:14px;font-weight:600;transition:background .15s,transform .15s,box-shadow .15s;border:2px solid var(--brand);box-shadow:0 2px 4px rgba(255,122,89,.18)}
.nav-cta:hover{background:var(--brand-dark);border-color:var(--brand-dark);text-decoration:none;transform:translateY(-1px);box-shadow:0 4px 10px rgba(255,122,89,.3)}

/* HERO */
.hero{position:relative;padding:88px 24px 80px;background:linear-gradient(180deg,#fff 0%,#f5f8fa 100%);overflow:hidden}
.hero::before{content:'';position:absolute;top:-120px;right:-120px;width:480px;height:480px;background:radial-gradient(circle,rgba(255,122,89,.14),transparent 70%);border-radius:50%;pointer-events:none}
.hero::after{content:'';position:absolute;bottom:-140px;left:-140px;width:480px;height:480px;background:radial-gradient(circle,rgba(0,152,212,.1),transparent 70%);border-radius:50%;pointer-events:none}
.hero-inner{max-width:920px;margin:0 auto;position:relative;z-index:1;text-align:center}
.badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:60px;background:var(--brand-soft);border:1px solid rgba(255,122,89,.25);color:var(--brand-dark);font-size:13px;font-weight:600;margin-bottom:24px}
.badge::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--brand)}
h1{font-size:clamp(36px,5vw,60px);font-weight:700;line-height:1.08;letter-spacing:-1.6px;color:var(--text);margin-bottom:22px}
h1 .accent{color:var(--brand)}
.hero p.sub{font-size:clamp(17px,1.6vw,20px);color:var(--muted);max-width:680px;margin:0 auto 32px;line-height:1.55;font-weight:400}

/* DUAL CTA buttons */
.hero-ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-bottom:18px}
.btn-orange{display:inline-flex;align-items:center;justify-content:center;padding:14px 30px;border-radius:60px;background:var(--brand);color:#fff!important;font-size:15px;font-weight:600;text-decoration:none;transition:background .15s,transform .15s,box-shadow .15s;border:2px solid var(--brand);box-shadow:0 4px 12px rgba(255,122,89,.25);font-family:inherit;cursor:pointer}
.btn-orange:hover{background:var(--brand-dark);border-color:var(--brand-dark);text-decoration:none;transform:translateY(-2px);box-shadow:0 8px 18px rgba(255,122,89,.35)}
.btn-outline-dark{display:inline-flex;align-items:center;justify-content:center;padding:14px 30px;border-radius:60px;background:transparent;color:var(--text)!important;font-size:15px;font-weight:600;text-decoration:none;transition:background .15s,border-color .15s;border:2px solid var(--text);font-family:inherit;cursor:pointer}
.btn-outline-dark:hover{background:var(--text);color:#fff!important;text-decoration:none}
.hero-trust{margin-top:14px;font-size:13px;color:var(--soft);font-weight:500}
.hero-trust .check{color:var(--green);margin-right:4px;font-weight:700}

/* TRUST STRIP — grayscale logo wall */
.trust-strip{background:#fff;padding:48px 24px;border-top:1px solid var(--border-soft);border-bottom:1px solid var(--border-soft)}
.trust-inner{max-width:1180px;margin:0 auto;text-align:center}
.trust-label{font-size:13px;color:var(--soft);font-weight:600;text-transform:uppercase;letter-spacing:1.4px;margin-bottom:28px}
.trust-logos{display:flex;justify-content:center;align-items:center;gap:48px;flex-wrap:wrap}
.trust-logo{font-size:16px;font-weight:700;color:var(--soft);letter-spacing:-.2px;opacity:.65;transition:opacity .2s,color .2s;cursor:default}
.trust-logo:hover{opacity:1;color:var(--muted)}
.trust-logo.upper{text-transform:uppercase;letter-spacing:2.5px;font-size:13px}
.trust-logo.italic{font-style:italic;font-family:Georgia,'Times New Roman',serif;font-weight:400;font-size:22px;letter-spacing:-.5px}
.trust-logo.serif{font-family:Georgia,'Times New Roman',serif;font-weight:400;font-size:20px;letter-spacing:0}
.trust-logo.script{font-style:italic;font-weight:500;font-size:18px}
.trust-logo.mono{font-family:'Courier New',monospace;letter-spacing:1px;font-size:14px}

/* STATS */
.stats{background:var(--surface);padding:72px 24px}
.stats-inner{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:32px;text-align:center}
.stat{padding:24px}
.stat-num{font-size:clamp(40px,5vw,58px);font-weight:700;color:var(--brand);letter-spacing:-2px;line-height:1}
.stat-num::after{content:''}
.stat-label{font-size:12px;color:var(--teal);font-weight:700;margin-top:10px;line-height:1.4;text-transform:uppercase;letter-spacing:1.4px}

/* SECTIONS */
.section{padding:96px 24px;background:#fff}
.section-inner{max-width:1180px;margin:0 auto}
.section-alt{background:var(--surface)}
.section-header{text-align:center;margin-bottom:64px;max-width:720px;margin-left:auto;margin-right:auto}
.eyebrow{display:inline-block;font-size:13px;font-weight:700;color:var(--brand);text-transform:uppercase;letter-spacing:1.4px;margin-bottom:14px}
.section-header h2{font-size:clamp(30px,4vw,46px);font-weight:700;letter-spacing:-1.2px;margin-bottom:16px;color:var(--text);line-height:1.12}
.section-header p{color:var(--muted);font-size:18px;line-height:1.55}

/* FEATURES */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}
.feature{padding:32px;border-radius:6px;background:#fff;border:1px solid var(--border);transition:transform .2s,box-shadow .2s,border-color .2s;text-align:left;position:relative}
.feature:hover{transform:translateY(-4px);box-shadow:0 16px 32px rgba(51,71,91,.1);border-color:var(--brand)}
.section-alt .feature{background:#fff}
.feature-icon{display:inline-flex;width:56px;height:56px;border-radius:50%;background:var(--brand);color:#fff;align-items:center;justify-content:center;font-size:24px;margin-bottom:20px;box-shadow:0 6px 14px rgba(255,122,89,.3)}
.feature:nth-child(2) .feature-icon{background:var(--teal);box-shadow:0 6px 14px rgba(0,152,212,.3)}
.feature:nth-child(3) .feature-icon{background:var(--green);box-shadow:0 6px 14px rgba(0,189,165,.3)}
.feature:nth-child(4) .feature-icon{background:var(--purple);box-shadow:0 6px 14px rgba(106,120,209,.3)}
.feature h3{font-size:20px;font-weight:600;margin-bottom:10px;color:var(--text);letter-spacing:-.3px;line-height:1.25}
.feature p{color:var(--muted);font-size:15px;line-height:1.6}

/* HUBS — all-in-one platform callouts */
.hubs-row{margin-top:80px}
.hubs-title{text-align:center;margin-bottom:32px}
.hubs-title h3{font-size:22px;font-weight:600;color:var(--text);letter-spacing:-.3px}
.hubs-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.hub{padding:24px 18px;border-radius:6px;background:#fff;border:1px solid var(--border-soft);text-align:center;transition:transform .15s,border-color .15s,box-shadow .15s;cursor:pointer}
.hub:hover{transform:translateY(-3px);box-shadow:0 8px 20px rgba(51,71,91,.08)}
.hub-icon{width:48px;height:48px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px;margin:0 auto 12px;color:#fff;font-weight:700}
.hub:nth-child(1){border-color:rgba(255,122,89,.3)}
.hub:nth-child(1) .hub-icon{background:var(--brand)}
.hub:nth-child(1):hover{border-color:var(--brand)}
.hub:nth-child(2){border-color:rgba(0,152,212,.3)}
.hub:nth-child(2) .hub-icon{background:var(--teal)}
.hub:nth-child(2):hover{border-color:var(--teal)}
.hub:nth-child(3){border-color:rgba(0,189,165,.3)}
.hub:nth-child(3) .hub-icon{background:var(--green)}
.hub:nth-child(3):hover{border-color:var(--green)}
.hub:nth-child(4){border-color:rgba(106,120,209,.3)}
.hub:nth-child(4) .hub-icon{background:var(--purple)}
.hub:nth-child(4):hover{border-color:var(--purple)}
.hub:nth-child(5){border-color:rgba(236,79,72,.3)}
.hub:nth-child(5) .hub-icon{background:var(--red)}
.hub:nth-child(5):hover{border-color:var(--red)}
.hub-name{font-size:14px;font-weight:700;color:var(--text);letter-spacing:-.1px;margin-bottom:4px}
.hub-desc{font-size:12px;color:var(--muted);font-weight:500}

/* STEPS — numbered orange circles */
.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;counter-reset:step}
.step{padding:32px;background:#fff;border:1px solid var(--border);border-radius:6px;position:relative;transition:transform .2s,box-shadow .2s,border-color .2s;text-align:center}
.step:hover{transform:translateY(-4px);box-shadow:0 16px 32px rgba(51,71,91,.1);border-color:var(--brand)}
.step-circle{display:inline-flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:50%;background:#fff;color:var(--brand);font-weight:700;font-size:22px;margin:0 auto 20px;border:2px solid var(--brand);font-family:inherit}
.step h3{font-size:20px;font-weight:600;margin-bottom:10px;color:var(--text);letter-spacing:-.3px}
.step p{color:var(--muted);font-size:15px;line-height:1.55}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{padding:36px 32px;border-radius:6px;background:#fff;border:1px solid var(--border);transition:box-shadow .2s,transform .2s;position:relative}
.section-alt .review{background:#fff}
.review:hover{box-shadow:0 16px 32px rgba(51,71,91,.1);transform:translateY(-3px)}
.review-logo{font-size:14px;font-weight:700;color:var(--soft);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px}
.review-stars{color:#ffb800;font-size:16px;margin-bottom:14px;letter-spacing:2px}
.review-quote{font-size:17px;color:var(--text);margin-bottom:24px;line-height:1.55;font-weight:400}
.review-author{display:flex;align-items:center;gap:14px;padding-top:20px;border-top:1px solid var(--border-soft)}
.review-avatar{width:48px;height:48px;border-radius:50%;background:var(--brand);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;flex-shrink:0}
.review:nth-child(2) .review-avatar{background:var(--teal)}
.review-name{font-weight:600;font-size:15px;display:block;color:var(--text)}
.review-role{font-size:13px;color:var(--soft);line-height:1.4}

/* FAQ — with +/- toggles */
.faq{max-width:780px;margin:0 auto}
.faq-item{border:1px solid var(--border);border-radius:6px;margin-bottom:12px;background:#fff;overflow:hidden;transition:border-color .2s,box-shadow .2s}
.section-alt .faq-item{background:#fff}
.faq-item.active{border-color:var(--brand);box-shadow:0 4px 12px rgba(255,122,89,.1)}
.faq-q{width:100%;padding:22px 24px;background:none;border:none;text-align:left;font-size:17px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit;gap:16px;transition:color .15s}
.faq-q:hover{color:var(--brand)}
.faq-q::after{content:'+';font-size:28px;color:var(--brand);transition:transform .3s;font-weight:400;line-height:.6;flex-shrink:0;font-family:inherit;display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px}
.faq-item.active .faq-q{color:var(--brand)}
.faq-item.active .faq-q::after{content:'\2212';transform:rotate(0deg);font-size:24px}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;padding:0 24px;line-height:1.6}
.faq-item.active .faq-a{max-height:320px;padding:0 24px 22px}

/* FOOTER CTA BAND */
.footer-band{background:linear-gradient(135deg,var(--brand) 0%,var(--brand-dark) 100%);padding:80px 24px;text-align:center;color:#fff;position:relative;overflow:hidden}
.footer-band::before{content:'';position:absolute;top:-100px;right:-50px;width:300px;height:300px;background:radial-gradient(circle,rgba(255,255,255,.12),transparent 70%);border-radius:50%;pointer-events:none}
.footer-band-inner{max-width:760px;margin:0 auto;position:relative;z-index:1}
.footer-band h2{font-size:clamp(32px,4.5vw,48px);font-weight:700;letter-spacing:-1.4px;margin-bottom:16px;color:#fff;line-height:1.15}
.footer-band p{font-size:18px;color:rgba(255,255,255,.92);max-width:560px;margin:0 auto 32px;line-height:1.5}
.cta-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;max-width:680px;margin:0 auto;background:#fff;padding:14px;border-radius:8px;box-shadow:0 12px 36px rgba(0,0,0,.18)}
.cta-form input{padding:14px 16px;border:1px solid var(--border);border-radius:4px;font-size:14px;font-family:inherit;outline:none;background:#fff;color:var(--text);transition:border-color .15s,box-shadow .15s}
.cta-form input::placeholder{color:var(--soft)}
.cta-form input:focus{border-color:var(--teal);box-shadow:0 0 0 3px rgba(0,152,212,.18)}
.cta-form button{grid-column:1/-1;padding:16px 32px;border:none;border-radius:60px;background:var(--brand);color:#fff;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;transition:background .15s,transform .15s}
.cta-form button:hover{background:var(--brand-dark);transform:translateY(-1px)}

/* FOOTER — DARK NAVY */
.footer{background:#33475b;color:#fff;padding:72px 24px 32px}
.footer-cols{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:48px;padding-bottom:48px;border-bottom:1px solid rgba(255,255,255,.1)}
.footer-brand{display:flex;flex-direction:column;gap:14px}
.footer-brand .logo{color:#fff;font-size:22px}
.footer-brand .logo-mark svg .sprocket-fill{fill:#fff}
.footer-brand p{color:rgba(255,255,255,.7);font-size:14px;max-width:280px;line-height:1.6}
.footer-col h4{font-size:13px;font-weight:700;color:#fff;margin-bottom:18px;text-transform:uppercase;letter-spacing:.8px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:11px}
.footer-col a{color:rgba(255,255,255,.75);font-size:14px;transition:color .15s}
.footer-col a:hover{color:var(--brand);text-decoration:none}
.footer-copy{max-width:1180px;margin:0 auto;padding-top:32px;font-size:13px;color:rgba(255,255,255,.55);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px}
.footer-copy-links{display:flex;gap:18px;flex-wrap:wrap}
.footer-copy-links a{color:rgba(255,255,255,.55);font-size:13px}
.footer-copy-links a:hover{color:#fff;text-decoration:none}

@media(max-width:960px){.steps-grid,.stats-inner{grid-template-columns:1fr;gap:20px}.footer-cols{grid-template-columns:1fr 1fr;gap:32px}.trust-logos{gap:32px}.nav-links{display:none}}
@media(max-width:640px){.nav-signin{display:none}.features-grid,.reviews-grid{grid-template-columns:1fr}.footer-cols{grid-template-columns:1fr}.section{padding:64px 20px}.hero{padding:64px 20px 56px}.hubs-grid{grid-template-columns:1fr 1fr}.hero-ctas .btn-orange,.hero-ctas .btn-outline-dark{flex:1;min-width:140px}}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="logo">
<span class="logo-mark"><svg viewBox="0 0 32 32" aria-hidden="true"><g class="sprocket-fill" fill="#FF7A59"><path d="M28 12.5a4 4 0 0 0-3.5 2H22V8.5a4 4 0 1 0-2 0V14h-2.5a4 4 0 1 0 0 2H20v5.5a4 4 0 1 0 2 0V16h2.5a4 4 0 1 0 3.5-3.5z"/></g></svg></span>
<span>Eko</span>
</a>
<ul class="nav-links">
<li><a href="#benefits" class="has-caret">Software </a></li>
<li><a href="#faq">Pricing</a></li>
<li><a href="#reviews" class="has-caret">Resources </a></li>
<li><a href="#how" class="has-caret">Partners </a></li>
</ul>
<div class="nav-actions"><a href="#" class="nav-signin">Contact Sales</a><a href="#form" class="nav-cta">Get free CRM</a></div>
</div></nav>

<section class="hero" id="form"><div class="hero-inner">
<div class="badge">{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="hero-ctas">
<a href="#form" class="btn-orange">{{CTA_BUTTON}}</a>
<a href="#benefits" class="btn-outline-dark">Get free CRM</a>
</div>
<div class="hero-trust"><span class="check">&#10003;</span>Free forever &middot; <span class="check">&#10003;</span>No credit card required &middot; <span class="check">&#10003;</span>Setup in 5 minutes</div>
</div></section>

<section class="trust-strip"><div class="trust-inner">
<div class="trust-label">Trusted by 200,000+ growing teams worldwide</div>
<div class="trust-logos">
<span class="trust-logo upper">NORTHWIND TRADERS</span>
<span class="trust-logo serif">Vertex Solutions</span>
<span class="trust-logo italic">Initech</span>
<span class="trust-logo">Pied Piper</span>
<span class="trust-logo script">Soylent Corp</span>
<span class="trust-logo mono">MASSIVE DYNAMIC</span>
</div></div></section>

<section class="stats"><div class="stats-inner">
<div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></section>

<section class="section" id="benefits"><div class="section-inner">
<div class="section-header"><span class="eyebrow">Sales Hub</span><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div>

<div class="hubs-row">
<div class="hubs-title"><h3>The all-in-one platform for scaling teams</h3></div>
<div class="hubs-grid">
<div class="hub"><div class="hub-icon">&#128235;</div><div class="hub-name">Marketing Hub</div><div class="hub-desc">Lead gen & automation</div></div>
<div class="hub"><div class="hub-icon">&#128176;</div><div class="hub-name">Sales Hub</div><div class="hub-desc">CRM & pipeline</div></div>
<div class="hub"><div class="hub-icon">&#128227;</div><div class="hub-name">Service Hub</div><div class="hub-desc">Help desk & feedback</div></div>
<div class="hub"><div class="hub-icon">&#127760;</div><div class="hub-name">CMS Hub</div><div class="hub-desc">Website & content</div></div>
<div class="hub"><div class="hub-icon">&#9881;</div><div class="hub-name">Operations Hub</div><div class="hub-desc">Sync & automation</div></div>
</div>
</div>
</div></section>

<section class="section section-alt" id="how"><div class="section-inner">
<div class="section-header"><span class="eyebrow">How it works</span><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-circle">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-circle">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-circle">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div></div></section>

<section class="section" id="reviews"><div class="section-inner">
<div class="section-header"><span class="eyebrow">Customer Stories</span><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-logo">NORTHWIND TRADERS</div><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</p><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-logo">VERTEX SOLUTIONS</div><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</p><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div>
</div></div></section>

<section class="section section-alt" id="faq"><div class="section-inner">
<div class="section-header"><span class="eyebrow">FAQ</span><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div></div></section>

<section class="footer-band"><div class="footer-band-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Work email" required>
<input type="tel" name="phone" placeholder="Phone number" required>
<input type="url" name="website" placeholder="Company website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div></section>

<footer class="footer">
<div class="footer-cols">
<div class="footer-brand"><div class="logo"><span class="logo-mark"><svg viewBox="0 0 32 32" aria-hidden="true"><g class="sprocket-fill" fill="#fff"><path d="M28 12.5a4 4 0 0 0-3.5 2H22V8.5a4 4 0 1 0-2 0V14h-2.5a4 4 0 1 0 0 2H20v5.5a4 4 0 1 0 2 0V16h2.5a4 4 0 1 0 3.5-3.5z"/></g></svg></span>Eko</div><p>The all-in-one platform built for growing teams. CRM, marketing, sales and service together.</p></div>
<div class="footer-col"><h4>Products</h4><ul><li><a href="#">Marketing Hub</a></li><li><a href="#">Sales Hub</a></li><li><a href="#">Service Hub</a></li><li><a href="#">CMS Hub</a></li><li><a href="#">Operations Hub</a></li></ul></div>
<div class="footer-col"><h4>Popular Features</h4><ul><li><a href="#">Free CRM</a></li><li><a href="#">Email Tracking</a></li><li><a href="#">Meeting Scheduler</a></li><li><a href="#">Sales Sequences</a></li><li><a href="#">Reporting Dashboards</a></li></ul></div>
<div class="footer-col"><h4>Free Tools</h4><ul><li><a href="#">Email Signature Maker</a></li><li><a href="#">Invoice Templates</a></li><li><a href="#">Website Grader</a></li><li><a href="#">Marketing Plan Generator</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Careers</a></li><li><a href="#">Customers</a></li><li><a href="#">Partners</a></li><li><a href="#">Contact</a></li></ul></div>
</div>
<div class="footer-copy">
<div>&copy; {{YEAR}} Eko AI &middot; contact@biz.ekoaiautomation.com &middot; All rights reserved.</div>
<div class="footer-copy-links"><a href="#">Privacy Policy</a><a href="#">Terms</a><a href="#">Cookie Settings</a><a href="#">Status</a></div>
</div>
</footer>
__FORM_SUBMIT_JS__
</body></html>
"""



# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE REGISTRY — single source of truth for template metadata.
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Vercel Modern ─────────────────────────────────────────────────────────────
_TPL_VERCEL_MODERN = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#000;
  --bg-1:#0a0a0a;
  --bg-2:#111;
  --text:#fff;
  --muted:#a1a1aa;
  --muted-2:#71717a;
  --border:rgba(255,255,255,.1);
  --border-2:#1f1f1f;
  --pink:#ff0080;
  --purple:#7928ca;
  --blue:#0070f3;
  --cyan:#00dfd8;
  --green:#0cce6b;
}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:'Geist Sans','Inter',-apple-system,BlinkMacSystemFont,system-ui,'Segoe UI',Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;font-weight:400;letter-spacing:-.01em;min-height:100vh}
a{color:var(--text);text-decoration:none;transition:color .15s}
a:hover{color:#fff}
.mono{font-family:'Geist Mono','SF Mono','JetBrains Mono',Menlo,monospace;font-feature-settings:"ss01","ss02"}

/* GRADIENT TEXT — Vercel signature */
.gradient-text{background:linear-gradient(90deg,#fff 0%,#888 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent}
.gradient-rainbow{background:linear-gradient(90deg,#ff0080 0%,#7928ca 35%,#0070f3 70%,#00dfd8 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent}

/* NAV — sticky black w/ blur, full Vercel menu */
.nav{position:sticky;top:0;z-index:9999;background:rgba(0,0,0,.7);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1280px;margin:0 auto;padding:0 24px;height:64px;display:flex;align-items:center;gap:32px}
.brand{display:flex;align-items:center;gap:8px;font-weight:600;font-size:15px;letter-spacing:-.02em;color:#fff}
.brand .tri{width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center}
.brand .tri svg{width:22px;height:22px;display:block;fill:#fff}
.nav-links{display:flex;list-style:none;gap:0;flex:1;margin:0;padding:0}
.nav-links li{padding:0 12px}
.nav-links a{color:var(--muted);font-size:14px;font-weight:400;letter-spacing:-.005em;display:inline-flex;align-items:center;gap:4px;transition:color .15s}
.nav-links a:hover{color:#fff}
.nav-links a .caret{font-size:9px;opacity:.6;transform:translateY(1px)}
.nav-utility{display:flex;gap:8px;align-items:center}
.nav-utility .log{color:var(--muted);font-size:14px;padding:7px 12px;transition:color .15s}
.nav-utility .log:hover{color:#fff}
.pill-white{background:#fff;color:#000;padding:7px 14px;border-radius:9999px;font-size:14px;font-weight:500;border:1px solid #fff;display:inline-flex;align-items:center;gap:4px;transition:background .15s,opacity .15s;cursor:pointer;font-family:inherit;text-decoration:none}
.pill-white:hover{background:#e5e5e5;color:#000;text-decoration:none}
.pill-outline{background:transparent;color:#fff;padding:7px 14px;border-radius:9999px;font-size:14px;font-weight:500;border:1px solid #333;display:inline-flex;align-items:center;gap:4px;transition:border-color .15s,background .15s;cursor:pointer;font-family:inherit;text-decoration:none}
.pill-outline:hover{border-color:#666;background:rgba(255,255,255,.04);color:#fff;text-decoration:none}
.nav-hamburger{display:none;background:none;border:none;color:#fff;font-size:20px;cursor:pointer;padding:6px}

/* HERO — Vercel huge gradient headline */
.hero{position:relative;padding:96px 24px 40px;text-align:center;max-width:1200px;margin:0 auto;overflow:hidden}
.hero::before{content:'';position:absolute;top:-200px;left:50%;transform:translateX(-50%);width:900px;height:600px;background:radial-gradient(ellipse 50% 60% at 50% 30%,rgba(121,40,202,.18) 0%,rgba(0,112,243,.10) 30%,transparent 70%);pointer-events:none;z-index:0}
.hero-inner{position:relative;z-index:1}
.eyebrow-mono{display:inline-block;font-family:'Geist Mono',monospace;font-size:13px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;margin-bottom:22px}
.hero h1{font-size:clamp(48px,8vw,108px);font-weight:700;line-height:.98;letter-spacing:-.05em;margin-bottom:24px;max-width:900px;margin-left:auto;margin-right:auto}
.hero h1 .gradient-text{display:inline}
.hero-sub{font-size:clamp(18px,2.2vw,22px);color:var(--muted);line-height:1.45;max-width:620px;margin:0 auto 36px;font-weight:400}
.hero-cta-row{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:64px}

/* DEPLOYMENT CARD — Vercel signature deploy mockup */
.deploy-card{max-width:880px;margin:0 auto;background:linear-gradient(180deg,#0a0a0a 0%,#000 100%);border:1px solid var(--border-2);border-radius:14px;overflow:hidden;box-shadow:0 0 0 1px rgba(255,255,255,.02),0 40px 80px -20px rgba(121,40,202,.18),0 20px 40px -10px rgba(0,0,0,.6);position:relative;text-align:left}
.deploy-card::before{content:'';position:absolute;inset:-1px;border-radius:14px;padding:1px;background:linear-gradient(135deg,rgba(255,0,128,.4),rgba(0,223,216,.2) 50%,transparent 80%);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.deploy-head{padding:14px 18px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.02)}
.dot-pulse{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 0 0 rgba(12,206,107,.6);animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(12,206,107,.5)}70%{box-shadow:0 0 0 10px rgba(12,206,107,0)}100%{box-shadow:0 0 0 0 rgba(12,206,107,0)}}
.deploy-branch{font-family:'Geist Mono',monospace;font-size:13px;color:#fff;letter-spacing:-.01em}
.deploy-branch .sha{color:var(--muted-2);margin-left:6px}
.deploy-status{margin-left:auto;font-family:'Geist Mono',monospace;font-size:12px;color:var(--green);background:rgba(12,206,107,.08);padding:3px 10px;border-radius:9999px;border:1px solid rgba(12,206,107,.18)}
.deploy-body{padding:8px 0}
.deploy-row{display:grid;grid-template-columns:14px 1fr auto auto auto;gap:14px;align-items:center;padding:11px 18px;border-bottom:1px solid var(--border);font-size:13px;transition:background .15s}
.deploy-row:hover{background:rgba(255,255,255,.02)}
.deploy-row:last-child{border-bottom:none}
.deploy-row .stat-dot{width:8px;height:8px;border-radius:50%;background:var(--green)}
.deploy-row.warn .stat-dot{background:#f5a623}
.deploy-row .msg{color:#fff;font-family:'Geist Mono',monospace;font-size:12.5px;letter-spacing:-.005em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.deploy-row .env{font-size:11px;background:rgba(255,255,255,.06);color:var(--muted);padding:2px 8px;border-radius:9999px;font-family:'Geist Mono',monospace;letter-spacing:.02em}
.deploy-row .env.prod{background:rgba(0,112,243,.12);color:#79bfff;border:1px solid rgba(0,112,243,.2)}
.deploy-row .author{font-family:'Geist Mono',monospace;font-size:12px;color:var(--muted-2)}
.deploy-row .time{font-family:'Geist Mono',monospace;font-size:12px;color:var(--muted-2)}

/* LOGO STRIP */
.trust-strip{padding:64px 24px 32px;text-align:center;border-top:1px solid var(--border);border-bottom:1px solid var(--border);background:var(--bg-1)}
.trust-label{font-size:13px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase;margin-bottom:28px;font-family:'Geist Mono',monospace}
.trust-logos{display:flex;justify-content:center;gap:48px;flex-wrap:wrap;align-items:center;max-width:1080px;margin:0 auto;opacity:.55}
.trust-logos span{font-size:18px;font-weight:600;color:#fff;letter-spacing:-.02em}

/* STATS */
.stats-band{padding:80px 24px;background:var(--bg)}
.stats-inner{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:48px;text-align:center}
.stat-num{font-size:clamp(40px,5.5vw,72px);font-weight:700;letter-spacing:-.04em;color:#fff;line-height:1;margin-bottom:8px;background:linear-gradient(90deg,#fff 0%,#999 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.stat-label{font-size:14px;color:var(--muted);letter-spacing:-.005em}

/* SECTION */
.section{padding:120px 24px;position:relative}
.section.alt{background:var(--bg-1);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.section-inner{max-width:1080px;margin:0 auto}
.section-head{max-width:680px;margin:0 auto 64px;text-align:center}
.section-eyebrow{display:inline-block;font-size:13px;color:var(--muted);font-family:'Geist Mono',monospace;letter-spacing:.04em;text-transform:uppercase;margin-bottom:16px}
.section-head h2{font-size:clamp(36px,5vw,60px);font-weight:600;letter-spacing:-.04em;line-height:1.05;color:#fff;margin-bottom:18px}
.section-head h2 .gradient-text{display:inline}
.section-head p{font-size:18px;color:var(--muted);line-height:1.5;font-weight:400}

/* BENEFITS — 2x2 grid, dark cards w/ gradient border on hover */
.benefits-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.benefit-card{background:var(--bg-1);border:1px solid var(--border-2);border-radius:12px;padding:36px 32px;position:relative;transition:background .2s,border-color .2s;overflow:hidden}
.benefit-card::before{content:'';position:absolute;inset:-1px;border-radius:12px;padding:1px;background:linear-gradient(135deg,var(--pink),var(--cyan));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:0;transition:opacity .25s;pointer-events:none}
.benefit-card:hover::before{opacity:1}
.benefit-card:hover{background:#0d0d0d}
.benefit-icon{width:40px;height:40px;border-radius:10px;background:rgba(255,255,255,.04);border:1px solid var(--border-2);color:#fff;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:24px}
.benefit-card h3{font-size:20px;font-weight:600;letter-spacing:-.02em;margin-bottom:8px;color:#fff;line-height:1.25}
.benefit-card p{font-size:15px;color:var(--muted);line-height:1.55;letter-spacing:-.005em}

/* CODE BLOCK — Vercel "Deploy in seconds" pattern */
.code-block{max-width:760px;margin:48px auto 0;background:var(--bg-1);border:1px solid var(--border-2);border-radius:12px;overflow:hidden;text-align:left;box-shadow:0 20px 40px -20px rgba(0,0,0,.6)}
.code-head{padding:10px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.02)}
.code-dot{width:11px;height:11px;border-radius:50%;background:#333}
.code-title{font-family:'Geist Mono',monospace;font-size:11px;color:var(--muted-2);margin-left:auto;letter-spacing:-.005em}
.code-body{padding:20px 22px;font-family:'Geist Mono',monospace;font-size:13.5px;line-height:1.7;color:#e4e4e7;overflow-x:auto}
.code-body .kw{color:var(--pink)}
.code-body .str{color:var(--green)}
.code-body .fn{color:#79bfff}
.code-body .com{color:var(--muted-2)}
.code-body .num{color:var(--cyan)}

/* HOW — numbered steps, sparse */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.step{padding:32px 28px;background:var(--bg-1);border:1px solid var(--border-2);border-radius:12px;position:relative}
.step-num{font-family:'Geist Mono',monospace;font-size:13px;color:var(--cyan);letter-spacing:.04em;margin-bottom:20px;text-transform:uppercase}
.step h3{font-size:19px;font-weight:600;letter-spacing:-.02em;margin-bottom:8px;color:#fff;line-height:1.3}
.step p{font-size:15px;color:var(--muted);line-height:1.55}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.review{padding:36px 32px;background:var(--bg-1);border:1px solid var(--border-2);border-radius:12px}
.review-quote{font-size:18px;color:#fff;line-height:1.5;font-weight:400;margin-bottom:24px;letter-spacing:-.012em}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,var(--pink),var(--purple),var(--blue));color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:600}
.review-name{font-size:14px;font-weight:500;color:#fff;letter-spacing:-.005em}
.review-role{font-size:13px;color:var(--muted);letter-spacing:-.005em}

/* FAQ */
.faq{max-width:760px;margin:0 auto;border-top:1px solid var(--border)}
.faq-item{border-bottom:1px solid var(--border)}
.faq-q{width:100%;text-align:left;background:none;border:none;padding:24px 0;font-size:17px;font-weight:500;letter-spacing:-.015em;color:#fff;cursor:pointer;font-family:inherit;display:flex;justify-content:space-between;align-items:center;line-height:1.4;gap:24px;transition:color .15s}
.faq-q:hover{color:#a1a1aa}
.faq-q::after{content:'+';font-size:22px;color:var(--muted);transition:transform .25s;flex-shrink:0;font-weight:400}
.faq-item.active .faq-q::after{transform:rotate(45deg);color:var(--cyan)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .25s;font-size:15px;color:var(--muted);line-height:1.65;letter-spacing:-.005em}
.faq-item.active .faq-a{max-height:600px;padding:0 0 24px}

/* CTA */
.cta-block{padding:120px 24px;text-align:center;position:relative;overflow:hidden;border-top:1px solid var(--border)}
.cta-block::before{content:'';position:absolute;top:50%;left:50%;width:800px;height:800px;background:radial-gradient(circle,rgba(121,40,202,.15) 0%,rgba(0,112,243,.08) 30%,transparent 70%);transform:translate(-50%,-50%);pointer-events:none}
.cta-inner{max-width:560px;margin:0 auto;position:relative;z-index:1}
.cta-inner h2{font-size:clamp(36px,5.5vw,60px);font-weight:600;letter-spacing:-.04em;line-height:1.05;margin-bottom:18px;color:#fff}
.cta-inner p{font-size:18px;color:var(--muted);line-height:1.5;margin-bottom:36px;letter-spacing:-.005em}
.cta-form{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:480px;margin:0 auto}
.cta-form input{padding:12px 14px;border-radius:8px;border:1px solid var(--border-2);background:rgba(255,255,255,.03);color:#fff;font-size:14px;font-family:inherit;outline:none;letter-spacing:-.005em;transition:border-color .15s,background .15s}
.cta-form input::placeholder{color:var(--muted-2)}
.cta-form input:focus{border-color:#fff;background:rgba(255,255,255,.05)}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:1/-1}
.cta-form button{grid-column:1/-1;padding:13px 24px;border-radius:9999px;border:none;background:#fff;color:#000;font-size:15px;font-weight:500;cursor:pointer;font-family:inherit;letter-spacing:-.005em;transition:background .15s,transform .15s;margin-top:8px}
.cta-form button:hover{background:#e5e5e5;transform:translateY(-1px)}

/* FOOTER */
.footer{padding:80px 24px 40px;border-top:1px solid var(--border);background:#000}
.footer-inner{max-width:1280px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px;border-bottom:1px solid var(--border)}
.footer-brand-block{max-width:280px}
.footer-brand-block .brand{font-size:15px;margin-bottom:14px}
.footer-tag{font-size:13px;color:var(--muted);line-height:1.55;letter-spacing:-.005em}
.footer-col h4{font-size:13px;font-weight:500;color:#fff;margin-bottom:14px;letter-spacing:-.005em}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:10px}
.footer-col a{color:var(--muted);font-size:13px;letter-spacing:-.005em;transition:color .15s}
.footer-col a:hover{color:#fff;text-decoration:none}
.footer-bot{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding-top:32px;font-size:12px;color:var(--muted)}
.footer-bot a{color:var(--muted)}
.footer-bot a:hover{color:#fff;text-decoration:none}
.footer-made{display:flex;align-items:center;gap:6px;color:var(--muted)}
.footer-made svg{width:11px;height:11px;fill:#fff;opacity:.8}

@media(max-width:900px){
.benefits-grid{grid-template-columns:1fr}
.reviews-grid{grid-template-columns:1fr}
.steps{grid-template-columns:1fr}
.stats-inner{grid-template-columns:1fr;gap:36px}
.footer-top{grid-template-columns:1fr 1fr;gap:32px}
.trust-logos{gap:24px}
.deploy-row{grid-template-columns:14px 1fr auto;gap:10px}
.deploy-row .env,.deploy-row .author{display:none}
}
@media(max-width:640px){
.nav-links,.nav-utility{display:none}
.nav-hamburger{display:block;margin-left:auto}
.nav-inner{padding:0 18px;gap:0;height:56px}
.hero{padding:60px 18px 32px}
.hero h1{font-size:42px;letter-spacing:-.03em}
.hero-sub{font-size:16px}
.hero-cta-row{gap:8px;margin-bottom:40px}
.deploy-card{margin:0 -4px;border-radius:10px}
.deploy-head{padding:10px 14px}
.deploy-row{padding:10px 14px}
.cta-form{grid-template-columns:1fr}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:auto}
.section{padding:72px 18px}
.cta-block{padding:72px 18px}
.benefit-card{padding:28px 22px}
.footer{padding:48px 18px 32px}
.footer-top{grid-template-columns:1fr 1fr;gap:24px}
.code-body{font-size:12px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="brand"><span class="tri"><svg viewBox="0 0 76 65" xmlns="http://www.w3.org/2000/svg"><path d="M37.5274 0L75.0548 65H0L37.5274 0Z"/></svg></span>Vercel</a>
<ul class="nav-links">
<li><a href="#">Products<span class="caret">&#9662;</span></a></li>
<li><a href="#">Solutions<span class="caret">&#9662;</span></a></li>
<li><a href="#">Resources<span class="caret">&#9662;</span></a></li>
<li><a href="#">Enterprise</a></li>
<li><a href="#">Docs</a></li>
<li><a href="#">Pricing</a></li>
</ul>
<div class="nav-utility">
<a href="#" class="log">Log In</a>
<a href="#form" class="pill-white">Sign Up</a>
<a href="#" class="pill-outline">Contact</a>
</div>
<button class="nav-hamburger" aria-label="Menu">&#9776;</button>
</div></nav>

<!-- HERO -->
<section class="hero" id="hero"><div class="hero-inner">
<span class="eyebrow-mono">{{BADGE}}</span>
<h1><span class="gradient-text">{{HERO_TITLE}}</span></h1>
<p class="hero-sub">{{HERO_SUBTITLE}}</p>
<div class="hero-cta-row">
<a href="#form" class="pill-white">{{CTA_BUTTON}} &rarr;</a>
<a href="#benefits" class="pill-outline">Get a Demo</a>
</div>

<!-- DEPLOYMENT CARD MOCKUP -->
<div class="deploy-card">
<div class="deploy-head">
<span class="dot-pulse"></span>
<span class="deploy-branch">main <span class="sha">&middot; 7a3f9b2</span></span>
<span class="deploy-status">&#10003; Ready</span>
</div>
<div class="deploy-body">
<div class="deploy-row"><span class="stat-dot"></span><span class="msg">feat: ship landing page generator v2</span><span class="env prod">Production</span><span class="author">@enderj</span><span class="time">12s ago</span></div>
<div class="deploy-row"><span class="stat-dot"></span><span class="msg">chore: bump dependencies to latest</span><span class="env">Preview</span><span class="author">@team</span><span class="time">4m ago</span></div>
<div class="deploy-row"><span class="stat-dot"></span><span class="msg">fix: resolve hydration mismatch on hero</span><span class="env">Preview</span><span class="author">@enderj</span><span class="time">28m ago</span></div>
<div class="deploy-row warn"><span class="stat-dot"></span><span class="msg">refactor: simplify analytics tracker</span><span class="env">Preview</span><span class="author">@bot</span><span class="time">2h ago</span></div>
</div>
</div>
</div></section>

<!-- TRUST STRIP -->
<div class="trust-strip">
<div class="trust-label">Trusted by the best front-end teams</div>
<div class="trust-logos">
<span>WASHINGTON POST</span><span>HASHICORP</span><span>NOTION</span><span>SUPABASE</span><span>RUNWAY</span><span>NETFLIX</span><span>STRIPE</span>
</div>
</div>

<!-- STATS -->
<section class="stats-band"><div class="stats-inner">
<div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></section>

<!-- BENEFITS -->
<section class="section alt" id="benefits"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow">Platform</div>
<h2><span class="gradient-text">{{BENEFITS_HEADLINE}}</span></h2>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>
<div class="benefits-grid">
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div>

<!-- CODE BLOCK -->
<div class="code-block">
<div class="code-head"><span class="code-dot"></span><span class="code-dot"></span><span class="code-dot"></span><span class="code-title">~/project &middot; npm i</span></div>
<div class="code-body"><span class="com">// 1. Install &mdash; 2. Deploy &mdash; 3. Done.</span><br>
<span class="kw">npm</span> <span class="fn">install</span> <span class="str">"@eko/landing"</span><br>
<span class="kw">import</span> { <span class="fn">deploy</span> } <span class="kw">from</span> <span class="str">"@eko/landing"</span>;<br>
<span class="kw">await</span> <span class="fn">deploy</span>({ region: <span class="str">"global"</span>, instant: <span class="num">true</span> });<br>
<span class="com">// &rarr; https://your-app.eko.app</span></div>
</div>
</div></section>

<!-- HOW -->
<section class="section" id="how"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow">Workflow</div>
<h2><span class="gradient-text">{{HOW_HEADLINE}}</span></h2>
<p>{{HOW_SUBHEADLINE}}</p>
</div>
<div class="steps">
<div class="step"><div class="step-num">01 &middot; PUSH</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">02 &middot; PREVIEW</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">03 &middot; SHIP</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>

<!-- REVIEWS -->
<section class="section alt" id="reviews"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow">Customers</div>
<h2><span class="gradient-text">{{REVIEWS_HEADLINE}}</span></h2>
<p>{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-grid">
<div class="review"><div class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div></div></div>
<div class="review"><div class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div></div></div>
</div>
</div></section>

<!-- FAQ -->
<section class="section" id="faq"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow">FAQ</div>
<h2><span class="gradient-text">{{FAQ_HEADLINE}}</span></h2>
<p>{{FAQ_SUBHEADLINE}}</p>
</div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<!-- CTA -->
<section class="cta-block" id="form"><div class="cta-inner">
<h2><span class="gradient-text">{{FOOTER_HEADLINE}}</span></h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}} &rarr;</button>
</form>
</div></section>

<!-- FOOTER -->
<footer class="footer"><div class="footer-inner">
<div class="footer-top">
<div class="footer-brand-block">
<a href="#" class="brand"><span class="tri"><svg viewBox="0 0 76 65" xmlns="http://www.w3.org/2000/svg"><path d="M37.5274 0L75.0548 65H0L37.5274 0Z"/></svg></span>Vercel</a>
<p class="footer-tag" style="margin-top:14px">The complete platform to build, scale, and secure a faster, more personalized web.</p>
</div>
<div class="footer-col"><h4>Products</h4><ul><li><a href="#">AI</a></li><li><a href="#">Enterprise</a></li><li><a href="#">Fluid Compute</a></li><li><a href="#">Next.js</a></li><li><a href="#">Observability</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#">Customers</a></li><li><a href="#">Docs</a></li><li><a href="#">Blog</a></li><li><a href="#">Templates</a></li><li><a href="#">Guides</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Careers</a></li><li><a href="#">Changelog</a></li><li><a href="#">Press</a></li><li><a href="#">Partners</a></li></ul></div>
<div class="footer-col"><h4>Legal</h4><ul><li><a href="#">Privacy Policy</a></li><li><a href="#">Terms</a></li><li><a href="#">DPA</a></li><li><a href="#">Cookie Policy</a></li></ul></div>
<div class="footer-col"><h4>Support</h4><ul><li><a href="#">Help</a></li><li><a href="#">Contact</a></li><li><a href="#">Status</a></li><li><a href="#">Security</a></li></ul></div>
</div>
<div class="footer-bot">
<div class="footer-made">Made with <svg viewBox="0 0 76 65" xmlns="http://www.w3.org/2000/svg"><path d="M37.5274 0L75.0548 65H0L37.5274 0Z"/></svg> Vercel &middot; &copy; {{YEAR}} Eko AI Inc.</div>
<div><a href="#">Twitter</a> &nbsp;&middot;&nbsp; <a href="#">GitHub</a> &nbsp;&middot;&nbsp; <a href="#">YouTube</a></div>
</div>
</div></footer>
__FORM_SUBMIT_JS__
</body></html>
"""

# ─── GitHub Dark ─────────────────────────────────────────────────────────────
_TPL_GITHUB_DARK = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0d1117;
  --bg-1:#010409;
  --bg-2:#161b22;
  --bg-card:#0d1117;
  --text:#c9d1d9;
  --text-bright:#f0f6fc;
  --muted:#8b949e;
  --muted-2:#6e7681;
  --border:#30363d;
  --border-soft:#21262d;
  --green:#238636;
  --green-h:#2ea043;
  --green-soft:rgba(35,134,54,.15);
  --blue:#1f6feb;
  --blue-soft:rgba(31,111,235,.15);
  --add:#3fb950;
  --del:#f85149;
}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif,'Apple Color Emoji','Segoe UI Emoji';background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;font-weight:400;min-height:100vh}
a{color:var(--blue);text-decoration:none;transition:color .15s}
a:hover{color:#58a6ff;text-decoration:underline}
.mono{font-family:'SFMono-Regular','Consolas','Liberation Mono','Menlo',monospace}

/* NAV — GitHub signature dark header */
.nav{position:sticky;top:0;z-index:9999;background:rgba(13,17,23,.95);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1280px;margin:0 auto;padding:0 24px;height:64px;display:flex;align-items:center;gap:16px}
.brand{display:flex;align-items:center;gap:0;color:var(--text-bright);font-weight:600;font-size:16px;flex-shrink:0}
.brand .octo{width:32px;height:32px;display:inline-block}
.brand .octo svg{width:32px;height:32px;display:block;fill:#fff}
.nav-search{display:flex;align-items:center;background:var(--bg-1);border:1px solid var(--border);border-radius:6px;padding:5px 12px;height:30px;gap:8px;width:280px;font-size:14px;color:var(--muted)}
.nav-search input{background:none;border:none;outline:none;color:var(--text);font-family:inherit;font-size:14px;flex:1;width:100%}
.nav-search input::placeholder{color:var(--muted)}
.nav-search .kbd{font-family:'SFMono-Regular',monospace;font-size:11px;color:var(--muted);border:1px solid var(--border);border-radius:3px;padding:1px 6px}
.nav-links{display:flex;list-style:none;gap:0;flex:1;margin:0;padding:0}
.nav-links li{padding:0 8px}
.nav-links a{color:var(--text-bright);font-size:14px;font-weight:600;display:inline-flex;align-items:center;gap:4px;letter-spacing:-.005em}
.nav-links a:hover{color:var(--text);text-decoration:none}
.nav-links .caret{font-size:9px;opacity:.7;margin-left:2px}
.nav-utility{display:flex;gap:14px;align-items:center}
.nav-utility .signin{color:var(--text-bright);font-size:14px;font-weight:400}
.nav-utility .signin:hover{color:var(--blue);text-decoration:none}
.btn-green{background:var(--green);color:#fff;padding:5px 16px;border-radius:6px;font-size:14px;font-weight:500;border:1px solid rgba(240,246,252,.1);display:inline-flex;align-items:center;gap:6px;transition:background .15s;cursor:pointer;font-family:inherit;text-decoration:none}
.btn-green:hover{background:var(--green-h);color:#fff;text-decoration:none}
.btn-outline{background:var(--bg-2);color:var(--text-bright);padding:5px 16px;border-radius:6px;font-size:14px;font-weight:500;border:1px solid var(--border);display:inline-flex;align-items:center;gap:6px;cursor:pointer;font-family:inherit;text-decoration:none;transition:background .15s}
.btn-outline:hover{background:#21262d;color:var(--text-bright);text-decoration:none;border-color:#8b949e}
.nav-hamburger{display:none;background:none;border:none;color:var(--text-bright);font-size:22px;cursor:pointer;padding:6px;margin-left:auto}

/* HERO */
.hero{position:relative;padding:96px 24px 72px;text-align:center;max-width:1080px;margin:0 auto;overflow:hidden}
.hero::before{content:'';position:absolute;top:-300px;left:50%;transform:translateX(-50%);width:1200px;height:700px;background:radial-gradient(ellipse 50% 60% at 50% 40%,rgba(35,134,54,.10) 0%,rgba(31,111,235,.06) 40%,transparent 70%);pointer-events:none;z-index:0}
.hero-inner{position:relative;z-index:1}
.hero-eyebrow{display:inline-flex;align-items:center;gap:8px;background:rgba(35,134,54,.08);border:1px solid rgba(35,134,54,.2);color:#7ee787;padding:6px 14px;border-radius:9999px;font-size:13px;font-weight:500;letter-spacing:.005em;margin-bottom:24px}
.hero-eyebrow .dot{width:6px;height:6px;border-radius:50%;background:var(--add);box-shadow:0 0 6px rgba(63,185,80,.6)}
.hero h1{font-size:clamp(40px,6vw,72px);font-weight:700;line-height:1.05;letter-spacing:-.04em;color:var(--text-bright);margin-bottom:24px;max-width:900px;margin-left:auto;margin-right:auto}
.hero-sub{font-size:clamp(17px,1.8vw,21px);color:var(--muted);line-height:1.5;max-width:580px;margin:0 auto 36px;font-weight:400}

/* HERO SIGNUP — GitHub's email + green pill pattern */
.hero-signup{display:flex;gap:8px;justify-content:center;max-width:520px;margin:0 auto 64px;flex-wrap:wrap}
.hero-signup input{padding:10px 14px;border:1px solid var(--border);border-radius:6px;background:var(--bg-1);color:var(--text);font-size:14px;font-family:inherit;outline:none;min-width:260px;flex:1;transition:border-color .15s,box-shadow .15s}
.hero-signup input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(31,111,235,.3)}
.hero-signup input::placeholder{color:var(--muted)}
.hero-signup .btn-green{padding:10px 18px;font-size:14px}

/* REPO CARD MOCKUP — GitHub signature */
.repo-card{max-width:920px;margin:0 auto;background:var(--bg);border:1px solid var(--border);border-radius:6px;overflow:hidden;text-align:left;box-shadow:0 16px 40px -20px rgba(0,0,0,.8)}
.repo-head{padding:14px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;flex-wrap:wrap;background:var(--bg)}
.repo-name{font-size:18px;font-weight:400;display:flex;align-items:center;gap:4px;color:var(--text-bright)}
.repo-name .ic{color:var(--muted);font-size:14px}
.repo-name .owner{color:var(--blue);font-weight:400}
.repo-name .slash{color:var(--muted);margin:0 4px}
.repo-name .name{color:var(--blue);font-weight:600}
.repo-pill{font-size:12px;background:transparent;color:var(--muted);padding:0 7px;border-radius:9999px;border:1px solid var(--border);height:20px;line-height:18px}
.repo-actions{margin-left:auto;display:flex;gap:6px}
.repo-action-btn{display:inline-flex;align-items:center;gap:6px;background:var(--bg-2);color:var(--text-bright);padding:3px 12px;border-radius:6px;border:1px solid var(--border);font-size:12px;font-weight:500}
.repo-action-btn .count{background:var(--bg-1);border:1px solid var(--border);padding:0 6px;border-radius:9999px;font-size:11px;color:var(--text);margin-left:4px}
.repo-body{display:grid;grid-template-columns:1fr 280px;min-height:300px}
.repo-files{border-right:1px solid var(--border)}
.repo-file-head{padding:10px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;background:var(--bg-2);font-size:13px;color:var(--text)}
.repo-branch-pill{background:transparent;border:1px solid var(--border);color:var(--text);padding:3px 10px;border-radius:6px;font-size:12px;display:inline-flex;align-items:center;gap:4px}
.repo-commit-info{font-size:12px;color:var(--muted);display:flex;align-items:center;gap:8px;margin-left:auto}
.repo-commit-info .sha{font-family:'SFMono-Regular',monospace;color:var(--muted)}
.repo-file-row{display:grid;grid-template-columns:18px 1fr auto auto;gap:14px;align-items:center;padding:8px 16px;border-bottom:1px solid var(--border-soft);font-size:13px;transition:background .15s}
.repo-file-row:hover{background:var(--bg-2)}
.repo-file-row:last-child{border-bottom:none}
.repo-file-row .ic{color:var(--muted);font-size:14px;line-height:1}
.repo-file-row .ic.dir{color:#79c0ff}
.repo-file-row .fname{color:var(--blue);font-size:13.5px}
.repo-file-row .fmsg{color:var(--muted);font-size:12px;text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:240px}
.repo-file-row .ftime{color:var(--muted);font-size:12px;font-family:'SFMono-Regular',monospace;flex-shrink:0}
.repo-side{background:var(--bg);padding:16px 18px;font-size:12px}
.repo-side h4{font-size:13px;font-weight:600;color:var(--text-bright);margin-bottom:8px}
.repo-side p{font-size:12px;color:var(--muted);line-height:1.5;margin-bottom:16px}
.repo-side .commit{margin-top:18px;padding-top:14px;border-top:1px solid var(--border-soft);font-family:'SFMono-Regular',monospace;font-size:11.5px;line-height:1.65}
.repo-side .commit .add{color:var(--add)}
.repo-side .commit .del{color:var(--del)}
.repo-side .commit .line{display:flex;align-items:center;gap:6px;color:var(--muted-2)}

/* STATS — big green numbers */
.stats-band{padding:80px 24px;background:var(--bg-2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.stats-inner{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:48px;text-align:center}
.stat-num{font-size:clamp(40px,5.5vw,72px);font-weight:700;letter-spacing:-.04em;color:var(--add);line-height:1;margin-bottom:8px}
.stat-label{font-size:15px;color:var(--muted);letter-spacing:-.005em}

/* SECTION */
.section{padding:96px 24px;position:relative}
.section.alt{background:var(--bg-2)}
.section-inner{max-width:1080px;margin:0 auto}
.section-head{max-width:680px;margin:0 auto 56px;text-align:center}
.section-eyebrow{display:inline-block;font-size:13px;color:#7ee787;font-family:'SFMono-Regular',monospace;letter-spacing:.04em;text-transform:uppercase;margin-bottom:14px}
.section-head h2{font-size:clamp(32px,4.5vw,52px);font-weight:700;letter-spacing:-.035em;line-height:1.1;color:var(--text-bright);margin-bottom:16px}
.section-head p{font-size:18px;color:var(--muted);line-height:1.5;font-weight:400}

/* BENEFITS — 2x2 grid */
.benefits-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.benefit-card{background:var(--bg-card);border:1px solid var(--border);border-radius:6px;padding:32px 28px;transition:border-color .15s,background .15s}
.benefit-card:hover{border-color:#8b949e}
.benefit-icon{width:44px;height:44px;border-radius:8px;background:var(--green-soft);border:1px solid rgba(35,134,54,.3);color:#7ee787;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:20px}
.benefit-card h3{font-size:20px;font-weight:600;letter-spacing:-.015em;margin-bottom:8px;color:var(--text-bright);line-height:1.3}
.benefit-card p{font-size:15px;color:var(--muted);line-height:1.55}

/* HOW — 3 steps */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:1px solid var(--border);border-radius:6px;overflow:hidden;background:var(--bg-card)}
.step{padding:32px 28px;border-left:1px solid var(--border)}
.step:first-child{border-left:none}
.step-num{font-family:'SFMono-Regular',monospace;font-size:13px;color:#7ee787;letter-spacing:.04em;margin-bottom:18px;display:inline-flex;align-items:center;gap:6px}
.step-num::before{content:'$';color:var(--muted-2)}
.step h3{font-size:18px;font-weight:600;letter-spacing:-.012em;margin-bottom:8px;color:var(--text-bright);line-height:1.3}
.step p{font-size:15px;color:var(--muted);line-height:1.55}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.review{padding:32px 30px;background:var(--bg-card);border:1px solid var(--border);border-radius:6px}
.review-quote{font-size:17px;color:var(--text);line-height:1.55;font-weight:400;margin-bottom:22px;letter-spacing:-.005em}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#3fb950,#1f6feb);color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:600;border:1px solid var(--border)}
.review-name{font-size:14px;font-weight:600;color:var(--text-bright);letter-spacing:-.005em}
.review-role{font-size:13px;color:var(--muted);letter-spacing:-.005em}

/* FAQ */
.faq{max-width:760px;margin:0 auto;border:1px solid var(--border);border-radius:6px;overflow:hidden;background:var(--bg-card)}
.faq-item{border-bottom:1px solid var(--border)}
.faq-item:last-child{border-bottom:none}
.faq-q{width:100%;text-align:left;background:none;border:none;padding:20px 24px;font-size:16px;font-weight:600;letter-spacing:-.005em;color:var(--text-bright);cursor:pointer;font-family:inherit;display:flex;justify-content:space-between;align-items:center;line-height:1.4;gap:24px;transition:background .15s}
.faq-q:hover{background:var(--bg-2)}
.faq-q::after{content:'+';font-size:20px;color:var(--muted);transition:transform .25s;flex-shrink:0;font-weight:400}
.faq-item.active .faq-q::after{transform:rotate(45deg);color:var(--add)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .25s;font-size:15px;color:var(--muted);line-height:1.65}
.faq-item.active .faq-a{max-height:600px;padding:0 24px 22px}

/* CTA */
.cta-block{padding:96px 24px;text-align:center;position:relative;background:var(--bg-2);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.cta-inner{max-width:560px;margin:0 auto}
.cta-inner h2{font-size:clamp(32px,5vw,48px);font-weight:700;letter-spacing:-.035em;line-height:1.1;margin-bottom:16px;color:var(--text-bright)}
.cta-inner p{font-size:17px;color:var(--muted);line-height:1.5;margin-bottom:32px}
.cta-form{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:480px;margin:0 auto}
.cta-form input{padding:10px 14px;border-radius:6px;border:1px solid var(--border);background:var(--bg-1);color:var(--text);font-size:14px;font-family:inherit;outline:none;transition:border-color .15s,box-shadow .15s}
.cta-form input::placeholder{color:var(--muted)}
.cta-form input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(31,111,235,.3)}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:1/-1}
.cta-form button{grid-column:1/-1;padding:12px 24px;border-radius:6px;border:1px solid rgba(240,246,252,.1);background:var(--green);color:#fff;font-size:14px;font-weight:500;cursor:pointer;font-family:inherit;transition:background .15s;margin-top:6px}
.cta-form button:hover{background:var(--green-h)}

/* FOOTER */
.footer{padding:64px 24px 32px;background:var(--bg);border-top:1px solid var(--border)}
.footer-inner{max-width:1280px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px;border-bottom:1px solid var(--border)}
.footer-brand-block{max-width:280px}
.footer-tag{font-size:12px;color:var(--muted);line-height:1.55;margin-top:12px}
.footer-col h4{font-size:14px;font-weight:600;color:var(--text-bright);margin-bottom:14px}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:8px}
.footer-col a{color:var(--muted);font-size:13px}
.footer-col a:hover{color:var(--blue);text-decoration:none}
.footer-bot{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding-top:24px;font-size:12px;color:var(--muted);align-items:center}
.footer-bot .octo-bot{width:24px;height:24px}
.footer-bot .octo-bot svg{width:24px;height:24px;fill:var(--muted)}

@media(max-width:900px){
.nav-search{display:none}
.nav-links{display:none}
.benefits-grid,.reviews-grid{grid-template-columns:1fr}
.steps{grid-template-columns:1fr}
.step{border-left:none;border-top:1px solid var(--border)}
.step:first-child{border-top:none}
.stats-inner{grid-template-columns:1fr;gap:36px}
.footer-top{grid-template-columns:1fr 1fr;gap:32px}
.repo-body{grid-template-columns:1fr}
.repo-side{border-top:1px solid var(--border);border-right:none}
}
@media(max-width:640px){
.nav-utility .signin,.nav-utility .btn-outline{display:none}
.nav-hamburger{display:block}
.nav-inner{padding:0 16px;gap:10px;height:56px}
.hero{padding:48px 18px 48px}
.hero h1{font-size:36px;letter-spacing:-.03em}
.hero-sub{font-size:16px}
.hero-signup{flex-direction:column}
.hero-signup input{min-width:0}
.hero-signup .btn-green{width:100%;justify-content:center}
.section{padding:64px 18px}
.cta-block{padding:64px 18px}
.cta-form{grid-template-columns:1fr}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:auto}
.footer{padding:48px 18px 32px}
.footer-top{grid-template-columns:1fr 1fr;gap:24px}
.repo-file-row{grid-template-columns:18px 1fr auto;gap:10px}
.repo-file-row .ftime{display:none}
.repo-actions{display:none}
.benefit-card{padding:24px 22px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="brand"><span class="octo"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg></span></a>
<div class="nav-search"><span>&#128269;</span><input type="text" placeholder="Search or jump to..." aria-label="Search"><span class="kbd">/</span></div>
<ul class="nav-links">
<li><a href="#">Product<span class="caret">&#9662;</span></a></li>
<li><a href="#">Solutions<span class="caret">&#9662;</span></a></li>
<li><a href="#">Resources<span class="caret">&#9662;</span></a></li>
<li><a href="#">Open Source<span class="caret">&#9662;</span></a></li>
<li><a href="#">Enterprise</a></li>
<li><a href="#">Pricing</a></li>
</ul>
<div class="nav-utility">
<a href="#" class="signin">Sign in</a>
<a href="#form" class="btn-green">Sign up</a>
<a href="#" class="btn-outline">Contact Sales</a>
</div>
<button class="nav-hamburger" aria-label="Menu">&#9776;</button>
</div></nav>

<!-- HERO -->
<section class="hero" id="hero"><div class="hero-inner">
<div class="hero-eyebrow"><span class="dot"></span>{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="hero-sub">{{HERO_SUBTITLE}}</p>

<form class="hero-signup" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST" onsubmit="event.preventDefault();document.querySelector('#form').scrollIntoView({behavior:'smooth'});return false;">
<input type="email" placeholder="Email address" aria-label="Email">
<button type="button" class="btn-green" onclick="document.querySelector('#form').scrollIntoView({behavior:'smooth'})">{{CTA_BUTTON}}</button>
</form>

<!-- REPO CARD MOCKUP -->
<div class="repo-card">
<div class="repo-head">
<div class="repo-name"><span class="ic">&#128193;</span><span class="owner">eko-ai</span><span class="slash">/</span><span class="name">landing-platform</span><span class="repo-pill">Public</span></div>
<div class="repo-actions">
<span class="repo-action-btn">&#128065; Watch<span class="count">1.2k</span></span>
<span class="repo-action-btn">&#9741; Fork<span class="count">340</span></span>
<span class="repo-action-btn">&#9733; Star<span class="count">42.8k</span></span>
</div>
</div>
<div class="repo-body">
<div class="repo-files">
<div class="repo-file-head">
<span class="repo-branch-pill">&#11138; main</span>
<span class="repo-commit-info"><span class="sha">7a3f9b2</span> &middot; 2 hours ago &middot; 1,847 commits</span>
</div>
<div class="repo-file-row"><span class="ic dir">&#128193;</span><span class="fname">src</span><span class="fmsg">feat: add landing page generator</span><span class="ftime">2h ago</span></div>
<div class="repo-file-row"><span class="ic dir">&#128193;</span><span class="fname">templates</span><span class="fmsg">ship 4 new brand templates</span><span class="ftime">2h ago</span></div>
<div class="repo-file-row"><span class="ic dir">&#128193;</span><span class="fname">tests</span><span class="fmsg">cover regression for placeholders</span><span class="ftime">5h ago</span></div>
<div class="repo-file-row"><span class="ic">&#128196;</span><span class="fname">.gitignore</span><span class="fmsg">chore: ignore .env</span><span class="ftime">4d ago</span></div>
<div class="repo-file-row"><span class="ic">&#128196;</span><span class="fname">README.md</span><span class="fmsg">docs: update quick start</span><span class="ftime">1d ago</span></div>
<div class="repo-file-row"><span class="ic">&#128196;</span><span class="fname">package.json</span><span class="fmsg">chore: bump deps to latest</span><span class="ftime">2d ago</span></div>
<div class="repo-file-row"><span class="ic">&#128196;</span><span class="fname">LICENSE</span><span class="fmsg">initial commit</span><span class="ftime">1y ago</span></div>
</div>
<div class="repo-side">
<h4>About</h4>
<p>Production-grade landing page generator. Brand templates, placeholder schema, instant deploy.</p>
<h4 style="margin-top:16px">Languages</h4>
<div style="display:flex;height:8px;border-radius:3px;overflow:hidden;background:var(--border-soft);margin-bottom:8px">
<div style="width:48%;background:#3178c6"></div><div style="width:32%;background:#f7df1e"></div><div style="width:20%;background:#7ee787"></div>
</div>
<p style="font-size:11px;margin:0"><span style="color:#79c0ff">&#9679; TypeScript</span> 48% &middot; <span style="color:#f7df1e">&#9679; JS</span> 32% &middot; <span style="color:#7ee787">&#9679; Python</span> 20%</p>
<div class="commit">
<div class="line"><span class="add">+ 248</span> <span class="del">- 32</span> &nbsp; landing.tsx</div>
<div class="line"><span class="add">+ 96</span> <span class="del">- 4</span> &nbsp; placeholders.ts</div>
<div class="line"><span class="add">+ 184</span> <span class="del">- 0</span> &nbsp; brands/vercel.ts</div>
</div>
</div>
</div>
</div>
</div></section>

<!-- STATS -->
<section class="stats-band"><div class="stats-inner">
<div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></section>

<!-- BENEFITS -->
<section class="section" id="benefits"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow"># BUILT FOR DEVELOPERS</div>
<h2>{{BENEFITS_HEADLINE}}</h2>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>
<div class="benefits-grid">
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div>
</div></section>

<!-- HOW -->
<section class="section alt" id="how"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow"># WORKFLOW</div>
<h2>{{HOW_HEADLINE}}</h2>
<p>{{HOW_SUBHEADLINE}}</p>
</div>
<div class="steps">
<div class="step"><div class="step-num"> clone</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num"> commit</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num"> push</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>

<!-- REVIEWS -->
<section class="section" id="reviews"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow"># LOVED BY DEVELOPERS</div>
<h2>{{REVIEWS_HEADLINE}}</h2>
<p>{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-grid">
<div class="review"><div class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div></div></div>
<div class="review"><div class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div></div></div>
</div>
</div></section>

<!-- FAQ -->
<section class="section alt" id="faq"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow"># FAQ</div>
<h2>{{FAQ_HEADLINE}}</h2>
<p>{{FAQ_SUBHEADLINE}}</p>
</div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<!-- CTA -->
<section class="cta-block" id="form"><div class="cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div></section>

<!-- FOOTER -->
<footer class="footer"><div class="footer-inner">
<div class="footer-top">
<div class="footer-brand-block">
<a href="#" class="brand"><span class="octo"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path fill="#8b949e" d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg></span></a>
<p class="footer-tag">Subscribe to our developer newsletter. Get tips, technical guides, and best practices.</p>
</div>
<div class="footer-col"><h4>Product</h4><ul><li><a href="#">Features</a></li><li><a href="#">Enterprise</a></li><li><a href="#">Copilot</a></li><li><a href="#">Security</a></li><li><a href="#">Actions</a></li></ul></div>
<div class="footer-col"><h4>Platform</h4><ul><li><a href="#">Developer API</a></li><li><a href="#">Partners</a></li><li><a href="#">Atom</a></li><li><a href="#">Electron</a></li><li><a href="#">GitHub Desktop</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#">Docs</a></li><li><a href="#">Roadmap</a></li><li><a href="#">Status</a></li><li><a href="#">Skills</a></li><li><a href="#">Blog</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Customer stories</a></li><li><a href="#">Newsroom</a></li><li><a href="#">Careers</a></li><li><a href="#">Diversity</a></li></ul></div>
</div>
<div class="footer-bot">
<div>&copy; {{YEAR}} Eko AI Inc. &nbsp;&middot;&nbsp; <a href="#" style="color:var(--muted)">Terms</a> &nbsp;&middot;&nbsp; <a href="#" style="color:var(--muted)">Privacy</a> &nbsp;&middot;&nbsp; <a href="#" style="color:var(--muted)">Sitemap</a> &nbsp;&middot;&nbsp; <a href="#" style="color:var(--muted)">Status</a></div>
<div class="octo-bot"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg></div>
</div>
</div></footer>
__FORM_SUBMIT_JS__
</body></html>
"""

# ─── Discord Vibrant ─────────────────────────────────────────────────────────────
_TPL_DISCORD_VIBRANT = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#5865F2;
  --blurple:#5865F2;
  --blurple-light:#7983F5;
  --blurple-dark:#4752C4;
  --blurple-pale:#EEF0FE;
  --dark:#23272a;
  --dark-2:#2c2f33;
  --white:#fff;
  --text:#23272a;
  --text-on-blurple:#fff;
  --muted-on-blurple:#dbdee1;
  --muted:#4f5660;
  --green:#43b581;
  --red:#f04747;
  --yellow:#faa61a;
}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:'gg sans','Noto Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;font-weight:400;min-height:100vh}
a{color:inherit;text-decoration:none;transition:color .15s,opacity .15s}

/* NAV — Blurple bg, white wordmark + nav links + white pill */
.nav{position:sticky;top:0;z-index:9999;background:var(--blurple);padding:16px 0}
.nav-inner{max-width:1260px;margin:0 auto;padding:0 40px;display:flex;align-items:center;gap:32px;height:48px}
.brand{display:flex;align-items:center;gap:8px;color:#fff;font-weight:800;font-size:22px;letter-spacing:-.01em;flex-shrink:0}
.brand .mascot{width:36px;height:28px;display:inline-flex;align-items:center;justify-content:center}
.brand .mascot svg{width:36px;height:28px;display:block;fill:#fff}
.nav-links{display:flex;list-style:none;gap:0;flex:1;justify-content:center;margin:0;padding:0}
.nav-links li{padding:0 14px}
.nav-links a{color:#fff;font-size:15px;font-weight:500;letter-spacing:.005em;transition:color .15s}
.nav-links a:hover{color:var(--blurple-pale);text-decoration:underline}
.nav-utility{display:flex;gap:14px;align-items:center}
.nav-utility .open-browser{color:#fff;font-size:14px;font-weight:500;text-decoration:underline}
.nav-utility .open-browser:hover{opacity:.85}
.pill-white{background:#fff;color:var(--blurple);padding:8px 18px;border-radius:9999px;font-size:14px;font-weight:600;border:none;display:inline-flex;align-items:center;gap:6px;transition:background .15s,color .15s,transform .15s;cursor:pointer;font-family:inherit;text-decoration:none;box-shadow:0 1px 0 rgba(0,0,0,.1)}
.pill-white:hover{background:#f6f6f6;color:var(--blurple);transform:translateY(-1px)}
.nav-hamburger{display:none;background:none;border:none;color:#fff;font-size:22px;cursor:pointer;padding:6px;margin-left:auto}

/* HERO — massive Blurple section with white text + dual CTAs (white + black) */
.hero{background:var(--blurple);color:#fff;padding:80px 24px 100px;text-align:center;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-200px;right:-200px;width:600px;height:600px;background:radial-gradient(circle,rgba(255,255,255,.12) 0%,transparent 60%);pointer-events:none}
.hero::after{content:'';position:absolute;bottom:-100px;left:-100px;width:500px;height:500px;background:radial-gradient(circle,rgba(120,135,240,.4) 0%,transparent 60%);pointer-events:none}
.hero-inner{max-width:1080px;margin:0 auto;position:relative;z-index:1}
.hero h1{font-size:clamp(40px,7vw,96px);font-weight:800;line-height:1.05;letter-spacing:-.025em;margin-bottom:24px;color:#fff;max-width:1000px;margin-left:auto;margin-right:auto}
.hero-sub{font-size:clamp(17px,1.6vw,20px);color:#fff;line-height:1.5;max-width:680px;margin:0 auto 36px;opacity:.96;font-weight:400}
.hero-cta-row{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;margin-bottom:60px}
.cta-pill{display:inline-flex;align-items:center;gap:8px;padding:14px 28px;border-radius:9999px;font-size:16px;font-weight:600;cursor:pointer;font-family:inherit;text-decoration:none;border:none;transition:background .15s,color .15s,transform .15s,box-shadow .15s}
.cta-pill.white{background:#fff;color:var(--text)}
.cta-pill.white:hover{background:#f6f6f6;color:var(--text);transform:translateY(-2px);box-shadow:0 8px 16px rgba(0,0,0,.16)}
.cta-pill.black{background:#23272a;color:#fff}
.cta-pill.black:hover{background:#1e2124;color:#fff;transform:translateY(-2px);box-shadow:0 8px 16px rgba(0,0,0,.24)}
.cta-pill.blurple{background:var(--blurple);color:#fff}
.cta-pill.blurple:hover{background:var(--blurple-dark);color:#fff;transform:translateY(-2px)}

/* HERO ILLUSTRATION — playful Discord scene */
.hero-art{max-width:780px;margin:24px auto 0;position:relative;height:300px;display:flex;justify-content:center;align-items:center;gap:32px;flex-wrap:wrap}
.hero-blob{background:#fff;border-radius:32px;padding:24px 28px;color:var(--text);box-shadow:0 24px 60px -20px rgba(0,0,0,.3);display:flex;align-items:center;gap:14px;max-width:340px;text-align:left;transform:rotate(-3deg)}
.hero-blob:nth-child(2){transform:rotate(2deg);background:#FEE75C;color:#000;max-width:280px}
.hero-blob:nth-child(3){transform:rotate(-1deg);background:var(--green);color:#fff;max-width:300px}
.hero-blob .avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#EB459E,#FEE75C);flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:22px}
.hero-blob:nth-child(2) .avatar{background:linear-gradient(135deg,#5865F2,#EB459E)}
.hero-blob:nth-child(3) .avatar{background:linear-gradient(135deg,#FEE75C,#FF73FA)}
.hero-blob-body .name{font-size:14px;font-weight:700;margin-bottom:2px;letter-spacing:-.005em}
.hero-blob-body .msg{font-size:14px;line-height:1.35;letter-spacing:-.005em}

/* WHITE SECTION (Discord alternates Blurple → White) */
.section-white{background:#fff;color:var(--text);padding:96px 24px;position:relative}
.section-white-inner{max-width:1180px;margin:0 auto}
.section-white .head{max-width:760px;margin:0 auto 64px;text-align:center}
.section-white .head h2{font-size:clamp(34px,5vw,56px);font-weight:800;letter-spacing:-.025em;line-height:1.1;color:var(--text);margin-bottom:18px}
.section-white .head p{font-size:18px;color:var(--muted);line-height:1.55}

/* BENEFITS — large illustrated icons, alternating layout, Discord uses split rows */
.benefit-row{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;margin-bottom:80px}
.benefit-row:last-child{margin-bottom:0}
.benefit-row:nth-child(even) .benefit-art{order:2}
.benefit-row:nth-child(even) .benefit-text{order:1}
.benefit-art{background:linear-gradient(135deg,#EEF0FE 0%,#F8F9FB 100%);border-radius:24px;padding:48px 32px;display:flex;align-items:center;justify-content:center;min-height:260px;font-size:140px;line-height:1;text-align:center;position:relative}
.benefit-row:nth-child(2) .benefit-art{background:linear-gradient(135deg,#FFF4E5 0%,#FFE5F5 100%)}
.benefit-row:nth-child(3) .benefit-art{background:linear-gradient(135deg,#E5FFF1 0%,#E5F5FF 100%)}
.benefit-row:nth-child(4) .benefit-art{background:linear-gradient(135deg,#FFE5E5 0%,#FFF4E5 100%)}
.benefit-text h3{font-size:clamp(26px,3vw,40px);font-weight:800;letter-spacing:-.02em;line-height:1.15;color:var(--text);margin-bottom:14px}
.benefit-text p{font-size:17px;color:var(--muted);line-height:1.55;margin-bottom:20px}
.benefit-text .ic{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:14px;background:var(--blurple);color:#fff;font-size:22px;margin-bottom:18px}

/* STATS — Discord "Reliable tech for staying close" strip */
.stats-band{background:var(--dark);color:#fff;padding:80px 24px}
.stats-inner{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:48px;text-align:center}
.stat-num{font-size:clamp(40px,5.5vw,72px);font-weight:800;letter-spacing:-.02em;color:#fff;line-height:1;margin-bottom:8px}
.stat-label{font-size:15px;color:var(--muted-on-blurple);letter-spacing:-.005em;line-height:1.4}

/* HOW — dark gray section, 3 step cards Discord-style */
.section-dark{background:var(--dark);color:#fff;padding:96px 24px}
.section-dark-inner{max-width:1180px;margin:0 auto}
.section-dark .head{max-width:760px;margin:0 auto 64px;text-align:center}
.section-dark .head h2{font-size:clamp(34px,5vw,56px);font-weight:800;letter-spacing:-.025em;line-height:1.1;color:#fff;margin-bottom:18px}
.section-dark .head p{font-size:18px;color:var(--muted-on-blurple);line-height:1.55}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.step{background:var(--dark-2);border-radius:20px;padding:36px 32px;position:relative;transition:transform .2s,background .2s}
.step:hover{background:#34373c;transform:translateY(-4px)}
.step-num{width:48px;height:48px;border-radius:50%;background:var(--blurple);color:#fff;font-weight:800;font-size:20px;display:flex;align-items:center;justify-content:center;margin-bottom:22px}
.step h3{font-size:22px;font-weight:700;letter-spacing:-.012em;margin-bottom:10px;color:#fff;line-height:1.25}
.step p{font-size:16px;color:var(--muted-on-blurple);line-height:1.55}

/* REVIEWS — white bg, colorful cards */
.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.review{padding:36px 32px;background:var(--blurple-pale);border-radius:20px;position:relative}
.review:nth-child(2){background:#FFF4E5}
.review-quote{font-size:19px;color:var(--text);line-height:1.5;font-weight:500;margin-bottom:24px;letter-spacing:-.005em}
.review-quote::before{content:'\201C';font-size:64px;line-height:.5;color:var(--blurple);position:absolute;top:32px;right:32px;opacity:.2;font-family:Georgia,serif}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#5865F2,#EB459E);color:#fff;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700;flex-shrink:0}
.review:nth-child(2) .review-avatar{background:linear-gradient(135deg,#FEE75C,#FF73FA);color:#23272a}
.review-name{font-size:15px;font-weight:700;color:var(--text);letter-spacing:-.005em}
.review-role{font-size:13px;color:var(--muted);letter-spacing:-.005em}

/* FAQ — white bg, Blurple toggle */
.faq{max-width:760px;margin:0 auto}
.faq-item{background:#F2F3F5;border-radius:12px;margin-bottom:8px;overflow:hidden;transition:background .15s}
.faq-item:hover{background:#EBEDEF}
.faq-item.active{background:var(--blurple-pale)}
.faq-q{width:100%;text-align:left;background:none;border:none;padding:22px 24px;font-size:17px;font-weight:700;letter-spacing:-.005em;color:var(--text);cursor:pointer;font-family:inherit;display:flex;justify-content:space-between;align-items:center;line-height:1.4;gap:24px}
.faq-q::after{content:'+';font-size:24px;color:var(--blurple);transition:transform .25s;flex-shrink:0;font-weight:700}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .25s;font-size:15px;color:var(--muted);line-height:1.65}
.faq-item.active .faq-a{max-height:600px;padding:0 24px 22px}

/* CTA — Blurple again */
.cta-block{background:var(--blurple);color:#fff;padding:96px 24px;text-align:center;position:relative;overflow:hidden}
.cta-block::before{content:'';position:absolute;top:50%;left:50%;width:800px;height:800px;background:radial-gradient(circle,rgba(255,255,255,.08) 0%,transparent 60%);transform:translate(-50%,-50%);pointer-events:none}
.cta-inner{max-width:560px;margin:0 auto;position:relative;z-index:1}
.cta-inner h2{font-size:clamp(34px,5vw,56px);font-weight:800;letter-spacing:-.025em;line-height:1.1;margin-bottom:18px;color:#fff}
.cta-inner p{font-size:18px;color:#fff;opacity:.95;line-height:1.5;margin-bottom:36px}
.cta-form{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:480px;margin:0 auto}
.cta-form input{padding:14px 18px;border-radius:12px;border:none;background:rgba(255,255,255,.95);color:var(--text);font-size:15px;font-family:inherit;outline:none;font-weight:500;transition:box-shadow .15s,background .15s}
.cta-form input::placeholder{color:var(--muted)}
.cta-form input:focus{background:#fff;box-shadow:0 0 0 4px rgba(255,255,255,.3)}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:1/-1}
.cta-form button{grid-column:1/-1;padding:14px 28px;border-radius:9999px;border:none;background:#fff;color:var(--blurple);font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;transition:background .15s,transform .15s;margin-top:8px}
.cta-form button:hover{background:#f6f6f6;transform:translateY(-2px)}

/* FOOTER — dark gray Discord style w/ Blurple wordmark */
.footer{background:var(--dark);color:#fff;padding:80px 24px 40px}
.footer-inner{max-width:1280px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px;border-bottom:1px solid rgba(255,255,255,.1)}
.footer-brand-block{max-width:280px}
.footer-brand-block .brand{font-size:24px;color:var(--blurple)}
.footer-brand-block .brand .mascot svg{fill:var(--blurple)}
.footer-soc{display:flex;gap:12px;margin-top:24px}
.footer-soc a{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;color:#fff;font-size:14px;transition:background .15s}
.footer-soc a:hover{background:var(--blurple)}
.footer-tag{font-size:13px;color:var(--muted-on-blurple);line-height:1.55;margin-top:12px}
.footer-col h4{font-size:14px;font-weight:700;color:var(--blurple-light);margin-bottom:14px;letter-spacing:0}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:10px}
.footer-col a{color:#fff;font-size:14px;font-weight:500}
.footer-col a:hover{color:var(--blurple-light);text-decoration:none}
.footer-bot{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding-top:32px;font-size:13px;color:var(--muted-on-blurple);align-items:center}
.footer-bot .lang{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,.06);padding:6px 12px;border-radius:8px;font-size:13px;color:#fff}

@media(max-width:900px){
.benefit-row{grid-template-columns:1fr;gap:32px;margin-bottom:56px}
.benefit-row:nth-child(even) .benefit-art{order:0}
.benefit-row:nth-child(even) .benefit-text{order:0}
.benefit-art{min-height:200px;font-size:100px}
.steps{grid-template-columns:1fr}
.reviews-grid{grid-template-columns:1fr}
.stats-inner{grid-template-columns:1fr;gap:36px}
.footer-top{grid-template-columns:1fr 1fr;gap:32px}
.hero-art{height:auto;flex-direction:column;gap:20px}
.hero-blob{max-width:none;transform:none !important;width:100%}
}
@media(max-width:640px){
.nav-links{display:none}
.nav-utility .open-browser{display:none}
.nav-hamburger{display:block}
.nav-inner{padding:0 18px;gap:0;height:40px}
.hero{padding:48px 18px 56px}
.hero h1{font-size:36px;letter-spacing:-.015em}
.hero-sub{font-size:16px}
.section-white,.section-dark,.cta-block{padding:64px 18px}
.footer{padding:48px 18px 32px}
.footer-top{grid-template-columns:1fr 1fr;gap:24px}
.cta-form{grid-template-columns:1fr}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:auto}
.benefit-text h3{font-size:26px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="brand"><span class="mascot"><svg viewBox="0 0 71 55" xmlns="http://www.w3.org/2000/svg"><path d="M60.105 4.898A58.55 58.55 0 0 0 45.653.415a.22.22 0 0 0-.233.11 40.784 40.784 0 0 0-1.8 3.697c-5.456-.817-10.886-.817-16.23 0-.485-1.164-1.201-2.587-1.828-3.697a.228.228 0 0 0-.233-.11 58.386 58.386 0 0 0-14.451 4.483.207.207 0 0 0-.095.082C1.578 18.73-.944 32.144.293 45.39a.244.244 0 0 0 .093.167c6.073 4.46 11.955 7.167 17.729 8.962a.23.23 0 0 0 .249-.082 42.08 42.08 0 0 0 3.627-5.9.225.225 0 0 0-.123-.312 38.772 38.772 0 0 1-5.539-2.64.228.228 0 0 1-.022-.378c.372-.279.744-.569 1.1-.862a.22.22 0 0 1 .229-.031c11.619 5.305 24.198 5.305 35.68 0a.219.219 0 0 1 .233.028c.356.293.728.586 1.103.865a.228.228 0 0 1-.02.378 36.384 36.384 0 0 1-5.54 2.637.227.227 0 0 0-.121.315 47.249 47.249 0 0 0 3.624 5.897.225.225 0 0 0 .249.084c5.801-1.794 11.684-4.502 17.757-8.962a.228.228 0 0 0 .092-.164c1.48-15.315-2.479-28.618-10.493-40.412a.18.18 0 0 0-.093-.084Zm-36.38 32.426c-3.497 0-6.38-3.211-6.38-7.156 0-3.944 2.827-7.156 6.38-7.156 3.583 0 6.438 3.24 6.382 7.156 0 3.945-2.827 7.156-6.382 7.156Zm23.593 0c-3.498 0-6.38-3.211-6.38-7.156 0-3.944 2.826-7.156 6.38-7.156 3.582 0 6.437 3.24 6.38 7.156 0 3.945-2.798 7.156-6.38 7.156Z"/></svg></span>Discord</a>
<ul class="nav-links">
<li><a href="#">Download</a></li>
<li><a href="#">Nitro</a></li>
<li><a href="#benefits">Discover</a></li>
<li><a href="#how">Safety</a></li>
<li><a href="#faq">Support</a></li>
<li><a href="#">Blog</a></li>
<li><a href="#">Careers</a></li>
</ul>
<div class="nav-utility">
<a href="#" class="open-browser">Open Discord</a>
<a href="#form" class="pill-white">Login</a>
</div>
<button class="nav-hamburger" aria-label="Menu">&#9776;</button>
</div></nav>

<!-- HERO -->
<section class="hero" id="hero"><div class="hero-inner">
<h1>{{HERO_TITLE}}</h1>
<p class="hero-sub">{{HERO_SUBTITLE}}</p>
<div class="hero-cta-row">
<a href="#form" class="cta-pill white"><span style="font-size:18px">&#8615;</span> {{CTA_BUTTON}}</a>
<a href="#benefits" class="cta-pill black">Open Discord in your browser</a>
</div>

<!-- Playful chat-bubble hero illustration -->
<div class="hero-art">
<div class="hero-blob"><div class="avatar">&#127918;</div><div class="hero-blob-body"><div class="name">gamerguy_42</div><div class="msg">Friday night raid?! anyone up for it?</div></div></div>
<div class="hero-blob"><div class="avatar">&#129305;</div><div class="hero-blob-body"><div class="name">study-buddy</div><div class="msg">study room is OPEN come work with us :)</div></div></div>
<div class="hero-blob"><div class="avatar">&#127908;</div><div class="hero-blob-body"><div class="name">music_lover</div><div class="msg">listening party in 5! drop your faves</div></div></div>
</div>
</div></section>

<!-- BENEFITS — white bg, illustrated rows alternating -->
<section class="section-white" id="benefits"><div class="section-white-inner">
<div class="head">
<h2>{{BENEFITS_HEADLINE}}</h2>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>

<div class="benefit-row">
<div class="benefit-art">{{BENEFIT_1_ICON}}</div>
<div class="benefit-text"><div class="ic">&#128172;</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p><a href="#form" class="cta-pill blurple">{{CTA_BUTTON}}</a></div>
</div>

<div class="benefit-row">
<div class="benefit-art">{{BENEFIT_2_ICON}}</div>
<div class="benefit-text"><div class="ic" style="background:#EB459E">&#127908;</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p><a href="#form" class="cta-pill blurple">{{CTA_BUTTON}}</a></div>
</div>

<div class="benefit-row">
<div class="benefit-art">{{BENEFIT_3_ICON}}</div>
<div class="benefit-text"><div class="ic" style="background:#43b581">&#128242;</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p><a href="#form" class="cta-pill blurple">{{CTA_BUTTON}}</a></div>
</div>

<div class="benefit-row">
<div class="benefit-art">{{BENEFIT_4_ICON}}</div>
<div class="benefit-text"><div class="ic" style="background:#faa61a">&#127919;</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p><a href="#form" class="cta-pill blurple">{{CTA_BUTTON}}</a></div>
</div>
</div></section>

<!-- STATS — "Reliable tech for staying close" strip -->
<section class="stats-band"><div class="stats-inner">
<div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></section>

<!-- HOW — dark gray with 3 step cards -->
<section class="section-dark" id="how"><div class="section-dark-inner">
<div class="head">
<h2>{{HOW_HEADLINE}}</h2>
<p>{{HOW_SUBHEADLINE}}</p>
</div>
<div class="steps">
<div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>

<!-- REVIEWS — white bg -->
<section class="section-white" id="reviews"><div class="section-white-inner">
<div class="head">
<h2>{{REVIEWS_HEADLINE}}</h2>
<p>{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-grid">
<div class="review"><div class="review-quote">{{REVIEW_1_QUOTE}}</div><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div></div></div>
<div class="review"><div class="review-quote">{{REVIEW_2_QUOTE}}</div><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div></div></div>
</div>
</div></section>

<!-- FAQ — white bg -->
<section class="section-white" id="faq"><div class="section-white-inner">
<div class="head">
<h2>{{FAQ_HEADLINE}}</h2>
<p>{{FAQ_SUBHEADLINE}}</p>
</div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<!-- CTA — Blurple again -->
<section class="cta-block" id="form"><div class="cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div></section>

<!-- FOOTER -->
<footer class="footer"><div class="footer-inner">
<div class="footer-top">
<div class="footer-brand-block">
<a href="#" class="brand"><span class="mascot"><svg viewBox="0 0 71 55" xmlns="http://www.w3.org/2000/svg"><path fill="#5865F2" d="M60.105 4.898A58.55 58.55 0 0 0 45.653.415a.22.22 0 0 0-.233.11 40.784 40.784 0 0 0-1.8 3.697c-5.456-.817-10.886-.817-16.23 0-.485-1.164-1.201-2.587-1.828-3.697a.228.228 0 0 0-.233-.11 58.386 58.386 0 0 0-14.451 4.483.207.207 0 0 0-.095.082C1.578 18.73-.944 32.144.293 45.39a.244.244 0 0 0 .093.167c6.073 4.46 11.955 7.167 17.729 8.962a.23.23 0 0 0 .249-.082 42.08 42.08 0 0 0 3.627-5.9.225.225 0 0 0-.123-.312 38.772 38.772 0 0 1-5.539-2.64.228.228 0 0 1-.022-.378c.372-.279.744-.569 1.1-.862a.22.22 0 0 1 .229-.031c11.619 5.305 24.198 5.305 35.68 0a.219.219 0 0 1 .233.028c.356.293.728.586 1.103.865a.228.228 0 0 1-.02.378 36.384 36.384 0 0 1-5.54 2.637.227.227 0 0 0-.121.315 47.249 47.249 0 0 0 3.624 5.897.225.225 0 0 0 .249.084c5.801-1.794 11.684-4.502 17.757-8.962a.228.228 0 0 0 .092-.164c1.48-15.315-2.479-28.618-10.493-40.412a.18.18 0 0 0-.093-.084Zm-36.38 32.426c-3.497 0-6.38-3.211-6.38-7.156 0-3.944 2.827-7.156 6.38-7.156 3.583 0 6.438 3.24 6.382 7.156 0 3.945-2.827 7.156-6.382 7.156Zm23.593 0c-3.498 0-6.38-3.211-6.38-7.156 0-3.944 2.826-7.156 6.38-7.156 3.582 0 6.437 3.24 6.38 7.156 0 3.945-2.798 7.156-6.38 7.156Z"/></svg></span>Discord</a>
<p class="footer-tag">Imagine a place where you can belong to a school club, a gaming group, or a worldwide art community.</p>
<div class="footer-soc"><a href="#">Tw</a><a href="#">Ig</a><a href="#">Fb</a><a href="#">Yt</a><a href="#">Tk</a></div>
</div>
<div class="footer-col"><h4>Product</h4><ul><li><a href="#">Download</a></li><li><a href="#">Nitro</a></li><li><a href="#">Status</a></li><li><a href="#">Mod Program</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Jobs</a></li><li><a href="#">Branding</a></li><li><a href="#">Newsroom</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#">College</a></li><li><a href="#">Support</a></li><li><a href="#">Safety</a></li><li><a href="#">Blog</a></li><li><a href="#">Feedback</a></li></ul></div>
<div class="footer-col"><h4>Policies</h4><ul><li><a href="#">Terms</a></li><li><a href="#">Privacy</a></li><li><a href="#">Cookies</a></li><li><a href="#">Guidelines</a></li><li><a href="#">Licenses</a></li></ul></div>
</div>
<div class="footer-bot">
<div>&copy; {{YEAR}} Eko AI Inc. &middot; All rights reserved.</div>
<div class="lang">&#127760; English, USA</div>
</div>
</div></footer>
__FORM_SUBMIT_JS__
</body></html>
"""

# ─── Mailchimp Whimsical ─────────────────────────────────────────────────────────────
_TPL_MAILCHIMP_WHIMSICAL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#fff;
  --yellow:#FFE01B;
  --yellow-2:#FFF066;
  --dark:#241c15;
  --dark-soft:#3a312a;
  --muted:#7c7269;
  --peach:#FF66BC;
  --teal:#0EAEDB;
  --cream:#FFF6E5;
  --hairline:#E6DEC8;
}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:'Helvetica Neue','Helvetica',Arial,sans-serif;background:var(--bg);color:var(--dark);line-height:1.55;-webkit-font-smoothing:antialiased;font-weight:400;min-height:100vh}
a{color:var(--dark);text-decoration:none;transition:color .15s,opacity .15s}
a:hover{color:var(--dark);text-decoration:underline}
.serif{font-family:'Cooper','Caecilia',Georgia,'Times New Roman',serif;font-weight:900;letter-spacing:-.015em}

/* NAV — Yellow background, brown text, Freddie monkey mascot */
.nav{position:sticky;top:0;z-index:9999;background:var(--yellow);border-bottom:3px solid var(--dark)}
.nav-inner{max-width:1260px;margin:0 auto;padding:0 32px;display:flex;align-items:center;gap:32px;height:64px}
.brand{display:flex;align-items:center;gap:10px;color:var(--dark);font-weight:900;font-size:22px;letter-spacing:-.02em;flex-shrink:0;font-family:'Cooper','Caecilia',Georgia,serif}
.brand .mascot{width:38px;height:38px;background:var(--dark);border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:22px;color:var(--yellow)}
.nav-links{display:flex;list-style:none;gap:0;flex:1;margin:0;padding:0}
.nav-links li{padding:0 14px}
.nav-links a{color:var(--dark);font-size:15px;font-weight:600;letter-spacing:-.005em}
.nav-links a:hover{color:var(--dark);text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}
.nav-utility{display:flex;gap:14px;align-items:center}
.nav-utility .login{color:var(--dark);font-size:15px;font-weight:600;padding:8px 0}
.nav-utility .login:hover{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}
.pill-dark{background:var(--dark);color:var(--yellow);padding:10px 22px;border-radius:9999px;font-size:15px;font-weight:700;border:2px solid var(--dark);display:inline-flex;align-items:center;gap:6px;transition:background .15s,color .15s,transform .15s;cursor:pointer;font-family:inherit;text-decoration:none}
.pill-dark:hover{background:var(--yellow);color:var(--dark);text-decoration:none;transform:translateY(-2px)}
.pill-ghost{background:transparent;color:var(--dark);padding:10px 22px;border-radius:9999px;font-size:15px;font-weight:700;border:2px solid var(--dark);display:inline-flex;align-items:center;gap:6px;cursor:pointer;font-family:inherit;text-decoration:none;transition:background .15s,transform .15s}
.pill-ghost:hover{background:var(--dark);color:var(--yellow);text-decoration:none;transform:translateY(-2px)}
.nav-hamburger{display:none;background:none;border:none;color:var(--dark);font-size:24px;cursor:pointer;padding:6px;margin-left:auto}

/* HERO — yellow bg, huge serif headline, Freddie illustration */
.hero{background:var(--yellow);color:var(--dark);padding:80px 32px 100px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:60px;right:80px;width:120px;height:120px;background:var(--peach);border-radius:50%;opacity:.7;pointer-events:none}
.hero::after{content:'';position:absolute;bottom:80px;left:60px;width:80px;height:80px;background:var(--teal);border-radius:50%;opacity:.7;pointer-events:none}
.hero-inner{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:1.2fr 1fr;gap:48px;align-items:center;position:relative;z-index:1}
.hero-text .eyebrow{display:inline-block;background:var(--dark);color:var(--yellow);padding:6px 14px;border-radius:9999px;font-size:13px;font-weight:700;letter-spacing:.03em;margin-bottom:24px;text-transform:uppercase}
.hero-text h1{font-size:clamp(44px,7vw,96px);font-weight:900;line-height:1;letter-spacing:-.025em;color:var(--dark);margin-bottom:24px;font-family:'Cooper','Caecilia',Georgia,'Times New Roman',serif}
.hero-text .sub{font-size:clamp(18px,1.6vw,22px);color:var(--dark);line-height:1.45;max-width:540px;margin-bottom:36px;font-weight:500}
.hero-cta-row{display:flex;gap:14px;flex-wrap:wrap}

/* Freddie hero illustration block */
.freddie{width:100%;max-width:440px;aspect-ratio:1/1;background:var(--peach);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:200px;line-height:1;margin:0 auto;position:relative;box-shadow:24px 24px 0 var(--dark);border:4px solid var(--dark)}
.freddie::before{content:'';position:absolute;top:-20px;right:30px;width:60px;height:60px;background:var(--yellow);border-radius:50%;border:3px solid var(--dark);transform:rotate(15deg)}
.freddie::after{content:'';position:absolute;bottom:30px;left:-20px;width:50px;height:50px;background:var(--teal);border-radius:50%;border:3px solid var(--dark)}

/* ZIGZAG STRIP — Mailchimp's signature divider */
.zigzag{background:var(--yellow);height:32px;background-image:linear-gradient(135deg,var(--yellow) 25%,transparent 25%),linear-gradient(225deg,var(--yellow) 25%,transparent 25%);background-position:0 100%;background-repeat:repeat-x;background-size:32px 32px;position:relative;border-bottom:3px solid var(--dark)}

/* STATS — Yellow strip with big serif numbers */
.stats-band{background:var(--cream);color:var(--dark);padding:72px 32px;border-bottom:3px solid var(--dark)}
.stats-inner{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:48px;text-align:center}
.stat-num{font-family:'Cooper','Caecilia',Georgia,serif;font-size:clamp(48px,6vw,84px);font-weight:900;letter-spacing:-.02em;color:var(--dark);line-height:1;margin-bottom:6px}
.stat-label{font-size:15px;color:var(--dark);font-weight:500;line-height:1.4}

/* SECTION */
.section{padding:96px 32px;background:#fff;position:relative}
.section.cream{background:var(--cream)}
.section-inner{max-width:1180px;margin:0 auto}
.section-head{max-width:760px;margin:0 auto 64px;text-align:center}
.section-eyebrow{display:inline-block;background:var(--dark);color:var(--yellow);padding:5px 14px;border-radius:9999px;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;margin-bottom:18px}
.section-head h2{font-family:'Cooper','Caecilia',Georgia,'Times New Roman',serif;font-size:clamp(36px,5.5vw,64px);font-weight:900;letter-spacing:-.02em;line-height:1.05;color:var(--dark);margin-bottom:18px}
.section-head p{font-size:18px;color:var(--dark);line-height:1.55;font-weight:500}

/* BENEFITS — 4 cards w/ yellow left border accent (Mailchimp signature) */
.benefits-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.benefit-card{background:#fff;border:3px solid var(--dark);border-radius:20px;padding:36px 32px;position:relative;transition:transform .2s,box-shadow .2s;box-shadow:8px 8px 0 var(--dark)}
.benefit-card::before{content:'';position:absolute;top:0;left:0;bottom:0;width:14px;background:var(--yellow);border-radius:17px 0 0 17px}
.benefit-card:hover{transform:translate(-3px,-3px);box-shadow:11px 11px 0 var(--dark)}
.benefit-card:nth-child(2)::before{background:var(--peach)}
.benefit-card:nth-child(3)::before{background:var(--teal)}
.benefit-card:nth-child(4)::before{background:#43b581}
.benefit-icon{display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;border-radius:50%;background:var(--yellow);border:2px solid var(--dark);color:var(--dark);font-size:30px;margin-bottom:20px;line-height:1;padding-left:14px}
.benefit-card:nth-child(2) .benefit-icon{background:var(--peach)}
.benefit-card:nth-child(3) .benefit-icon{background:var(--teal)}
.benefit-card:nth-child(4) .benefit-icon{background:#FFD96B}
.benefit-card h3{font-family:'Cooper','Caecilia',Georgia,serif;font-size:24px;font-weight:900;letter-spacing:-.012em;margin-bottom:10px;color:var(--dark);line-height:1.2;padding-left:14px}
.benefit-card p{font-size:16px;color:var(--dark);line-height:1.55;padding-left:14px;font-weight:400}

/* HOW — 3 numbered steps with serif typography */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
.step{text-align:center;padding:0}
.step-num{font-family:'Cooper','Caecilia',Georgia,serif;font-size:80px;font-weight:900;line-height:1;color:var(--yellow);-webkit-text-stroke:3px var(--dark);text-stroke:3px var(--dark);margin-bottom:18px}
.step h3{font-family:'Cooper','Caecilia',Georgia,serif;font-size:24px;font-weight:900;letter-spacing:-.012em;margin-bottom:10px;color:var(--dark);line-height:1.25}
.step p{font-size:16px;color:var(--dark);line-height:1.55;max-width:300px;margin:0 auto;font-weight:400}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.review{background:var(--yellow);border:3px solid var(--dark);border-radius:20px;padding:36px 32px;position:relative;box-shadow:8px 8px 0 var(--dark)}
.review:nth-child(2){background:var(--peach)}
.review-quote{font-family:'Cooper','Caecilia',Georgia,serif;font-size:22px;color:var(--dark);line-height:1.35;font-weight:700;margin-bottom:24px;letter-spacing:-.012em}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:50px;height:50px;border-radius:50%;background:var(--dark);color:var(--yellow);display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;flex-shrink:0;border:2px solid var(--dark)}
.review:nth-child(2) .review-avatar{background:var(--dark);color:var(--peach)}
.review-name{font-size:16px;font-weight:700;color:var(--dark);letter-spacing:-.005em}
.review-role{font-size:13px;color:var(--dark);opacity:.7}

/* FAQ — cream bg, yellow + toggle */
.faq{max-width:760px;margin:0 auto}
.faq-item{background:#fff;border:3px solid var(--dark);border-radius:14px;margin-bottom:12px;overflow:hidden;transition:background .15s,transform .15s,box-shadow .15s;box-shadow:6px 6px 0 var(--dark)}
.faq-item.active{background:var(--yellow)}
.faq-q{width:100%;text-align:left;background:none;border:none;padding:22px 26px;font-family:'Cooper','Caecilia',Georgia,serif;font-size:19px;font-weight:900;letter-spacing:-.012em;color:var(--dark);cursor:pointer;font-family:'Cooper','Caecilia',Georgia,serif;display:flex;justify-content:space-between;align-items:center;line-height:1.3;gap:24px}
.faq-q::after{content:'+';font-size:28px;color:var(--dark);transition:transform .25s;flex-shrink:0;font-weight:900;width:32px;height:32px;display:flex;align-items:center;justify-content:center;border:2px solid var(--dark);border-radius:50%;background:var(--yellow);font-family:'Helvetica Neue',Arial,sans-serif;line-height:1}
.faq-item.active .faq-q::after{transform:rotate(45deg);background:#fff}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .25s;font-size:16px;color:var(--dark);line-height:1.65;font-weight:400}
.faq-item.active .faq-a{max-height:600px;padding:0 26px 22px}

/* CTA — yellow */
.cta-block{background:var(--yellow);color:var(--dark);padding:120px 32px;text-align:center;position:relative;overflow:hidden;border-top:3px solid var(--dark);border-bottom:3px solid var(--dark)}
.cta-block::before{content:'';position:absolute;top:30px;left:50px;width:80px;height:80px;background:var(--peach);border-radius:50%;border:3px solid var(--dark);pointer-events:none}
.cta-block::after{content:'';position:absolute;bottom:30px;right:50px;width:100px;height:100px;background:var(--teal);border-radius:50%;border:3px solid var(--dark);pointer-events:none}
.cta-inner{max-width:560px;margin:0 auto;position:relative;z-index:1}
.cta-inner h2{font-family:'Cooper','Caecilia',Georgia,serif;font-size:clamp(36px,5.5vw,64px);font-weight:900;letter-spacing:-.02em;line-height:1.05;margin-bottom:18px;color:var(--dark)}
.cta-inner p{font-size:18px;color:var(--dark);line-height:1.5;margin-bottom:36px;font-weight:500}
.cta-form{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;max-width:480px;margin:0 auto}
.cta-form input{padding:14px 18px;border-radius:12px;border:2px solid var(--dark);background:#fff;color:var(--dark);font-size:15px;font-family:inherit;outline:none;font-weight:500;transition:box-shadow .15s,transform .15s}
.cta-form input::placeholder{color:var(--muted)}
.cta-form input:focus{box-shadow:4px 4px 0 var(--dark);transform:translate(-2px,-2px)}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:1/-1}
.cta-form button{grid-column:1/-1;padding:14px 28px;border-radius:9999px;border:2px solid var(--dark);background:var(--dark);color:var(--yellow);font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;transition:background .15s,color .15s,transform .15s,box-shadow .15s;margin-top:8px}
.cta-form button:hover{background:var(--yellow);color:var(--dark);transform:translateY(-2px);box-shadow:4px 4px 0 var(--dark)}

/* FOOTER — dark brown with yellow accents */
.footer{background:var(--dark);color:#fff;padding:80px 32px 40px;position:relative}
.footer::before{content:'';position:absolute;top:0;left:0;right:0;height:24px;background:var(--yellow);background-image:linear-gradient(135deg,var(--dark) 25%,transparent 25%),linear-gradient(225deg,var(--dark) 25%,transparent 25%);background-position:0 0;background-repeat:repeat-x;background-size:24px 24px}
.footer-inner{max-width:1280px;margin:0 auto;padding-top:24px}
.footer-top{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px;border-bottom:2px solid rgba(255,224,27,.2)}
.footer-brand-block{max-width:280px}
.footer-brand-block .brand{font-size:24px;color:var(--yellow)}
.footer-brand-block .brand .mascot{background:var(--yellow);color:var(--dark)}
.footer-tag{font-size:14px;color:#fff;opacity:.85;line-height:1.55;margin-top:14px}
.footer-soc{display:flex;gap:10px;margin-top:24px}
.footer-soc a{width:38px;height:38px;border-radius:50%;background:var(--yellow);color:var(--dark);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;transition:transform .15s}
.footer-soc a:hover{transform:translateY(-3px);text-decoration:none}
.footer-col h4{font-family:'Cooper','Caecilia',Georgia,serif;font-size:17px;font-weight:900;color:var(--yellow);margin-bottom:16px}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:10px}
.footer-col a{color:#fff;font-size:14px;font-weight:500;opacity:.9}
.footer-col a:hover{color:var(--yellow);text-decoration:none;opacity:1}
.footer-bot{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding-top:32px;font-size:13px;color:#fff;opacity:.7;align-items:center}

@media(max-width:900px){
.hero-inner{grid-template-columns:1fr;gap:36px;text-align:center}
.hero-text .sub{margin-left:auto;margin-right:auto}
.hero-cta-row{justify-content:center}
.freddie{max-width:300px}
.benefits-grid,.reviews-grid{grid-template-columns:1fr}
.steps{grid-template-columns:1fr;gap:48px}
.stats-inner{grid-template-columns:1fr;gap:36px}
.footer-top{grid-template-columns:1fr 1fr;gap:32px}
}
@media(max-width:640px){
.nav-links{display:none}
.nav-utility .login{display:none}
.nav-hamburger{display:block}
.nav-inner{padding:0 18px;gap:0;height:56px}
.hero{padding:48px 18px 64px}
.hero-text h1{font-size:42px;letter-spacing:-.015em}
.hero-text .sub{font-size:16px}
.section{padding:64px 18px}
.cta-block{padding:64px 18px}
.cta-block::before,.cta-block::after{display:none}
.footer{padding:48px 18px 32px}
.footer-top{grid-template-columns:1fr 1fr;gap:24px}
.cta-form{grid-template-columns:1fr}
.cta-form input[type=email],.cta-form input[type=url]{grid-column:auto}
.benefit-card{padding:28px 22px}
.benefit-card h3,.benefit-card p{padding-left:8px}
.freddie{font-size:140px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="brand"><span class="mascot">&#128053;</span>Mailchimp</a>
<ul class="nav-links">
<li><a href="#benefits">Why Mailchimp</a></li>
<li><a href="#how">Products</a></li>
<li><a href="#">Pricing</a></li>
<li><a href="#reviews">Resources</a></li>
<li><a href="#faq">Inspiration</a></li>
</ul>
<div class="nav-utility">
<a href="#" class="login">Log in</a>
<a href="#form" class="pill-dark">Sign Up Free</a>
</div>
<button class="nav-hamburger" aria-label="Menu">&#9776;</button>
</div></nav>

<!-- HERO — yellow w/ split layout & Freddie -->
<section class="hero" id="hero"><div class="hero-inner">
<div class="hero-text">
<span class="eyebrow">{{BADGE}}</span>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="hero-cta-row">
<a href="#form" class="pill-dark">{{CTA_BUTTON}} &rarr;</a>
<a href="#benefits" class="pill-ghost">Talk to Sales</a>
</div>
</div>
<div class="freddie">&#128053;</div>
</div></section>

<!-- STATS -->
<section class="stats-band"><div class="stats-inner">
<div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></section>

<!-- BENEFITS -->
<section class="section" id="benefits"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow">Features</div>
<h2>{{BENEFITS_HEADLINE}}</h2>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>
<div class="benefits-grid">
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="benefit-card"><div class="benefit-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div>
</div></section>

<!-- HOW -->
<section class="section cream" id="how"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow">How it works</div>
<h2>{{HOW_HEADLINE}}</h2>
<p>{{HOW_SUBHEADLINE}}</p>
</div>
<div class="steps">
<div class="step"><div class="step-num">01</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">02</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">03</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>

<!-- REVIEWS -->
<section class="section" id="reviews"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow">Customers</div>
<h2>{{REVIEWS_HEADLINE}}</h2>
<p>{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-grid">
<div class="review"><div class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div></div></div>
<div class="review"><div class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</div><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div></div></div>
</div>
</div></section>

<!-- FAQ -->
<section class="section cream" id="faq"><div class="section-inner">
<div class="section-head">
<div class="section-eyebrow">FAQ</div>
<h2>{{FAQ_HEADLINE}}</h2>
<p>{{FAQ_SUBHEADLINE}}</p>
</div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<!-- CTA -->
<section class="cta-block" id="form"><div class="cta-inner">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}} &rarr;</button>
</form>
</div></section>

<!-- FOOTER -->
<footer class="footer"><div class="footer-inner">
<div class="footer-top">
<div class="footer-brand-block">
<a href="#" class="brand"><span class="mascot">&#128053;</span>Mailchimp</a>
<p class="footer-tag">An all-in-one Intuit Mailchimp marketing platform for managing your business.</p>
<div class="footer-soc"><a href="#">Tw</a><a href="#">Fb</a><a href="#">Ig</a><a href="#">In</a><a href="#">Yt</a></div>
</div>
<div class="footer-col"><h4>Why Mailchimp</h4><ul><li><a href="#">Email Marketing</a></li><li><a href="#">Marketing CRM</a></li><li><a href="#">Subject Line Helper</a></li><li><a href="#">All Features</a></li></ul></div>
<div class="footer-col"><h4>Products</h4><ul><li><a href="#">Websites</a></li><li><a href="#">Landing Pages</a></li><li><a href="#">Pop-up Forms</a></li><li><a href="#">Mobile App</a></li><li><a href="#">Pricing</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#">Help Center</a></li><li><a href="#">Email Templates</a></li><li><a href="#">Knowledge Base</a></li><li><a href="#">Smart Tips</a></li><li><a href="#">Research</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About Us</a></li><li><a href="#">Newsroom</a></li><li><a href="#">Careers</a></li><li><a href="#">Diversity</a></li><li><a href="#">Press &amp; Awards</a></li></ul></div>
</div>
<div class="footer-bot">
<div>&copy; {{YEAR}} Eko AI Inc. &middot; All Rights Reserved. &middot; <a href="#" style="color:#fff;text-decoration:underline">Privacy</a> &middot; <a href="#" style="color:#fff;text-decoration:underline">Terms</a> &middot; <a href="#" style="color:#fff;text-decoration:underline">Cookie Preferences</a></div>
<div>&#128053; Backed by Intuit</div>
</div>
</div></footer>
__FORM_SUBMIT_JS__
</body></html>
"""

# ─── Slack Pro ─────────────────────────────────────────────────────────────
_TPL_SLACK_PRO = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--cream:#f4ede4;--text:#1d1c1d;--muted:#454245;--aubergine:#611f69;--aubergine-dark:#4a154b;--mint:#2eb67d;--yellow:#ecb22e;--red:#e01e5a;--teal:#36c5f0;--border:#e0dcd6;--surface:#ffffff;--chat-bg:#f8f8f8;--sidebar:#3f0e40}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:"Slack-Lato","Lato","Helvetica Neue",Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh;font-weight:400}
a{color:var(--aubergine);text-decoration:none}
img{max-width:100%;display:block}

/* NAV — white sticky with Slack 4-color hashtag logo */
.nav{position:sticky;top:0;left:0;right:0;z-index:100;background:#fff;border-bottom:1px solid var(--border)}
.nav-inner{max-width:1340px;margin:0 auto;padding:0 24px;height:70px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.logo{display:flex;align-items:center;gap:10px;flex-shrink:0}
.logo-mark{width:30px;height:30px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:3px}
.logo-mark span{border-radius:3px}
.logo-mark span:nth-child(1){background:var(--red)}
.logo-mark span:nth-child(2){background:var(--yellow)}
.logo-mark span:nth-child(3){background:var(--teal)}
.logo-mark span:nth-child(4){background:var(--mint)}
.logo-text{font-family:"Slack-Lato","Lato",sans-serif;font-weight:900;font-size:24px;color:var(--text);letter-spacing:-.5px}
.nav-links{display:flex;gap:28px;list-style:none;align-items:center;flex:1;justify-content:center}
.nav-links a{color:var(--text);font-size:15px;font-weight:700;display:inline-flex;align-items:center;gap:4px;transition:color .15s}
.nav-links a::after{content:'\02C5';font-size:13px;color:var(--muted)}
.nav-links li:last-child a::after{content:''}
.nav-links a:hover{color:var(--aubergine)}
.nav-right{display:flex;align-items:center;gap:14px;flex-shrink:0}
.nav-signin{color:var(--text);font-size:14px;font-weight:700;padding:8px 4px}
.nav-signin:hover{color:var(--aubergine);text-decoration:underline}
.nav-outline{display:inline-flex;align-items:center;justify-content:center;padding:10px 16px;border:2px solid var(--aubergine);background:#fff;color:var(--aubergine);font-weight:900;font-size:13px;letter-spacing:.6px;text-transform:uppercase;border-radius:4px;transition:background .15s,color .15s;font-family:inherit;cursor:pointer}
.nav-outline:hover{background:var(--aubergine);color:#fff;text-decoration:none}
.nav-cta{display:inline-flex;align-items:center;justify-content:center;padding:10px 16px;background:var(--aubergine);color:#fff!important;font-weight:900;font-size:13px;letter-spacing:.6px;text-transform:uppercase;border-radius:4px;transition:background .15s;font-family:inherit}
.nav-cta:hover{background:var(--aubergine-dark);text-decoration:none}

/* HERO — full bleed aubergine */
.hero{background:var(--aubergine);color:#fff;padding:88px 24px 96px;position:relative;overflow:hidden}
.hero::before,.hero::after{content:'';position:absolute;border-radius:50%;filter:blur(40px);opacity:.45;pointer-events:none}
.blob{position:absolute;border-radius:50%;filter:blur(50px);opacity:.55;pointer-events:none}
.blob-1{width:220px;height:220px;background:var(--mint);top:-60px;right:8%}
.blob-2{width:180px;height:180px;background:var(--yellow);top:30%;left:-40px}
.blob-3{width:200px;height:200px;background:var(--red);bottom:-60px;right:18%}
.blob-4{width:160px;height:160px;background:var(--teal);bottom:10%;left:25%}
.hero-inner{max-width:1140px;margin:0 auto;text-align:center;position:relative;z-index:2}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);color:#fff;font-size:13px;font-weight:700;margin-bottom:24px;text-transform:uppercase;letter-spacing:.6px}
.badge::before{content:'\2728'}
.hero h1{font-size:clamp(40px,6vw,72px);font-weight:900;line-height:1.05;letter-spacing:-2px;margin-bottom:24px;color:#fff;max-width:980px;margin-left:auto;margin-right:auto}
.hero p.sub{font-size:clamp(17px,2.2vw,22px);color:rgba(255,255,255,.88);max-width:680px;margin:0 auto 36px;line-height:1.45;font-weight:400}
.hero-ctas{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-bottom:60px}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:16px 28px;border-radius:4px;font-weight:900;font-size:14px;letter-spacing:.6px;text-transform:uppercase;cursor:pointer;border:none;font-family:inherit;text-decoration:none;transition:all .2s}
.btn-white{background:#fff;color:var(--aubergine)!important}
.btn-white:hover{background:#f4ede4;transform:translateY(-1px);text-decoration:none}
.btn-white-outline{background:transparent;color:#fff!important;border:2px solid #fff}
.btn-white-outline:hover{background:#fff;color:var(--aubergine)!important;text-decoration:none}

/* HERO FORM — beneath CTA, on aubergine */
.hero-form{max-width:680px;margin:0 auto;padding:24px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:12px;backdrop-filter:blur(6px);display:grid;grid-template-columns:1fr 1fr;gap:10px}
.hero-form input{padding:14px 16px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.95);color:var(--text);font-size:14px;border-radius:6px;font-family:inherit;outline:none;transition:border-color .15s,box-shadow .15s}
.hero-form input:focus{border-color:var(--mint);box-shadow:0 0 0 3px rgba(46,182,125,.3)}
.hero-form input::placeholder{color:var(--muted)}
.hero-form input[name="website"]{grid-column:1/3}
.hero-form button{grid-column:1/3;padding:16px;background:#fff;color:var(--aubergine);border:none;border-radius:6px;font-weight:900;font-size:14px;letter-spacing:.6px;text-transform:uppercase;cursor:pointer;font-family:inherit;transition:background .15s,transform .15s}
.hero-form button:hover{background:var(--cream);transform:translateY(-1px)}

/* STATS strip — on white below hero */
.stats-strip{background:#fff;padding:48px 24px;border-bottom:1px solid var(--border)}
.stats-inner{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;text-align:center}
.stat{padding:8px}
.stat-num{font-size:48px;font-weight:900;color:var(--text);letter-spacing:-1.5px;line-height:1}
.stat-label{font-size:14px;color:var(--muted);margin-top:8px;font-weight:700;text-transform:uppercase;letter-spacing:.4px}
.stat:nth-child(1) .stat-num{color:var(--aubergine)}
.stat:nth-child(2) .stat-num{color:var(--mint)}
.stat:nth-child(3) .stat-num{color:var(--red)}

/* SECTIONS */
.section{padding:96px 24px}
.section-cream{background:var(--cream)}
.section-white{background:#fff}
.section-inner{max-width:1140px;margin:0 auto}
.section-header{text-align:center;margin-bottom:56px;max-width:780px;margin-left:auto;margin-right:auto}
.eyebrow{display:inline-block;font-size:13px;font-weight:900;color:var(--aubergine);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px}
.section-header h2{font-size:clamp(32px,4.5vw,52px);font-weight:900;letter-spacing:-1.4px;line-height:1.1;color:var(--text);margin-bottom:16px}
.section-header p{color:var(--muted);font-size:18px;line-height:1.55}

/* FEATURE CARDS — white with 4-color icon rotation */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:24px}
.feature-card{background:#fff;border-radius:12px;padding:32px 28px;box-shadow:0 4px 24px rgba(0,0,0,.06);border:1px solid rgba(0,0,0,.04);transition:transform .2s,box-shadow .2s}
.feature-card:hover{transform:translateY(-4px);box-shadow:0 12px 36px rgba(0,0,0,.1)}
.feature-icon{width:56px;height:56px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:26px;color:#fff;margin-bottom:20px;font-weight:900}
.feature-card:nth-child(1) .feature-icon{background:var(--mint)}
.feature-card:nth-child(2) .feature-icon{background:var(--yellow);color:var(--text)}
.feature-card:nth-child(3) .feature-icon{background:var(--red)}
.feature-card:nth-child(4) .feature-icon{background:var(--teal);color:var(--text)}
.feature-card h3{font-size:20px;font-weight:900;color:var(--text);margin-bottom:10px;letter-spacing:-.4px;line-height:1.25}
.feature-card p{color:var(--muted);font-size:15px;line-height:1.55}

/* CHANNELS MOCKUP — Slack-style chat UI */
.mockup-section{padding:0 24px 96px;background:var(--cream)}
.mockup-inner{max-width:1140px;margin:0 auto}
.mockup{background:#fff;border-radius:12px;box-shadow:0 24px 60px rgba(97,31,105,.2);overflow:hidden;display:grid;grid-template-columns:240px 1fr;min-height:380px;border:1px solid rgba(0,0,0,.06)}
.mockup-sidebar{background:var(--sidebar);color:rgba(255,255,255,.85);padding:20px 16px;font-size:14px}
.mockup-workspace{font-weight:900;color:#fff;font-size:16px;margin-bottom:18px;display:flex;align-items:center;gap:8px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,.1)}
.mockup-workspace::before{content:'\25C9';color:var(--mint);font-size:11px}
.mockup-section-title{font-size:11px;color:rgba(255,255,255,.55);text-transform:uppercase;letter-spacing:.5px;margin:14px 0 8px;font-weight:700}
.mockup-channel{padding:5px 8px;border-radius:4px;display:flex;align-items:center;gap:6px;color:rgba(255,255,255,.85);font-size:14px;margin-bottom:1px;cursor:pointer}
.mockup-channel.active{background:#1164a3;color:#fff;font-weight:700}
.mockup-channel::before{content:'#';opacity:.7}
.mockup-main{display:flex;flex-direction:column;background:#fff}
.mockup-channel-header{padding:14px 22px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;font-weight:900;color:var(--text);font-size:15px}
.mockup-channel-header::before{content:'#';color:var(--muted);font-weight:400;font-size:18px}
.mockup-messages{padding:22px;display:flex;flex-direction:column;gap:18px;flex:1}
.mockup-msg{display:grid;grid-template-columns:36px 1fr;gap:10px;align-items:flex-start}
.mockup-avatar{width:36px;height:36px;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:13px}
.mockup-msg:nth-child(1) .mockup-avatar{background:var(--mint)}
.mockup-msg:nth-child(2) .mockup-avatar{background:var(--yellow);color:var(--text)}
.mockup-msg:nth-child(3) .mockup-avatar{background:var(--red)}
.mockup-msg-head{display:flex;align-items:baseline;gap:8px;margin-bottom:4px}
.mockup-msg-name{font-weight:900;color:var(--text);font-size:14px}
.mockup-msg-time{color:var(--muted);font-size:12px}
.mockup-msg-body{color:var(--text);font-size:14px;line-height:1.5}
.mockup-msg-body strong{color:var(--aubergine);background:rgba(97,31,105,.08);padding:1px 4px;border-radius:3px}

/* STEPS — How It Works */
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.step{padding:32px;text-align:left}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:50%;background:var(--aubergine);color:#fff;font-weight:900;font-size:20px;margin-bottom:20px}
.step:nth-child(2) .step-num{background:var(--mint)}
.step:nth-child(3) .step-num{background:var(--yellow);color:var(--text)}
.step h3{font-size:22px;font-weight:900;color:var(--text);margin-bottom:10px;letter-spacing:-.5px;line-height:1.2}
.step p{color:var(--muted);font-size:15px;line-height:1.6}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{background:#fff;border-radius:12px;padding:36px 32px;box-shadow:0 4px 20px rgba(0,0,0,.06);border:1px solid rgba(0,0,0,.04);position:relative}
.review::before{content:'\201C';position:absolute;top:14px;left:24px;font-size:64px;line-height:1;font-family:Georgia,serif;font-weight:900;opacity:.95}
.review:nth-child(1)::before{color:var(--red)}
.review:nth-child(2)::before{color:var(--teal)}
.review-quote{font-size:17px;color:var(--text);line-height:1.55;font-weight:400;margin:36px 0 24px;font-style:italic}
.review-author{display:flex;align-items:center;gap:14px;padding-top:20px;border-top:1px solid var(--border)}
.review-avatar{width:48px;height:48px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:15px}
.review:nth-child(1) .review-avatar{background:var(--mint)}
.review:nth-child(2) .review-avatar{background:var(--aubergine)}
.review-name{font-weight:900;color:var(--text);font-size:15px;letter-spacing:-.2px}
.review-role{color:var(--muted);font-size:13px;margin-top:2px}

/* FAQ */
.faq{max-width:820px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--border);background:transparent}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:24px 4px;background:none;border:none;color:var(--text);font-size:18px;font-weight:900;text-align:left;cursor:pointer;font-family:inherit;letter-spacing:-.3px;line-height:1.4;transition:color .15s}
.faq-q:hover{color:var(--aubergine)}
.faq-q::after{content:'+';font-size:24px;color:var(--aubergine);font-weight:900;line-height:1;flex-shrink:0;transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:16px;line-height:1.65;padding:0 4px}
.faq-item.active .faq-a{max-height:300px;padding:0 4px 24px}

/* FOOTER */
.footer-cta{background:var(--aubergine);padding:80px 24px;color:#fff;text-align:center;position:relative;overflow:hidden}
.footer-cta::before{content:'';position:absolute;top:-80px;left:10%;width:200px;height:200px;background:var(--yellow);border-radius:50%;filter:blur(80px);opacity:.4;pointer-events:none}
.footer-cta::after{content:'';position:absolute;bottom:-80px;right:10%;width:200px;height:200px;background:var(--mint);border-radius:50%;filter:blur(80px);opacity:.4;pointer-events:none}
.footer-cta-inner{max-width:780px;margin:0 auto;position:relative;z-index:1}
.footer-cta h2{font-size:clamp(32px,4.5vw,52px);font-weight:900;letter-spacing:-1.4px;line-height:1.1;color:#fff;margin-bottom:18px}
.footer-cta p{font-size:18px;color:rgba(255,255,255,.88);margin-bottom:32px;line-height:1.55}
.footer-cta-btn{display:inline-flex;align-items:center;justify-content:center;padding:18px 36px;background:#fff;color:var(--aubergine);border-radius:4px;font-weight:900;font-size:14px;text-transform:uppercase;letter-spacing:.6px;transition:transform .15s,background .15s}
.footer-cta-btn:hover{background:var(--cream);transform:translateY(-2px);text-decoration:none}

.footer{background:var(--aubergine-dark);color:rgba(255,255,255,.75);padding:64px 24px 32px}
.footer-inner{max-width:1140px;margin:0 auto}
.footer-cols{display:grid;grid-template-columns:1.5fr repeat(4,1fr);gap:32px;padding-bottom:48px;border-bottom:1px solid rgba(255,255,255,.12)}
.footer-brand .logo-text{color:#fff}
.footer-brand p{margin-top:14px;font-size:14px;line-height:1.6;color:rgba(255,255,255,.7);max-width:280px}
.footer-col h4{font-size:13px;font-weight:900;color:#fff;text-transform:uppercase;letter-spacing:.8px;margin-bottom:16px}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:10px}
.footer-col a{color:rgba(255,255,255,.75);font-size:14px;transition:color .15s}
.footer-col a:hover{color:#fff;text-decoration:underline}
.footer-bottom{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;padding-top:24px;font-size:13px;color:rgba(255,255,255,.6)}
.footer-bottom .logo-mark{width:24px;height:24px;gap:2px}

@media(max-width:900px){
  .nav-links{display:none}
  .footer-cols{grid-template-columns:1fr 1fr;gap:28px}
}
@media(max-width:640px){
  .hero{padding:60px 18px 72px}
  .hero-form{grid-template-columns:1fr}
  .hero-form input[name="website"]{grid-column:1}
  .hero-form button{grid-column:1}
  .hero-ctas{flex-direction:column}
  .hero-ctas .btn{width:100%}
  .section{padding:64px 18px}
  .stats-strip{padding:36px 18px}
  .features-grid,.steps-grid,.reviews-grid{grid-template-columns:1fr}
  .mockup{grid-template-columns:1fr}
  .mockup-sidebar{display:none}
  .footer-cols{grid-template-columns:1fr}
  .nav-outline{display:none}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
  <a href="#" class="logo">
    <span class="logo-mark"><span></span><span></span><span></span><span></span></span>
    <span class="logo-text">slack</span>
  </a>
  <ul class="nav-links">
    <li><a href="#benefits">Features</a></li>
    <li><a href="#how">Solutions</a></li>
    <li><a href="#reviews">Enterprise</a></li>
    <li><a href="#faq">Resources</a></li>
    <li><a href="#form">Pricing</a></li>
  </ul>
  <div class="nav-right">
    <a href="#form" class="nav-signin">Sign in</a>
    <a href="#form" class="nav-outline">Talk to Sales</a>
    <a href="#form" class="nav-cta">Try for Free</a>
  </div>
</div></nav>

<section class="hero" id="form">
  <span class="blob blob-1"></span>
  <span class="blob blob-2"></span>
  <span class="blob blob-3"></span>
  <span class="blob blob-4"></span>
  <div class="hero-inner">
    <div class="badge">{{BADGE}}</div>
    <h1>{{HERO_TITLE}}</h1>
    <p class="sub">{{HERO_SUBTITLE}}</p>
    <div class="hero-ctas">
      <a href="#hero-form" class="btn btn-white">{{CTA_BUTTON}}</a>
      <a href="#how" class="btn btn-white-outline">Watch the demo</a>
    </div>
    <form id="hero-form" class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
      <input type="text" name="first_name" placeholder="First Name" required>
      <input type="text" name="last_name" placeholder="Last Name" required>
      <input type="email" name="email" placeholder="Work email" required>
      <input type="tel" name="phone" placeholder="Phone" required>
      <input type="url" name="website" placeholder="Company website" required>
      <button type="submit">{{CTA_BUTTON}}</button>
    </form>
  </div>
</section>

<section class="stats-strip">
  <div class="stats-inner">
    <div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
    <div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
    <div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
  </div>
</section>

<section class="section section-white" id="benefits">
  <div class="section-inner">
    <div class="section-header">
      <span class="eyebrow">Why teams choose us</span>
      <h2>{{BENEFITS_HEADLINE}}</h2>
      <p>{{BENEFITS_SUBHEADLINE}}</p>
    </div>
    <div class="features-grid">
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
    </div>
  </div>
</section>

<section class="mockup-section">
  <div class="mockup-inner">
    <div class="mockup">
      <aside class="mockup-sidebar">
        <div class="mockup-workspace">Acme HQ</div>
        <div class="mockup-section-title">Channels</div>
        <div class="mockup-channel active">general</div>
        <div class="mockup-channel">growth-loop</div>
        <div class="mockup-channel">launches</div>
        <div class="mockup-channel">design-review</div>
        <div class="mockup-section-title">Direct messages</div>
        <div class="mockup-channel" style="padding-left:8px">Riley Chen</div>
        <div class="mockup-channel" style="padding-left:8px">Sam Adeyemi</div>
      </aside>
      <div class="mockup-main">
        <div class="mockup-channel-header">general</div>
        <div class="mockup-messages">
          <div class="mockup-msg">
            <div class="mockup-avatar">MK</div>
            <div>
              <div class="mockup-msg-head"><span class="mockup-msg-name">Maya Kapoor</span><span class="mockup-msg-time">9:42 AM</span></div>
              <div class="mockup-msg-body">Pulled the Q3 numbers into <strong>#growth-loop</strong> — conversions are up 38% since we shipped.</div>
            </div>
          </div>
          <div class="mockup-msg">
            <div class="mockup-avatar">JT</div>
            <div>
              <div class="mockup-msg-head"><span class="mockup-msg-name">Jordan Tate</span><span class="mockup-msg-time">9:44 AM</span></div>
              <div class="mockup-msg-body">Love this. Can we surface it in <strong>@leadership</strong> stand-up tomorrow?</div>
            </div>
          </div>
          <div class="mockup-msg">
            <div class="mockup-avatar">RC</div>
            <div>
              <div class="mockup-msg-head"><span class="mockup-msg-name">Riley Chen</span><span class="mockup-msg-time">9:45 AM</span></div>
              <div class="mockup-msg-body">Already on the agenda. The team is going to be thrilled.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-white" id="how">
  <div class="section-inner">
    <div class="section-header">
      <span class="eyebrow">How it works</span>
      <h2>{{HOW_HEADLINE}}</h2>
      <p>{{HOW_SUBHEADLINE}}</p>
    </div>
    <div class="steps-grid">
      <div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
      <div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
      <div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
    </div>
  </div>
</section>

<section class="section section-cream" id="reviews">
  <div class="section-inner">
    <div class="section-header">
      <span class="eyebrow">Loved by teams</span>
      <h2>{{REVIEWS_HEADLINE}}</h2>
      <p>{{REVIEWS_SUBHEADLINE}}</p>
    </div>
    <div class="reviews-grid">
      <div class="review">
        <p class="review-quote">{{REVIEW_1_QUOTE}}</p>
        <div class="review-author">
          <div class="review-avatar">{{REVIEW_1_INITIALS}}</div>
          <div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div>
        </div>
      </div>
      <div class="review">
        <p class="review-quote">{{REVIEW_2_QUOTE}}</p>
        <div class="review-author">
          <div class="review-avatar">{{REVIEW_2_INITIALS}}</div>
          <div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-white" id="faq">
  <div class="section-inner">
    <div class="section-header">
      <span class="eyebrow">FAQ</span>
      <h2>{{FAQ_HEADLINE}}</h2>
      <p>{{FAQ_SUBHEADLINE}}</p>
    </div>
    <div class="faq">
      <div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
      <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
      <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
      <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
    </div>
  </div>
</section>

<section class="footer-cta">
  <div class="footer-cta-inner">
    <h2>{{FOOTER_HEADLINE}}</h2>
    <p>{{FOOTER_SUBHEADLINE}}</p>
    <a href="#form" class="footer-cta-btn">{{FOOTER_CTA}}</a>
  </div>
</section>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-cols">
      <div class="footer-brand">
        <a href="#" class="logo">
          <span class="logo-mark"><span></span><span></span><span></span><span></span></span>
          <span class="logo-text" style="color:#fff">slack</span>
        </a>
        <p>Where work happens — channels, messaging, automation and search, all in one place.</p>
      </div>
      <div class="footer-col"><h4>Product</h4><ul><li><a href="#benefits">Features</a></li><li><a href="#form">Integrations</a></li><li><a href="#form">Enterprise</a></li><li><a href="#form">Security</a></li></ul></div>
      <div class="footer-col"><h4>Pricing</h4><ul><li><a href="#form">Plans</a></li><li><a href="#form">Paid vs. Free</a></li><li><a href="#form">For Startups</a></li></ul></div>
      <div class="footer-col"><h4>Resources</h4><ul><li><a href="#faq">Help Center</a></li><li><a href="#how">Guides</a></li><li><a href="#reviews">Customers</a></li><li><a href="#form">Developers</a></li></ul></div>
      <div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Newsroom</a></li><li><a href="#">Careers</a></li><li><a href="#">Contact</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <span>© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com</span>
      <span>Privacy · Terms · Cookies</span>
    </div>
  </div>
</footer>

__FORM_SUBMIT_JS__
</body></html>
"""

# ─── Coinbase Finance ─────────────────────────────────────────────────────────────
_TPL_COINBASE_FINANCE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--pale:#f7f9fc;--text:#0a0b0d;--muted:#5b616e;--border:#ebedf0;--border-soft:#d8dadc;--blue:#0052ff;--blue-hover:#0041cc;--mint:#27d4a8;--mint-soft:#e6faf3;--red:#cf202f;--red-soft:#fdeaec;--dark-footer:#050505;--star:#f4a000}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:"Inter","Helvetica Neue","Helvetica","Arial",-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh;font-weight:400;font-feature-settings:'ss01','cv11'}
a{color:var(--blue);text-decoration:none}
img{max-width:100%;display:block}

/* NAV — clean white sticky */
.nav{position:sticky;top:0;left:0;right:0;z-index:100;background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(12px);-webkit-backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1280px;margin:0 auto;padding:0 24px;height:72px;display:flex;align-items:center;justify-content:space-between;gap:32px}
.logo{display:flex;align-items:center;gap:10px;flex-shrink:0}
.logo-mark{width:32px;height:32px;border-radius:50%;background:var(--blue);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:18px;letter-spacing:-1px}
.logo-text{font-weight:700;font-size:20px;color:var(--text);letter-spacing:-.4px}
.nav-links{display:flex;gap:28px;list-style:none;align-items:center;flex:1;justify-content:flex-start;margin-left:8px}
.nav-links a{color:var(--text);font-size:15px;font-weight:500;display:inline-flex;align-items:center;gap:4px;transition:color .15s}
.nav-links a.has-caret::after{content:'\02C5';font-size:13px;color:var(--muted);margin-top:2px}
.nav-links a:hover{color:var(--blue)}
.nav-right{display:flex;align-items:center;gap:14px;flex-shrink:0}
.nav-signin{color:var(--text);font-size:15px;font-weight:500;padding:8px 4px}
.nav-signin:hover{color:var(--blue)}
.nav-cta{display:inline-flex;align-items:center;justify-content:center;padding:11px 22px;background:var(--text);color:#fff!important;border-radius:999px;font-weight:600;font-size:14px;transition:background .15s,transform .15s;font-family:inherit}
.nav-cta:hover{background:#272a2f;text-decoration:none;transform:translateY(-1px)}

/* HERO — huge dark headline, signup form, ticker below */
.hero{padding:96px 24px 60px;background:#fff;position:relative}
.hero-inner{max-width:1180px;margin:0 auto;text-align:center}
.eyebrow{display:inline-block;font-size:14px;font-weight:600;color:var(--blue);background:rgba(0,82,255,.08);padding:6px 14px;border-radius:999px;margin-bottom:24px;letter-spacing:-.1px}
.eyebrow::before{content:'\2728  ';margin-right:4px}
.hero h1{font-size:clamp(40px,6vw,80px);font-weight:700;line-height:1;letter-spacing:-3px;color:var(--text);margin-bottom:24px;max-width:1000px;margin-left:auto;margin-right:auto}
.hero h1 .accent{color:var(--blue)}
.hero p.sub{font-size:clamp(17px,2.2vw,21px);color:var(--muted);max-width:640px;margin:0 auto 40px;line-height:1.45;font-weight:400}

/* Coinbase-style signup form: pill input + dark pill CTA */
.hero-form-wrap{max-width:560px;margin:0 auto 24px}
.hero-form{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.hero-form input{padding:15px 20px;border:1px solid var(--border-soft);border-radius:999px;font-size:15px;font-family:inherit;outline:none;background:#fff;color:var(--text);transition:border-color .15s,box-shadow .15s;font-weight:500}
.hero-form input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(0,82,255,.12)}
.hero-form input::placeholder{color:var(--muted)}
.hero-form input[name="email"],.hero-form input[name="website"]{grid-column:1/3}
.hero-form button{grid-column:1/3;padding:16px 28px;background:var(--text);color:#fff;border:none;border-radius:999px;font-weight:600;font-size:15px;cursor:pointer;font-family:inherit;transition:background .15s,transform .15s;letter-spacing:-.1px}
.hero-form button:hover{background:#272a2f;transform:translateY(-1px)}
.hero-disclaimer{font-size:13px;color:var(--muted);margin-top:14px;font-weight:400}
.hero-disclaimer a{color:var(--blue);text-decoration:underline}

/* TICKER STRIP — fake crypto prices with sparkline placeholders */
.ticker{background:var(--pale);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:0;overflow:hidden;position:relative;margin-top:48px}
.ticker-inner{display:flex;align-items:center;gap:48px;padding:18px 24px;overflow-x:auto;-webkit-overflow-scrolling:touch;white-space:nowrap;font-feature-settings:'tnum'}
.ticker-inner::-webkit-scrollbar{display:none}
.ticker-item{display:inline-flex;align-items:center;gap:12px;flex-shrink:0}
.ticker-icon{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:12px;letter-spacing:-.5px}
.ti-btc{background:#f7931a}
.ti-eth{background:#627eea}
.ti-sol{background:linear-gradient(135deg,#9945ff,#14f195)}
.ti-usdc{background:#2775ca}
.ti-link{background:#2a5ada}
.ti-doge{background:#c2a633}
.ti-ada{background:#0033ad}
.ti-xrp{background:#23292f}
.ticker-meta{display:flex;flex-direction:column;gap:1px;align-items:flex-start}
.ticker-symbol{font-size:13px;font-weight:700;color:var(--text);letter-spacing:-.1px;line-height:1}
.ticker-name{font-size:11px;color:var(--muted);font-weight:500;line-height:1}
.ticker-price{font-size:14px;font-weight:700;color:var(--text);letter-spacing:-.1px;font-feature-settings:'tnum'}
.ticker-change{font-size:12px;font-weight:600;padding:2px 6px;border-radius:4px;letter-spacing:-.1px;font-feature-settings:'tnum'}
.ticker-up{color:var(--mint);background:var(--mint-soft)}
.ticker-down{color:var(--red);background:var(--red-soft)}
.ticker-spark{width:60px;height:24px;display:block;flex-shrink:0}

/* SECTIONS */
.section{padding:96px 24px}
.section-pale{background:var(--pale)}
.section-white{background:#fff}
.section-inner{max-width:1180px;margin:0 auto}
.section-header{text-align:center;margin-bottom:64px;max-width:760px;margin-left:auto;margin-right:auto}
.section-header .small-eyebrow{display:inline-block;font-size:13px;font-weight:700;color:var(--blue);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:14px}
.section-header h2{font-size:clamp(32px,4.5vw,56px);font-weight:700;letter-spacing:-2px;line-height:1.05;color:var(--text);margin-bottom:18px}
.section-header p{color:var(--muted);font-size:19px;line-height:1.55;font-weight:400}

/* STATS — big blue numbers */
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;margin-bottom:24px}
.stat-card{background:#fff;border:1px solid var(--border);border-radius:16px;padding:36px 32px;text-align:left;transition:transform .15s,box-shadow .15s}
.stat-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,82,255,.08)}
.stat-num{font-size:52px;font-weight:700;color:var(--blue);letter-spacing:-2.5px;line-height:1;font-feature-settings:'tnum'}
.stat-label{font-size:14px;color:var(--muted);margin-top:10px;font-weight:500}

/* FEATURE CARDS — white with blue→mint gradient icons */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.feature-card{background:#fff;border:1px solid var(--border);border-radius:16px;padding:36px 32px;transition:transform .2s,box-shadow .2s,border-color .2s}
.feature-card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(0,82,255,.1);border-color:rgba(0,82,255,.2)}
.feature-icon{width:56px;height:56px;border-radius:14px;background:linear-gradient(135deg,var(--blue),var(--mint));display:flex;align-items:center;justify-content:center;font-size:24px;color:#fff;margin-bottom:24px;box-shadow:0 4px 14px rgba(0,82,255,.18)}
.feature-card h3{font-size:20px;font-weight:700;color:var(--text);margin-bottom:10px;letter-spacing:-.4px;line-height:1.25}
.feature-card p{color:var(--muted);font-size:15px;line-height:1.55}

/* TRUST BADGES */
.trust-section{padding:64px 24px;background:#fff;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.trust-inner{max-width:1180px;margin:0 auto}
.trust-title{text-align:center;font-size:14px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:32px}
.trust-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px}
.trust-badge{display:flex;flex-direction:column;align-items:center;gap:8px;padding:24px 16px;background:var(--pale);border:1px solid var(--border);border-radius:12px;text-align:center;transition:border-color .15s,transform .15s}
.trust-badge:hover{border-color:var(--blue);transform:translateY(-2px)}
.trust-icon{font-size:28px;line-height:1}
.trust-label{font-size:13px;font-weight:700;color:var(--text);letter-spacing:-.1px}
.trust-sub{font-size:11px;color:var(--muted);font-weight:500}

/* STEPS */
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}
.step{background:#fff;border:1px solid var(--border);border-radius:16px;padding:36px 32px;position:relative;transition:transform .15s,box-shadow .15s}
.step:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.06)}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;font-size:18px;margin-bottom:20px;letter-spacing:-.5px}
.step h3{font-size:22px;font-weight:700;color:var(--text);margin-bottom:10px;letter-spacing:-.5px;line-height:1.2}
.step p{color:var(--muted);font-size:15px;line-height:1.6}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{background:#fff;border:1px solid var(--border);border-radius:16px;padding:36px 32px;transition:border-color .15s,transform .15s}
.review:hover{border-color:rgba(0,82,255,.2);transform:translateY(-2px)}
.review-stars{color:var(--star);font-size:16px;letter-spacing:2px;margin-bottom:16px}
.review-quote{font-size:17px;color:var(--text);line-height:1.55;font-weight:500;margin-bottom:24px;letter-spacing:-.2px}
.review-author{display:flex;align-items:center;gap:14px;padding-top:20px;border-top:1px solid var(--border)}
.review-avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--blue),var(--mint));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px}
.review-name{font-weight:700;color:var(--text);font-size:15px;letter-spacing:-.2px}
.review-role{color:var(--muted);font-size:13px;margin-top:2px;font-weight:500}

/* FAQ */
.faq{max-width:860px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--border);background:transparent}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:28px 4px;background:none;border:none;color:var(--text);font-size:19px;font-weight:600;text-align:left;cursor:pointer;font-family:inherit;letter-spacing:-.4px;line-height:1.4;transition:color .15s}
.faq-q:hover{color:var(--blue)}
.faq-q::after{content:'+';font-size:24px;color:var(--blue);font-weight:500;line-height:1;flex-shrink:0;transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:16px;line-height:1.65;padding:0 4px;font-weight:400}
.faq-item.active .faq-a{max-height:320px;padding:0 4px 28px}

/* FOOTER CTA — dark navy */
.footer-cta{background:linear-gradient(135deg,var(--blue),#0033cc);padding:88px 24px;color:#fff;text-align:center;position:relative;overflow:hidden}
.footer-cta::before{content:'';position:absolute;top:-120px;left:-80px;width:380px;height:380px;background:radial-gradient(circle,rgba(39,212,168,.35),transparent 65%);border-radius:50%;pointer-events:none}
.footer-cta::after{content:'';position:absolute;bottom:-120px;right:-80px;width:380px;height:380px;background:radial-gradient(circle,rgba(255,255,255,.18),transparent 65%);border-radius:50%;pointer-events:none}
.footer-cta-inner{max-width:780px;margin:0 auto;position:relative;z-index:1}
.footer-cta h2{font-size:clamp(32px,4.5vw,56px);font-weight:700;letter-spacing:-2px;line-height:1.05;color:#fff;margin-bottom:18px}
.footer-cta p{font-size:19px;color:rgba(255,255,255,.92);margin-bottom:36px;line-height:1.55}
.footer-cta-btn{display:inline-flex;align-items:center;justify-content:center;padding:18px 36px;background:#fff;color:var(--text);border-radius:999px;font-weight:700;font-size:15px;transition:transform .15s,background .15s;letter-spacing:-.1px}
.footer-cta-btn:hover{background:var(--pale);transform:translateY(-2px);text-decoration:none}

/* FOOTER — very dark with 6 columns */
.footer{background:var(--dark-footer);color:rgba(255,255,255,.65);padding:80px 24px 32px}
.footer-inner{max-width:1280px;margin:0 auto}
.footer-cols{display:grid;grid-template-columns:repeat(6,1fr);gap:32px;padding-bottom:56px;border-bottom:1px solid rgba(255,255,255,.1)}
.footer-col h4{font-size:14px;font-weight:700;color:#fff;margin-bottom:20px;letter-spacing:-.2px}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:12px}
.footer-col a{color:rgba(255,255,255,.65);font-size:14px;transition:color .15s}
.footer-col a:hover{color:#fff;text-decoration:underline}
.footer-bottom{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:18px;padding-top:32px;font-size:13px;color:rgba(255,255,255,.55)}
.footer-bottom .footer-logo{display:flex;align-items:center;gap:10px}
.footer-bottom .footer-logo .logo-mark{width:28px;height:28px;font-size:16px}
.footer-bottom .footer-logo span{color:#fff;font-weight:700;font-size:18px}
.footer-disclaimer{margin-top:24px;font-size:12px;color:rgba(255,255,255,.45);line-height:1.6;max-width:920px}

@media(max-width:900px){
  .nav-links{display:none}
  .footer-cols{grid-template-columns:repeat(3,1fr);gap:28px}
  .ticker-inner{gap:32px}
}
@media(max-width:640px){
  .hero{padding:64px 18px 40px}
  .hero-form{grid-template-columns:1fr}
  .hero-form input[name="email"],.hero-form input[name="website"]{grid-column:1}
  .section{padding:64px 18px}
  .trust-section{padding:48px 18px}
  .stats-grid,.features-grid,.steps-grid,.reviews-grid,.trust-grid{grid-template-columns:1fr 1fr}
  .footer-cols{grid-template-columns:1fr 1fr;gap:24px}
  .footer-cta{padding:64px 18px}
  .nav-cta{padding:9px 18px;font-size:13px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
  <a href="#" class="logo">
    <span class="logo-mark">C</span>
    <span class="logo-text">Coinbase</span>
  </a>
  <ul class="nav-links">
    <li><a href="#benefits" class="has-caret">Individual</a></li>
    <li><a href="#how" class="has-caret">Business</a></li>
    <li><a href="#reviews" class="has-caret">Developers</a></li>
    <li><a href="#faq">Pricing</a></li>
    <li><a href="#form">Company</a></li>
  </ul>
  <div class="nav-right">
    <a href="#form" class="nav-signin">Sign in</a>
    <a href="#form" class="nav-cta">Get Started</a>
  </div>
</div></nav>

<section class="hero" id="form">
  <div class="hero-inner">
    <span class="eyebrow">{{BADGE}}</span>
    <h1>{{HERO_TITLE}}</h1>
    <p class="sub">{{HERO_SUBTITLE}}</p>
    <div class="hero-form-wrap">
      <form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
        <input type="text" name="first_name" placeholder="First name" required>
        <input type="text" name="last_name" placeholder="Last name" required>
        <input type="email" name="email" placeholder="Enter your email" required>
        <input type="tel" name="phone" placeholder="Phone number" required>
        <input type="url" name="website" placeholder="Company website" required>
        <button type="submit">{{CTA_BUTTON}}</button>
      </form>
      <div class="hero-disclaimer">By continuing you agree to our <a href="#faq">User Agreement</a> and <a href="#faq">Privacy Policy</a>.</div>
    </div>
  </div>
</section>

<div class="ticker">
  <div class="ticker-inner">
    <div class="ticker-item">
      <div class="ticker-icon ti-btc">B</div>
      <div class="ticker-meta"><span class="ticker-symbol">BTC</span><span class="ticker-name">Bitcoin</span></div>
      <span class="ticker-price">$67,432</span>
      <span class="ticker-change ticker-up">+2.34%</span>
      <svg class="ticker-spark" viewBox="0 0 60 24"><polyline fill="none" stroke="#27d4a8" stroke-width="1.5" points="0,18 8,14 16,16 24,10 32,12 40,7 48,9 60,3"/></svg>
    </div>
    <div class="ticker-item">
      <div class="ticker-icon ti-eth">E</div>
      <div class="ticker-meta"><span class="ticker-symbol">ETH</span><span class="ticker-name">Ethereum</span></div>
      <span class="ticker-price">$3,890.21</span>
      <span class="ticker-change ticker-up">+1.12%</span>
      <svg class="ticker-spark" viewBox="0 0 60 24"><polyline fill="none" stroke="#27d4a8" stroke-width="1.5" points="0,16 8,18 16,14 24,15 32,10 40,11 48,8 60,6"/></svg>
    </div>
    <div class="ticker-item">
      <div class="ticker-icon ti-sol">S</div>
      <div class="ticker-meta"><span class="ticker-symbol">SOL</span><span class="ticker-name">Solana</span></div>
      <span class="ticker-price">$245.18</span>
      <span class="ticker-change ticker-down">-0.84%</span>
      <svg class="ticker-spark" viewBox="0 0 60 24"><polyline fill="none" stroke="#cf202f" stroke-width="1.5" points="0,6 8,8 16,10 24,9 32,13 40,12 48,16 60,17"/></svg>
    </div>
    <div class="ticker-item">
      <div class="ticker-icon ti-usdc">U</div>
      <div class="ticker-meta"><span class="ticker-symbol">USDC</span><span class="ticker-name">USD Coin</span></div>
      <span class="ticker-price">$1.0001</span>
      <span class="ticker-change ticker-up">+0.01%</span>
      <svg class="ticker-spark" viewBox="0 0 60 24"><polyline fill="none" stroke="#27d4a8" stroke-width="1.5" points="0,12 8,12 16,11 24,12 32,12 40,11 48,12 60,12"/></svg>
    </div>
    <div class="ticker-item">
      <div class="ticker-icon ti-link">L</div>
      <div class="ticker-meta"><span class="ticker-symbol">LINK</span><span class="ticker-name">Chainlink</span></div>
      <span class="ticker-price">$18.47</span>
      <span class="ticker-change ticker-up">+4.12%</span>
      <svg class="ticker-spark" viewBox="0 0 60 24"><polyline fill="none" stroke="#27d4a8" stroke-width="1.5" points="0,18 8,15 16,12 24,14 32,9 40,8 48,5 60,4"/></svg>
    </div>
    <div class="ticker-item">
      <div class="ticker-icon ti-doge">D</div>
      <div class="ticker-meta"><span class="ticker-symbol">DOGE</span><span class="ticker-name">Dogecoin</span></div>
      <span class="ticker-price">$0.187</span>
      <span class="ticker-change ticker-down">-1.42%</span>
      <svg class="ticker-spark" viewBox="0 0 60 24"><polyline fill="none" stroke="#cf202f" stroke-width="1.5" points="0,8 8,10 16,9 24,12 32,11 40,14 48,15 60,17"/></svg>
    </div>
    <div class="ticker-item">
      <div class="ticker-icon ti-ada">A</div>
      <div class="ticker-meta"><span class="ticker-symbol">ADA</span><span class="ticker-name">Cardano</span></div>
      <span class="ticker-price">$0.62</span>
      <span class="ticker-change ticker-up">+0.78%</span>
      <svg class="ticker-spark" viewBox="0 0 60 24"><polyline fill="none" stroke="#27d4a8" stroke-width="1.5" points="0,14 8,13 16,12 24,11 32,10 40,11 48,9 60,8"/></svg>
    </div>
    <div class="ticker-item">
      <div class="ticker-icon ti-xrp">X</div>
      <div class="ticker-meta"><span class="ticker-symbol">XRP</span><span class="ticker-name">XRP</span></div>
      <span class="ticker-price">$0.524</span>
      <span class="ticker-change ticker-up">+2.91%</span>
      <svg class="ticker-spark" viewBox="0 0 60 24"><polyline fill="none" stroke="#27d4a8" stroke-width="1.5" points="0,18 8,16 16,14 24,11 32,12 40,8 48,7 60,5"/></svg>
    </div>
  </div>
</div>

<section class="section section-white" id="stats">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">By the numbers</span>
      <h2>Trusted by millions worldwide.</h2>
    </div>
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
      <div class="stat-card"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
      <div class="stat-card"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
    </div>
  </div>
</section>

<section class="section section-pale" id="benefits">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">Why us</span>
      <h2>{{BENEFITS_HEADLINE}}</h2>
      <p>{{BENEFITS_SUBHEADLINE}}</p>
    </div>
    <div class="features-grid">
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
    </div>
  </div>
</section>

<section class="trust-section">
  <div class="trust-inner">
    <div class="trust-title">Built on trust. Backed by leaders.</div>
    <div class="trust-grid">
      <div class="trust-badge"><div class="trust-icon">&#128272;</div><div class="trust-label">FDIC Insured</div><div class="trust-sub">Up to $250K</div></div>
      <div class="trust-badge"><div class="trust-icon">&#128737;</div><div class="trust-label">SOC 2 Type II</div><div class="trust-sub">Certified</div></div>
      <div class="trust-badge"><div class="trust-icon">&#9989;</div><div class="trust-label">$100M+ Secured</div><div class="trust-sub">Cold storage</div></div>
      <div class="trust-badge"><div class="trust-icon">&#127963;</div><div class="trust-label">SEC Registered</div><div class="trust-sub">Compliant</div></div>
      <div class="trust-badge"><div class="trust-icon">&#127758;</div><div class="trust-label">100+ Countries</div><div class="trust-sub">Available</div></div>
      <div class="trust-badge"><div class="trust-icon">&#128172;</div><div class="trust-label">24/7 Support</div><div class="trust-sub">Live agents</div></div>
    </div>
  </div>
</section>

<section class="section section-white" id="how">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">Getting started</span>
      <h2>{{HOW_HEADLINE}}</h2>
      <p>{{HOW_SUBHEADLINE}}</p>
    </div>
    <div class="steps-grid">
      <div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
      <div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
      <div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
    </div>
  </div>
</section>

<section class="section section-pale" id="reviews">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">Customer stories</span>
      <h2>{{REVIEWS_HEADLINE}}</h2>
      <p>{{REVIEWS_SUBHEADLINE}}</p>
    </div>
    <div class="reviews-grid">
      <div class="review">
        <div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
        <div class="review-author">
          <div class="review-avatar">{{REVIEW_1_INITIALS}}</div>
          <div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div>
        </div>
      </div>
      <div class="review">
        <div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
        <div class="review-author">
          <div class="review-avatar">{{REVIEW_2_INITIALS}}</div>
          <div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-white" id="faq">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">Questions</span>
      <h2>{{FAQ_HEADLINE}}</h2>
      <p>{{FAQ_SUBHEADLINE}}</p>
    </div>
    <div class="faq">
      <div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
      <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
      <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
      <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
    </div>
  </div>
</section>

<section class="footer-cta">
  <div class="footer-cta-inner">
    <h2>{{FOOTER_HEADLINE}}</h2>
    <p>{{FOOTER_SUBHEADLINE}}</p>
    <a href="#form" class="footer-cta-btn">{{FOOTER_CTA}}</a>
  </div>
</section>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-cols">
      <div class="footer-col"><h4>Get Started</h4><ul><li><a href="#form">Sign up</a></li><li><a href="#form">Mobile app</a></li><li><a href="#form">Buy & sell</a></li><li><a href="#form">Wallet</a></li></ul></div>
      <div class="footer-col"><h4>Resources</h4><ul><li><a href="#how">How it works</a></li><li><a href="#benefits">Features</a></li><li><a href="#reviews">Reviews</a></li><li><a href="#faq">FAQ</a></li></ul></div>
      <div class="footer-col"><h4>Products</h4><ul><li><a href="#form">Individual</a></li><li><a href="#form">Business</a></li><li><a href="#form">Institutional</a></li><li><a href="#form">Developer</a></li></ul></div>
      <div class="footer-col"><h4>Learn</h4><ul><li><a href="#">Guides</a></li><li><a href="#">Glossary</a></li><li><a href="#">Newsroom</a></li><li><a href="#">Research</a></li></ul></div>
      <div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Careers</a></li><li><a href="#">Partners</a></li><li><a href="#">Contact</a></li></ul></div>
      <div class="footer-col"><h4>Legal</h4><ul><li><a href="#">Privacy</a></li><li><a href="#">Terms</a></li><li><a href="#">Cookies</a></li><li><a href="#">Disclosures</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <div class="footer-logo">
        <span class="logo-mark">C</span>
        <span>Coinbase</span>
      </div>
      <span>© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com</span>
    </div>
    <div class="footer-disclaimer">Cryptocurrency services are provided by Eko AI. Investing involves risk including loss of principal. Past performance does not guarantee future results. This is a marketing landing page; products and availability may vary by region.</div>
  </div>
</footer>

__FORM_SUBMIT_JS__
</body></html>
"""

# ─── Webflow Pro ─────────────────────────────────────────────────────────────
_TPL_WEBFLOW_PRO = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#000;--surface:#0c0c10;--surface-2:#1a1a1f;--border:#2a2a30;--border-bright:#3a3a44;--text:#fff;--muted:#969699;--muted-soft:#6b6b70;--electric:#4353ff;--electric-dim:#2a36b8;--cyan:#00d1ff;--accent:#a3a4ff}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:"Inter","Helvetica Neue","Helvetica","Arial",-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh;font-weight:400}
a{color:var(--cyan);text-decoration:none}
img{max-width:100%;display:block}
.divider{height:1px;background:linear-gradient(90deg,transparent,var(--electric),transparent);opacity:.5;margin:0 auto;max-width:1280px}

/* NAV — black sticky */
.nav{position:sticky;top:0;left:0;right:0;z-index:100;background:rgba(0,0,0,.75);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1320px;margin:0 auto;padding:0 28px;height:72px;display:flex;align-items:center;justify-content:space-between;gap:32px}
.logo{display:flex;align-items:center;gap:10px;flex-shrink:0}
.logo-mark{width:32px;height:32px;background:var(--electric);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:18px;letter-spacing:-1px;box-shadow:0 0 16px rgba(67,83,255,.45)}
.logo-text{font-weight:800;font-size:20px;color:#fff;letter-spacing:-.5px}
.nav-links{display:flex;gap:28px;list-style:none;align-items:center;flex:1;justify-content:flex-start;margin-left:8px}
.nav-links a{color:var(--muted);font-size:15px;font-weight:500;display:inline-flex;align-items:center;gap:4px;transition:color .15s}
.nav-links a.has-caret::after{content:'\02C5';font-size:13px;margin-top:2px;opacity:.6}
.nav-links a:hover{color:#fff}
.nav-right{display:flex;align-items:center;gap:14px;flex-shrink:0}
.nav-signin{color:var(--muted);font-size:15px;font-weight:500;padding:8px 4px;transition:color .15s}
.nav-signin:hover{color:#fff}
.nav-cta{display:inline-flex;align-items:center;justify-content:center;padding:11px 22px;background:#fff;color:#000!important;border-radius:999px;font-weight:700;font-size:14px;transition:background .15s,transform .15s;font-family:inherit;letter-spacing:-.1px}
.nav-cta:hover{background:#e8e8ec;text-decoration:none;transform:translateY(-1px)}

/* HERO — black with radial glow */
.hero{padding:96px 28px 64px;position:relative;overflow:hidden;background:#000}
.hero::before{content:'';position:absolute;top:-200px;left:50%;transform:translateX(-50%);width:900px;height:600px;background:radial-gradient(ellipse,rgba(67,83,255,.35),transparent 65%);pointer-events:none;filter:blur(60px)}
.hero::after{content:'';position:absolute;bottom:-100px;left:0;right:0;height:200px;background:linear-gradient(180deg,transparent,#000);pointer-events:none;z-index:1}
.hero-inner{max-width:1180px;margin:0 auto;text-align:center;position:relative;z-index:2}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:#fff;background:rgba(255,255,255,.06);border:1px solid var(--border);padding:6px 14px;border-radius:999px;margin-bottom:28px;letter-spacing:-.1px;backdrop-filter:blur(8px)}
.eyebrow .dot{width:8px;height:8px;border-radius:50%;background:var(--electric);box-shadow:0 0 8px var(--electric);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.hero h1{font-size:clamp(48px,7vw,96px);font-weight:800;line-height:.95;letter-spacing:-3px;color:#fff;margin-bottom:28px;max-width:1100px;margin-left:auto;margin-right:auto}
.hero h1 .accent{background:linear-gradient(135deg,var(--electric),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero p.sub{font-size:clamp(18px,2.4vw,23px);color:var(--muted);max-width:680px;margin:0 auto 40px;line-height:1.45;font-weight:400}
.hero-ctas{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-bottom:56px}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:16px 28px;border-radius:999px;font-weight:700;font-size:15px;cursor:pointer;border:none;font-family:inherit;text-decoration:none;transition:all .2s;letter-spacing:-.1px;gap:8px}
.btn-white{background:#fff;color:#000!important}
.btn-white:hover{background:#e8e8ec;transform:translateY(-1px);text-decoration:none}
.btn-outline{background:transparent;color:#fff!important;border:1px solid var(--border-bright)}
.btn-outline:hover{background:rgba(255,255,255,.06);border-color:#fff;text-decoration:none}

/* HERO FORM — dark glass */
.hero-form-wrap{max-width:680px;margin:0 auto}
.hero-form{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:24px;background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:16px;backdrop-filter:blur(12px);box-shadow:0 24px 60px rgba(0,0,0,.6),0 0 0 1px rgba(67,83,255,.08)}
.hero-form input{padding:14px 18px;border:1px solid var(--border-bright);background:#0c0c10;color:#fff;font-size:15px;border-radius:8px;font-family:inherit;outline:none;transition:border-color .15s,box-shadow .15s;font-weight:500}
.hero-form input:focus{border-color:var(--electric);box-shadow:0 0 0 3px rgba(67,83,255,.2)}
.hero-form input::placeholder{color:var(--muted-soft)}
.hero-form input[name="website"]{grid-column:1/3}
.hero-form button{grid-column:1/3;padding:16px;background:var(--electric);color:#fff;border:none;border-radius:8px;font-weight:700;font-size:15px;cursor:pointer;font-family:inherit;transition:background .15s,transform .15s;letter-spacing:-.1px;box-shadow:0 8px 24px rgba(67,83,255,.35)}
.hero-form button:hover{background:#5663ff;transform:translateY(-1px)}

/* DESIGNER CANVAS MOCKUP */
.mockup-section{padding:0 28px 96px;background:#000;position:relative;z-index:3}
.mockup-inner{max-width:1180px;margin:0 auto}
.mockup{background:var(--surface);border:1px solid var(--border);border-radius:18px;overflow:hidden;display:grid;grid-template-columns:240px 1fr 240px;min-height:440px;box-shadow:0 40px 100px rgba(67,83,255,.18),0 0 0 1px rgba(255,255,255,.04)}
.mockup-topbar{grid-column:1/4;display:flex;align-items:center;padding:12px 16px;border-bottom:1px solid var(--border);background:var(--surface-2);gap:12px}
.mockup-dots{display:flex;gap:6px}
.mockup-dots span{width:12px;height:12px;border-radius:50%;background:#3a3a44}
.mockup-dots span:nth-child(1){background:#ff5f57}
.mockup-dots span:nth-child(2){background:#ffbd2e}
.mockup-dots span:nth-child(3){background:#28c840}
.mockup-tab{font-size:12px;color:var(--muted);padding:4px 10px;border-radius:4px;background:rgba(255,255,255,.04);display:inline-flex;align-items:center;gap:6px;font-weight:500}
.mockup-tab.active{background:var(--electric);color:#fff}
.mockup-body{display:contents}
.mockup-left,.mockup-right{background:var(--surface-2);padding:18px 14px;font-size:12px;color:var(--muted);border-right:1px solid var(--border)}
.mockup-right{border-right:none;border-left:1px solid var(--border)}
.mockup-panel-title{font-size:11px;color:var(--muted-soft);text-transform:uppercase;letter-spacing:.6px;margin-bottom:10px;font-weight:700}
.mockup-tree-item{padding:5px 8px;border-radius:4px;display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted);margin-bottom:2px;cursor:pointer}
.mockup-tree-item::before{content:'\25BC';font-size:9px;color:var(--muted-soft)}
.mockup-tree-item.leaf::before{content:'\2022';font-size:11px}
.mockup-tree-item.active{background:rgba(67,83,255,.18);color:#fff}
.mockup-tree-item.l2{padding-left:18px}
.mockup-tree-item.l3{padding-left:28px}
.mockup-tree-item.l4{padding-left:38px}
.mockup-canvas{background:#1a1a1f;background-image:radial-gradient(circle,rgba(67,83,255,.08) 1px,transparent 1px);background-size:18px 18px;padding:36px 28px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;position:relative}
.mockup-canvas::before{content:'';position:absolute;top:14px;left:14px;right:14px;bottom:14px;border:1px dashed rgba(67,83,255,.35);border-radius:8px;pointer-events:none}
.mockup-canvas-h{font-size:32px;font-weight:800;color:#fff;letter-spacing:-1.4px;margin-bottom:12px;line-height:1.05;max-width:380px}
.mockup-canvas-p{font-size:13px;color:var(--muted);max-width:340px;line-height:1.5;margin-bottom:18px}
.mockup-canvas-btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 20px;background:var(--electric);color:#fff;border-radius:999px;font-size:13px;font-weight:700}
.mockup-prop{display:flex;align-items:center;justify-content:space-between;padding:6px 4px;border-bottom:1px solid rgba(255,255,255,.04);font-size:11px}
.mockup-prop-key{color:var(--muted)}
.mockup-prop-val{color:#fff;font-weight:600;font-family:"SF Mono","Menlo",monospace;font-size:11px}
.mockup-swatch{display:flex;align-items:center;gap:6px}
.mockup-swatch-box{width:14px;height:14px;border-radius:3px;background:var(--electric);border:1px solid var(--border-bright)}

/* TRUST STRIP */
.trust-strip{padding:48px 28px;background:#000;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.trust-inner{max-width:1180px;margin:0 auto}
.trust-title{text-align:center;font-size:13px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:1.4px;margin-bottom:28px}
.trust-brands{display:flex;justify-content:space-around;align-items:center;gap:32px;flex-wrap:wrap;color:var(--muted-soft);font-weight:800;font-size:18px;letter-spacing:1.2px;text-transform:uppercase;opacity:.85}
.trust-brands span{transition:color .15s,opacity .15s;cursor:default}
.trust-brands span:hover{color:#fff;opacity:1}

/* SECTIONS */
.section{padding:112px 28px;position:relative}
.section-inner{max-width:1180px;margin:0 auto}
.section-header{text-align:center;margin-bottom:72px;max-width:780px;margin-left:auto;margin-right:auto}
.small-eyebrow{display:inline-block;font-size:12px;font-weight:700;color:var(--cyan);text-transform:uppercase;letter-spacing:2px;margin-bottom:18px}
.section-header h2{font-size:clamp(36px,5vw,64px);font-weight:800;letter-spacing:-2px;line-height:1.02;color:#fff;margin-bottom:18px}
.section-header h2 .accent{background:linear-gradient(135deg,var(--electric),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.section-header p{color:var(--muted);font-size:19px;line-height:1.5;font-weight:400}

/* STATS */
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;margin-bottom:24px}
.stat-card{padding:36px 32px;text-align:left;border-top:1px solid var(--border)}
.stat-eyebrow{font-size:12px;font-weight:700;color:var(--cyan);text-transform:uppercase;letter-spacing:1.4px;margin-bottom:14px}
.stat-num{font-size:64px;font-weight:900;color:#fff;letter-spacing:-3px;line-height:1;font-feature-settings:'tnum'}
.stat-label{font-size:15px;color:var(--muted);margin-top:14px;font-weight:500;line-height:1.5}

/* FEATURE CARDS — dark with electric hover */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:20px}
.feature-card{background:var(--surface-2);border:1px solid var(--border);border-radius:18px;padding:36px 32px;transition:transform .2s,border-color .2s,box-shadow .2s}
.feature-card:hover{transform:translateY(-4px);border-color:var(--electric);box-shadow:0 16px 40px rgba(67,83,255,.18)}
.feature-icon{width:52px;height:52px;border-radius:12px;background:rgba(67,83,255,.14);border:1px solid rgba(67,83,255,.3);display:flex;align-items:center;justify-content:center;font-size:22px;color:var(--electric);margin-bottom:24px}
.feature-card h3{font-size:21px;font-weight:700;color:#fff;margin-bottom:12px;letter-spacing:-.5px;line-height:1.2}
.feature-card p{color:var(--muted);font-size:15px;line-height:1.6}

/* STEPS */
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.step{background:var(--surface-2);border:1px solid var(--border);border-radius:18px;padding:36px 32px;position:relative;transition:border-color .15s,transform .15s}
.step:hover{border-color:var(--border-bright);transform:translateY(-2px)}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,var(--electric),var(--cyan));color:#fff;font-weight:900;font-size:18px;margin-bottom:22px;box-shadow:0 4px 14px rgba(67,83,255,.35)}
.step h3{font-size:22px;font-weight:700;color:#fff;margin-bottom:10px;letter-spacing:-.5px;line-height:1.2}
.step p{color:var(--muted);font-size:15px;line-height:1.6}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}
.review{background:var(--surface-2);border:1px solid var(--border);border-radius:18px;padding:40px 36px;transition:border-color .15s,transform .15s}
.review:hover{border-color:var(--border-bright);transform:translateY(-2px)}
.review-mark{font-size:48px;color:var(--electric);line-height:.5;margin-bottom:18px;font-family:Georgia,serif;font-weight:900;height:24px}
.review-quote{font-size:17px;color:var(--muted);line-height:1.6;font-weight:400;margin-bottom:28px;letter-spacing:-.1px}
.review-author{display:flex;align-items:center;gap:14px;padding-top:24px;border-top:1px solid var(--border)}
.review-avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--electric),var(--cyan));display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:14px}
.review-name{font-weight:700;color:#fff;font-size:15px;letter-spacing:-.2px}
.review-role{color:var(--muted);font-size:13px;margin-top:2px;font-weight:500}

/* FAQ */
.faq{max-width:860px;margin:0 auto}
.faq-item{border:1px solid var(--border);background:var(--surface-2);border-radius:14px;margin-bottom:10px;overflow:hidden;transition:border-color .15s}
.faq-item:hover{border-color:var(--border-bright)}
.faq-item.active{border-color:var(--electric)}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:24px 28px;background:none;border:none;color:#fff;font-size:18px;font-weight:600;text-align:left;cursor:pointer;font-family:inherit;letter-spacing:-.3px;line-height:1.4;transition:color .15s}
.faq-q::after{content:'+';font-size:24px;color:var(--electric);font-weight:500;line-height:1;flex-shrink:0;transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:16px;line-height:1.65;padding:0 28px;font-weight:400}
.faq-item.active .faq-a{max-height:340px;padding:0 28px 24px}

/* FOOTER CTA */
.footer-cta{padding:120px 28px;background:#000;text-align:center;position:relative;overflow:hidden;border-top:1px solid var(--border)}
.footer-cta::before{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:900px;height:600px;background:radial-gradient(ellipse,rgba(67,83,255,.32),transparent 60%);pointer-events:none;filter:blur(60px)}
.footer-cta-inner{max-width:880px;margin:0 auto;position:relative;z-index:1}
.footer-cta h2{font-size:clamp(42px,6vw,80px);font-weight:800;letter-spacing:-2.5px;line-height:.98;color:#fff;margin-bottom:22px}
.footer-cta h2 .accent{background:linear-gradient(135deg,var(--electric),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.footer-cta p{font-size:20px;color:var(--muted);margin-bottom:38px;line-height:1.5;max-width:600px;margin-left:auto;margin-right:auto}
.footer-cta-btn{display:inline-flex;align-items:center;justify-content:center;padding:18px 36px;background:#fff;color:#000;border-radius:999px;font-weight:700;font-size:15px;transition:transform .15s,background .15s;letter-spacing:-.1px;gap:8px}
.footer-cta-btn:hover{background:#e8e8ec;transform:translateY(-2px);text-decoration:none}
.footer-cta-btn::after{content:'\2192'}

/* FOOTER */
.footer{background:#000;color:rgba(255,255,255,.55);padding:0 28px 32px;border-top:1px solid var(--border)}
.footer-inner{max-width:1320px;margin:0 auto;padding-top:72px}
.footer-wordmark{font-size:clamp(56px,10vw,140px);font-weight:900;letter-spacing:-5px;line-height:.9;color:#fff;margin-bottom:48px;background:linear-gradient(180deg,rgba(255,255,255,.95),rgba(255,255,255,.4));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.footer-cols{display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:32px;padding-bottom:48px;border-bottom:1px solid var(--border)}
.footer-brand p{font-size:14px;line-height:1.6;color:var(--muted);max-width:280px}
.footer-col h4{font-size:13px;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:.8px;margin-bottom:18px}
.footer-col ul{list-style:none}
.footer-col li{margin-bottom:10px}
.footer-col a{color:var(--muted);font-size:14px;transition:color .15s}
.footer-col a:hover{color:var(--cyan);text-decoration:underline}
.footer-bottom{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:18px;padding-top:28px;font-size:13px;color:var(--muted-soft)}
.footer-bottom .footer-logo{display:flex;align-items:center;gap:10px}
.footer-bottom .footer-logo span:last-child{color:#fff;font-weight:700;font-size:17px}

@media(max-width:900px){
  .nav-links{display:none}
  .mockup{grid-template-columns:1fr}
  .mockup-left,.mockup-right{display:none}
  .footer-cols{grid-template-columns:1fr 1fr;gap:28px}
  .trust-brands{gap:18px;font-size:15px}
}
@media(max-width:640px){
  .hero{padding:64px 18px 48px}
  .hero-form{grid-template-columns:1fr;padding:18px}
  .hero-form input[name="website"]{grid-column:1}
  .hero-form button{grid-column:1}
  .hero-ctas{flex-direction:column}
  .hero-ctas .btn{width:100%}
  .section{padding:72px 18px}
  .stats-grid,.features-grid,.steps-grid,.reviews-grid{grid-template-columns:1fr}
  .footer-cols{grid-template-columns:1fr}
  .footer-cta{padding:80px 18px}
  .mockup-topbar{padding:10px 12px}
  .nav-inner{padding:0 18px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
  <a href="#" class="logo">
    <span class="logo-mark">W</span>
    <span class="logo-text">Webflow</span>
  </a>
  <ul class="nav-links">
    <li><a href="#benefits" class="has-caret">Why Webflow</a></li>
    <li><a href="#how">Templates</a></li>
    <li><a href="#faq">Pricing</a></li>
    <li><a href="#reviews" class="has-caret">Customers</a></li>
    <li><a href="#form" class="has-caret">Resources</a></li>
  </ul>
  <div class="nav-right">
    <a href="#form" class="nav-signin">Contact Sales</a>
    <a href="#form" class="nav-cta">Get started &mdash; it's free</a>
  </div>
</div></nav>

<section class="hero" id="form">
  <div class="hero-inner">
    <div class="eyebrow"><span class="dot"></span>{{BADGE}}</div>
    <h1>{{HERO_TITLE}}</h1>
    <p class="sub">{{HERO_SUBTITLE}}</p>
    <div class="hero-ctas">
      <a href="#hero-form" class="btn btn-white">{{CTA_BUTTON}}</a>
      <a href="#how" class="btn btn-outline">Watch the demo &rarr;</a>
    </div>
    <div class="hero-form-wrap">
      <form id="hero-form" class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
        <input type="text" name="first_name" placeholder="First name" required>
        <input type="text" name="last_name" placeholder="Last name" required>
        <input type="email" name="email" placeholder="Work email" required>
        <input type="tel" name="phone" placeholder="Phone" required>
        <input type="url" name="website" placeholder="Company website" required>
        <button type="submit">{{CTA_BUTTON}}</button>
      </form>
    </div>
  </div>
</section>

<section class="mockup-section">
  <div class="mockup-inner">
    <div class="mockup">
      <div class="mockup-topbar">
        <div class="mockup-dots"><span></span><span></span><span></span></div>
        <div class="mockup-tab active">&#9881; Designer</div>
        <div class="mockup-tab">Editor</div>
        <div class="mockup-tab">Preview</div>
        <div style="flex:1"></div>
        <div class="mockup-tab" style="background:var(--electric);color:#fff">Publish</div>
      </div>
      <aside class="mockup-left">
        <div class="mockup-panel-title">Navigator</div>
        <div class="mockup-tree-item">Body</div>
        <div class="mockup-tree-item l2">Section &mdash; Hero</div>
        <div class="mockup-tree-item l3">Container</div>
        <div class="mockup-tree-item l4 active leaf">Heading</div>
        <div class="mockup-tree-item l4 leaf">Paragraph</div>
        <div class="mockup-tree-item l4 leaf">Button</div>
        <div class="mockup-tree-item l2">Section &mdash; Features</div>
        <div class="mockup-tree-item l3">Grid</div>
        <div class="mockup-tree-item l2">Footer</div>
      </aside>
      <div class="mockup-canvas">
        <div class="mockup-canvas-h">Build it once. Customize on the fly.</div>
        <div class="mockup-canvas-p">A visual development platform that lets you design, build and launch responsive sites in minutes.</div>
        <div class="mockup-canvas-btn">Get started</div>
      </div>
      <aside class="mockup-right">
        <div class="mockup-panel-title">Style &mdash; Heading</div>
        <div class="mockup-prop"><span class="mockup-prop-key">Tag</span><span class="mockup-prop-val">H1</span></div>
        <div class="mockup-prop"><span class="mockup-prop-key">Font</span><span class="mockup-prop-val">Inter 800</span></div>
        <div class="mockup-prop"><span class="mockup-prop-key">Size</span><span class="mockup-prop-val">96px</span></div>
        <div class="mockup-prop"><span class="mockup-prop-key">Line height</span><span class="mockup-prop-val">0.95</span></div>
        <div class="mockup-prop"><span class="mockup-prop-key">Letter</span><span class="mockup-prop-val">-3px</span></div>
        <div class="mockup-prop"><span class="mockup-prop-key">Color</span><span class="mockup-prop-val"><span class="mockup-swatch"><span class="mockup-swatch-box"></span>#4353FF</span></span></div>
        <div class="mockup-panel-title" style="margin-top:18px">Spacing</div>
        <div class="mockup-prop"><span class="mockup-prop-key">Margin top</span><span class="mockup-prop-val">0</span></div>
        <div class="mockup-prop"><span class="mockup-prop-key">Margin btm</span><span class="mockup-prop-val">28px</span></div>
        <div class="mockup-prop"><span class="mockup-prop-key">Padding</span><span class="mockup-prop-val">0 28px</span></div>
      </aside>
    </div>
  </div>
</section>

<section class="trust-strip">
  <div class="trust-inner">
    <div class="trust-title">Powering web experiences for</div>
    <div class="trust-brands">
      <span>NETFLIX</span>
      <span>FUNDRAISE</span>
      <span>IDEO</span>
      <span>ORANGEBEARD</span>
      <span>SOLAR</span>
      <span>NATIVE INSTRUMENTS</span>
    </div>
  </div>
</section>

<section class="section" id="stats">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">Real impact</span>
      <h2>Numbers that <span class="accent">scale.</span></h2>
    </div>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-eyebrow">Faster Launch</div>
        <div class="stat-num">{{STAT_1_NUM}}</div>
        <div class="stat-label">{{STAT_1_LABEL}}</div>
      </div>
      <div class="stat-card">
        <div class="stat-eyebrow">Active Teams</div>
        <div class="stat-num">{{STAT_2_NUM}}</div>
        <div class="stat-label">{{STAT_2_LABEL}}</div>
      </div>
      <div class="stat-card">
        <div class="stat-eyebrow">Built Faster</div>
        <div class="stat-num">{{STAT_3_NUM}}</div>
        <div class="stat-label">{{STAT_3_LABEL}}</div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section class="section" id="benefits">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">Capabilities</span>
      <h2>{{BENEFITS_HEADLINE}}</h2>
      <p>{{BENEFITS_SUBHEADLINE}}</p>
    </div>
    <div class="features-grid">
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
      <div class="feature-card"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section class="section" id="how">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">How it works</span>
      <h2>{{HOW_HEADLINE}}</h2>
      <p>{{HOW_SUBHEADLINE}}</p>
    </div>
    <div class="steps-grid">
      <div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
      <div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
      <div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section class="section" id="reviews">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">Loved by builders</span>
      <h2>{{REVIEWS_HEADLINE}}</h2>
      <p>{{REVIEWS_SUBHEADLINE}}</p>
    </div>
    <div class="reviews-grid">
      <div class="review">
        <div class="review-mark">&ldquo;</div>
        <p class="review-quote">{{REVIEW_1_QUOTE}}</p>
        <div class="review-author">
          <div class="review-avatar">{{REVIEW_1_INITIALS}}</div>
          <div><div class="review-name">{{REVIEW_1_NAME}}</div><div class="review-role">{{REVIEW_1_ROLE}}</div></div>
        </div>
      </div>
      <div class="review">
        <div class="review-mark">&ldquo;</div>
        <p class="review-quote">{{REVIEW_2_QUOTE}}</p>
        <div class="review-author">
          <div class="review-avatar">{{REVIEW_2_INITIALS}}</div>
          <div><div class="review-name">{{REVIEW_2_NAME}}</div><div class="review-role">{{REVIEW_2_ROLE}}</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section class="section" id="faq">
  <div class="section-inner">
    <div class="section-header">
      <span class="small-eyebrow">FAQ</span>
      <h2>{{FAQ_HEADLINE}}</h2>
      <p>{{FAQ_SUBHEADLINE}}</p>
    </div>
    <div class="faq">
      <div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
      <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
      <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
      <div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
    </div>
  </div>
</section>

<section class="footer-cta">
  <div class="footer-cta-inner">
    <h2>{{FOOTER_HEADLINE}}</h2>
    <p>{{FOOTER_SUBHEADLINE}}</p>
    <a href="#form" class="footer-cta-btn">{{FOOTER_CTA}}</a>
  </div>
</section>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-wordmark">Webflow</div>
    <div class="footer-cols">
      <div class="footer-brand">
        <p>The visual development platform for building production-grade websites without writing code.</p>
      </div>
      <div class="footer-col"><h4>Product</h4><ul><li><a href="#benefits">Why Webflow</a></li><li><a href="#how">Templates</a></li><li><a href="#form">Hosting</a></li><li><a href="#form">Enterprise</a></li></ul></div>
      <div class="footer-col"><h4>Solutions</h4><ul><li><a href="#form">Marketing</a></li><li><a href="#form">Ecommerce</a></li><li><a href="#form">Designers</a></li><li><a href="#form">Developers</a></li></ul></div>
      <div class="footer-col"><h4>Resources</h4><ul><li><a href="#faq">Help Center</a></li><li><a href="#how">Webflow University</a></li><li><a href="#reviews">Community</a></li><li><a href="#form">Forum</a></li></ul></div>
      <div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Careers</a></li><li><a href="#">Press</a></li><li><a href="#">Contact</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <div class="footer-logo">
        <span class="logo-mark">W</span>
        <span>Webflow</span>
      </div>
      <span>© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com · Privacy · Terms · Cookies</span>
    </div>
  </div>
</footer>

__FORM_SUBMIT_JS__
</body></html>
"""

# ─── Figma Creative ─────────────────────────────────────────────────────────────
_TPL_FIGMA_CREATIVE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--text:#000;--muted:#3b3b3b;--soft:#fafafa;--border:#ebebeb;--red:#f24e1e;--orange:#ff7262;--purple:#a259ff;--blue:#1abcfe;--green:#0acf83;--dark:#0d0d0d}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:'Whyte','Inter',system-ui,-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text);line-height:1.45;-webkit-font-smoothing:antialiased;font-weight:400;letter-spacing:-.011em;min-height:100vh;overflow-x:hidden}
a{color:inherit;text-decoration:none}
@keyframes fadeInUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes floatA{0%,100%{transform:translate(0,0) rotate(0)}50%{transform:translate(10px,-12px) rotate(2deg)}}
@keyframes floatB{0%,100%{transform:translate(0,0) rotate(0)}50%{transform:translate(-8px,10px) rotate(-3deg)}}

/* NAV — white sticky with Figma 5-color logo */
.nav{position:sticky;top:0;left:0;right:0;z-index:9999;background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(14px);-webkit-backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1280px;margin:0 auto;padding:0 32px;height:64px;display:flex;align-items:center;justify-content:space-between;gap:32px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;letter-spacing:-.01em;color:#000}
.brand-logo{width:24px;height:36px;position:relative;flex-shrink:0}
.brand-logo span{position:absolute;width:12px;height:12px;display:block}
.brand-logo .s1{top:0;left:0;background:#f24e1e;border-top-left-radius:6px;border-top-right-radius:6px}
.brand-logo .s2{top:0;left:12px;background:#ff7262;border-top-right-radius:6px}
.brand-logo .s3{top:12px;left:0;background:#a259ff}
.brand-logo .s4{top:12px;left:12px;background:#1abcfe;border-radius:50%}
.brand-logo .s5{top:24px;left:0;background:#0acf83;border-bottom-left-radius:6px}
.nav-links{display:flex;gap:26px;list-style:none;align-items:center;flex:1;justify-content:center}
.nav-links a{color:#1e1e1e;font-size:14px;font-weight:500;display:inline-flex;align-items:center;gap:4px;padding:6px 0;transition:color .15s}
.nav-links a:hover{color:#a259ff}
.nav-links a .ch{font-size:10px;opacity:.6}
.nav-right{display:flex;align-items:center;gap:14px}
.nav-right a{font-size:14px;font-weight:500;color:#1e1e1e}
.nav-login{padding:8px 16px;border:1px solid #d4d4d4;border-radius:999px;font-size:14px;font-weight:500;transition:border-color .15s}
.nav-login:hover{border-color:#000}
.nav-cta{padding:8px 18px;background:#000;color:#fff!important;border-radius:999px;font-size:14px;font-weight:500;transition:background .15s}
.nav-cta:hover{background:#1e1e1e}

/* HERO — multi-color gradient mesh */
.hero{position:relative;padding:80px 24px 60px;text-align:center;overflow:hidden;background:radial-gradient(circle at 30% 20%,#f24e1e 0%,transparent 40%),radial-gradient(circle at 70% 30%,#a259ff 0%,transparent 40%),radial-gradient(circle at 20% 80%,#0acf83 0%,transparent 40%),radial-gradient(circle at 80% 70%,#1abcfe 0%,transparent 40%),#fff}
.hero::before{content:'';position:absolute;inset:0;background:rgba(255,255,255,.55);pointer-events:none}
.hero-inner{position:relative;max-width:980px;margin:0 auto;animation:fadeInUp .8s ease both}
.badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;background:#fff;border:1px solid var(--border);border-radius:999px;font-size:13px;font-weight:500;color:#1e1e1e;margin-bottom:28px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.badge .dot{width:6px;height:6px;border-radius:50%;background:linear-gradient(135deg,#f24e1e,#a259ff)}
.hero h1{font-size:clamp(48px,7vw,96px);font-weight:700;line-height:.95;letter-spacing:-.04em;margin-bottom:24px;color:#000}
.hero h1 .swatch{background:linear-gradient(90deg,#f24e1e,#a259ff,#1abcfe,#0acf83);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero p{font-size:clamp(17px,2vw,22px);color:#1e1e1e;max-width:680px;margin:0 auto 36px;line-height:1.45;font-weight:400}
.hero-ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-bottom:36px}
.btn-pri{padding:14px 28px;background:#000;color:#fff;border-radius:999px;font-size:16px;font-weight:500;border:none;cursor:pointer;transition:background .15s;display:inline-flex;align-items:center;gap:8px}
.btn-pri:hover{background:#1e1e1e}
.btn-out{padding:14px 28px;background:transparent;color:#000;border:1px solid #000;border-radius:999px;font-size:16px;font-weight:500;cursor:pointer;transition:all .15s}
.btn-out:hover{background:#000;color:#fff}

/* CANVAS MOCKUP under hero */
.canvas-mock{position:relative;max-width:1100px;margin:32px auto 0;background:#fff;border:1px solid var(--border);border-radius:12px;box-shadow:0 24px 60px rgba(0,0,0,.12),0 4px 12px rgba(0,0,0,.04);overflow:hidden;animation:fadeInUp 1s ease .2s both}
.canvas-bar{display:flex;align-items:center;gap:8px;padding:10px 14px;background:#f5f5f5;border-bottom:1px solid var(--border)}
.canvas-bar .cdot{width:11px;height:11px;border-radius:50%}
.canvas-bar .cdot.r{background:#ff5f56}.canvas-bar .cdot.y{background:#ffbd2e}.canvas-bar .cdot.g{background:#27c93f}
.canvas-bar .ctitle{margin-left:12px;font-size:12px;color:#666;font-weight:500}
.canvas-body{display:grid;grid-template-columns:60px 1fr 240px;height:380px}
.canvas-tools{background:#fafafa;border-right:1px solid var(--border);padding:14px 0;display:flex;flex-direction:column;align-items:center;gap:14px}
.canvas-tools .tool{width:32px;height:32px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:13px;color:#3b3b3b;font-weight:600;cursor:pointer;transition:background .15s}
.canvas-tools .tool:hover{background:#ececec}
.canvas-tools .tool.active{background:#a259ff;color:#fff}
.canvas-stage{background:#f5f5f5;position:relative;overflow:hidden}
.canvas-stage::before{content:'';position:absolute;inset:0;background-image:radial-gradient(#d8d8d8 1px,transparent 1px);background-size:18px 18px;opacity:.6}
.shape{position:absolute;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.08)}
.s-rect{top:18%;left:14%;width:160px;height:110px;background:linear-gradient(135deg,#f24e1e,#ff7262);animation:floatA 6s ease-in-out infinite}
.s-circle{top:46%;left:32%;width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#1abcfe,#0acf83);animation:floatB 7s ease-in-out infinite}
.s-pill{top:22%;left:46%;width:220px;height:64px;border-radius:999px;background:#a259ff;animation:floatA 8s ease-in-out infinite}
.s-tri{top:58%;left:58%;width:0;height:0;border-left:60px solid transparent;border-right:60px solid transparent;border-bottom:104px solid #0acf83;animation:floatB 9s ease-in-out infinite;box-shadow:none}
.canvas-panel{background:#fafafa;border-left:1px solid var(--border);padding:18px;font-size:12px}
.canvas-panel h4{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#7a7a7a;margin-bottom:10px;font-weight:600}
.canvas-panel .pgroup{margin-bottom:18px}
.canvas-panel .prow{display:flex;align-items:center;justify-content:space-between;padding:6px 0;font-size:12px;color:#1e1e1e}
.canvas-panel .pval{color:#666;font-variant-numeric:tabular-nums}
.canvas-panel .swatch-color{width:14px;height:14px;border-radius:3px;display:inline-block;vertical-align:middle;margin-right:6px}

/* STATS */
.stats{display:flex;justify-content:center;gap:64px;margin:60px auto 0;flex-wrap:wrap;max-width:900px;position:relative;z-index:2}
.stat-block{text-align:center}
.stat-num{font-size:56px;font-weight:800;letter-spacing:-.04em;line-height:1;color:#000;margin-bottom:6px}
.stat-num.c1{background:linear-gradient(135deg,#f24e1e,#ff7262);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stat-num.c2{background:linear-gradient(135deg,#a259ff,#1abcfe);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stat-num.c3{background:linear-gradient(135deg,#0acf83,#1abcfe);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stat-label{font-size:14px;color:#3b3b3b;font-weight:500}

/* TRUST STRIP */
.trust{padding:32px 24px;border-top:1px solid var(--border);border-bottom:1px solid var(--border);background:#fff}
.trust-inner{max-width:1100px;margin:0 auto;text-align:center}
.trust h3{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:#7a7a7a;font-weight:600;margin-bottom:20px}
.trust-row{display:flex;justify-content:center;gap:48px;flex-wrap:wrap;align-items:center}
.trust-logo{font-size:18px;font-weight:700;color:#1e1e1e;letter-spacing:-.02em;opacity:.7}

/* SECTIONS */
.section{padding:120px 24px}
.section-alt{background:#fafafa}
.section-inner{max-width:1200px;margin:0 auto}
.section-header{text-align:center;margin-bottom:64px}
.section-eyebrow{display:inline-block;font-size:13px;text-transform:uppercase;letter-spacing:.12em;font-weight:600;margin-bottom:14px;background:linear-gradient(90deg,#f24e1e,#a259ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.section-header h2{font-size:clamp(36px,5vw,56px);font-weight:700;letter-spacing:-.03em;line-height:1.05;margin-bottom:16px;color:#000;max-width:760px;margin-left:auto;margin-right:auto}
.section-header .underline{display:inline-block;height:6px;width:120px;background:linear-gradient(90deg,#f24e1e,#ff7262,#a259ff,#1abcfe,#0acf83);border-radius:3px;margin-top:18px}
.section-header p{color:#3b3b3b;font-size:18px;max-width:620px;margin:0 auto;line-height:1.5}

/* FEATURE CARDS — 5-color rotation */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature-card{padding:32px;background:#fff;border:1px solid var(--border);border-radius:16px;transition:transform .2s ease,box-shadow .2s ease;display:flex;flex-direction:column}
.feature-card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(0,0,0,.08)}
.feature-icon{width:52px;height:52px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:20px;color:#fff;font-weight:700}
.feature-card:nth-child(1) .feature-icon{background:#f24e1e}
.feature-card:nth-child(2) .feature-icon{background:#1abcfe}
.feature-card:nth-child(3) .feature-icon{background:#a259ff}
.feature-card:nth-child(4) .feature-icon{background:#0acf83}
.feature-card h3{font-size:20px;font-weight:600;letter-spacing:-.015em;margin-bottom:10px;color:#000}
.feature-card p{color:#3b3b3b;font-size:15px;line-height:1.55}

/* HOW / STEPS */
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:32px}
.step-card{padding:36px 28px;background:#fff;border:1px solid var(--border);border-radius:16px;text-align:left;position:relative}
.step-num{width:48px;height:48px;border-radius:12px;display:inline-flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;color:#fff;margin-bottom:20px}
.step-card:nth-child(1) .step-num{background:linear-gradient(135deg,#f24e1e,#ff7262)}
.step-card:nth-child(2) .step-num{background:linear-gradient(135deg,#a259ff,#1abcfe)}
.step-card:nth-child(3) .step-num{background:linear-gradient(135deg,#0acf83,#1abcfe)}
.step-card h3{font-size:22px;font-weight:600;letter-spacing:-.015em;margin-bottom:12px;color:#000}
.step-card p{color:#3b3b3b;font-size:15px;line-height:1.55}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:24px}
.review-card{padding:36px;background:#fff;border:1px solid var(--border);border-radius:16px}
.review-stars{color:#fbbf24;font-size:18px;letter-spacing:2px;margin-bottom:18px}
.review-card p{font-size:18px;line-height:1.5;color:#000;font-style:italic;margin-bottom:24px;letter-spacing:-.01em}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:15px;flex-shrink:0}
.review-card:nth-child(1) .review-avatar{background:linear-gradient(135deg,#f24e1e,#ff7262)}
.review-card:nth-child(2) .review-avatar{background:linear-gradient(135deg,#1abcfe,#a259ff)}
.review-author strong{display:block;color:#000;font-size:15px;font-weight:600}
.review-author div:last-child{font-size:14px;color:#3b3b3b}

/* FAQ */
.faq-list{max-width:820px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--border)}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;padding:24px 0;background:none;border:none;color:#000;font-size:18px;font-weight:500;text-align:left;cursor:pointer;letter-spacing:-.01em;font-family:inherit}
.faq-q::after{content:'+';font-size:28px;font-weight:300;background:linear-gradient(135deg,#f24e1e,#a259ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .3s ease,padding .3s ease;color:#3b3b3b;font-size:16px;line-height:1.6}
.faq-item.active .faq-a{max-height:300px;padding-bottom:24px}

/* FORM SECTION */
.form-section{padding:120px 24px;background:radial-gradient(circle at 30% 20%,rgba(242,78,30,.18) 0%,transparent 45%),radial-gradient(circle at 70% 30%,rgba(162,89,255,.18) 0%,transparent 45%),radial-gradient(circle at 20% 80%,rgba(10,207,131,.18) 0%,transparent 45%),radial-gradient(circle at 80% 70%,rgba(26,188,254,.18) 0%,transparent 45%),#fff}
.form-card{max-width:560px;margin:0 auto;background:#fff;border:1px solid var(--border);border-radius:20px;padding:48px;box-shadow:0 24px 60px rgba(0,0,0,.08)}
.form-card h2{font-size:clamp(28px,4vw,40px);font-weight:700;letter-spacing:-.03em;line-height:1.05;margin-bottom:12px;color:#000;text-align:center}
.form-card p{color:#3b3b3b;font-size:16px;text-align:center;margin-bottom:28px}
.form-card form{display:flex;flex-direction:column;gap:12px}
.form-card input{width:100%;padding:14px 16px;border:1px solid var(--border);border-radius:10px;font-size:15px;font-family:inherit;color:#000;background:#fff;outline:none;transition:border-color .15s,box-shadow .15s}
.form-card input::placeholder{color:#9a9a9a}
.form-card input:focus{border-color:#a259ff;box-shadow:0 0 0 3px rgba(162,89,255,.15)}
.form-card button{padding:16px;background:#000;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:600;cursor:pointer;font-family:inherit;margin-top:6px;transition:background .15s}
.form-card button:hover{background:#1e1e1e}

/* FOOTER */
.footer{background:#000;color:#fff;padding:80px 24px 40px}
.footer-inner{max-width:1200px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:40px;padding-bottom:48px;border-bottom:1px solid #222}
.footer-brand{display:flex;flex-direction:column;gap:14px}
.footer-brand .brand{color:#fff}
.footer-brand p{color:#9a9a9a;font-size:14px;line-height:1.55;max-width:300px}
.footer-col h4{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:#fff;margin-bottom:18px;font-weight:600}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.footer-col a{color:#9a9a9a;font-size:14px;transition:color .15s}
.footer-col a:hover{color:#fff}
.footer-bottom{padding-top:32px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;color:#7a7a7a;font-size:13px}

/* MOBILE */
@media(max-width:640px){
  .nav-links{display:none}
  .nav-right .nav-login{display:none}
  .nav-inner{padding:0 18px}
  .hero{padding:60px 18px 48px}
  .canvas-body{grid-template-columns:50px 1fr;height:300px}
  .canvas-panel{display:none}
  .stats{gap:32px;margin-top:40px}
  .stat-num{font-size:42px}
  .section{padding:72px 18px}
  .form-card{padding:32px 22px}
  .footer-top{grid-template-columns:1fr 1fr;gap:32px}
  .footer-brand{grid-column:1/-1}
  .trust-row{gap:24px}
  .trust-logo{font-size:15px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="brand"><span class="brand-logo"><span class="s1"></span><span class="s2"></span><span class="s3"></span><span class="s4"></span><span class="s5"></span></span>Figma</a>
<ul class="nav-links">
<li><a href="#benefits">Product <span class="ch">⌄</span></a></li>
<li><a href="#how-it-works">Solutions <span class="ch">⌄</span></a></li>
<li><a href="#reviews">Community</a></li>
<li><a href="#faq">Resources <span class="ch">⌄</span></a></li>
<li><a href="#form">Pricing <span class="ch">⌄</span></a></li>
</ul>
<div class="nav-right">
<a href="#form">Contact Sales</a>
<a href="#form" class="nav-login">Log in</a>
<a href="#form" class="nav-cta">Sign up</a>
</div></div></nav>

<section class="hero">
<div class="hero-inner">
<div class="badge"><span class="dot"></span>{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p>{{HERO_SUBTITLE}}</p>
<div class="hero-ctas">
<a href="#form" class="btn-pri">{{CTA_BUTTON}} →</a>
<a href="#how-it-works" class="btn-out">View pricing</a>
</div>

<div class="canvas-mock">
<div class="canvas-bar"><span class="cdot r"></span><span class="cdot y"></span><span class="cdot g"></span><span class="ctitle">Untitled — Figma</span></div>
<div class="canvas-body">
<div class="canvas-tools">
<div class="tool active">V</div>
<div class="tool">F</div>
<div class="tool">R</div>
<div class="tool">O</div>
<div class="tool">T</div>
<div class="tool">P</div>
<div class="tool">⌘</div>
</div>
<div class="canvas-stage">
<div class="shape s-rect"></div>
<div class="shape s-circle"></div>
<div class="shape s-pill"></div>
<div class="shape s-tri"></div>
</div>
<div class="canvas-panel">
<div class="pgroup"><h4>Design</h4>
<div class="prow"><span>Fill</span><span class="pval"><span class="swatch-color" style="background:#a259ff"></span>A259FF</span></div>
<div class="prow"><span>Stroke</span><span class="pval">None</span></div>
<div class="prow"><span>Effects</span><span class="pval">Drop shadow</span></div>
</div>
<div class="pgroup"><h4>Auto layout</h4>
<div class="prow"><span>Direction</span><span class="pval">→ Horizontal</span></div>
<div class="prow"><span>Spacing</span><span class="pval">16</span></div>
<div class="prow"><span>Padding</span><span class="pval">24</span></div>
</div>
</div>
</div></div>

<div class="stats">
<div class="stat-block"><div class="stat-num c1">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat-block"><div class="stat-num c2">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat-block"><div class="stat-num c3">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</div>
</section>

<section class="trust"><div class="trust-inner">
<h3>Powering design at</h3>
<div class="trust-row">
<div class="trust-logo">Google</div>
<div class="trust-logo">Microsoft</div>
<div class="trust-logo">Slack</div>
<div class="trust-logo">GitHub</div>
<div class="trust-logo">Spotify</div>
<div class="trust-logo">Twitter</div>
<div class="trust-logo">Uber</div>
<div class="trust-logo">Volvo</div>
</div>
</div></section>

<section class="section" id="benefits"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">Product</span>
<h2>{{BENEFITS_HEADLINE}}</h2>
<div class="underline"></div>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>
<div class="features-grid">
<div class="feature-card"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature-card"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature-card"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature-card"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div></div></section>

<section class="section section-alt" id="how-it-works"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">How it works</span>
<h2>{{HOW_HEADLINE}}</h2>
<div class="underline"></div>
<p>{{HOW_SUBHEADLINE}}</p>
</div>
<div class="steps-grid">
<div class="step-card"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step-card"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step-card"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div></div></section>

<section class="section" id="reviews"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">Loved by designers</span>
<h2>{{REVIEWS_HEADLINE}}</h2>
<div class="underline"></div>
<p>{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-grid">
<div class="review-card"><div class="review-stars">★★★★★</div><p>"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><strong>{{REVIEW_1_NAME}}</strong><div>{{REVIEW_1_ROLE}}</div></div></div></div>
<div class="review-card"><div class="review-stars">★★★★★</div><p>"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><strong>{{REVIEW_2_NAME}}</strong><div>{{REVIEW_2_ROLE}}</div></div></div></div>
</div></div></section>

<section class="section section-alt" id="faq"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">FAQ</span>
<h2>{{FAQ_HEADLINE}}</h2>
<div class="underline"></div>
<p>{{FAQ_SUBHEADLINE}}</p>
</div>
<div class="faq-list">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div></div></section>

<section class="form-section" id="form">
<div class="form-card">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Work email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div>
</section>

<footer class="footer"><div class="footer-inner">
<div class="footer-top">
<div class="footer-brand">
<a href="#" class="brand" style="color:#fff"><span class="brand-logo"><span class="s1"></span><span class="s2"></span><span class="s3"></span><span class="s4"></span><span class="s5"></span></span>Figma</a>
<p>Build prototypes that look real. Design, prototype, and gather feedback all in one place.</p>
</div>
<div class="footer-col"><h4>Use cases</h4><ul>
<li><a href="#">UI design</a></li><li><a href="#">UX design</a></li>
<li><a href="#">Wireframing</a></li><li><a href="#">Prototyping</a></li>
<li><a href="#">Design systems</a></li>
</ul></div>
<div class="footer-col"><h4>Resources</h4><ul>
<li><a href="#">Blog</a></li><li><a href="#">Best practices</a></li>
<li><a href="#">Colors</a></li><li><a href="#">Color wheel</a></li>
<li><a href="#">Support</a></li>
</ul></div>
<div class="footer-col"><h4>Community</h4><ul>
<li><a href="#">Forum</a></li><li><a href="#">Plugins</a></li>
<li><a href="#">Widgets</a></li><li><a href="#">Templates</a></li>
<li><a href="#">Partners</a></li>
</ul></div>
<div class="footer-col"><h4>Compare</h4><ul>
<li><a href="#">Figma vs Sketch</a></li><li><a href="#">Figma vs Adobe XD</a></li>
<li><a href="#">Figma vs InVision</a></li><li><a href="#">Figma vs Miro</a></li>
<li><a href="#">All comparisons</a></li>
</ul></div>
</div>
<div class="footer-bottom">
<div>© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com</div>
<div>Made with ❤ on the canvas</div>
</div>
</div></footer>

__FORM_SUBMIT_JS__
</body></html>
"""

# ─── Robinhood Trade ─────────────────────────────────────────────────────────────
_TPL_ROBINHOOD_TRADE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--text:#0c0c0c;--muted:#5b6371;--soft:#f6f7f8;--border:#e5e7eb;--green:#00C805;--green-d:#00a504;--green-soft:#e6faea;--dark:#0c0c0c;--dark-2:#161616}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:'Capsule','Inter',system-ui,-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;font-weight:400;letter-spacing:-.005em;min-height:100vh;overflow-x:hidden}
a{color:inherit;text-decoration:none}
@keyframes fadeInUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes glowPulse{0%,100%{filter:drop-shadow(0 0 6px rgba(0,200,5,.5))}50%{filter:drop-shadow(0 0 14px rgba(0,200,5,.85))}}
@keyframes tickerScroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}

/* NAV */
.nav{position:sticky;top:0;left:0;right:0;z-index:9999;background:rgba(255,255,255,.96);backdrop-filter:saturate(180%) blur(12px);-webkit-backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1280px;margin:0 auto;padding:0 32px;height:72px;display:flex;align-items:center;justify-content:space-between;gap:32px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:22px;letter-spacing:-.02em;color:var(--dark)}
.brand-logo{width:28px;height:28px;flex-shrink:0;color:var(--green);animation:glowPulse 3s ease-in-out infinite}
.nav-links{display:flex;gap:30px;list-style:none;align-items:center;flex:1;justify-content:center}
.nav-links a{color:var(--dark);font-size:15px;font-weight:500;transition:color .15s;padding:6px 0}
.nav-links a:hover{color:var(--green-d)}
.nav-right{display:flex;align-items:center;gap:18px}
.nav-login{color:var(--dark);font-size:15px;font-weight:500}
.nav-login:hover{color:var(--green-d)}
.nav-cta{padding:10px 22px;background:var(--green);color:#fff!important;border-radius:999px;font-size:15px;font-weight:600;transition:background .15s,transform .1s}
.nav-cta:hover{background:var(--green-d);transform:translateY(-1px)}

/* HERO */
.hero{padding:90px 24px 60px;background:#fff;position:relative;overflow:hidden}
.hero-inner{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:1.05fr 1fr;gap:64px;align-items:center}
.hero-text{animation:fadeInUp .8s ease both}
.badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;background:var(--green-soft);border-radius:999px;font-size:13px;font-weight:600;color:var(--green-d);margin-bottom:24px}
.badge .dot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 0 3px rgba(0,200,5,.25)}
.hero h1{font-size:clamp(48px,7vw,88px);font-weight:700;line-height:1;letter-spacing:-.04em;color:var(--dark);margin-bottom:22px}
.hero p{font-size:clamp(17px,1.6vw,21px);color:var(--muted);max-width:540px;line-height:1.5;margin-bottom:32px}
.hero-ctas{display:flex;gap:18px;align-items:center;flex-wrap:wrap;margin-bottom:28px}
.btn-pri{padding:16px 32px;background:var(--green);color:#fff;border-radius:999px;font-size:16px;font-weight:600;border:none;cursor:pointer;transition:background .15s,transform .1s;display:inline-flex;align-items:center;gap:8px}
.btn-pri:hover{background:var(--green-d);transform:translateY(-1px)}
.ghost-link{color:var(--dark);font-size:15px;font-weight:500;transition:color .15s;display:inline-flex;align-items:center;gap:6px}
.ghost-link:hover{color:var(--green-d)}
.hero-foot{font-size:13px;color:var(--muted);line-height:1.5;max-width:520px}

/* STOCK CHART MOCKUP */
.chart-card{background:var(--dark);border-radius:24px;padding:28px;color:#fff;box-shadow:0 32px 80px rgba(0,0,0,.35);position:relative;overflow:hidden;animation:fadeInUp 1s ease .15s both}
.chart-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:24px}
.chart-sym{display:flex;align-items:center;gap:12px}
.chart-sym .ico{width:38px;height:38px;border-radius:50%;background:var(--green-soft);color:var(--green-d);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.chart-sym .meta strong{display:block;font-size:18px;font-weight:700;letter-spacing:-.01em}
.chart-sym .meta span{font-size:13px;color:#9aa1ad}
.chart-price{text-align:right}
.chart-price .big{font-size:32px;font-weight:700;letter-spacing:-.02em;line-height:1}
.chart-price .ch{display:inline-flex;align-items:center;gap:4px;font-size:14px;color:var(--green);font-weight:600;margin-top:6px}
.chart-graph{height:170px;position:relative;margin:0 -4px}
.chart-graph svg{width:100%;height:100%;display:block;overflow:visible}
.chart-line{fill:none;stroke:var(--green);stroke-width:2.5;filter:drop-shadow(0 0 8px rgba(0,200,5,.55))}
.chart-fill{fill:url(#chartGrad)}
.chart-dot{fill:var(--green);filter:drop-shadow(0 0 10px rgba(0,200,5,.9))}
.chart-bars{display:flex;align-items:flex-end;gap:3px;height:48px;margin-top:14px}
.chart-bars .bar{flex:1;border-radius:1.5px;min-height:6px}
.chart-time{display:flex;justify-content:space-between;gap:6px;margin-top:18px;padding-top:14px;border-top:1px solid #222}
.chart-time .tf{flex:1;padding:8px 0;text-align:center;font-size:12px;font-weight:600;color:#9aa1ad;border-radius:6px;cursor:pointer;transition:all .15s}
.chart-time .tf.active{background:var(--green);color:#000}

/* TICKER STRIP */
.ticker{background:var(--dark);color:#fff;padding:14px 0;border-top:1px solid #1e1e1e;border-bottom:1px solid #1e1e1e;overflow:hidden;white-space:nowrap}
.ticker-track{display:inline-flex;gap:48px;animation:tickerScroll 40s linear infinite;padding-right:48px}
.ticker-item{display:inline-flex;align-items:center;gap:10px;font-size:14px;font-weight:600;font-variant-numeric:tabular-nums}
.ticker-item .sym{color:#fff}
.ticker-item .pr{color:#9aa1ad}
.ticker-item .pl{color:var(--green)}
.ticker-item .ng{color:#ff5c5c}

/* SECTIONS */
.section{padding:110px 24px}
.section-inner{max-width:1180px;margin:0 auto}
.section-alt{background:var(--dark);color:#fff}
.section-soft{background:var(--soft)}
.section-header{text-align:center;margin-bottom:64px}
.section-eyebrow{display:inline-block;font-size:13px;text-transform:uppercase;letter-spacing:.16em;font-weight:700;color:var(--green-d);margin-bottom:14px}
.section-alt .section-eyebrow{color:var(--green)}
.section-header h2{font-size:clamp(34px,4.5vw,52px);font-weight:700;letter-spacing:-.03em;line-height:1.05;margin-bottom:16px;color:inherit;max-width:760px;margin-left:auto;margin-right:auto}
.section-header p{color:var(--muted);font-size:18px;max-width:580px;margin:0 auto;line-height:1.5}
.section-alt .section-header p{color:#9aa1ad}

/* TRUST STRIP */
.trust{padding:40px 24px;background:#fff;border-bottom:1px solid var(--border)}
.trust-inner{max-width:1180px;margin:0 auto;display:flex;justify-content:center;align-items:center;gap:40px;flex-wrap:wrap}
.trust-item{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--muted);font-weight:600}
.trust-item svg{flex-shrink:0}

/* FEATURE GRID */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.feature-card{padding:36px 30px;background:#fff;border:1px solid var(--border);border-radius:20px;transition:transform .2s,border-color .2s,box-shadow .2s}
.feature-card:hover{transform:translateY(-4px);border-color:var(--green);box-shadow:0 12px 32px rgba(0,200,5,.08)}
.section-alt .feature-card{background:var(--dark-2);border-color:#222}
.section-alt .feature-card:hover{border-color:var(--green)}
.feature-icon{width:52px;height:52px;border-radius:14px;background:var(--green-soft);color:var(--green-d);display:flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:22px;font-weight:700}
.section-alt .feature-icon{background:rgba(0,200,5,.15);color:var(--green)}
.feature-card h3{font-size:20px;font-weight:600;letter-spacing:-.015em;margin-bottom:10px}
.feature-card p{color:var(--muted);font-size:15px;line-height:1.55}
.section-alt .feature-card p{color:#9aa1ad}

/* STATS BLOCK */
.stats-band{padding:96px 24px;background:var(--dark);color:#fff;text-align:center}
.stats-band h2{font-size:clamp(32px,4.5vw,52px);font-weight:700;letter-spacing:-.03em;margin-bottom:48px;max-width:780px;margin-left:auto;margin-right:auto;line-height:1.1}
.stats-row{display:grid;grid-template-columns:repeat(3,1fr);gap:48px;max-width:980px;margin:0 auto}
.stat-block{text-align:center}
.stat-num{font-size:clamp(48px,6vw,88px);font-weight:800;letter-spacing:-.04em;line-height:1;color:var(--green);margin-bottom:10px;font-variant-numeric:tabular-nums}
.stat-label{font-size:14px;color:#9aa1ad;font-weight:500;text-transform:uppercase;letter-spacing:.08em}

/* STEPS */
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;counter-reset:step}
.step-card{padding:36px 28px;background:#fff;border:1px solid var(--border);border-radius:20px;position:relative;counter-increment:step}
.step-card::before{content:counter(step,decimal-leading-zero);position:absolute;top:24px;right:28px;font-size:64px;font-weight:800;color:var(--green);opacity:.18;line-height:1;letter-spacing:-.04em}
.step-icon{width:48px;height:48px;border-radius:12px;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;margin-bottom:20px}
.step-card h3{font-size:22px;font-weight:600;letter-spacing:-.015em;margin-bottom:10px}
.step-card p{color:var(--muted);font-size:15px;line-height:1.55}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:24px}
.review-card{padding:36px;background:#fff;border:1px solid var(--border);border-radius:20px;transition:box-shadow .2s,transform .2s}
.review-card:hover{box-shadow:0 12px 32px rgba(0,0,0,.06);transform:translateY(-2px)}
.review-stars{color:var(--green);font-size:16px;letter-spacing:3px;margin-bottom:18px}
.review-card p{font-size:17px;line-height:1.55;color:var(--dark);margin-bottom:24px;font-style:italic}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:44px;height:44px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0}
.review-author strong{display:block;color:var(--dark);font-size:15px;font-weight:600}
.review-author div:last-child{font-size:14px;color:var(--muted)}

/* FAQ */
.faq-list{max-width:820px;margin:0 auto;background:#fff;border:1px solid var(--border);border-radius:20px;overflow:hidden}
.faq-item{border-bottom:1px solid var(--border)}
.faq-item:last-child{border-bottom:none}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;padding:24px 28px;background:none;border:none;color:var(--dark);font-size:17px;font-weight:600;text-align:left;cursor:pointer;letter-spacing:-.01em;font-family:inherit;transition:background .15s}
.faq-q:hover{background:var(--soft)}
.faq-q::after{content:'+';font-size:28px;font-weight:300;color:var(--green);transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .3s ease,padding .3s ease;color:var(--muted);font-size:16px;line-height:1.6;padding:0 28px}
.faq-item.active .faq-a{max-height:300px;padding:0 28px 24px}

/* FORM SECTION */
.form-section{padding:120px 24px;background:var(--dark);color:#fff;text-align:center;position:relative;overflow:hidden}
.form-section::before{content:'';position:absolute;top:0;left:0;right:0;height:300px;background:radial-gradient(ellipse at 50% 0%,rgba(0,200,5,.18) 0%,transparent 60%);pointer-events:none}
.form-card{position:relative;max-width:520px;margin:0 auto;background:var(--dark-2);border:1px solid #222;border-radius:24px;padding:48px 40px;text-align:left}
.form-card h2{font-size:clamp(28px,3.6vw,40px);font-weight:700;letter-spacing:-.025em;line-height:1.1;margin-bottom:12px;color:#fff;text-align:center}
.form-card p{color:#9aa1ad;font-size:16px;text-align:center;margin-bottom:28px}
.form-card form{display:flex;flex-direction:column;gap:12px}
.form-card input{width:100%;padding:15px 18px;border:1px solid #2a2a2a;border-radius:12px;font-size:15px;font-family:inherit;color:#fff;background:#0a0a0a;outline:none;transition:border-color .15s,box-shadow .15s}
.form-card input::placeholder{color:#5b6371}
.form-card input:focus{border-color:var(--green);box-shadow:0 0 0 3px rgba(0,200,5,.15)}
.form-card button{padding:16px;background:var(--green);color:#fff;border:none;border-radius:12px;font-size:16px;font-weight:600;cursor:pointer;font-family:inherit;margin-top:8px;transition:background .15s}
.form-card button:hover{background:var(--green-d)}
.form-note{margin-top:18px;font-size:12px;color:#5b6371;text-align:center;line-height:1.5}

/* FOOTER */
.footer{background:var(--dark);color:#fff;padding:72px 24px 40px;border-top:1px solid #1e1e1e}
.footer-inner{max-width:1180px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:1.4fr repeat(5,1fr);gap:40px;padding-bottom:48px;border-bottom:1px solid #222}
.footer-brand{display:flex;flex-direction:column;gap:14px}
.footer-brand .brand{color:#fff}
.footer-brand p{color:#9aa1ad;font-size:14px;line-height:1.55;max-width:280px}
.footer-col h4{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:#fff;margin-bottom:18px;font-weight:600}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.footer-col a{color:#9aa1ad;font-size:14px;transition:color .15s}
.footer-col a:hover{color:var(--green)}
.footer-legal{padding-top:32px;font-size:11px;color:#5b6371;line-height:1.7;max-width:1180px}
.footer-legal p{margin-bottom:12px}
.footer-bottom{display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-top:24px;color:#5b6371;font-size:12px;padding-top:20px;border-top:1px solid #1e1e1e}

/* MOBILE */
@media(max-width:900px){
  .hero-inner{grid-template-columns:1fr;gap:48px}
  .chart-card{max-width:520px;margin:0 auto}
}
@media(max-width:640px){
  .nav-links{display:none}
  .nav-right .nav-login{display:none}
  .nav-inner{padding:0 18px;height:64px}
  .hero{padding:56px 18px 48px}
  .section{padding:72px 18px}
  .stats-band{padding:72px 18px}
  .stats-row{grid-template-columns:1fr;gap:32px}
  .form-card{padding:36px 24px}
  .form-section{padding:72px 18px}
  .footer-top{grid-template-columns:1fr 1fr;gap:32px}
  .footer-brand{grid-column:1/-1}
  .trust-inner{gap:20px}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="brand">
<svg class="brand-logo" viewBox="0 0 32 32" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
<path d="M16 2C13 8 8 12 4 14c4 .5 8 3 10 7 2-4 6-6.5 10-7-4-2-9-6-8-12z"/>
<path d="M16 16v14" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/>
</svg>
Robinhood
</a>
<ul class="nav-links">
<li><a href="#benefits">Investing</a></li>
<li><a href="#how-it-works">Crypto</a></li>
<li><a href="#reviews">Retirement</a></li>
<li><a href="#faq">Wallet</a></li>
<li><a href="#form">Gold</a></li>
<li><a href="#how-it-works">Learn</a></li>
</ul>
<div class="nav-right">
<a href="#form" class="nav-login">Log in</a>
<a href="#form" class="nav-cta">Sign Up</a>
</div></div></nav>

<section class="hero"><div class="hero-inner">
<div class="hero-text">
<div class="badge"><span class="dot"></span>{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p>{{HERO_SUBTITLE}}</p>
<div class="hero-ctas">
<a href="#form" class="btn-pri">{{CTA_BUTTON}} →</a>
<a href="#form" class="ghost-link">Already have an account? Log in →</a>
</div>
<div class="hero-foot">Commission-free trading. No account minimums. Sign up in minutes and start investing today.</div>
</div>

<div class="chart-card">
<div class="chart-head">
<div class="chart-sym">
<div class="ico">E</div>
<div class="meta"><strong>EKO INC</strong><span>NASDAQ · EKO</span></div>
</div>
<div class="chart-price">
<div class="big">$182.45</div>
<div class="ch">▲ +$3.21 (1.81%) Today</div>
</div>
</div>
<div class="chart-graph">
<svg viewBox="0 0 500 170" preserveAspectRatio="none">
<defs><linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#00C805" stop-opacity=".35"/>
<stop offset="100%" stop-color="#00C805" stop-opacity="0"/>
</linearGradient></defs>
<path class="chart-fill" d="M0,130 C30,120 60,140 90,125 C120,110 150,118 180,95 C210,72 240,90 270,70 C300,50 330,62 360,48 C390,35 420,55 450,30 C470,18 490,28 500,22 L500,170 L0,170 Z"/>
<path class="chart-line" d="M0,130 C30,120 60,140 90,125 C120,110 150,118 180,95 C210,72 240,90 270,70 C300,50 330,62 360,48 C390,35 420,55 450,30 C470,18 490,28 500,22"/>
<circle class="chart-dot" cx="500" cy="22" r="5"/>
</svg>
</div>
<div class="chart-bars">
<div class="bar" style="height:32%;background:#00C805"></div>
<div class="bar" style="height:48%;background:#00C805"></div>
<div class="bar" style="height:24%;background:#ff5c5c"></div>
<div class="bar" style="height:56%;background:#00C805"></div>
<div class="bar" style="height:38%;background:#00C805"></div>
<div class="bar" style="height:22%;background:#ff5c5c"></div>
<div class="bar" style="height:64%;background:#00C805"></div>
<div class="bar" style="height:42%;background:#00C805"></div>
<div class="bar" style="height:78%;background:#00C805"></div>
<div class="bar" style="height:52%;background:#00C805"></div>
<div class="bar" style="height:88%;background:#00C805"></div>
<div class="bar" style="height:96%;background:#00C805"></div>
</div>
<div class="chart-time">
<div class="tf">1D</div>
<div class="tf">1W</div>
<div class="tf active">1M</div>
<div class="tf">3M</div>
<div class="tf">1Y</div>
<div class="tf">ALL</div>
</div>
</div>
</div></section>

<div class="ticker">
<div class="ticker-track">
<span class="ticker-item"><span class="sym">AAPL</span> <span class="pr">$182.41</span> <span class="pl">▲ 1.81%</span></span>
<span class="ticker-item"><span class="sym">TSLA</span> <span class="pr">$248.50</span> <span class="ng">▼ 0.62%</span></span>
<span class="ticker-item"><span class="sym">NVDA</span> <span class="pr">$921.40</span> <span class="pl">▲ 3.12%</span></span>
<span class="ticker-item"><span class="sym">MSFT</span> <span class="pr">$415.80</span> <span class="pl">▲ 0.94%</span></span>
<span class="ticker-item"><span class="sym">GOOG</span> <span class="pr">$172.20</span> <span class="pl">▲ 1.45%</span></span>
<span class="ticker-item"><span class="sym">META</span> <span class="pr">$498.10</span> <span class="ng">▼ 0.31%</span></span>
<span class="ticker-item"><span class="sym">AMZN</span> <span class="pr">$184.72</span> <span class="pl">▲ 2.10%</span></span>
<span class="ticker-item"><span class="sym">BTC</span> <span class="pr">$68,420</span> <span class="pl">▲ 4.20%</span></span>
<span class="ticker-item"><span class="sym">ETH</span> <span class="pr">$3,612</span> <span class="pl">▲ 2.85%</span></span>
<span class="ticker-item"><span class="sym">AAPL</span> <span class="pr">$182.41</span> <span class="pl">▲ 1.81%</span></span>
<span class="ticker-item"><span class="sym">TSLA</span> <span class="pr">$248.50</span> <span class="ng">▼ 0.62%</span></span>
<span class="ticker-item"><span class="sym">NVDA</span> <span class="pr">$921.40</span> <span class="pl">▲ 3.12%</span></span>
<span class="ticker-item"><span class="sym">MSFT</span> <span class="pr">$415.80</span> <span class="pl">▲ 0.94%</span></span>
<span class="ticker-item"><span class="sym">GOOG</span> <span class="pr">$172.20</span> <span class="pl">▲ 1.45%</span></span>
<span class="ticker-item"><span class="sym">META</span> <span class="pr">$498.10</span> <span class="ng">▼ 0.31%</span></span>
</div>
</div>

<section class="trust"><div class="trust-inner">
<div class="trust-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L3 7v6c0 5 4 9 9 10 5-1 9-5 9-10V7l-9-5z"/></svg>SIPC Protected up to $500,000</div>
<div class="trust-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9 12l2 2 4-4"/></svg>FINRA Member</div>
<div class="trust-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>256-bit Encryption</div>
<div class="trust-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>24/5 Live Trading</div>
</div></section>

<section class="section section-soft" id="benefits"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">Why Robinhood</span>
<h2>{{BENEFITS_HEADLINE}}</h2>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>
<div class="features-grid">
<div class="feature-card"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature-card"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature-card"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature-card"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div></div></section>

<section class="stats-band">
<h2>Trusted by millions of investors</h2>
<div class="stats-row">
<div class="stat-block"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat-block"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat-block"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</section>

<section class="section" id="how-it-works"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">Getting Started</span>
<h2>{{HOW_HEADLINE}}</h2>
<p>{{HOW_SUBHEADLINE}}</p>
</div>
<div class="steps-grid">
<div class="step-card"><div class="step-icon">→</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step-card"><div class="step-icon">$</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step-card"><div class="step-icon">↗</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div></div></section>

<section class="section section-soft" id="reviews"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">Investor Stories</span>
<h2>{{REVIEWS_HEADLINE}}</h2>
<p>{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-grid">
<div class="review-card"><div class="review-stars">★★★★★</div><p>"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><strong>{{REVIEW_1_NAME}}</strong><div>{{REVIEW_1_ROLE}}</div></div></div></div>
<div class="review-card"><div class="review-stars">★★★★★</div><p>"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><strong>{{REVIEW_2_NAME}}</strong><div>{{REVIEW_2_ROLE}}</div></div></div></div>
</div></div></section>

<section class="section" id="faq"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">FAQ</span>
<h2>{{FAQ_HEADLINE}}</h2>
<p>{{FAQ_SUBHEADLINE}}</p>
</div>
<div class="faq-list">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div></div></section>

<section class="form-section" id="form">
<div class="form-card">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<form action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
<div class="form-note">By signing up, you agree to receive communications. Investing involves risk, including loss of principal.</div>
</div>
</section>

<footer class="footer"><div class="footer-inner">
<div class="footer-top">
<div class="footer-brand">
<a href="#" class="brand" style="color:#fff">
<svg class="brand-logo" viewBox="0 0 32 32" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
<path d="M16 2C13 8 8 12 4 14c4 .5 8 3 10 7 2-4 6-6.5 10-7-4-2-9-6-8-12z"/>
<path d="M16 16v14" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/>
</svg>
Robinhood
</a>
<p>Investing for everyone. Commission-free. No account minimums.</p>
</div>
<div class="footer-col"><h4>Invest</h4><ul>
<li><a href="#">Stocks & ETFs</a></li><li><a href="#">Options</a></li>
<li><a href="#">Margin</a></li><li><a href="#">Cash sweep</a></li>
<li><a href="#">Retirement</a></li>
</ul></div>
<div class="footer-col"><h4>Crypto</h4><ul>
<li><a href="#">Bitcoin</a></li><li><a href="#">Ethereum</a></li>
<li><a href="#">Wallet</a></li><li><a href="#">Earn rewards</a></li>
<li><a href="#">Learn crypto</a></li>
</ul></div>
<div class="footer-col"><h4>Card</h4><ul>
<li><a href="#">Robinhood Card</a></li><li><a href="#">Rewards</a></li>
<li><a href="#">Round-ups</a></li><li><a href="#">Direct deposit</a></li>
</ul></div>
<div class="footer-col"><h4>Money</h4><ul>
<li><a href="#">Spending</a></li><li><a href="#">Cash management</a></li>
<li><a href="#">Robinhood Gold</a></li><li><a href="#">Pricing</a></li>
</ul></div>
<div class="footer-col"><h4>About</h4><ul>
<li><a href="#">Newsroom</a></li><li><a href="#">Careers</a></li>
<li><a href="#">Support</a></li><li><a href="#">Snacks newsletter</a></li>
</ul></div>
</div>
<div class="footer-legal">
<p>All investments involve risk and loss of principal is possible. Information provided is for educational purposes only and is not a recommendation. Securities trading is offered to self-directed customers by Robinhood Financial. Robinhood Financial is a member of FINRA and SIPC. Cryptocurrency services are offered through Robinhood Crypto, LLC ("RHC") (NMLS ID: 1702840).</p>
<p>Margin investing involves the risk of greater investment losses. Before using margin, customers must determine whether this type of trading strategy is right for them given their specific investment objectives, experience, risk tolerance, and financial situation.</p>
</div>
<div class="footer-bottom">
<div>© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com</div>
<div>Member FINRA · SIPC</div>
</div>
</div></footer>

__FORM_SUBMIT_JS__
</body></html>
"""

# ─── Patagonia Outdoors ─────────────────────────────────────────────────────────────
_TPL_PATAGONIA_OUTDOORS = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--text:#2c2625;--muted:#7a7270;--cream:#f2eeda;--cream-d:#e8e2c8;--green:#3b5b3a;--green-d:#2e4a2d;--green-l:#5a7c4f;--blue:#3978aa;--red:#a13d2d;--dark:#2c2625;--border:#d8d1bf}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh;-webkit-text-size-adjust:100%}
body{font-family:'Acumin Pro','Adobe Acumin','Helvetica Neue',Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.55;-webkit-font-smoothing:antialiased;font-weight:400;min-height:100vh;overflow-x:hidden}
a{color:inherit;text-decoration:none}
@keyframes fadeInUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

/* NAV — warm cream */
.nav{position:sticky;top:0;left:0;right:0;z-index:9999;background:var(--cream);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1320px;margin:0 auto;padding:0 32px;height:72px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.brand{display:flex;align-items:center;gap:12px;font-weight:700;font-size:22px;letter-spacing:.01em;color:var(--dark);text-transform:none}
.brand-logo{width:46px;height:18px;color:var(--green);flex-shrink:0}
.nav-links{display:flex;gap:32px;list-style:none;align-items:center;flex:1;justify-content:center}
.nav-links a{color:var(--dark);font-size:15px;font-weight:600;letter-spacing:.01em;text-transform:none;transition:color .15s;padding:6px 0;border-bottom:2px solid transparent}
.nav-links a:hover{color:var(--green);border-bottom-color:var(--green)}
.nav-right{display:flex;align-items:center;gap:18px}
.nav-icon{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--dark);transition:background .15s;cursor:pointer}
.nav-icon:hover{background:var(--cream-d)}
.nav-icon svg{width:20px;height:20px}
.nav-bag{position:relative}
.nav-bag .count{position:absolute;top:0;right:-2px;width:18px;height:18px;border-radius:50%;background:var(--red);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center}

/* HERO */
.hero{position:relative;height:680px;background:linear-gradient(135deg,var(--green) 0%,var(--green-l) 60%,#7a9a5d 100%);overflow:hidden;display:flex;align-items:flex-end;color:#fff}
.hero::before{content:'';position:absolute;inset:0;background-image:radial-gradient(ellipse at 30% 20%,rgba(255,255,255,.18) 0%,transparent 50%),radial-gradient(ellipse at 80% 80%,rgba(0,0,0,.3) 0%,transparent 60%),linear-gradient(180deg,transparent 50%,rgba(0,0,0,.35) 100%);pointer-events:none}
.hero::after{content:'';position:absolute;bottom:0;left:0;right:0;height:50%;background:linear-gradient(180deg,transparent,rgba(44,38,37,.55))}
.hero-mountains{position:absolute;bottom:0;left:0;right:0;height:45%;pointer-events:none;opacity:.45}
.hero-mountains svg{width:100%;height:100%;display:block}
.hero-inner{position:relative;z-index:2;max-width:1320px;width:100%;margin:0 auto;padding:0 32px 80px;animation:fadeInUp 1s ease both}
.eyebrow{display:inline-block;font-size:13px;text-transform:uppercase;letter-spacing:.22em;font-weight:700;color:#fff;margin-bottom:20px;padding-bottom:6px;border-bottom:2px solid #fff;background:none}
.hero h1{font-size:clamp(40px,5.5vw,72px);font-weight:700;line-height:1.05;letter-spacing:-.015em;color:#fff;max-width:820px;margin-bottom:24px;text-shadow:0 2px 16px rgba(0,0,0,.2)}
.hero p{font-size:clamp(16px,1.6vw,20px);color:#f5f0dd;max-width:600px;line-height:1.55;margin-bottom:32px;text-shadow:0 1px 8px rgba(0,0,0,.25)}
.hero-ctas{display:flex;gap:14px;flex-wrap:wrap}
.btn-out{padding:14px 28px;background:transparent;color:#fff;border:1.5px solid #fff;font-size:15px;font-weight:700;text-transform:none;cursor:pointer;transition:all .15s;letter-spacing:.02em}
.btn-out:hover{background:#fff;color:var(--dark)}
.btn-fill{padding:14px 28px;background:#fff;color:var(--dark);border:1.5px solid #fff;font-size:15px;font-weight:700;cursor:pointer;transition:all .15s;letter-spacing:.02em}
.btn-fill:hover{background:transparent;color:#fff}

/* ACTIVISM STRIP */
.activism-strip{background:var(--red);color:#fff;padding:14px 24px;text-align:center;font-size:14px;font-weight:600;letter-spacing:.02em}
.activism-strip a{color:#fff;text-decoration:underline}

/* SECTIONS */
.section{padding:100px 24px}
.section-cream{background:var(--cream)}
.section-inner{max-width:1320px;margin:0 auto}
.section-header{margin-bottom:60px;max-width:880px}
.section-header.center{text-align:center;margin-left:auto;margin-right:auto}
.section-eyebrow{display:inline-block;font-size:12px;text-transform:uppercase;letter-spacing:.22em;font-weight:700;color:var(--green);margin-bottom:18px}
.section-header h2{font-size:clamp(32px,4.5vw,52px);font-weight:700;letter-spacing:-.015em;line-height:1.1;margin-bottom:18px;color:var(--dark)}
.section-header p{color:var(--muted);font-size:18px;line-height:1.55;max-width:640px}
.section-header.center p{margin-left:auto;margin-right:auto}

/* WORN WEAR / EDITORIAL CARDS */
.editorial-grid{display:grid;grid-template-columns:1fr 1fr;gap:32px}
.ed-card{background:#fff;border:1px solid var(--border);overflow:hidden;display:flex;flex-direction:column;transition:transform .25s}
.ed-card:hover{transform:translateY(-4px)}
.ed-photo{height:280px;position:relative;overflow:hidden}
.ed-photo .tag{position:absolute;top:18px;left:18px;background:var(--red);color:#fff;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;padding:6px 12px}
.ed-photo.p1{background:linear-gradient(135deg,#3978aa,#5a8db8 60%,#7a9ec4)}
.ed-photo.p2{background:linear-gradient(135deg,#a13d2d,#c7654b 60%,#dba07e)}
.ed-body{padding:28px;flex:1;display:flex;flex-direction:column}
.ed-body h3{font-size:24px;font-weight:700;letter-spacing:-.01em;line-height:1.2;margin-bottom:12px;color:var(--dark)}
.ed-body p{color:var(--muted);font-size:15px;line-height:1.6;margin-bottom:18px;flex:1}
.ed-link{color:var(--green);font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;border-bottom:2px solid var(--green);padding-bottom:3px;align-self:flex-start;transition:color .15s,border-color .15s}
.ed-link:hover{color:var(--green-d);border-color:var(--green-d)}

/* FEATURES with photo */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature-card{background:var(--cream);border:1px solid var(--border);overflow:hidden;display:flex;flex-direction:column;transition:transform .2s}
.feature-card:hover{transform:translateY(-4px)}
.feature-photo{height:200px;display:flex;align-items:center;justify-content:center;font-size:48px;color:#fff;font-weight:700}
.feature-card:nth-child(1) .feature-photo{background:linear-gradient(135deg,#3b5b3a,#5a7c4f)}
.feature-card:nth-child(2) .feature-photo{background:linear-gradient(135deg,#3978aa,#5a8db8)}
.feature-card:nth-child(3) .feature-photo{background:linear-gradient(135deg,#a13d2d,#c7654b)}
.feature-card:nth-child(4) .feature-photo{background:linear-gradient(135deg,#7a6b3d,#a89656)}
.feature-body{padding:26px;flex:1;display:flex;flex-direction:column}
.feature-body h3{font-size:20px;font-weight:700;letter-spacing:-.01em;margin-bottom:10px;color:var(--dark)}
.feature-body p{color:var(--muted);font-size:14px;line-height:1.6;margin-bottom:16px;flex:1}
.feature-link{color:var(--green);font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;border-bottom:2px solid var(--green);padding-bottom:2px;align-self:flex-start}

/* SHOP FILTER MOCKUP */
.shop-wrap{display:grid;grid-template-columns:240px 1fr;gap:36px;align-items:start}
.shop-filters{background:#fff;border:1px solid var(--border);padding:24px}
.shop-filters h4{font-size:11px;text-transform:uppercase;letter-spacing:.14em;font-weight:700;color:var(--muted);margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--border)}
.shop-filters .filter-group{margin-bottom:22px;padding-bottom:18px;border-bottom:1px solid var(--border)}
.shop-filters .filter-group:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}
.shop-filters .filter-title{display:flex;justify-content:space-between;font-size:14px;font-weight:700;color:var(--dark);margin-bottom:12px;cursor:pointer}
.shop-filters .filter-title::after{content:'−';color:var(--muted)}
.shop-filters .filter-options{display:flex;flex-direction:column;gap:8px}
.shop-filters .filter-option{font-size:14px;color:var(--muted);display:flex;align-items:center;gap:8px}
.shop-filters .filter-option input{accent-color:var(--green)}
.shop-filters .color-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.shop-filters .swatch{width:22px;height:22px;border-radius:50%;border:1px solid var(--border);cursor:pointer}
.steps-area{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px}
.step-card{background:#fff;border:1px solid var(--border);padding:24px;display:flex;flex-direction:column}
.step-tag{font-size:11px;text-transform:uppercase;letter-spacing:.14em;font-weight:700;color:var(--red);margin-bottom:10px}
.step-num-row{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.step-num{width:38px;height:38px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;flex-shrink:0}
.step-card h3{font-size:18px;font-weight:700;color:var(--dark);letter-spacing:-.005em}
.step-card p{color:var(--muted);font-size:14px;line-height:1.55;margin-bottom:14px;flex:1}
.step-card .step-link{color:var(--green);font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;border-bottom:2px solid var(--green);padding-bottom:2px;align-self:flex-start}

/* MISSION / STATS BAND */
.mission{background:var(--green);color:#fff;padding:100px 24px;text-align:center;position:relative;overflow:hidden}
.mission::before{content:'';position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,rgba(255,255,255,.08) 0%,transparent 40%),radial-gradient(circle at 80% 70%,rgba(255,255,255,.05) 0%,transparent 40%);pointer-events:none}
.mission-inner{position:relative;max-width:1100px;margin:0 auto}
.mission .eyebrow{color:#fff;border-color:#fff}
.mission h2{font-size:clamp(36px,5vw,60px);font-weight:700;letter-spacing:-.015em;line-height:1.1;margin-bottom:24px;color:#fff;max-width:900px;margin-left:auto;margin-right:auto}
.mission p{font-size:18px;color:#e6e2c8;max-width:680px;margin:0 auto 56px;line-height:1.55}
.stats-row{display:grid;grid-template-columns:repeat(3,1fr);gap:48px;max-width:980px;margin:0 auto}
.stat-block{text-align:center;padding:0 12px}
.stat-num{font-size:clamp(48px,5.5vw,80px);font-weight:800;letter-spacing:-.025em;line-height:1;color:#fff;margin-bottom:12px;font-variant-numeric:tabular-nums}
.stat-label{font-size:14px;color:#e6e2c8;font-weight:500;text-transform:uppercase;letter-spacing:.1em}

/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:28px}
.review-card{background:var(--cream);padding:36px;border-left:4px solid var(--green);display:flex;flex-direction:column}
.review-card:nth-child(2){border-left-color:var(--red)}
.review-tag{font-size:11px;text-transform:uppercase;letter-spacing:.14em;font-weight:700;color:var(--green);margin-bottom:18px}
.review-card:nth-child(2) .review-tag{color:var(--red)}
.review-card p{font-size:19px;line-height:1.5;color:var(--dark);margin-bottom:28px;font-weight:500;flex:1}
.review-author{display:flex;align-items:center;gap:14px;padding-top:18px;border-top:1px solid var(--border)}
.review-avatar{width:48px;height:48px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;flex-shrink:0}
.review-card:nth-child(2) .review-avatar{background:var(--red)}
.review-author strong{display:block;color:var(--dark);font-size:15px;font-weight:700}
.review-author div:last-child{font-size:13px;color:var(--muted);letter-spacing:.02em}

/* FAQ */
.faq-list{max-width:880px;margin:0 auto}
.faq-item{border-top:1px solid var(--border)}
.faq-item:last-child{border-bottom:1px solid var(--border)}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;padding:26px 0;background:none;border:none;color:var(--dark);font-size:18px;font-weight:700;text-align:left;cursor:pointer;letter-spacing:-.005em;font-family:inherit;gap:24px}
.faq-q::after{content:'+';font-size:24px;font-weight:400;color:var(--green);transition:transform .3s;flex-shrink:0}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .3s ease,padding .3s ease;color:var(--muted);font-size:16px;line-height:1.65}
.faq-item.active .faq-a{max-height:300px;padding-bottom:26px}

/* FORM SECTION */
.form-section{padding:120px 24px;background:var(--cream);position:relative}
.form-wrap{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}
.form-side h2{font-size:clamp(32px,4.5vw,52px);font-weight:700;letter-spacing:-.015em;line-height:1.1;margin-bottom:18px;color:var(--dark)}
.form-side p{color:var(--muted);font-size:17px;line-height:1.6;margin-bottom:24px}
.form-side .pledge-row{display:flex;flex-direction:column;gap:14px}
.pledge-item{display:flex;align-items:center;gap:12px;font-size:14px;color:var(--dark);font-weight:600}
.pledge-item .icn{width:28px;height:28px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;flex-shrink:0}
.form-card{background:#fff;border:1px solid var(--border);padding:40px}
.form-card form{display:flex;flex-direction:column;gap:14px}
.form-card input{width:100%;padding:14px 16px;border:1px solid var(--border);font-size:15px;font-family:inherit;color:var(--dark);background:#fff;outline:none;transition:border-color .15s}
.form-card input::placeholder{color:#a89e9a}
.form-card input:focus{border-color:var(--green)}
.form-card button{padding:16px;background:var(--green);color:#fff;border:none;font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;margin-top:6px;text-transform:uppercase;letter-spacing:.06em;transition:background .15s}
.form-card button:hover{background:var(--green-d)}

/* FOOTER */
.footer{background:var(--dark);color:var(--cream);padding:72px 24px 36px}
.footer-inner{max-width:1320px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:1.3fr repeat(4,1fr);gap:40px;padding-bottom:48px;border-bottom:1px solid #463d3b}
.footer-brand{display:flex;flex-direction:column;gap:14px}
.footer-brand .brand{color:var(--cream)}
.footer-brand .brand-logo{color:var(--cream)}
.footer-brand p{color:#a89e9a;font-size:14px;line-height:1.55;max-width:280px}
.footer-col h4{font-size:12px;text-transform:uppercase;letter-spacing:.16em;color:var(--cream);margin-bottom:18px;font-weight:700}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.footer-col a{color:#a89e9a;font-size:14px;transition:color .15s}
.footer-col a:hover{color:var(--cream)}
.footer-badges{display:flex;gap:20px;flex-wrap:wrap;padding:32px 0;border-bottom:1px solid #463d3b;margin-bottom:24px}
.footer-badge{display:flex;align-items:center;gap:10px;padding:10px 16px;border:1px solid #463d3b}
.footer-badge .bicn{width:30px;height:30px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px}
.footer-badge strong{display:block;color:var(--cream);font-size:13px;font-weight:700;line-height:1.2}
.footer-badge span{display:block;color:#a89e9a;font-size:11px;letter-spacing:.04em}
.footer-bottom{display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;color:#a89e9a;font-size:12px;padding-top:8px}

/* MOBILE */
@media(max-width:900px){
  .editorial-grid{grid-template-columns:1fr}
  .shop-wrap{grid-template-columns:1fr;gap:24px}
  .form-wrap{grid-template-columns:1fr;gap:36px}
}
@media(max-width:640px){
  .nav-links{display:none}
  .nav-inner{padding:0 18px;height:60px}
  .hero{height:560px}
  .hero-inner{padding:0 18px 56px}
  .section{padding:64px 18px}
  .mission{padding:64px 18px}
  .stats-row{grid-template-columns:1fr;gap:32px}
  .form-section{padding:64px 18px}
  .form-card{padding:28px 22px}
  .footer-top{grid-template-columns:1fr 1fr;gap:28px}
  .footer-brand{grid-column:1/-1}
  .footer-badges{flex-direction:column}
}
</style></head>
<body>__TRACKING_PIXEL__

<nav class="nav"><div class="nav-inner">
<a href="#" class="brand">
<svg class="brand-logo" viewBox="0 0 60 24" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
<path d="M0 22 L12 8 L18 14 L26 4 L34 16 L42 6 L50 18 L60 10 L60 22 Z"/>
</svg>
Patagonia
</a>
<ul class="nav-links">
<li><a href="#benefits">Shop</a></li>
<li><a href="#how-it-works">Activism</a></li>
<li><a href="#reviews">Sports & Activities</a></li>
<li><a href="#faq">Stories</a></li>
</ul>
<div class="nav-right">
<div class="nav-icon" title="Search">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
</div>
<div class="nav-icon" title="Account">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
</div>
<div class="nav-icon nav-bag" title="Bag">
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/></svg>
<span class="count">2</span>
</div>
</div></div></nav>

<div class="activism-strip">Worn Wear: Trade in your used Patagonia gear for credit toward something new. <a href="#how-it-works">Learn more →</a></div>

<section class="hero">
<div class="hero-mountains">
<svg viewBox="0 0 1440 400" preserveAspectRatio="none" fill="rgba(255,255,255,0.7)">
<path d="M0,400 L0,260 L160,140 L300,220 L480,90 L660,200 L820,120 L1000,210 L1200,100 L1320,180 L1440,140 L1440,400 Z" fill="rgba(255,255,255,0.18)"/>
<path d="M0,400 L0,320 L120,220 L280,300 L440,200 L600,290 L760,210 L940,300 L1140,200 L1280,280 L1440,240 L1440,400 Z" fill="rgba(0,0,0,0.18)"/>
</svg>
</div>
<div class="hero-inner">
<span class="eyebrow">WORN WEAR · {{BADGE}}</span>
<h1>{{HERO_TITLE}}</h1>
<p>{{HERO_SUBTITLE}}</p>
<div class="hero-ctas">
<a href="#form" class="btn-out">{{CTA_BUTTON}}</a>
<a href="#how-it-works" class="btn-fill">Read Manifesto</a>
</div>
</div>
</section>

<section class="section" id="benefits"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">Stories from the field</span>
<h2>{{BENEFITS_HEADLINE}}</h2>
<p>{{BENEFITS_SUBHEADLINE}}</p>
</div>
<div class="editorial-grid">
<div class="ed-card">
<div class="ed-photo p1"><div class="tag">Buy Less, Demand More</div></div>
<div class="ed-body">
<h3>{{BENEFIT_1_TITLE}}</h3>
<p>{{BENEFIT_1_DESC}}</p>
<a href="#form" class="ed-link">{{BENEFIT_1_ICON}} Read the Manifesto</a>
</div>
</div>
<div class="ed-card">
<div class="ed-photo p2"><div class="tag">Worn Wear</div></div>
<div class="ed-body">
<h3>{{BENEFIT_2_TITLE}}</h3>
<p>{{BENEFIT_2_DESC}}</p>
<a href="#form" class="ed-link">{{BENEFIT_2_ICON}} Trade In Your Gear</a>
</div>
</div>
</div>

<div style="margin-top:48px"><div class="features-grid">
<div class="feature-card">
<div class="feature-photo">{{BENEFIT_3_ICON}}</div>
<div class="feature-body"><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p><a href="#form" class="feature-link">Learn more</a></div>
</div>
<div class="feature-card">
<div class="feature-photo">{{BENEFIT_4_ICON}}</div>
<div class="feature-body"><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p><a href="#form" class="feature-link">Learn more</a></div>
</div>
<div class="feature-card">
<div class="feature-photo">🏔</div>
<div class="feature-body"><h3>Built to Last</h3><p>Made from recycled materials with our Ironclad Guarantee. If a Patagonia product breaks down or wears out, we repair it, replace it, or refund you.</p><a href="#form" class="feature-link">Our Guarantee</a></div>
</div>
<div class="feature-card">
<div class="feature-photo">🌱</div>
<div class="feature-body"><h3>1% for the Planet</h3><p>Since 1985, we've pledged 1% of sales to the preservation and restoration of the natural environment. Over $140M donated to date.</p><a href="#form" class="feature-link">See Grantees</a></div>
</div>
</div></div>
</div></section>

<section class="mission"><div class="mission-inner">
<span class="eyebrow">Our Mission</span>
<h2>We're in business to save our home planet.</h2>
<p>Earth is now our only shareholder. Every dollar that's not reinvested back into Patagonia is distributed as dividends to protect the planet.</p>
<div class="stats-row">
<div class="stat-block"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat-block"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat-block"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</div></section>

<section class="section section-cream" id="how-it-works"><div class="section-inner">
<div class="section-header">
<span class="section-eyebrow">How it works</span>
<h2>{{HOW_HEADLINE}}</h2>
<p>{{HOW_SUBHEADLINE}}</p>
</div>

<div class="shop-wrap">
<aside class="shop-filters">
<h4>Filter</h4>
<div class="filter-group">
<div class="filter-title">Activity</div>
<div class="filter-options">
<label class="filter-option"><input type="checkbox" checked> Climbing</label>
<label class="filter-option"><input type="checkbox"> Trail Running</label>
<label class="filter-option"><input type="checkbox" checked> Hiking</label>
<label class="filter-option"><input type="checkbox"> Skiing</label>
<label class="filter-option"><input type="checkbox"> Fishing</label>
</div>
</div>
<div class="filter-group">
<div class="filter-title">Gender</div>
<div class="filter-options">
<label class="filter-option"><input type="checkbox"> Men</label>
<label class="filter-option"><input type="checkbox"> Women</label>
<label class="filter-option"><input type="checkbox"> Kids</label>
</div>
</div>
<div class="filter-group">
<div class="filter-title">Category</div>
<div class="filter-options">
<label class="filter-option"><input type="checkbox" checked> Jackets</label>
<label class="filter-option"><input type="checkbox"> Pants</label>
<label class="filter-option"><input type="checkbox"> Fleece</label>
<label class="filter-option"><input type="checkbox"> Packs</label>
</div>
</div>
<div class="filter-group">
<div class="filter-title">Color</div>
<div class="color-row">
<span class="swatch" style="background:#3b5b3a"></span>
<span class="swatch" style="background:#3978aa"></span>
<span class="swatch" style="background:#a13d2d"></span>
<span class="swatch" style="background:#2c2625"></span>
<span class="swatch" style="background:#f2eeda"></span>
<span class="swatch" style="background:#a89656"></span>
</div>
</div>
</aside>

<div class="steps-area">
<div class="step-card">
<div class="step-tag">Step 01</div>
<div class="step-num-row"><div class="step-num">1</div></div>
<h3>{{STEP_1_TITLE}}</h3>
<p>{{STEP_1_DESC}}</p>
<a href="#form" class="step-link">Start →</a>
</div>
<div class="step-card">
<div class="step-tag">Step 02</div>
<div class="step-num-row"><div class="step-num">2</div></div>
<h3>{{STEP_2_TITLE}}</h3>
<p>{{STEP_2_DESC}}</p>
<a href="#form" class="step-link">Continue →</a>
</div>
<div class="step-card">
<div class="step-tag">Step 03</div>
<div class="step-num-row"><div class="step-num">3</div></div>
<h3>{{STEP_3_TITLE}}</h3>
<p>{{STEP_3_DESC}}</p>
<a href="#form" class="step-link">Finish →</a>
</div>
</div>
</div>
</div></section>

<section class="section" id="reviews"><div class="section-inner">
<div class="section-header center">
<span class="section-eyebrow">Voices from the trail</span>
<h2>{{REVIEWS_HEADLINE}}</h2>
<p>{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-grid">
<div class="review-card">
<div class="review-tag">Climber · Yosemite, CA</div>
<p>"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author">
<div class="review-avatar">{{REVIEW_1_INITIALS}}</div>
<div><strong>{{REVIEW_1_NAME}}</strong><div>{{REVIEW_1_ROLE}}</div></div>
</div>
</div>
<div class="review-card">
<div class="review-tag">Trail Runner · Patagonia, AR</div>
<p>"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author">
<div class="review-avatar">{{REVIEW_2_INITIALS}}</div>
<div><strong>{{REVIEW_2_NAME}}</strong><div>{{REVIEW_2_ROLE}}</div></div>
</div>
</div>
</div>
</div></section>

<section class="section section-cream" id="faq"><div class="section-inner">
<div class="section-header center">
<span class="section-eyebrow">Frequently asked</span>
<h2>{{FAQ_HEADLINE}}</h2>
<p>{{FAQ_SUBHEADLINE}}</p>
</div>
<div class="faq-list">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div>
</div></section>

<section class="form-section" id="form">
<div class="form-wrap">
<div class="form-side">
<span class="section-eyebrow">Don't Buy This Jacket</span>
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<div class="pledge-row">
<div class="pledge-item"><span class="icn">1%</span> 1% of sales pledged to grassroots environmental groups</div>
<div class="pledge-item"><span class="icn">B</span> Certified B Corporation since 2012</div>
<div class="pledge-item"><span class="icn">♺</span> Ironclad Guarantee — we'll repair, replace, or refund</div>
</div>
</div>
<div class="form-card">
<form action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{FOOTER_CTA}}</button>
</form>
</div>
</div>
</section>

<footer class="footer"><div class="footer-inner">
<div class="footer-top">
<div class="footer-brand">
<a href="#" class="brand" style="color:var(--cream)">
<svg class="brand-logo" viewBox="0 0 60 24" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
<path d="M0 22 L12 8 L18 14 L26 4 L34 16 L42 6 L50 18 L60 10 L60 22 Z"/>
</svg>
Patagonia
</a>
<p>In business to save our home planet. Earth is our only shareholder.</p>
</div>
<div class="footer-col"><h4>Shop</h4><ul>
<li><a href="#">Men</a></li><li><a href="#">Women</a></li>
<li><a href="#">Kids & Baby</a></li><li><a href="#">Worn Wear</a></li>
<li><a href="#">Gift Cards</a></li>
</ul></div>
<div class="footer-col"><h4>Activism</h4><ul>
<li><a href="#">Patagonia Action Works</a></li><li><a href="#">Environmental Grants</a></li>
<li><a href="#">Films</a></li><li><a href="#">Tin Shed Ventures</a></li>
</ul></div>
<div class="footer-col"><h4>Customer Service</h4><ul>
<li><a href="#">Help Center</a></li><li><a href="#">Shipping</a></li>
<li><a href="#">Returns & Exchanges</a></li><li><a href="#">Repairs</a></li>
<li><a href="#">Order Status</a></li>
</ul></div>
<div class="footer-col"><h4>About</h4><ul>
<li><a href="#">Our Footprint</a></li><li><a href="#">Stories</a></li>
<li><a href="#">Careers</a></li><li><a href="#">Press Room</a></li>
<li><a href="#">Our Story</a></li>
</ul></div>
</div>
<div class="footer-badges">
<div class="footer-badge"><span class="bicn">1%</span><div><strong>1% for the Planet</strong><span>Founding member since 2002</span></div></div>
<div class="footer-badge"><span class="bicn">B</span><div><strong>Certified B Corp</strong><span>Verified since 2012</span></div></div>
<div class="footer-badge"><span class="bicn">♺</span><div><strong>Fair Trade Certified</strong><span>Sewn factory bonus</span></div></div>
</div>
<div class="footer-bottom">
<div>© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com</div>
<div>Earth is our only shareholder.</div>
</div>
</div></footer>

__FORM_SUBMIT_JS__
</body></html>
"""

TEMPLATES: dict = {
    "eko-classic": {
        "name": "Eko Classic",
        "tagline": "Dark blue with cyan gradient — the original Eko AI signature",
        "vibe": "dark, modern, tech",
        "best_for": "SaaS, tech, AI startups",
        "accent": "#0B4FD8",
        "html": _TPL_EKO_CLASSIC,
    },
    "apple-minimal": {
        "name": "Apple Minimal",
        "tagline": "White, huge SF Pro typography, ultra-minimal premium aesthetic",
        "vibe": "white, minimal, premium",
        "best_for": "luxury services, high-end products, design studios",
        "accent": "#0066cc",
        "html": _TPL_APPLE_MINIMAL,
    },
    "stripe-gradient": {
        "name": "Stripe Gradient",
        "tagline": "Gradient mesh hero, technical typography, conversion-focused",
        "vibe": "gradient, technical, sophisticated",
        "best_for": "fintech, B2B SaaS, developer tools",
        "accent": "#635bff",
        "html": _TPL_STRIPE_GRADIENT,
    },
    "linear-dark": {
        "name": "Linear Dark",
        "tagline": "Pure black with neon purple, sharp geometric grid pattern",
        "vibe": "dark, geometric, futuristic",
        "best_for": "project management, dev tools, AI products",
        "accent": "#5e6ad2",
        "html": _TPL_LINEAR_DARK,
    },
    "airbnb-warm": {
        "name": "Airbnb Warm",
        "tagline": "Coral red CTA, rounded pill shapes, hospitality-friendly",
        "vibe": "warm, rounded, hospitality",
        "best_for": "restaurants, hotels, spas, travel, food",
        "accent": "#FF5A5F",
        "html": _TPL_AIRBNB_WARM,
    },
    "notion-clean": {
        "name": "Notion Clean",
        "tagline": "Off-white background, Lyon serif font, soft blocks, editorial feel",
        "vibe": "editorial, serif, soft",
        "best_for": "consultants, agencies, coaching, knowledge work",
        "accent": "#2eaadc",
        "html": _TPL_NOTION_CLEAN,
    },
    "tesla-bold": {
        "name": "Tesla Bold",
        "tagline": "Full-bleed dark hero, condensed uppercase, automotive-grade boldness",
        "vibe": "dark, bold, automotive",
        "best_for": "premium services, technology, automotive, fitness",
        "accent": "#3e6ae1",
        "html": _TPL_TESLA_BOLD,
    },
    "bestbuy-retail": {
        "name": "Best Buy Retail",
        "tagline": "Blue + yellow, deal cards with strike-through pricing, urgency-driven",
        "vibe": "retail, urgency, deal-driven",
        "best_for": "e-commerce, retail, deal-focused offers, mass market",
        "accent": "#0046BE",
        "html": _TPL_BESTBUY_RETAIL,
    },
    "spotify-vibe": {
        "name": "Spotify Vibe",
        "tagline": "Pitch black with vibrant green accent, music-energy vibe",
        "vibe": "dark, energetic, lifestyle",
        "best_for": "fitness, gyms, music studios, lifestyle brands",
        "accent": "#1DB954",
        "html": _TPL_SPOTIFY_VIBE,
    },
    "hubspot-sales": {
        "name": "HubSpot Sales",
        "tagline": "Orange CTA, B2B SaaS conversion-optimized, trust signals",
        "vibe": "B2B, conversion, professional",
        "best_for": "B2B services, agencies, consultants, legal, finance",
        "accent": "#FF7A59",
        "html": _TPL_HUBSPOT_SALES,
    },
    "vercel-modern": {
        "name": "Vercel Modern",
        "tagline": "Black + gradient + mono — dev-tool aesthetic",
        "vibe": "dark, modern, developer",
        "best_for": "SaaS, dev tools, AI startups",
        "accent": "#0070f3",
        "html": _TPL_VERCEL_MODERN,
    },
    "github-dark": {
        "name": "GitHub Dark",
        "tagline": "Dark navy with green CTAs and code blocks",
        "vibe": "dark, technical, code-centric",
        "best_for": "Open source, dev tools, infrastructure",
        "accent": "#238636",
        "html": _TPL_GITHUB_DARK,
    },
    "discord-vibrant": {
        "name": "Discord Vibrant",
        "tagline": "Blurple with playful community vibe",
        "vibe": "vibrant, community, playful",
        "best_for": "Community apps, gaming, social",
        "accent": "#5865F2",
        "html": _TPL_DISCORD_VIBRANT,
    },
    "mailchimp-whimsical": {
        "name": "Mailchimp Whimsical",
        "tagline": "Yellow + serif + cartoon mascot",
        "vibe": "whimsical, friendly, illustrated",
        "best_for": "Small business marketing, agencies",
        "accent": "#FFE01B",
        "html": _TPL_MAILCHIMP_WHIMSICAL,
    },
    "slack-pro": {
        "name": "Slack Pro",
        "tagline": "Aubergine + 4-color hashtag identity",
        "vibe": "productive, vibrant, modern",
        "best_for": "Enterprise SaaS, productivity tools",
        "accent": "#611f69",
        "html": _TPL_SLACK_PRO,
    },
    "coinbase-finance": {
        "name": "Coinbase Finance",
        "tagline": "Clean blue with crypto ticker",
        "vibe": "clean, trustworthy, financial",
        "best_for": "Fintech, crypto, investment platforms",
        "accent": "#0052FF",
        "html": _TPL_COINBASE_FINANCE,
    },
    "webflow-pro": {
        "name": "Webflow Pro",
        "tagline": "Black + electric blue + designer canvas",
        "vibe": "professional, designer, polished",
        "best_for": "Design agencies, CMS platforms, no-code",
        "accent": "#4353ff",
        "html": _TPL_WEBFLOW_PRO,
    },
    "figma-creative": {
        "name": "Figma Creative",
        "tagline": "Multi-color gradient mesh + design tool aesthetic",
        "vibe": "creative, colorful, modern",
        "best_for": "Design tools, creative agencies, startups",
        "accent": "#a259ff",
        "html": _TPL_FIGMA_CREATIVE,
    },
    "robinhood-trade": {
        "name": "Robinhood Trade",
        "tagline": "Bright green + animated stock chart",
        "vibe": "modern, fintech, trustworthy",
        "best_for": "Trading, brokerages, investment apps",
        "accent": "#00C805",
        "html": _TPL_ROBINHOOD_TRADE,
    },
    "patagonia-outdoors": {
        "name": "Patagonia Outdoors",
        "tagline": "Earth tones + activism + photography",
        "vibe": "earthy, conscious, outdoors",
        "best_for": "Outdoor brands, sustainability, conservation",
        "accent": "#3b5b3a",
        "html": _TPL_PATAGONIA_OUTDOORS,
    },
}

DEFAULT_TEMPLATE_ID = "eko-classic"


# ═══════════════════════════════════════════════════════════════════════════════
# DEFAULT COPY — fallback values used if AI fails to generate. Same 56 keys
# apply to all templates because the placeholder vocabulary is shared.
# ═══════════════════════════════════════════════════════════════════════════════

_DEFAULT_COPY = {
    "TITLE": "Eko AI — Your 24/7 AI Agent",
    "BADGE": "AI-Powered Automation for Local Businesses",
    "HERO_TITLE": "Your Business Never Sleeps With <span class='gradient accent'>Eko AI</span>",
    "HERO_SUBTITLE": "Never miss a customer call again. Eko AI answers questions, books appointments, and follows up automatically—so you can focus on growing your business.",
    "CTA_BUTTON": "Get Your Free AI Analysis",
    "STAT_1_NUM": "24/7",
    "STAT_1_LABEL": "Always Available",
    "STAT_2_NUM": "500+",
    "STAT_2_LABEL": "Businesses Served",
    "STAT_3_NUM": "98%",
    "STAT_3_LABEL": "Customer Satisfaction",
    "BENEFITS_HEADLINE": "Why Business Owners Love Eko AI",
    "BENEFITS_SUBHEADLINE": "Everything you need to never miss a customer",
    "BENEFIT_1_ICON": "📞",
    "BENEFIT_1_TITLE": "Answer Calls 24/7",
    "BENEFIT_1_DESC": "Never miss a call again. Your AI answers, qualifies leads, and transfers when needed.",
    "BENEFIT_2_ICON": "💬",
    "BENEFIT_2_TITLE": "Respond on WhatsApp",
    "BENEFIT_2_DESC": "Instant replies to customer inquiries. Product questions, pricing, availability—all automatic.",
    "BENEFIT_3_ICON": "📅",
    "BENEFIT_3_TITLE": "Book Appointments",
    "BENEFIT_3_DESC": "Connects directly to your calendar. Customers book, reschedule, or cancel without human help.",
    "BENEFIT_4_ICON": "🤝",
    "BENEFIT_4_TITLE": "Follow Up Automatically",
    "BENEFIT_4_DESC": "No lead falls through the cracks. Automated follow-ups nurture prospects until they convert.",
    "HOW_HEADLINE": "How It Works",
    "HOW_SUBHEADLINE": "Get started in 3 simple steps",
    "STEP_1_TITLE": "Book Your Demo",
    "STEP_1_DESC": "15 minutes. We learn about your business and show you exactly how AI will work for you.",
    "STEP_2_TITLE": "We Configure Everything",
    "STEP_2_DESC": "Our team trains your AI agent with your business info, services, pricing, and brand voice.",
    "STEP_3_TITLE": "Go Live & Scale",
    "STEP_3_DESC": "Your AI starts working immediately. Answer calls, book appointments, follow up—24/7 from day one.",
    "REVIEWS_HEADLINE": "Loved by Business Owners",
    "REVIEWS_SUBHEADLINE": "See what our customers say",
    "REVIEW_1_QUOTE": "We went from missing 30% of calls to booking every single one. Eko AI paid for itself in the first week.",
    "REVIEW_1_INITIALS": "MR",
    "REVIEW_1_NAME": "Maria Rodriguez",
    "REVIEW_1_ROLE": "Spa Owner, Miami",
    "REVIEW_2_QUOTE": "Finally, an AI that actually sounds like me! Clients don't even know they're talking to a bot.",
    "REVIEW_2_INITIALS": "JC",
    "REVIEW_2_NAME": "James Chen",
    "REVIEW_2_ROLE": "Gym Owner, San Francisco",
    "FAQ_HEADLINE": "Frequently Asked Questions",
    "FAQ_SUBHEADLINE": "Everything you need to know",
    "FAQ_1_Q": "How quickly can Eko AI be set up?",
    "FAQ_1_A": "Most businesses are live within 48 hours of their demo. We handle all the configuration, training, and integration.",
    "FAQ_2_Q": "Does it work with my existing tools?",
    "FAQ_2_A": "Yes. Eko AI integrates with Google Calendar, Outlook, Cal.com, most CRMs, and popular business phone systems.",
    "FAQ_3_Q": "What if the AI can't answer a question?",
    "FAQ_3_A": "Your AI is trained specifically on your business. For edge cases, it can transfer to you or take a message with full context.",
    "FAQ_4_Q": "Can I cancel anytime?",
    "FAQ_4_A": "Yes. No long-term contracts, no cancellation fees. We earn your business every month.",
    "FOOTER_HEADLINE": "Ready to never miss a customer again?",
    "FOOTER_SUBHEADLINE": "Join 500+ businesses already using Eko AI to automate their customer interactions.",
    "FOOTER_CTA": "Get Your Free AI Analysis",
}


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPT — identical across all templates. The AI generates one copy
# JSON that renders against any chosen template (same 56-key vocabulary).
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT_TEMPLATE = """You are a conversion copywriter for local businesses. Generate landing page copy for Eko AI based on the user's instructions.

═══════════════════════════════════════════════════════════════════════════════
ABOUT EKO AI — THE FULL PLATFORM
═══════════════════════════════════════════════════════════════════════════════

Eko AI is a complete AI-powered business automation platform for local businesses.
It is NOT just a phone bot — it covers customer communication, content marketing,
sales funnels, and CRM in one integrated system.

CAPABILITY LIBRARY (pick the 4 most relevant for the BENEFIT cards, based on the
user's niche and prompt — do NOT default to the same 4 every time):

1. **24/7 AI Receptionist** — Answers phone calls, WhatsApp messages, and emails
   instantly in the business's voice. Never miss a customer again. Handles FAQs,
   quotes, hours, directions, multilingual (English + Spanish out of the box).

2. **Smart Appointment Booking** — Direct Cal.com / Google Calendar / Outlook
   integration. Customers book, reschedule, cancel without human help. Sends
   SMS/WhatsApp reminders, manages waitlists, supports Google Meet and Zoom.

3. **AI Social Media Content Studio** — Auto-generates short-form (≈30s, 4 scenes)
   and long-form (≈80s, 6 scenes) videos with FLUX AI imagery, Ken Burns motion,
   crossfade transitions, multilingual Edge-TTS, and yellow karaoke subtitles.
   Auto-publishes to Instagram, Facebook, TikTok, YouTube, and LinkedIn via
   Buffer on peak-hour slots. End-frame CTA is dynamic.

4. **Self-Service Landing Page Builder** — Unlimited niche-specific landing pages
   from a simple prompt. Built-in A/B testing (Compare tab), Random pool
   rotation, SEO-friendly URLs, lead-source attribution per page.

5. **AI Email Reply Agent** — Auto-responds to inbound emails with contextual
   replies. Language detection, keyword routing, threading by lead.

6. **Voice AI Outbound (VAPI)** — AI agent makes outbound calls for follow-ups,
   confirmations, lead qualification, and re-activation campaigns.

7. **AI Proposal Generator** — Auto-generates personalized sales proposals.

8. **Smart CRM with Lead Scoring** — Auto-enriches leads, scores 0-100, churn
   prediction, interaction timeline across all channels.

9. **Automated Nurture Sequences** — Multi-touch email + SMS, milestone
   celebrations, behavior triggers.

10. **Unified Inbox** — All channels threaded per customer, AI summarization,
    hot-lead flags, suggested replies.

11. **Accounting Vertical Pack** (Growth — Contable) — Local invoice OCR
    (PDF/XML/photo, 500 docs/mo), native ERP integrations (Contasol, Anfix, SII,
    Alegra), offline bank reconciliation agent, monthly VAT/income-tax templates,
    pre-trained expense categorization. Use when the user mentions
    contadores / accountants / asesoría / despacho contable.

12. **Real Estate Vertical Pack** (Growth — Inmobiliario) — WhatsApp Business API
    (1 number, 2,000 conversations/mo), lead capture and scoring from WhatsApp +
    web, Idealista / Fotocasa integration, post-visit follow-up sequences,
    auto-classification of rent/buy/valuation inquiries. Use when the user
    mentions inmobiliaria / real estate / agente inmobiliario / brokers.

13. **Legal & Clinic Vertical Pack** (Growth — Legal/Clínico) — Document manager
    with auto-tagging and search, contract OCR + clause extraction, local
    e-signature (no cloud), immutable GDPR/HIPAA audit log, DPIA templates,
    auto-anonymization filters. Use when the user mentions abogado / bufete /
    legal / clínica / consultorio / law firm / healthcare practice.

═══════════════════════════════════════════════════════════════════════════════
PER-SECTION COPY RULES — apply ALL of these
═══════════════════════════════════════════════════════════════════════════════

HERO_SUBTITLE (max 200 chars): Must mention 24/7 availability AND at least ONE
other Eko AI capability by name.

BENEFITS (4 cards): Each TITLE MUST name an Eko AI feature explicitly. Each
DESCRIPTION (max 120 chars) MUST include a technical specific (Cal.com sync,
FLUX, IG/TikTok, 0-100 scoring, etc.).

HOW_IT_WORKS (3 steps): Step 2 (configuration) MUST list the 4 capabilities
the business is activating, by name.

REVIEWS (2 testimonials, max 150 chars): AT LEAST ONE must mention a
non-phone-bot capability by name (Content Studio, Lead Scoring, etc.).

FAQs (4 Q&As): AT LEAST 2 must be feature-education ("Does Eko create content?",
"Can I A/B test landing pages?", "Does it score leads?", etc.).

FOOTER: NOT generic anxiety ("Stop losing X"). MUST hint at all-in-one
platform value ("Your Entire Customer Journey, Automated"). Subheadline names
1-2 specific features.

═══════════════════════════════════════════════════════════════════════════════
GUARDRAILS
═══════════════════════════════════════════════════════════════════════════════

- DO NOT mention a capability the user explicitly excluded.
- DO NOT use the phrase "Eko AI is just a phone bot".
- DO NOT default to the same 4 BENEFITs every time.
- If REVIEWS, FAQs, or FOOTER mention ZERO features by name, you have failed
  the brief — rewrite that section before returning the JSON.
- Healthcare / legal niches: be conservative with Content Studio (compliance).

═══════════════════════════════════════════════════════════════════════════════

Return ONLY a JSON object with these exact keys. No markdown, no explanations.

Required JSON structure:
{
  "TITLE": "Page title (50 chars max)",
  "BADGE": "Short badge above headline",
  "HERO_TITLE": "Main headline with HTML span: 'Your X Never Sleeps With <span class=\\'accent\\'>Eko AI</span>' (use class='accent' so it works in all templates)",
  "HERO_SUBTITLE": "One paragraph value prop (max 200 chars, must name a feature)",
  "CTA_BUTTON": "Button text (e.g., 'Get Your Free AI Analysis')",
  "STAT_1_NUM": "First stat number", "STAT_1_LABEL": "First stat label",
  "STAT_2_NUM": "Second stat number", "STAT_2_LABEL": "Second stat label",
  "STAT_3_NUM": "Third stat number", "STAT_3_LABEL": "Third stat label",
  "BENEFITS_HEADLINE": "Benefits headline", "BENEFITS_SUBHEADLINE": "Subheadline",
  "BENEFIT_1_ICON": "Single emoji", "BENEFIT_1_TITLE": "Benefit 1 title (names a feature)", "BENEFIT_1_DESC": "Benefit 1 description (max 120 chars, with tech specific)",
  "BENEFIT_2_ICON": "Single emoji", "BENEFIT_2_TITLE": "Benefit 2 title", "BENEFIT_2_DESC": "Benefit 2 description",
  "BENEFIT_3_ICON": "Single emoji", "BENEFIT_3_TITLE": "Benefit 3 title", "BENEFIT_3_DESC": "Benefit 3 description",
  "BENEFIT_4_ICON": "Single emoji", "BENEFIT_4_TITLE": "Benefit 4 title", "BENEFIT_4_DESC": "Benefit 4 description",
  "HOW_HEADLINE": "How It Works headline", "HOW_SUBHEADLINE": "Subheadline",
  "STEP_1_TITLE": "Step 1 title", "STEP_1_DESC": "Step 1 description (max 120 chars)",
  "STEP_2_TITLE": "Step 2 title (names the 4 capabilities)", "STEP_2_DESC": "Step 2 description",
  "STEP_3_TITLE": "Step 3 title", "STEP_3_DESC": "Step 3 description",
  "REVIEWS_HEADLINE": "Reviews headline", "REVIEWS_SUBHEADLINE": "Subheadline",
  "REVIEW_1_QUOTE": "First testimonial (mentions a feature)", "REVIEW_1_INITIALS": "2-letter initials", "REVIEW_1_NAME": "Name", "REVIEW_1_ROLE": "Role + location",
  "REVIEW_2_QUOTE": "Second testimonial", "REVIEW_2_INITIALS": "Initials", "REVIEW_2_NAME": "Name", "REVIEW_2_ROLE": "Role + location",
  "FAQ_HEADLINE": "FAQ headline", "FAQ_SUBHEADLINE": "Subheadline",
  "FAQ_1_Q": "Feature-education FAQ", "FAQ_1_A": "Answer (max 150 chars)",
  "FAQ_2_Q": "Feature-education FAQ", "FAQ_2_A": "Answer",
  "FAQ_3_Q": "Standard objection FAQ", "FAQ_3_A": "Answer",
  "FAQ_4_Q": "Standard objection FAQ", "FAQ_4_A": "Answer",
  "FOOTER_HEADLINE": "Platform-value headline (NOT anxiety messaging)",
  "FOOTER_SUBHEADLINE": "Subheadline naming 1-2 features (max 120 chars)",
  "FOOTER_CTA": "Footer button text"
}

IMPORTANT — LANGUAGE: Auto-detect the language of USER INSTRUCTIONS below.
Write ALL output copy in that SAME language. If the user wrote the prompt in
Spanish, every value in the JSON must be in Spanish. If in English, every
value in English. NEVER mix languages within one page. Brand names (Eko AI,
Cal.com, VAPI, FLUX, Buffer) and common tech terms (CRM, SEO, FAQ) stay
English in both cases.

USER INSTRUCTIONS:
{custom_prompt}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

def list_templates() -> list:
    """Return template metadata for the selector UI (without HTML body)."""
    return [
        {
            "id": tid,
            "name": tdata["name"],
            "tagline": tdata["tagline"],
            "vibe": tdata["vibe"],
            "best_for": tdata["best_for"],
            "accent": tdata["accent"],
        }
        for tid, tdata in TEMPLATES.items()
    ]


def render_template(copy: dict, landing_page_id: int, year: int,
                    template_id: Optional[str] = None) -> str:
    """Render the chosen template with AI-generated copy.

    Falls back to DEFAULT_TEMPLATE_ID if template_id is unknown / None.
    Missing copy keys fall back to _DEFAULT_COPY.
    """
    tpl_id = template_id if template_id in TEMPLATES else DEFAULT_TEMPLATE_ID
    html = TEMPLATES[tpl_id]["html"]
    # Substitute shared bits (tracking pixel and form JS) before per-key copy
    html = html.replace("__TRACKING_PIXEL__", _TRACKING_PIXEL)
    html = html.replace("__FORM_SUBMIT_JS__", _FORM_SUBMIT_JS)
    # Merge defaults with AI-generated copy, then add LP_ID and YEAR
    data = {**_DEFAULT_COPY, **copy, "LP_ID": str(landing_page_id), "YEAR": str(year)}
    for key, value in data.items():
        html = html.replace("{{" + key + "}}", str(value))
    return html


def render_template_preview(template_id: str) -> str:
    """Render a template with sample default copy — used for the selector preview.

    Uses LP_ID=0 so the tracking pixel doesn't record fake visits.
    """
    from datetime import datetime
    return render_template({}, 0, datetime.now().year, template_id)
