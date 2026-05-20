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
