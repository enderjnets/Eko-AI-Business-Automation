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
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;overflow-x:hidden}
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
:root{--bg:#fff;--text:#1d1d1f;--muted:#86868b;--accent:#0066cc;--light:#f5f5f7}
html{scroll-behavior:smooth}body{font-family:'SF Pro Display','SF Pro Text',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.47;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(255,255,255,.72);backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid rgba(0,0,0,.06)}
.nav-inner{max-width:1024px;margin:0 auto;padding:0 22px;height:44px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:21px;font-weight:600;letter-spacing:-.022em}
.nav-links{display:flex;gap:32px;list-style:none}
.nav-links a{color:var(--text);font-size:12px;font-weight:400;opacity:.8}.nav-links a:hover{opacity:1;text-decoration:none}
.hero{padding:140px 22px 80px;text-align:center;background:var(--bg)}
.hero h1{font-size:clamp(48px,8vw,96px);font-weight:600;line-height:1.05;letter-spacing:-.005em;margin-bottom:8px;color:var(--text)}
.hero h1 .accent{color:var(--accent)}
.hero .sub{font-size:clamp(21px,3vw,28px);font-weight:400;color:var(--muted);max-width:680px;margin:0 auto 32px;letter-spacing:.011em}
.hero-badge{display:inline-block;font-size:17px;color:var(--accent);font-weight:400;margin-bottom:20px;letter-spacing:-.022em}
.cta-form{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;max-width:560px;margin:32px auto 24px}
.cta-form input{flex:1 1 240px;padding:14px 18px;border-radius:980px;border:1px solid #d2d2d7;background:#fff;color:var(--text);font-size:15px;font-family:inherit;outline:none;transition:border-color .2s}
.cta-form input:focus{border-color:var(--accent)}
.cta-form button{padding:14px 28px;border-radius:980px;border:none;background:var(--accent);color:#fff;font-size:15px;font-weight:400;cursor:pointer;transition:background .2s}
.cta-form button:hover{background:#0051a4}
.stats{display:flex;justify-content:center;gap:60px;margin-top:60px;padding:60px 0;border-top:1px solid #d2d2d7;border-bottom:1px solid #d2d2d7;flex-wrap:wrap}
.stat-num{font-size:56px;font-weight:600;letter-spacing:-.025em;color:var(--text)}.stat-label{font-size:14px;color:var(--muted);margin-top:4px}
.section{padding:120px 22px;max-width:980px;margin:0 auto;text-align:center}
.section-alt{background:var(--light)}
.section-header h2{font-size:clamp(40px,6vw,64px);font-weight:600;letter-spacing:-.005em;line-height:1.08;margin-bottom:14px}
.section-header p{font-size:21px;color:var(--muted);max-width:600px;margin:0 auto 64px;letter-spacing:.011em}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;text-align:left}
.feature{padding:0}.feature-icon{font-size:48px;margin-bottom:16px}
.feature h3{font-size:21px;font-weight:600;letter-spacing:-.022em;margin-bottom:8px;color:var(--text)}
.feature p{font-size:17px;color:var(--muted);letter-spacing:-.022em}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:48px;text-align:left}
.step-num{font-size:64px;font-weight:600;color:var(--accent);letter-spacing:-.025em;margin-bottom:8px;display:block}
.step h3{font-size:21px;font-weight:600;letter-spacing:-.022em;margin-bottom:8px}
.step p{font-size:17px;color:var(--muted)}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:32px;text-align:left}
.review{padding:32px;border-radius:18px;background:#fff;border:1px solid #d2d2d7}
.review-stars{color:#f5a623;font-size:14px;margin-bottom:14px}
.review-quote{font-size:19px;line-height:1.42;letter-spacing:-.011em;color:var(--text);margin-bottom:24px}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#0066cc,#5ac8fa);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:15px}
.review-name{font-size:15px;font-weight:600;display:block}.review-role{font-size:13px;color:var(--muted)}
.faq{max-width:720px;margin:48px auto 0;text-align:left}
.faq-item{border-bottom:1px solid #d2d2d7}
.faq-q{width:100%;padding:24px 0;background:none;border:none;text-align:left;font-size:19px;font-weight:600;letter-spacing:-.022em;color:var(--text);cursor:pointer;display:flex;justify-content:space-between;align-items:center}
.faq-q::after{content:'+';font-size:24px;color:var(--accent);font-weight:400;transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;font-size:17px;color:var(--muted);line-height:1.5}
.faq-item.active .faq-a{max-height:240px;padding:0 0 24px}
.footer{background:var(--light);padding:80px 22px;text-align:center}
.footer h2{font-size:clamp(32px,5vw,48px);font-weight:600;letter-spacing:-.005em;margin-bottom:16px}
.footer p{font-size:19px;color:var(--muted);max-width:560px;margin:0 auto 32px}
.footer-btn{display:inline-block;padding:14px 32px;border-radius:980px;background:var(--accent);color:#fff;font-size:17px;font-weight:400;text-decoration:none}
.footer-btn:hover{background:#0051a4;text-decoration:none;color:#fff}
.copy{margin-top:48px;font-size:12px;color:var(--muted)}
@media(max-width:640px){.nav-links{gap:16px}.stats{gap:32px}.stat-num{font-size:40px}.section{padding:80px 22px}.review{padding:24px}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner"><a href="#" class="logo">Eko AI</a>
<ul class="nav-links"><li><a href="#benefits">Features</a></li><li><a href="#how">How It Works</a></li><li><a href="#reviews">Customers</a></li><li><a href="#faq">FAQ</a></li><li><a href="#form">Get Started</a></li></ul></div></nav>
<section class="hero" id="form"><span class="hero-badge">{{BADGE}}</span><h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button></form>
<div class="stats"><div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div></div></section>
<section class="section" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section section-alt" id="how"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><span class="step-num">01</span><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><span class="step-num">02</span><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><span class="step-num">03</span><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div></div></section>
<section class="section section-alt" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
<div class="copy">© {{YEAR}} Eko AI. contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 3: STRIPE GRADIENT — Gradient mesh hero, technical/clean, sophisticated
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_STRIPE_GRADIENT = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--text:#0a2540;--muted:#425466;--accent:#635bff;--purple:#8a4ff5;--green:#00d4ff;--bg:#fff;--surface:#f6f9fc}
html{scroll-behavior:smooth}body{font-family:'Inter','SF Pro Text',-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
.nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);border-bottom:1px solid rgba(0,0,0,.05)}
.nav-inner{max-width:1080px;margin:0 auto;padding:0 24px;height:64px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:24px;font-weight:700;color:var(--text);letter-spacing:-.5px}
.nav-links{display:flex;gap:32px;list-style:none}.nav-links a{color:var(--muted);font-size:15px;font-weight:500}.nav-links a:hover{color:var(--text)}
.nav-cta{padding:8px 16px;border-radius:20px;background:var(--text);color:#fff!important;font-size:14px;font-weight:600}
.hero{position:relative;padding:120px 24px 80px;overflow:hidden;background:linear-gradient(135deg,#f6f9fc 0%,#e8f0fe 30%,#fbe4ff 70%,#fff6e8 100%)}
.hero::before{content:'';position:absolute;top:-200px;right:-200px;width:600px;height:600px;background:radial-gradient(circle,rgba(99,91,255,.3),transparent 70%);border-radius:50%;filter:blur(60px)}
.hero::after{content:'';position:absolute;bottom:-200px;left:-200px;width:600px;height:600px;background:radial-gradient(circle,rgba(0,212,255,.25),transparent 70%);border-radius:50%;filter:blur(60px)}
.hero-inner{max-width:980px;margin:0 auto;position:relative;z-index:1;text-align:center}
.badge{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:999px;background:#fff;border:1px solid rgba(99,91,255,.2);color:var(--accent);font-size:13px;font-weight:600;margin-bottom:24px;box-shadow:0 4px 16px rgba(99,91,255,.1)}
h1{font-size:clamp(40px,7vw,76px);font-weight:800;line-height:1.05;letter-spacing:-2.5px;color:var(--text);margin-bottom:24px}
h1 .gradient{background:linear-gradient(135deg,var(--accent),var(--purple) 50%,var(--green));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p.sub{font-size:clamp(18px,2.5vw,22px);color:var(--muted);max-width:640px;margin:0 auto 36px;line-height:1.55}
.hero-form{display:flex;flex-wrap:wrap;gap:8px;max-width:560px;margin:0 auto;padding:8px;background:#fff;border-radius:14px;box-shadow:0 16px 56px rgba(10,37,64,.16);justify-content:center}
.hero-form input{flex:1 1 200px;padding:14px 16px;border:1px solid #e6e6e6;border-radius:10px;font-size:15px;font-family:inherit;outline:none;background:#fafbfc}
.hero-form input:focus{border-color:var(--accent);background:#fff}
.hero-form button{flex:0 0 auto;padding:14px 28px;border:none;border-radius:10px;background:linear-gradient(135deg,var(--accent),var(--purple));color:#fff;font-size:15px;font-weight:600;cursor:pointer;box-shadow:0 4px 12px rgba(99,91,255,.4)}
.stats{display:flex;justify-content:center;gap:48px;margin-top:64px;flex-wrap:wrap}
.stat-num{font-size:44px;font-weight:800;color:var(--text);letter-spacing:-1px}
.stat-label{font-size:14px;color:var(--muted);font-weight:500}
.section{padding:96px 24px;max-width:1080px;margin:0 auto}
.section-alt{background:var(--surface)}
.section-header{text-align:center;margin-bottom:56px}
.section-header h2{font-size:clamp(32px,4.5vw,48px);font-weight:800;letter-spacing:-1.5px;margin-bottom:16px}
.section-header p{color:var(--muted);font-size:19px;max-width:560px;margin:0 auto}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature{padding:32px;border-radius:16px;background:#fff;border:1px solid #e6e6e6;transition:all .25s;position:relative}
.feature:hover{transform:translateY(-4px);box-shadow:0 20px 48px rgba(10,37,64,.08);border-color:rgba(99,91,255,.2)}
.feature-icon{display:inline-flex;width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,var(--accent),var(--purple));color:#fff;align-items:center;justify-content:center;font-size:22px;margin-bottom:16px}
.feature h3{font-size:18px;font-weight:700;margin-bottom:8px}.feature p{color:var(--muted);font-size:15px}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:32px}
.step{padding:0;text-align:left}
.step-badge{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,var(--accent),var(--purple));color:#fff;font-weight:700;font-size:14px;margin-bottom:16px}
.step h3{font-size:20px;font-weight:700;margin-bottom:8px}.step p{color:var(--muted);font-size:16px}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{padding:32px;border-radius:16px;background:#fff;border:1px solid #e6e6e6}
.review-stars{color:#ffb800;font-size:16px;margin-bottom:14px}
.review-quote{font-size:18px;color:var(--text);margin-bottom:24px;line-height:1.5}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--green));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.review-name{font-weight:700;font-size:15px;display:block}.review-role{font-size:13px;color:var(--muted)}
.faq{max-width:760px;margin:0 auto}
.faq-item{border:1px solid #e6e6e6;border-radius:12px;margin-bottom:12px;background:#fff;overflow:hidden}
.faq-q{width:100%;padding:20px 24px;background:none;border:none;text-align:left;font-size:17px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text)}
.faq-q::after{content:'+';font-size:22px;color:var(--accent);transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;padding:0 24px;line-height:1.6}
.faq-item.active .faq-a{max-height:240px;padding:0 24px 20px}
.footer{padding:96px 24px;text-align:center;background:linear-gradient(135deg,#0a2540,#1a3a6c);color:#fff}
.footer h2{font-size:clamp(32px,5vw,48px);font-weight:800;letter-spacing:-1.5px;margin-bottom:16px}
.footer p{font-size:18px;color:rgba(255,255,255,.7);max-width:560px;margin:0 auto 32px}
.footer-btn{display:inline-block;padding:14px 32px;border-radius:10px;background:#fff;color:var(--text);font-weight:600;font-size:16px}
.footer-copy{margin-top:48px;font-size:13px;color:rgba(255,255,255,.5)}
@media(max-width:640px){.nav-links{display:none}.stats{gap:24px}.features-grid,.steps-grid,.reviews-grid{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner"><a href="#" class="logo">Eko<span style="color:var(--accent)">.AI</span></a>
<ul class="nav-links"><li><a href="#benefits">Products</a></li><li><a href="#how">Solutions</a></li><li><a href="#reviews">Customers</a></li><li><a href="#faq">Pricing</a></li><li><a href="#form" class="nav-cta">Get Started →</a></li></ul></div></nav>
<section class="hero" id="form"><div class="hero-inner">
<div class="badge">⚡ {{BADGE}}</div><h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}} →</button></form>
<div class="stats"><div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div></div></div></section>
<section class="section" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section section-alt" id="how"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-badge">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-badge">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-badge">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div></div></section>
<section class="section section-alt" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}} →</a>
<div class="footer-copy">© {{YEAR}} Eko AI. contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 4: LINEAR DARK — Pure black bg, neon purple accents, sharp geometric
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_LINEAR_DARK = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#08080a;--surface:#0f0f12;--surface-2:#15151a;--text:#fff;--muted:#888;--accent:#5e6ad2;--accent-2:#a78bfa;--green:#1eb1aa}
html{scroll-behavior:smooth}body{font-family:'Inter','SF Pro Text',-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased}
body::before{content:'';position:fixed;inset:0;background-image:radial-gradient(circle at 50% 0%,rgba(94,106,210,.08),transparent 50%),linear-gradient(rgba(255,255,255,.02) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.02) 1px,transparent 1px);background-size:100% 100%,40px 40px,40px 40px;pointer-events:none;z-index:0}
a{color:var(--accent-2);text-decoration:none}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(8,8,10,.7);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.05)}
.nav-inner{max-width:1160px;margin:0 auto;padding:0 32px;height:56px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:18px;font-weight:600;color:var(--text);letter-spacing:-.3px}
.nav-links{display:flex;gap:28px;list-style:none}
.nav-links a{color:var(--muted);font-size:14px;font-weight:500}.nav-links a:hover{color:var(--text)}
.nav-cta{padding:7px 14px;border-radius:6px;background:var(--text);color:var(--bg)!important;font-size:13px;font-weight:600}
.hero{position:relative;z-index:1;padding:140px 32px 96px;text-align:center;max-width:1160px;margin:0 auto}
.badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:999px;background:rgba(94,106,210,.12);border:1px solid rgba(94,106,210,.3);color:var(--accent-2);font-size:13px;font-weight:500;margin-bottom:32px}
h1{font-size:clamp(40px,7vw,72px);font-weight:600;line-height:1.05;letter-spacing:-2.5px;margin-bottom:24px}
h1 .grad{background:linear-gradient(135deg,var(--accent),var(--accent-2),var(--green));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p.sub{font-size:clamp(17px,2.5vw,21px);color:var(--muted);max-width:600px;margin:0 auto 40px;line-height:1.5}
.hero-form{display:flex;flex-wrap:wrap;gap:10px;max-width:540px;margin:0 auto;justify-content:center}
.hero-form input{flex:1 1 200px;padding:13px 16px;border:1px solid rgba(255,255,255,.1);border-radius:8px;background:var(--surface);color:var(--text);font-size:14px;font-family:inherit;outline:none;transition:border-color .2s}
.hero-form input:focus{border-color:var(--accent)}.hero-form input::placeholder{color:#555}
.hero-form button{flex:0 0 auto;padding:13px 24px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:14px;font-weight:600;cursor:pointer;transition:background .2s}
.hero-form button:hover{background:var(--accent-2)}
.stats{display:flex;justify-content:center;gap:64px;margin-top:80px;flex-wrap:wrap}
.stat-num{font-size:40px;font-weight:600;color:var(--text);letter-spacing:-1.5px;font-feature-settings:'tnum'}
.stat-label{font-size:13px;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.5px}
.section{position:relative;z-index:1;padding:96px 32px;max-width:1160px;margin:0 auto}
.section-header{text-align:center;margin-bottom:64px}
.section-header h2{font-size:clamp(32px,5vw,48px);font-weight:600;letter-spacing:-1.5px;margin-bottom:14px}
.section-header p{color:var(--muted);font-size:18px;max-width:560px;margin:0 auto}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.05);border-radius:12px;overflow:hidden}
.feature{padding:32px;background:var(--surface);transition:background .2s}
.feature:hover{background:var(--surface-2)}
.feature-icon{display:inline-flex;width:36px;height:36px;border-radius:8px;background:rgba(94,106,210,.15);color:var(--accent-2);align-items:center;justify-content:center;font-size:18px;margin-bottom:16px}
.feature h3{font-size:16px;font-weight:600;margin-bottom:8px;color:var(--text)}
.feature p{color:var(--muted);font-size:14px;line-height:1.55}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:32px}
.step{padding:32px;border:1px solid rgba(255,255,255,.06);border-radius:12px;background:var(--surface);position:relative}
.step-num{position:absolute;top:24px;right:24px;font-size:48px;font-weight:700;color:rgba(94,106,210,.15);letter-spacing:-2px}
.step h3{font-size:18px;font-weight:600;margin-bottom:10px}.step p{color:var(--muted);font-size:14px}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}
.review{padding:28px;border:1px solid rgba(255,255,255,.06);border-radius:12px;background:var(--surface)}
.review-stars{color:#fbbf24;font-size:14px;margin-bottom:14px;letter-spacing:2px}
.review-quote{font-size:16px;color:var(--text);margin-bottom:20px;line-height:1.55}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent-2));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:13px}
.review-name{font-weight:600;font-size:14px;display:block}.review-role{font-size:12px;color:var(--muted)}
.faq{max-width:720px;margin:0 auto}
.faq-item{border-bottom:1px solid rgba(255,255,255,.06)}
.faq-q{width:100%;padding:20px 0;background:none;border:none;text-align:left;font-size:16px;font-weight:500;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text)}
.faq-q::after{content:'+';font-size:22px;color:var(--accent-2);transition:transform .3s;font-weight:300}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:14px;line-height:1.6}
.faq-item.active .faq-a{max-height:240px;padding:0 0 20px}
.footer{position:relative;z-index:1;padding:96px 32px;text-align:center;background:radial-gradient(ellipse at 50% 100%,rgba(94,106,210,.15),transparent 70%);border-top:1px solid rgba(255,255,255,.05)}
.footer h2{font-size:clamp(32px,5vw,48px);font-weight:600;letter-spacing:-1.5px;margin-bottom:16px}
.footer p{font-size:17px;color:var(--muted);max-width:560px;margin:0 auto 28px}
.footer-btn{display:inline-block;padding:13px 32px;border-radius:8px;background:var(--accent);color:#fff;font-weight:600;font-size:14px}
.footer-btn:hover{background:var(--accent-2)}
.copy{margin-top:48px;font-size:12px;color:#555}
@media(max-width:640px){.nav-links{display:none}.stats{gap:32px}.features-grid{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner"><a href="#" class="logo">◢ Eko AI</a>
<ul class="nav-links"><li><a href="#benefits">Features</a></li><li><a href="#how">Method</a></li><li><a href="#reviews">Customers</a></li><li><a href="#faq">FAQ</a></li><li><a href="#form" class="nav-cta">Get started</a></li></ul></div></nav>
<section class="hero" id="form"><div class="badge">⚡ {{BADGE}}</div><h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button></form>
<div class="stats"><div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div></div></section>
<section class="section" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section" id="how"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><span class="step-num">01</span><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><span class="step-num">02</span><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><span class="step-num">03</span><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div></div></section>
<section class="section" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
<div class="copy">© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""


# Continued in next file part — templates 5-10


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 5: AIRBNB WARM — Coral red, rounded corners, friendly hospitality vibe
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_AIRBNB_WARM = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--coral:#FF5A5F;--coral-dark:#E04E52;--text:#222;--muted:#717171;--bg:#fff;--surface:#f7f7f7;--border:#dddddd}
html{scroll-behavior:smooth}body{font-family:'Cereal','Inter','Circular',-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:var(--coral);text-decoration:none}
.nav{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid var(--border);box-shadow:0 1px 0 rgba(0,0,0,.02)}
.nav-inner{max-width:1280px;margin:0 auto;padding:0 24px;height:80px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:22px;font-weight:700;color:var(--coral);letter-spacing:-.4px}.logo span{color:var(--text)}
.nav-links{display:flex;gap:24px;list-style:none}.nav-links a{color:var(--text);font-size:14px;font-weight:500}.nav-links a:hover{color:var(--coral)}
.nav-cta{padding:10px 18px;border-radius:22px;background:linear-gradient(135deg,var(--coral),#E61E4D);color:#fff!important;font-weight:600;font-size:14px}
.hero{padding:80px 24px 100px;background:linear-gradient(180deg,#fff 0%,#fff4f4 100%);text-align:center}
.hero-inner{max-width:920px;margin:0 auto}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 18px;border-radius:28px;background:#fff;border:1px solid var(--border);color:var(--coral);font-size:13px;font-weight:600;margin-bottom:28px;box-shadow:0 2px 8px rgba(0,0,0,.05)}
h1{font-size:clamp(40px,7vw,72px);font-weight:800;line-height:1.08;letter-spacing:-1.5px;margin-bottom:24px;color:var(--text)}
h1 .accent{color:var(--coral)}
.hero p.sub{font-size:clamp(17px,2.5vw,21px);color:var(--muted);max-width:640px;margin:0 auto 36px;line-height:1.5}
.hero-form{display:flex;flex-wrap:wrap;gap:8px;max-width:580px;margin:0 auto 24px;padding:8px;background:#fff;border-radius:60px;border:1px solid var(--border);box-shadow:0 8px 28px rgba(0,0,0,.08)}
.hero-form input{flex:1 1 200px;padding:14px 18px;border:none;border-radius:50px;font-size:14px;font-family:inherit;outline:none;background:transparent;color:var(--text)}
.hero-form input:focus{background:var(--surface)}
.hero-form button{flex:0 0 auto;padding:14px 28px;border:none;border-radius:50px;background:linear-gradient(135deg,var(--coral),#E61E4D);color:#fff;font-size:14px;font-weight:700;cursor:pointer;letter-spacing:.2px}
.hero-form button:hover{background:var(--coral-dark)}
.stats{display:flex;justify-content:center;gap:56px;margin-top:64px;flex-wrap:wrap}
.stat{text-align:center}.stat-num{font-size:44px;font-weight:800;color:var(--coral);letter-spacing:-1px}
.stat-label{font-size:14px;color:var(--muted);margin-top:4px;font-weight:500}
.section{padding:96px 24px;max-width:1280px;margin:0 auto}
.section-alt{background:var(--surface)}
.section-header{text-align:center;margin-bottom:56px}
.section-header h2{font-size:clamp(32px,5vw,48px);font-weight:800;letter-spacing:-1.2px;margin-bottom:14px}
.section-header p{color:var(--muted);font-size:18px;max-width:560px;margin:0 auto}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature{padding:32px;border-radius:16px;background:#fff;border:1px solid var(--border);transition:all .2s}
.feature:hover{transform:translateY(-4px);box-shadow:0 16px 40px rgba(0,0,0,.08)}
.feature-icon{font-size:40px;margin-bottom:16px}
.feature h3{font-size:18px;font-weight:700;margin-bottom:8px;color:var(--text)}
.feature p{color:var(--muted);font-size:15px;line-height:1.55}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:48px}
.step{text-align:center;padding:24px}
.step-num{width:64px;height:64px;border-radius:50%;background:#fff;border:2px solid var(--coral);color:var(--coral);display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:800;margin:0 auto 20px}
.step h3{font-size:20px;font-weight:700;margin-bottom:10px}.step p{color:var(--muted);font-size:15px}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{padding:32px;border-radius:16px;background:#fff;border:1px solid var(--border)}
.review-stars{color:#FF5A5F;font-size:16px;margin-bottom:14px}
.review-quote{font-size:17px;color:var(--text);margin-bottom:24px;line-height:1.55;font-style:italic}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,var(--coral),#E61E4D);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.review-name{font-weight:700;font-size:15px;display:block}.review-role{font-size:13px;color:var(--muted)}
.faq{max-width:780px;margin:0 auto}
.faq-item{border-radius:16px;background:#fff;border:1px solid var(--border);margin-bottom:12px;overflow:hidden}
.faq-q{width:100%;padding:24px;background:none;border:none;text-align:left;font-size:17px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text)}
.faq-q::after{content:'+';font-size:24px;color:var(--coral);transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;padding:0 24px;line-height:1.6}
.faq-item.active .faq-a{max-height:260px;padding:0 24px 20px}
.footer{padding:96px 24px;text-align:center;background:linear-gradient(135deg,var(--coral),#E61E4D);color:#fff}
.footer h2{font-size:clamp(32px,5vw,48px);font-weight:800;letter-spacing:-1.2px;margin-bottom:16px}
.footer p{font-size:18px;opacity:.92;max-width:560px;margin:0 auto 32px}
.footer-btn{display:inline-block;padding:16px 36px;border-radius:50px;background:#fff;color:var(--coral);font-weight:700;font-size:16px}
.footer-btn:hover{background:var(--surface)}
.copy{margin-top:48px;font-size:13px;opacity:.7}
@media(max-width:640px){.nav-links{display:none}.stats{gap:32px}.features-grid,.reviews-grid{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner"><a href="#" class="logo">eko<span> AI</span></a>
<ul class="nav-links"><li><a href="#benefits">Features</a></li><li><a href="#how">How It Works</a></li><li><a href="#reviews">Reviews</a></li><li><a href="#faq">FAQ</a></li><li><a href="#form" class="nav-cta">Get Started</a></li></ul></div></nav>
<section class="hero" id="form"><div class="hero-inner">
<div class="badge">⚡ {{BADGE}}</div><h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button></form>
<div class="stats"><div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div></div></div></section>
<section class="section" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section section-alt" id="how"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div></div></section>
<section class="section section-alt" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
<div class="copy">© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 6: NOTION CLEAN — Off-white, serif, playful, blocks, soft shadows
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_NOTION_CLEAN = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#f7f6f3;--surface:#fff;--text:#191919;--muted:#787774;--accent:#2eaadc;--border:#e9e9e7}
html{scroll-behavior:smooth}body{font-family:'Lyon','Georgia',-apple-system,serif;background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased}
.sans{font-family:'Inter','Segoe UI',sans-serif}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid currentColor}
.nav{position:sticky;top:0;z-index:100;background:rgba(247,246,243,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}
.nav-inner{max-width:1080px;margin:0 auto;padding:0 24px;height:60px;display:flex;align-items:center;justify-content:space-between}
.logo{font-family:'Lyon',serif;font-size:22px;font-weight:700;color:var(--text);letter-spacing:-.3px}
.nav-links{display:flex;gap:24px;list-style:none}.nav-links a{color:var(--muted);font-family:'Inter',sans-serif;font-size:14px;font-weight:500;border:none}.nav-links a:hover{color:var(--text)}
.nav-cta{padding:8px 16px;border-radius:6px;background:var(--text);color:#fff!important;border:none!important;font-size:14px;font-weight:600}
.hero{padding:100px 24px 80px;max-width:1080px;margin:0 auto;text-align:center}
.badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:6px;background:#fff;border:1px solid var(--border);color:var(--text);font-family:'Inter',sans-serif;font-size:13px;font-weight:500;margin-bottom:32px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
h1{font-family:'Lyon','Georgia',serif;font-size:clamp(44px,8vw,80px);font-weight:700;line-height:1.05;letter-spacing:-2px;margin-bottom:24px}
h1 em{font-style:italic;color:var(--accent)}
.hero p.sub{font-family:'Inter',sans-serif;font-size:clamp(17px,2.5vw,20px);color:var(--muted);max-width:600px;margin:0 auto 40px;line-height:1.55}
.hero-form{display:flex;flex-wrap:wrap;gap:8px;max-width:560px;margin:0 auto;justify-content:center;font-family:'Inter',sans-serif}
.hero-form input{flex:1 1 200px;padding:12px 16px;border:1px solid var(--border);border-radius:6px;background:#fff;color:var(--text);font-size:14px;font-family:inherit;outline:none}
.hero-form input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(46,170,220,.15)}
.hero-form button{flex:0 0 auto;padding:12px 24px;border:none;border-radius:6px;background:var(--text);color:#fff;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit}
.hero-form button:hover{background:#000}
.stats{display:flex;justify-content:center;gap:64px;margin-top:64px;flex-wrap:wrap;font-family:'Inter',sans-serif}
.stat-num{font-size:40px;font-weight:700;color:var(--text);letter-spacing:-1px}
.stat-label{font-size:13px;color:var(--muted);margin-top:4px}
.section{padding:80px 24px;max-width:1080px;margin:0 auto}
.section-alt{background:#fff;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.section-header{text-align:center;margin-bottom:48px}
.section-header h2{font-family:'Lyon',serif;font-size:clamp(32px,5vw,48px);font-weight:700;letter-spacing:-1.2px;margin-bottom:16px}
.section-header p{font-family:'Inter',sans-serif;color:var(--muted);font-size:17px;max-width:540px;margin:0 auto}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;font-family:'Inter',sans-serif}
.feature{padding:28px;border-radius:8px;background:#fff;border:1px solid var(--border);transition:transform .2s,box-shadow .2s}
.feature:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.06)}
.feature-icon{font-size:36px;margin-bottom:16px}
.feature h3{font-family:'Lyon',serif;font-size:20px;font-weight:700;margin-bottom:8px;letter-spacing:-.3px}
.feature p{color:var(--muted);font-size:14.5px;line-height:1.55}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:32px;font-family:'Inter',sans-serif}
.step{padding:28px;border-radius:8px;background:#fff;border:1px solid var(--border)}
.step-num{display:inline-flex;width:32px;height:32px;border-radius:6px;background:var(--text);color:#fff;align-items:center;justify-content:center;font-weight:700;font-size:14px;margin-bottom:14px}
.step h3{font-family:'Lyon',serif;font-size:19px;font-weight:700;margin-bottom:8px}
.step p{color:var(--muted);font-size:14.5px}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;font-family:'Inter',sans-serif}
.review{padding:28px;border-radius:8px;background:#fff;border:1px solid var(--border)}
.review-stars{color:#fbbf24;font-size:14px;margin-bottom:14px}
.review-quote{font-family:'Lyon',serif;font-size:18px;color:var(--text);margin-bottom:24px;line-height:1.5}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:40px;height:40px;border-radius:6px;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.review-name{font-weight:600;font-size:14px;display:block}.review-role{font-size:12px;color:var(--muted)}
.faq{max-width:720px;margin:0 auto;font-family:'Inter',sans-serif}
.faq-item{border-bottom:1px solid var(--border)}
.faq-q{width:100%;padding:20px 0;background:none;border:none;text-align:left;font-family:'Lyon',serif;font-size:18px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);letter-spacing:-.3px}
.faq-q::after{content:'›';font-size:24px;color:var(--muted);transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(90deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;line-height:1.65}
.faq-item.active .faq-a{max-height:240px;padding:0 0 20px}
.footer{padding:80px 24px;text-align:center;background:#fff;border-top:1px solid var(--border)}
.footer h2{font-family:'Lyon',serif;font-size:clamp(32px,5vw,44px);font-weight:700;letter-spacing:-1px;margin-bottom:16px}
.footer p{font-family:'Inter',sans-serif;font-size:17px;color:var(--muted);max-width:540px;margin:0 auto 32px}
.footer-btn{display:inline-block;padding:12px 28px;border-radius:6px;background:var(--text);color:#fff;font-family:'Inter',sans-serif;font-weight:600;font-size:14px;border:none}
.footer-btn:hover{background:#000}
.copy{margin-top:40px;font-family:'Inter',sans-serif;font-size:12px;color:var(--muted)}
@media(max-width:640px){.nav-links{display:none}.stats{gap:32px}.features-grid,.reviews-grid{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner"><a href="#" class="logo">Eko</a>
<ul class="nav-links"><li><a href="#benefits">Features</a></li><li><a href="#how">Setup</a></li><li><a href="#reviews">Stories</a></li><li><a href="#faq">FAQ</a></li><li><a href="#form" class="nav-cta">Get started</a></li></ul></div></nav>
<section class="hero" id="form"><div class="badge">📝 {{BADGE}}</div><h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button></form>
<div class="stats"><div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div></div></section>
<section class="section section-alt" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section" id="how"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section section-alt" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div></div></section>
<section class="section" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
<div class="copy">© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 7: TESLA BOLD — Full-bleed dark hero, minimal nav, huge CTA
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_TESLA_BOLD = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#000;--text:#fff;--muted:#a3a3a3;--accent:#fff;--surface:#171717;--cta:#3e6ae1}
html{scroll-behavior:smooth}body{font-family:'Gotham','Inter',-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.4;-webkit-font-smoothing:antialiased}
a{color:var(--text);text-decoration:none}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:16px 40px;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(180deg,rgba(0,0,0,.6),transparent)}
.logo{font-size:24px;font-weight:700;color:#fff;letter-spacing:-.5px;font-stretch:condensed}
.nav-links{display:flex;gap:32px;list-style:none}
.nav-links a{color:#fff;font-size:14px;font-weight:600;letter-spacing:.5px;text-transform:uppercase}
.nav-cta{padding:8px 20px;border:1px solid #fff;border-radius:0;background:rgba(0,0,0,.2);font-weight:600;font-size:13px}
.nav-cta:hover{background:#fff;color:#000!important}
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;justify-content:flex-end;padding:120px 40px 80px;background:radial-gradient(ellipse at 50% 60%,#1a1a1a 0%,#000 70%),linear-gradient(180deg,#0a0a0a 0%,#000 100%);overflow:hidden}
.hero::before{content:'';position:absolute;top:30%;left:50%;width:120vw;height:80vh;transform:translateX(-50%);background:radial-gradient(ellipse,rgba(255,255,255,.04) 0%,transparent 50%);pointer-events:none}
.hero-inner{position:relative;text-align:center;max-width:1080px;margin:0 auto;width:100%}
.badge{display:inline-block;padding:6px 14px;color:var(--muted);font-size:12px;font-weight:600;letter-spacing:2px;text-transform:uppercase;margin-bottom:24px}
h1{font-size:clamp(48px,9vw,96px);font-weight:600;line-height:1.02;letter-spacing:-3px;margin-bottom:20px;text-transform:uppercase;font-stretch:condensed}
.hero p.sub{font-size:clamp(15px,2vw,18px);color:var(--muted);max-width:600px;margin:0 auto 40px;line-height:1.5}
.cta-block{display:flex;flex-direction:column;gap:14px;max-width:520px;margin:0 auto}
.cta-form{display:flex;flex-wrap:wrap;gap:8px}
.cta-form input{flex:1 1 240px;padding:14px 18px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.05);color:#fff;font-size:14px;font-family:inherit;outline:none;border-radius:0}
.cta-form input:focus{border-color:#fff;background:rgba(255,255,255,.1)}.cta-form input::placeholder{color:#666}
.cta-form button{flex:1 1 100%;padding:14px 28px;border:none;background:var(--cta);color:#fff;font-size:14px;font-weight:700;cursor:pointer;letter-spacing:1.5px;text-transform:uppercase;border-radius:0}
.cta-form button:hover{background:#3457b8}
.scroll-indicator{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);color:var(--muted);font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6}
.section{padding:120px 40px;max-width:1280px;margin:0 auto;text-align:center}
.section-dark{background:var(--surface)}
.section-header h2{font-size:clamp(36px,6vw,64px);font-weight:600;letter-spacing:-2px;text-transform:uppercase;font-stretch:condensed;margin-bottom:16px;line-height:1.05}
.section-header p{color:var(--muted);font-size:16px;max-width:600px;margin:0 auto 64px}
.stats-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:0;background:#0a0a0a;border-top:1px solid rgba(255,255,255,.1);border-bottom:1px solid rgba(255,255,255,.1)}
.stat{padding:48px 24px;border-right:1px solid rgba(255,255,255,.1);text-align:center}
.stat:last-child{border-right:none}
.stat-num{font-size:48px;font-weight:600;letter-spacing:-1.5px;font-stretch:condensed}.stat-label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-top:8px}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.08)}
.feature{padding:48px 32px;background:#000;text-align:left;transition:background .2s}
.feature:hover{background:#0a0a0a}
.feature-icon{font-size:36px;margin-bottom:24px}
.feature h3{font-size:18px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}
.feature p{color:var(--muted);font-size:14px;line-height:1.6}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:48px;text-align:left}
.step-num{display:block;font-size:64px;font-weight:600;color:var(--muted);letter-spacing:-2px;margin-bottom:8px;font-stretch:condensed;line-height:1}
.step h3{font-size:20px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}.step p{color:var(--muted);font-size:14px}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;text-align:left}
.review{padding:32px;border:1px solid rgba(255,255,255,.1);background:#000}
.review-stars{color:#fff;font-size:14px;margin-bottom:16px;letter-spacing:3px}
.review-quote{font-size:17px;color:var(--text);margin-bottom:24px;line-height:1.5}
.review-author{display:flex;align-items:center;gap:12px;font-size:13px}
.review-name{font-weight:700;text-transform:uppercase;letter-spacing:.5px}.review-role{color:var(--muted)}
.faq{max-width:720px;margin:0 auto;text-align:left}
.faq-item{border-bottom:1px solid rgba(255,255,255,.1)}
.faq-q{width:100%;padding:24px 0;background:none;border:none;text-align:left;font-size:17px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:#fff}
.faq-q::after{content:'+';font-size:24px;color:var(--muted);transition:transform .3s;font-weight:300}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:14px;line-height:1.6}
.faq-item.active .faq-a{max-height:240px;padding:0 0 20px}
.footer{padding:160px 40px;text-align:center;background:radial-gradient(ellipse at 50% 50%,#171717 0%,#000 70%)}
.footer h2{font-size:clamp(40px,7vw,72px);font-weight:600;letter-spacing:-2px;text-transform:uppercase;font-stretch:condensed;margin-bottom:20px;line-height:1.05}
.footer p{font-size:17px;color:var(--muted);max-width:560px;margin:0 auto 40px}
.footer-btn{display:inline-block;padding:16px 48px;background:var(--cta);color:#fff;font-weight:700;font-size:14px;letter-spacing:1.5px;text-transform:uppercase}
.footer-btn:hover{background:#3457b8;color:#fff}
.copy{margin-top:64px;font-size:11px;color:#444;letter-spacing:1px;text-transform:uppercase}
@media(max-width:640px){.nav-links{display:none}.nav{padding:16px 20px}.section{padding:80px 20px}.features-grid{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><a href="#" class="logo">EKO AI</a>
<ul class="nav-links"><li><a href="#benefits">Features</a></li><li><a href="#how">How</a></li><li><a href="#reviews">Owners</a></li><li><a href="#faq">FAQ</a></li><li><a href="#form" class="nav-cta">Get Started</a></li></ul></nav>
<section class="hero" id="form"><div class="hero-inner">
<div class="badge">{{BADGE}}</div><h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="cta-block">
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button></form></div></div>
<div class="scroll-indicator">▼ Scroll to explore</div></section>
<div class="stats-strip">
<div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div></div>
<section class="section" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section section-dark" id="how"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><span class="step-num">01</span><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><span class="step-num">02</span><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><span class="step-num">03</span><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div><span class="review-name">{{REVIEW_1_NAME}}</span> · <span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div><span class="review-name">{{REVIEW_2_NAME}}</span> · <span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div></div></section>
<section class="section section-dark" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
<div class="copy">© {{YEAR}} EKO AI · contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""



# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 8: BEST BUY RETAIL — White bg, blue+yellow, deal cards, pricing emphasis
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_BESTBUY_RETAIL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--blue:#0046BE;--blue-dark:#003494;--yellow:#FFE000;--yellow-dark:#FFD200;--text:#1d252c;--muted:#5c6e7d;--bg:#fff;--surface:#f0f2f4;--border:#cdd5dd}
html{scroll-behavior:smooth}body{font-family:'Human BBY','Inter',-apple-system,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
.top-bar{background:var(--blue);color:#fff;padding:6px 24px;text-align:center;font-size:13px;font-weight:600}
.top-bar .deal{color:var(--yellow)}
.nav{background:var(--blue);padding:0 24px;height:64px;display:flex;align-items:center;gap:24px;border-bottom:4px solid var(--yellow)}
.logo{font-size:24px;font-weight:900;color:var(--yellow);letter-spacing:-.5px;display:flex;align-items:center;gap:6px}
.logo .tag{background:var(--yellow);color:var(--blue);padding:2px 8px;border-radius:3px;font-size:11px;font-weight:900;letter-spacing:.5px}
.nav-links{display:flex;gap:24px;list-style:none;margin-left:auto}
.nav-links a{color:#fff;font-size:14px;font-weight:600}.nav-links a:hover{text-decoration:underline}
.nav-cta{background:var(--yellow);color:var(--text)!important;padding:10px 18px;border-radius:4px;font-weight:700;font-size:14px}
.hero{padding:48px 24px;background:linear-gradient(180deg,#fff 0%,var(--surface) 100%);text-align:center}
.hero-inner{max-width:1280px;margin:0 auto}
.deal-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:4px;background:var(--yellow);color:var(--text);font-weight:700;font-size:13px;margin-bottom:20px;letter-spacing:.3px;text-transform:uppercase}
h1{font-size:clamp(36px,6vw,56px);font-weight:900;line-height:1.1;letter-spacing:-1.5px;margin-bottom:16px;color:var(--text)}
h1 .accent{color:var(--blue)}
.hero p.sub{font-size:18px;color:var(--muted);max-width:680px;margin:0 auto 28px;line-height:1.5}
.price-strip{display:inline-flex;align-items:baseline;gap:12px;margin-bottom:32px;background:#fff;padding:12px 20px;border-radius:6px;border:2px solid var(--yellow);box-shadow:0 4px 12px rgba(0,0,0,.06)}
.price-was{text-decoration:line-through;color:var(--muted);font-size:18px}
.price-now{color:#cc0000;font-size:32px;font-weight:900;letter-spacing:-.5px}
.price-tag{background:#cc0000;color:#fff;padding:4px 10px;border-radius:3px;font-size:12px;font-weight:700}
.hero-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px;max-width:720px;margin:0 auto 24px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.08)}
.hero-form input{padding:12px 14px;border:1px solid var(--border);border-radius:4px;font-size:14px;font-family:inherit;outline:none;background:#fff}
.hero-form input:focus{border-color:var(--blue);box-shadow:0 0 0 2px rgba(0,70,190,.15)}
.hero-form button{grid-column:1/-1;padding:14px 28px;border:none;border-radius:4px;background:var(--blue);color:#fff;font-size:15px;font-weight:700;cursor:pointer;letter-spacing:.3px;text-transform:uppercase}
.hero-form button:hover{background:var(--blue-dark)}
.stats-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:32px;max-width:980px;margin-left:auto;margin-right:auto}
.stat-tile{padding:24px;border-radius:6px;background:#fff;border-left:4px solid var(--yellow);text-align:left;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.stat-num{font-size:36px;font-weight:900;color:var(--blue);letter-spacing:-1px;line-height:1}
.stat-label{font-size:13px;color:var(--muted);margin-top:6px;text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.section{padding:80px 24px;max-width:1280px;margin:0 auto}
.section-alt{background:var(--surface)}
.section-header{margin-bottom:48px}
.section-header h2{font-size:clamp(28px,4vw,42px);font-weight:900;letter-spacing:-1px;margin-bottom:12px}
.section-header h2 .accent{color:var(--blue)}
.section-header p{color:var(--muted);font-size:17px;max-width:560px}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.feature{padding:24px;border:1px solid var(--border);border-radius:6px;background:#fff;border-top:4px solid var(--yellow);transition:transform .2s,box-shadow .2s}
.feature:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.08)}
.feature-icon{width:48px;height:48px;border-radius:6px;background:var(--yellow);color:var(--text);display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:14px}
.feature h3{font-size:18px;font-weight:700;margin-bottom:8px;color:var(--text)}
.feature p{color:var(--muted);font-size:14.5px}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.step{padding:28px;border-radius:6px;background:#fff;border:1px solid var(--border);position:relative;padding-top:48px}
.step-num{position:absolute;top:24px;left:24px;width:36px;height:36px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:16px}
.step h3{font-size:18px;font-weight:700;margin-bottom:8px}.step p{color:var(--muted);font-size:14.5px}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.review{padding:24px;border:1px solid var(--border);border-radius:6px;background:#fff}
.review-stars{color:#FFB300;font-size:16px;margin-bottom:10px}
.review-quote{font-size:15px;color:var(--text);margin-bottom:16px;line-height:1.55}
.review-author{display:flex;align-items:center;gap:10px}
.review-avatar{width:36px;height:36px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.review-name{font-weight:700;font-size:14px;display:block}.review-role{font-size:12px;color:var(--muted)}
.faq{max-width:840px;margin:0 auto}
.faq-item{border:1px solid var(--border);border-radius:6px;background:#fff;margin-bottom:8px;overflow:hidden}
.faq-q{width:100%;padding:18px 20px;background:none;border:none;text-align:left;font-size:16px;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text)}
.faq-q::after{content:'⌄';font-size:18px;color:var(--blue);transition:transform .3s}
.faq-item.active .faq-q::after{transform:rotate(180deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:14.5px;padding:0 20px;line-height:1.6}
.faq-item.active .faq-a{max-height:240px;padding:0 20px 16px}
.footer{padding:80px 24px;text-align:center;background:var(--blue);color:#fff}
.footer h2{font-size:clamp(28px,4vw,42px);font-weight:900;letter-spacing:-1px;margin-bottom:12px;color:#fff}
.footer h2 .accent{color:var(--yellow)}
.footer p{font-size:17px;opacity:.92;max-width:560px;margin:0 auto 28px;color:rgba(255,255,255,.95)}
.footer-btn{display:inline-block;padding:14px 32px;background:var(--yellow);color:var(--text);font-weight:900;font-size:15px;letter-spacing:.5px;text-transform:uppercase;border-radius:4px}
.footer-btn:hover{background:var(--yellow-dark)}
.copy{margin-top:40px;font-size:12px;opacity:.6}
@media(max-width:640px){.nav-links{display:none}.features-grid{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<div class="top-bar">⚡ Limited time: <span class="deal">Free AI Analysis</span> for your business — Get yours today</div>
<nav class="nav"><a href="#" class="logo">eko<span class="tag">AI</span></a>
<ul class="nav-links"><li><a href="#benefits">Features</a></li><li><a href="#how">Setup</a></li><li><a href="#reviews">Reviews</a></li><li><a href="#faq">FAQ</a></li><li><a href="#form" class="nav-cta">Get Free Analysis</a></li></ul></nav>
<section class="hero" id="form"><div class="hero-inner">
<div class="deal-badge">⚡ {{BADGE}}</div><h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="price-strip"><span class="price-was">$299</span><span class="price-now">FREE</span><span class="price-tag">SAVE 100%</span></div>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button></form>
<div class="stats-row">
<div class="stat-tile"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat-tile"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat-tile"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div></div></div></section>
<section class="section" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section section-alt" id="how"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div></div></section>
<section class="section section-alt" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
<div class="copy">© {{YEAR}} eko AI · contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 9: SPOTIFY VIBE — Pitch black bg, vibrant green accent, music-energy
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_SPOTIFY_VIBE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#000;--surface:#121212;--surface-2:#1a1a1a;--text:#fff;--muted:#b3b3b3;--green:#1DB954;--green-dark:#169c46}
html{scroll-behavior:smooth}body{font-family:'Circular','Inter',-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:var(--green);text-decoration:none}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(0,0,0,.85);backdrop-filter:blur(12px);padding:16px 32px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:24px;font-weight:900;color:var(--text);letter-spacing:-.5px;display:flex;align-items:center;gap:6px}
.logo .dot{width:10px;height:10px;border-radius:50%;background:var(--green);display:inline-block}
.nav-links{display:flex;gap:28px;list-style:none}
.nav-links a{color:var(--muted);font-size:14px;font-weight:700}.nav-links a:hover{color:#fff}
.nav-cta{padding:10px 24px;border-radius:50px;background:var(--green);color:#000!important;font-weight:700;font-size:14px}
.nav-cta:hover{background:#1ed760;transform:scale(1.04)}
.hero{padding:140px 32px 96px;background:radial-gradient(ellipse at top,rgba(29,185,84,.15) 0%,#000 60%);text-align:center;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40'%3E%3Ccircle cx='1' cy='1' r='1' fill='%23222'/%3E%3C/svg%3E");opacity:.4;pointer-events:none}
.hero-inner{position:relative;z-index:1;max-width:980px;margin:0 auto}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:50px;background:rgba(29,185,84,.15);border:1px solid rgba(29,185,84,.4);color:var(--green);font-size:13px;font-weight:700;margin-bottom:28px;letter-spacing:.3px}
h1{font-size:clamp(48px,8vw,88px);font-weight:900;line-height:1;letter-spacing:-3px;margin-bottom:24px}
h1 .green{color:var(--green)}
.hero p.sub{font-size:clamp(17px,2.5vw,22px);color:var(--muted);max-width:640px;margin:0 auto 40px;line-height:1.45}
.hero-form{display:flex;flex-wrap:wrap;gap:10px;max-width:560px;margin:0 auto;justify-content:center}
.hero-form input{flex:1 1 200px;padding:14px 18px;border:1px solid #2a2a2a;border-radius:50px;background:#1a1a1a;color:#fff;font-size:14px;font-family:inherit;outline:none;transition:all .2s}
.hero-form input:focus{border-color:var(--green);background:#222}.hero-form input::placeholder{color:#666}
.hero-form button{flex:0 0 auto;padding:14px 32px;border:none;border-radius:50px;background:var(--green);color:#000;font-size:15px;font-weight:900;cursor:pointer;letter-spacing:.5px;text-transform:uppercase;transition:all .2s}
.hero-form button:hover{background:#1ed760;transform:scale(1.04)}
.stats{display:flex;justify-content:center;gap:64px;margin-top:80px;flex-wrap:wrap}
.stat-num{font-size:56px;font-weight:900;color:var(--green);letter-spacing:-1.5px;line-height:1}
.stat-label{font-size:14px;color:var(--muted);margin-top:8px;text-transform:uppercase;letter-spacing:.5px;font-weight:700}
.section{padding:96px 32px;max-width:1280px;margin:0 auto}
.section-alt{background:var(--surface)}
.section-header{margin-bottom:56px;text-align:center}
.section-header h2{font-size:clamp(36px,5vw,56px);font-weight:900;letter-spacing:-2px;margin-bottom:14px;line-height:1.05}
.section-header p{color:var(--muted);font-size:18px;max-width:560px;margin:0 auto;font-weight:500}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature{padding:32px;border-radius:8px;background:var(--surface-2);transition:all .25s;cursor:pointer}
.feature:hover{background:#2a2a2a;transform:translateY(-4px)}
.feature-icon{display:inline-flex;width:48px;height:48px;border-radius:50%;background:rgba(29,185,84,.15);color:var(--green);align-items:center;justify-content:center;font-size:22px;margin-bottom:18px}
.feature h3{font-size:18px;font-weight:900;margin-bottom:8px;color:#fff;letter-spacing:-.3px}
.feature p{color:var(--muted);font-size:14.5px;line-height:1.55}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.step{padding:32px;border-radius:8px;background:var(--surface-2);position:relative}
.step-num{display:inline-block;font-size:14px;font-weight:900;color:var(--green);text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}
.step h3{font-size:20px;font-weight:900;margin-bottom:10px;letter-spacing:-.3px}.step p{color:var(--muted);font-size:14.5px}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}
.review{padding:32px;border-radius:8px;background:var(--surface-2)}
.review-stars{color:var(--green);font-size:14px;margin-bottom:14px;letter-spacing:2px}
.review-quote{font-size:17px;color:#fff;margin-bottom:24px;line-height:1.5;font-weight:500}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:48px;height:48px;border-radius:50%;background:var(--green);color:#000;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:15px}
.review-name{font-weight:900;font-size:15px;display:block}.review-role{font-size:13px;color:var(--muted)}
.faq{max-width:760px;margin:0 auto}
.faq-item{border-bottom:1px solid #1a1a1a}
.faq-q{width:100%;padding:24px 0;background:none;border:none;text-align:left;font-size:17px;font-weight:900;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:#fff;letter-spacing:-.3px}
.faq-q::after{content:'+';font-size:24px;color:var(--green);transition:transform .3s;font-weight:300}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:14.5px;line-height:1.6}
.faq-item.active .faq-a{max-height:240px;padding:0 0 20px}
.footer{padding:120px 32px;text-align:center;background:linear-gradient(180deg,#000 0%,#0a3a1f 100%);border-top:1px solid #1a1a1a}
.footer h2{font-size:clamp(36px,6vw,64px);font-weight:900;letter-spacing:-2px;margin-bottom:20px;line-height:1.05}
.footer p{font-size:18px;color:var(--muted);max-width:560px;margin:0 auto 40px}
.footer-btn{display:inline-block;padding:18px 40px;border-radius:50px;background:var(--green);color:#000;font-weight:900;font-size:16px;text-transform:uppercase;letter-spacing:1px}
.footer-btn:hover{background:#1ed760;transform:scale(1.04)}
.copy{margin-top:64px;font-size:12px;color:#444;font-weight:700}
@media(max-width:640px){.nav-links{display:none}.stats{gap:32px}.features-grid{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><a href="#" class="logo"><span class="dot"></span>EKO AI</a>
<ul class="nav-links"><li><a href="#benefits">Features</a></li><li><a href="#how">How</a></li><li><a href="#reviews">Reviews</a></li><li><a href="#faq">FAQ</a></li></ul>
<a href="#form" class="nav-cta">Get Started</a></nav>
<section class="hero" id="form"><div class="hero-inner">
<div class="badge">⚡ {{BADGE}}</div><h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
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
<section class="section section-alt" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section" id="how"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><span class="step-num">STEP 01</span><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><span class="step-num">STEP 02</span><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><span class="step-num">STEP 03</span><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section section-alt" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">●●●●●</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">●●●●●</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div></div></section>
<section class="section" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
<div class="copy">© {{YEAR}} EKO AI · contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 10: HUBSPOT SALES — Orange CTA, B2B SaaS feel, conversion-optimized
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_HUBSPOT_SALES = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--surface:#f5f8fa;--text:#33475b;--text-dark:#2d3e50;--muted:#7c98b6;--orange:#FF7A59;--orange-dark:#FF5C35;--blue:#516F90;--border:#cbd6e2}
html{scroll-behavior:smooth}body{font-family:'Lexend Deca','Inter','Avenir Next',-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--orange);text-decoration:none}a:hover{text-decoration:underline}
.nav{background:#fff;border-bottom:1px solid var(--border);padding:0 32px;height:72px;display:flex;align-items:center;justify-content:space-between;max-width:1280px;margin:0 auto}
.logo{font-size:22px;font-weight:700;color:var(--text-dark);letter-spacing:-.3px;display:flex;align-items:center;gap:8px}
.logo .arrow{width:24px;height:24px;border-radius:6px;background:var(--orange);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:900}
.nav-links{display:flex;gap:28px;list-style:none}
.nav-links a{color:var(--text);font-size:15px;font-weight:600}.nav-links a:hover{color:var(--orange);text-decoration:none}
.nav-cta{padding:10px 20px;border-radius:3px;background:var(--orange);color:#fff!important;font-weight:700;font-size:14px;border:none}
.nav-cta:hover{background:var(--orange-dark);text-decoration:none}
.hero{padding:80px 32px 96px;background:linear-gradient(180deg,#fff 0%,var(--surface) 100%);text-align:center;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:1400px;height:200px;background:radial-gradient(ellipse,rgba(255,122,89,.08),transparent 50%);pointer-events:none}
.hero-inner{position:relative;max-width:1080px;margin:0 auto}
.badge{display:inline-flex;align-items:center;gap:8px;padding:6px 16px;border-radius:20px;background:#fff;border:2px solid var(--orange);color:var(--orange);font-size:13px;font-weight:700;margin-bottom:28px}
h1{font-size:clamp(40px,6vw,64px);font-weight:700;line-height:1.1;letter-spacing:-1.5px;margin-bottom:24px;color:var(--text-dark)}
h1 .accent{color:var(--orange)}
.hero p.sub{font-size:clamp(17px,2.5vw,21px);color:var(--text);max-width:680px;margin:0 auto 36px;line-height:1.55}
.hero-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;max-width:680px;margin:0 auto;padding:24px;background:#fff;border-radius:8px;border:1px solid var(--border);box-shadow:0 10px 32px rgba(0,0,0,.06)}
.hero-form input{padding:13px 16px;border:1px solid var(--border);border-radius:3px;background:#fff;color:var(--text-dark);font-size:14.5px;font-family:inherit;outline:none}
.hero-form input:focus{border-color:var(--orange);box-shadow:0 0 0 3px rgba(255,122,89,.15)}
.hero-form button{grid-column:1/-1;padding:14px 28px;border:none;border-radius:3px;background:var(--orange);color:#fff;font-size:15px;font-weight:700;cursor:pointer;letter-spacing:.3px}
.hero-form button:hover{background:var(--orange-dark)}
.trust-bar{margin-top:32px;color:var(--muted);font-size:13px;font-weight:600}
.stats-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:48px;max-width:980px;margin-left:auto;margin-right:auto}
.stat{padding:24px;text-align:center}
.stat-num{font-size:44px;font-weight:700;color:var(--orange);letter-spacing:-1.5px;line-height:1}
.stat-label{font-size:14px;color:var(--text);margin-top:6px;font-weight:600}
.section{padding:96px 32px;max-width:1280px;margin:0 auto}
.section-alt{background:var(--surface)}
.section-header{text-align:center;margin-bottom:64px}
.section-header h2{font-size:clamp(32px,4.5vw,44px);font-weight:700;letter-spacing:-1.2px;margin-bottom:14px;color:var(--text-dark)}
.section-header p{color:var(--text);font-size:18px;max-width:600px;margin:0 auto}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature{padding:32px;border-radius:8px;background:#fff;border:1px solid var(--border);text-align:left;transition:all .2s}
.feature:hover{border-color:var(--orange);box-shadow:0 8px 24px rgba(0,0,0,.06)}
.feature-icon{width:48px;height:48px;border-radius:8px;background:rgba(255,122,89,.12);color:var(--orange);display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px}
.feature h3{font-size:18px;font-weight:700;margin-bottom:10px;color:var(--text-dark)}
.feature p{color:var(--text);font-size:14.5px;line-height:1.6}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:32px}
.step{padding:0;text-align:center}
.step-num{display:inline-flex;width:56px;height:56px;border-radius:50%;background:#fff;border:3px solid var(--orange);color:var(--orange);align-items:center;justify-content:center;font-weight:700;font-size:20px;margin-bottom:18px}
.step h3{font-size:19px;font-weight:700;margin-bottom:10px;color:var(--text-dark)}.step p{color:var(--text);font-size:15px}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{padding:32px;border-radius:8px;background:#fff;border:1px solid var(--border);position:relative}
.review::before{content:'"';position:absolute;top:8px;left:24px;font-size:80px;color:var(--orange);opacity:.15;font-family:Georgia,serif;line-height:1}
.review-stars{color:#FFB300;font-size:16px;margin-bottom:14px;position:relative}
.review-quote{font-size:16px;color:var(--text-dark);margin-bottom:24px;line-height:1.6;position:relative}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:44px;height:44px;border-radius:50%;background:var(--orange);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.review-name{font-weight:700;font-size:14.5px;display:block;color:var(--text-dark)}.review-role{font-size:13px;color:var(--muted)}
.faq{max-width:780px;margin:0 auto}
.faq-item{border:1px solid var(--border);border-radius:8px;background:#fff;margin-bottom:12px;overflow:hidden}
.faq-q{width:100%;padding:22px 24px;background:none;border:none;text-align:left;font-size:17px;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text-dark)}
.faq-q::after{content:'+';font-size:24px;color:var(--orange);transition:transform .3s;font-weight:300}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--text);font-size:15px;padding:0 24px;line-height:1.65}
.faq-item.active .faq-a{max-height:280px;padding:0 24px 20px}
.footer{padding:96px 32px;text-align:center;background:linear-gradient(135deg,#FF7A59 0%,#FF5C35 100%);color:#fff}
.footer h2{font-size:clamp(32px,5vw,48px);font-weight:700;letter-spacing:-1.2px;margin-bottom:16px}
.footer p{font-size:18px;max-width:600px;margin:0 auto 32px;opacity:.95}
.footer-btn{display:inline-block;padding:16px 36px;border-radius:3px;background:#fff;color:var(--orange-dark);font-weight:700;font-size:15px;letter-spacing:.3px}
.footer-btn:hover{background:var(--surface);color:var(--orange-dark)}
.copy{margin-top:48px;font-size:13px;opacity:.85}
@media(max-width:640px){.nav-links{display:none}.features-grid,.reviews-grid{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><a href="#" class="logo"><span class="arrow">▸</span>Eko AI</a>
<ul class="nav-links"><li><a href="#benefits">Software</a></li><li><a href="#how">How It Works</a></li><li><a href="#reviews">Customers</a></li><li><a href="#faq">Resources</a></li></ul>
<a href="#form" class="nav-cta">Get a Free Analysis</a></nav>
<section class="hero" id="form"><div class="hero-inner">
<div class="badge">⚡ {{BADGE}}</div><h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name*" required>
<input type="text" name="last_name" placeholder="Last Name*" required>
<input type="email" name="email" placeholder="Work Email*" required>
<input type="tel" name="phone" placeholder="Phone Number*" required>
<input type="url" name="website" placeholder="Website URL*" required>
<button type="submit">{{CTA_BUTTON}} →</button></form>
<div class="trust-bar">✓ No credit card required ✓ Cancel anytime ✓ Setup in 48 hours</div>
<div class="stats-row">
<div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div></div></div></section>
<section class="section section-alt" id="benefits"><div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div></div></section>
<section class="section" id="how"><div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div></section>
<section class="section section-alt" id="reviews"><div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div></div></section>
<section class="section" id="faq"><div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div></div></section>
<footer class="footer"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}} →</a>
<div class="copy">© {{YEAR}} Eko AI · contact@biz.ekoaiautomation.com</div></footer>
__FORM_SUBMIT_JS__
</body></html>"""



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

IMPORTANT: All copy MUST be written in English only.

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
