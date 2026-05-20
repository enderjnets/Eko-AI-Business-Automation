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
:root{--bg:#fff;--text:#1d1d1f;--muted:#86868b;--accent:#0066cc;--light:#f5f5f7;--hairline:#d2d2d7}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:'SF Pro Display','SF Pro Text',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.47059;-webkit-font-smoothing:antialiased;font-weight:400;letter-spacing:-.022em;min-height:100vh}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.nav{position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(255,255,255,.72);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid rgba(0,0,0,.06)}
.nav-inner{max-width:1024px;margin:0 auto;padding:0 22px;height:44px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:18px;font-weight:500;letter-spacing:-.022em;color:var(--text);display:flex;align-items:center;gap:6px}
.logo .mark{display:inline-block;width:14px;height:17px;background:var(--text);-webkit-mask:radial-gradient(circle at 70% 18%,transparent 3px,#000 3.5px) ,linear-gradient(#000,#000);mask:radial-gradient(circle at 70% 18%,transparent 3px,#000 3.5px),linear-gradient(#000,#000);border-radius:50% 50% 45% 45%/55% 55% 45% 45%;position:relative;top:-1px;opacity:.9}
.nav-links{display:flex;gap:0;list-style:none;flex:1;justify-content:center;margin:0 24px}
.nav-links li{padding:0 14px}
.nav-links a{color:var(--text);font-size:12px;font-weight:400;opacity:.88;letter-spacing:-.01em}.nav-links a:hover{opacity:1;text-decoration:none}
.nav-utility{display:flex;gap:14px;align-items:center}
.nav-utility a{font-size:12px;color:var(--text);opacity:.88}
.hero{padding:100px 22px 22px;text-align:center;background:var(--bg)}
.hero-badge{display:inline-block;font-size:17px;color:var(--accent);font-weight:400;margin-bottom:6px;letter-spacing:-.022em}
.hero h1{font-size:clamp(40px,5vw,80px);font-weight:600;line-height:1.05;letter-spacing:-.015em;margin:0 auto 8px;max-width:980px;color:var(--text)}
.hero h1 .accent{color:var(--accent);font-weight:600}
.hero .sub{font-size:clamp(19px,1.8vw,24px);font-weight:400;color:var(--text);max-width:760px;margin:0 auto 18px;line-height:1.21;letter-spacing:.009em}
.hero-cta-row{display:flex;justify-content:center;gap:18px;margin:18px auto 0;flex-wrap:wrap}
.btn-pill{display:inline-flex;align-items:center;padding:12px 22px;border-radius:980px;font-size:17px;line-height:1.17648;font-weight:400;letter-spacing:-.022em;transition:background .2s,opacity .2s;cursor:pointer;border:none;font-family:inherit;text-decoration:none}
.btn-primary{background:var(--accent);color:#fff}.btn-primary:hover{background:#0077ed;text-decoration:none;color:#fff}
.btn-link{color:var(--accent);background:transparent;padding:12px 0}.btn-link:hover{text-decoration:underline}
.btn-link::after{content:' \203A';font-size:18px}
.hero-stage{margin:50px auto 0;max-width:980px;height:380px;border-radius:18px;background:linear-gradient(160deg,#f5f5f7 0%,#e8eaed 35%,#d2dbe6 65%,#a8bcd4 100%);position:relative;overflow:hidden}
.hero-stage::before{content:'';position:absolute;inset:14% 18%;border-radius:14px;background:linear-gradient(180deg,#1d1d1f 0%,#3a3a3c 100%);box-shadow:inset 0 0 0 6px #2a2a2c,0 30px 60px -20px rgba(0,0,0,.35)}
.hero-stage::after{content:'';position:absolute;left:50%;bottom:8%;width:38%;height:6px;background:#2a2a2c;border-radius:0 0 6px 6px;transform:translateX(-50%)}
.cta-form{max-width:560px;margin:60px auto 0;display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.cta-form input{flex:1 1 220px;padding:13px 18px;border-radius:980px;border:1px solid var(--hairline);background:#fff;color:var(--text);font-size:15px;font-family:inherit;outline:none;transition:border-color .2s,box-shadow .2s}
.cta-form input:focus{border-color:var(--accent);box-shadow:0 0 0 4px rgba(0,102,204,.15)}
.cta-form button{padding:13px 28px;border-radius:980px;border:none;background:var(--accent);color:#fff;font-size:15px;font-weight:400;letter-spacing:-.022em;cursor:pointer;font-family:inherit;transition:background .2s}
.cta-form button:hover{background:#0077ed}
.stats{display:flex;justify-content:center;gap:88px;margin:80px auto 0;max-width:980px;padding:54px 22px;border-top:1px solid var(--hairline);border-bottom:1px solid var(--hairline);flex-wrap:wrap;text-align:center}
.stat-num{font-size:clamp(40px,5vw,64px);font-weight:600;letter-spacing:-.015em;color:var(--text);line-height:1}
.stat-label{font-size:14px;color:var(--muted);margin-top:8px;letter-spacing:-.016em}
.section{padding:120px 22px}
.section-inner{max-width:980px;margin:0 auto;text-align:center}
.section-alt{background:var(--light)}
.section-eyebrow{display:block;font-size:17px;color:var(--accent);font-weight:400;margin-bottom:12px;letter-spacing:-.022em}
.section-header h2{font-size:clamp(40px,5vw,72px);font-weight:600;letter-spacing:-.015em;line-height:1.06;margin-bottom:18px;color:var(--text)}
.section-header p{font-size:clamp(19px,2vw,24px);color:var(--text);max-width:680px;margin:0 auto 72px;line-height:1.21;letter-spacing:.009em;opacity:.92}
.features-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;text-align:left}
.feature{padding:48px 40px;background:var(--bg);border-radius:18px;min-height:260px;display:flex;flex-direction:column;justify-content:flex-end;position:relative;overflow:hidden}
.section-alt .feature{background:#fff}
.feature::before{content:'';position:absolute;top:32px;right:32px;width:64px;height:64px;border-radius:14px;background:linear-gradient(135deg,var(--accent),#5ac8fa);opacity:.92}
.feature-icon{font-size:32px;margin-bottom:16px;position:relative;z-index:2;display:none}
.feature h3{font-size:clamp(22px,2vw,28px);font-weight:600;letter-spacing:-.012em;margin-bottom:6px;color:var(--text);line-height:1.14}
.feature p{font-size:17px;color:var(--muted);letter-spacing:-.022em;line-height:1.47}
.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:64px;text-align:left;margin-top:24px}
.step{border-top:1px solid var(--hairline);padding-top:24px}
.step-num{font-size:14px;font-weight:600;color:var(--accent);letter-spacing:.04em;text-transform:uppercase;margin-bottom:14px;display:block}
.step h3{font-size:24px;font-weight:600;letter-spacing:-.012em;margin-bottom:8px;color:var(--text);line-height:1.16}
.step p{font-size:17px;color:var(--muted);letter-spacing:-.022em;line-height:1.47}
.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;text-align:left;margin-top:24px}
.review{padding:40px;border-radius:18px;background:#fff;border:1px solid var(--hairline)}
.section-alt .review{background:var(--bg)}
.review-stars{color:#f5a623;font-size:13px;margin-bottom:18px;letter-spacing:2px}
.review-quote{font-size:21px;line-height:1.33;letter-spacing:.011em;color:var(--text);margin-bottom:28px;font-weight:400}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#0066cc,#5ac8fa);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:16px;letter-spacing:.01em}
.review-name{font-size:15px;font-weight:600;display:block;color:var(--text)}.review-role{font-size:13px;color:var(--muted)}
.faq{max-width:820px;margin:32px auto 0;text-align:left}
.faq-item{border-bottom:1px solid var(--hairline)}
.faq-item:first-child{border-top:1px solid var(--hairline)}
.faq-q{width:100%;padding:28px 8px;background:none;border:none;text-align:left;font-size:19px;font-weight:600;letter-spacing:-.012em;color:var(--text);cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:24px;font-family:inherit;line-height:1.3}
.faq-q::after{content:'+';font-size:28px;color:var(--accent);font-weight:300;transition:transform .3s;flex-shrink:0}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;font-size:17px;color:var(--muted);line-height:1.5;padding:0 8px;letter-spacing:-.022em}
.faq-item.active .faq-a{max-height:300px;padding:0 8px 28px}
.footer{background:var(--light);padding:0 0 22px;color:var(--muted)}
.footer-cta-block{padding:120px 22px;text-align:center;background:var(--bg)}
.footer-cta-block h2{font-size:clamp(40px,5vw,64px);font-weight:600;letter-spacing:-.015em;margin-bottom:18px;color:var(--text);line-height:1.07}
.footer-cta-block p{font-size:clamp(19px,2vw,22px);color:var(--text);max-width:620px;margin:0 auto 32px;line-height:1.21;letter-spacing:.009em;opacity:.92}
.footer-btn-row{display:flex;justify-content:center;gap:18px;flex-wrap:wrap}
.footer-inner{max-width:980px;margin:0 auto;padding:32px 22px 0;font-size:12px;line-height:1.33337;letter-spacing:-.01em}
.footer-cols{display:grid;grid-template-columns:repeat(5,1fr);gap:42px;padding:24px 0;border-bottom:1px solid var(--hairline)}
.footer-col h4{font-size:12px;font-weight:600;color:var(--text);margin-bottom:10px}
.footer-col ul{list-style:none}
.footer-col li{padding:4px 0}
.footer-col a{font-size:12px;color:var(--muted);text-decoration:none}.footer-col a:hover{text-decoration:underline;color:var(--muted)}
.copy{padding:18px 0;font-size:12px;color:var(--muted)}
@media(max-width:834px){.nav-links{display:none}.features-grid,.steps-grid,.reviews-grid{grid-template-columns:1fr}.footer-cols{grid-template-columns:repeat(2,1fr);gap:24px}.stats{gap:36px}.section{padding:80px 22px}.hero-stage{height:240px}}
@media(max-width:480px){.cta-form input,.cta-form button{flex:1 1 100%}.footer-cols{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner">
<a href="#" class="logo" aria-label="Eko"><svg width="14" height="17" viewBox="0 0 14 17" fill="currentColor" aria-hidden="true"><path d="M11.6 9.07c-.02-2.06 1.68-3.05 1.76-3.1-.96-1.4-2.45-1.6-2.98-1.62-1.27-.13-2.48.74-3.13.74-.65 0-1.65-.72-2.71-.7-1.39.02-2.68.81-3.4 2.05-1.45 2.51-.37 6.21 1.04 8.25.69.99 1.51 2.11 2.58 2.07 1.04-.04 1.43-.67 2.69-.67 1.25 0 1.6.67 2.7.65 1.11-.02 1.82-1.01 2.5-2 .79-1.15 1.11-2.27 1.13-2.33-.02-.01-2.17-.83-2.19-3.31zM9.55 3.04c.57-.7.96-1.66.85-2.62-.83.03-1.84.55-2.43 1.24-.53.62-1 1.6-.87 2.54.93.07 1.88-.47 2.45-1.16z"/></svg>
Eko</a>
<ul class="nav-links">
<li><a href="#benefits">Overview</a></li>
<li><a href="#benefits">Features</a></li>
<li><a href="#how">How it works</a></li>
<li><a href="#reviews">Customers</a></li>
<li><a href="#faq">Support</a></li>
</ul>
<div class="nav-utility"><a href="#form">Buy</a></div>
</div></nav>

<section class="hero" id="form">
<div style="height:44px"></div>
<span class="hero-badge">{{BADGE}}</span>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="hero-cta-row">
<a href="#cta-form" class="btn-pill btn-primary">{{CTA_BUTTON}}</a>
<a href="#how" class="btn-pill btn-link">Learn more</a>
</div>
<div class="hero-stage" aria-hidden="true"></div>
<form id="cta-form" class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First Name" required>
<input type="text" name="last_name" placeholder="Last Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button>
</form>
<div class="stats">
<div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</section>

<section class="section section-alt" id="benefits"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">Features</span><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div></div></section>

<section class="section" id="how"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">How it works</span><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><span class="step-num">Step 01</span><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><span class="step-num">Step 02</span><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><span class="step-num">Step 03</span><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div></div></section>

<section class="section section-alt" id="reviews"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">Customer stories</span><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div>
</div></div></section>

<section class="section" id="faq"><div class="section-inner">
<div class="section-header"><span class="section-eyebrow">Help &amp; support</span><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div></div></section>

<footer class="footer">
<div class="footer-cta-block">
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<div class="footer-btn-row">
<a href="#form" class="btn-pill btn-primary">{{FOOTER_CTA}}</a>
<a href="#benefits" class="btn-pill btn-link">Learn more</a>
</div>
</div>
<div class="footer-inner">
<div class="footer-cols">
<div class="footer-col"><h4>Shop &amp; Learn</h4><ul><li><a href="#benefits">Features</a></li><li><a href="#how">How it works</a></li><li><a href="#reviews">Customers</a></li><li><a href="#faq">Support</a></li></ul></div>
<div class="footer-col"><h4>Services</h4><ul><li><a href="#form">Get started</a></li><li><a href="#form">Pricing</a></li><li><a href="#form">Demo</a></li></ul></div>
<div class="footer-col"><h4>Account</h4><ul><li><a href="#form">Manage</a></li><li><a href="#form">Sign in</a></li></ul></div>
<div class="footer-col"><h4>About Eko</h4><ul><li><a href="#">Newsroom</a></li><li><a href="#">Careers</a></li><li><a href="#">Contact</a></li></ul></div>
<div class="footer-col"><h4>For Business</h4><ul><li><a href="#">Enterprise</a></li><li><a href="#">Partners</a></li><li><a href="#">Education</a></li></ul></div>
</div>
<div class="copy">Copyright &copy; {{YEAR}} Eko AI Inc. All rights reserved. &nbsp;|&nbsp; <a href="#" style="color:var(--muted)">Privacy Policy</a> &nbsp;|&nbsp; <a href="#" style="color:var(--muted)">Terms of Use</a> &nbsp;|&nbsp; contact@biz.ekoaiautomation.com</div>
</div>
</footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 3: STRIPE GRADIENT — Gradient mesh hero, technical/clean, sophisticated
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_STRIPE_GRADIENT = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--text:#0a2540;--muted:#425466;--soft:#697386;--brand:#635bff;--brand2:#00d4ff;--mint:#a3f7bf;--pink:#ff80bf;--bg:#f6f9fc;--surface:#fff;--border:#e3e8ee}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:'Sohne','Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--muted);line-height:1.55;-webkit-font-smoothing:antialiased;min-height:100vh;font-feature-settings:'cv11','ss03'}
a{color:var(--brand);text-decoration:none}
img{max-width:100%;display:block}
.container{max-width:1080px;margin:0 auto;padding:0 24px}
/* NAV */
.nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.92);backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid rgba(10,37,64,.06)}
.nav-inner{max-width:1200px;margin:0 auto;padding:0 24px;height:72px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:22px;font-weight:700;color:var(--text);letter-spacing:-.6px;display:flex;align-items:center;gap:6px}
.logo-dot{width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,var(--brand),var(--brand2))}
.nav-links{display:flex;gap:28px;list-style:none;align-items:center}
.nav-links a{color:var(--text);font-size:15px;font-weight:500}
.nav-links a:hover{color:var(--brand)}
.nav-actions{display:flex;align-items:center;gap:18px}
.nav-signin{color:var(--text);font-size:15px;font-weight:500}
.nav-cta{padding:8px 16px;border-radius:999px;background:var(--text);color:#fff!important;font-size:14px;font-weight:600;transition:transform .15s}
.nav-cta:hover{transform:translateY(-1px)}
/* HERO — Stripe gradient mesh */
.hero{position:relative;padding:120px 24px 96px;overflow:hidden;background:linear-gradient(180deg,#f6f9fc 0%,#ffffff 100%)}
.mesh{position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:0}
.mesh span{position:absolute;border-radius:50%;filter:blur(90px);opacity:.55;mix-blend-mode:multiply;animation:drift 18s ease-in-out infinite alternate}
.mesh .m1{width:520px;height:520px;background:#635bff;top:-120px;left:-80px;animation-delay:0s}
.mesh .m2{width:480px;height:480px;background:#00d4ff;top:-60px;right:-120px;animation-delay:-4s}
.mesh .m3{width:420px;height:420px;background:#ff80bf;bottom:-160px;left:30%;animation-delay:-8s}
.mesh .m4{width:360px;height:360px;background:#a3f7bf;bottom:-100px;right:10%;animation-delay:-12s}
@keyframes drift{0%{transform:translate(0,0) scale(1)}100%{transform:translate(40px,30px) scale(1.1)}}
.hero-inner{max-width:980px;margin:0 auto;position:relative;z-index:1;text-align:center}
.badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:999px;background:#fff;border:1px solid rgba(99,91,255,.18);color:var(--brand);font-size:13px;font-weight:600;margin-bottom:28px;box-shadow:0 4px 16px rgba(99,91,255,.08)}
.badge::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--brand);box-shadow:0 0 0 4px rgba(99,91,255,.18)}
h1{font-size:clamp(44px,7vw,84px);font-weight:700;line-height:1.02;letter-spacing:-2.5px;color:var(--text);margin-bottom:22px}
h1 .gradient{background:linear-gradient(120deg,#635bff 0%,#8b5cf6 35%,#00d4ff 75%,#a3f7bf 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.hero p.sub{font-size:clamp(18px,2vw,21px);color:var(--muted);max-width:620px;margin:0 auto 36px;line-height:1.5}
.hero-form{display:flex;flex-wrap:wrap;gap:8px;max-width:600px;margin:0 auto;padding:8px;background:#fff;border-radius:16px;box-shadow:0 20px 60px rgba(10,37,64,.12),0 2px 6px rgba(10,37,64,.04);justify-content:center}
.hero-form input{flex:1 1 220px;padding:14px 16px;border:1px solid var(--border);border-radius:10px;font-size:15px;font-family:inherit;outline:none;background:#fafbfc;color:var(--text);transition:all .2s}
.hero-form input:focus{border-color:var(--brand);background:#fff;box-shadow:0 0 0 4px rgba(99,91,255,.12)}
.hero-form button{flex:0 0 auto;padding:14px 28px;border:none;border-radius:24px;background:linear-gradient(135deg,#635bff,#00d4ff);color:#fff;font-size:15px;font-weight:600;cursor:pointer;box-shadow:0 8px 24px rgba(99,91,255,.4);transition:transform .15s,box-shadow .2s}
.hero-form button:hover{transform:translateY(-1px);box-shadow:0 12px 28px rgba(99,91,255,.5)}
.stats{display:flex;justify-content:center;gap:64px;margin-top:72px;flex-wrap:wrap}
.stat-num{font-size:48px;font-weight:700;color:var(--text);letter-spacing:-1.5px;background:linear-gradient(135deg,#0a2540,#635bff);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.stat-label{font-size:14px;color:var(--soft);font-weight:500;margin-top:4px}
/* SECTIONS */
.section{padding:112px 24px}
.section-inner{max-width:1080px;margin:0 auto}
.section-alt{background:#fff}
.section-header{text-align:center;margin-bottom:64px}
.eyebrow{display:inline-block;font-size:13px;font-weight:600;color:var(--brand);text-transform:uppercase;letter-spacing:.8px;margin-bottom:12px}
.section-header h2{font-size:clamp(34px,4.5vw,52px);font-weight:700;letter-spacing:-1.8px;margin-bottom:16px;color:var(--text)}
.section-header p{color:var(--muted);font-size:19px;max-width:600px;margin:0 auto;line-height:1.5}
/* FEATURES */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature{padding:32px;border-radius:16px;background:#fff;border:1px solid var(--border);transition:transform .25s,box-shadow .25s;position:relative}
.feature:hover{transform:translateY(-4px);box-shadow:0 16px 40px rgba(10,37,64,.08)}
.feature-icon{display:inline-flex;width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px;box-shadow:0 8px 16px rgba(99,91,255,.25)}
.feature:nth-child(2) .feature-icon{background:linear-gradient(135deg,#00d4ff,#a3f7bf);box-shadow:0 8px 16px rgba(0,212,255,.25)}
.feature:nth-child(3) .feature-icon{background:linear-gradient(135deg,#ff80bf,#635bff);box-shadow:0 8px 16px rgba(255,128,191,.25)}
.feature:nth-child(4) .feature-icon{background:linear-gradient(135deg,#fbbf24,#ff80bf);box-shadow:0 8px 16px rgba(251,191,36,.25)}
.feature h3{font-size:18px;font-weight:600;margin-bottom:8px;color:var(--text);letter-spacing:-.3px}
.feature p{color:var(--muted);font-size:15px;line-height:1.55}
/* HOW IT WORKS w/ code preview */
.steps-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:48px;align-items:center}
.steps-list .step{padding:24px 0;border-bottom:1px solid var(--border);display:flex;gap:18px}
.steps-list .step:last-child{border-bottom:none}
.step-badge{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff;font-weight:700;font-size:15px}
.step-body h3{font-size:19px;font-weight:600;margin-bottom:6px;color:var(--text);letter-spacing:-.3px}
.step-body p{color:var(--muted);font-size:15px}
.code-preview{background:#0a2540;border-radius:14px;padding:20px 22px;font-family:'SF Mono','Menlo','Monaco',monospace;font-size:13.5px;line-height:1.75;box-shadow:0 24px 60px rgba(10,37,64,.25);position:relative;overflow:hidden}
.code-preview::before{content:'';position:absolute;inset:0;background:radial-gradient(circle at top right,rgba(99,91,255,.25),transparent 60%);pointer-events:none}
.code-dots{display:flex;gap:6px;margin-bottom:14px}
.code-dots span{width:11px;height:11px;border-radius:50%;background:rgba(255,255,255,.18)}
.code-line{color:#a3f7bf;white-space:pre;position:relative;z-index:1}
.cd-kw{color:#ff80bf}.cd-fn{color:#00d4ff}.cd-str{color:#fbbf24}.cd-co{color:#697386}.cd-pr{color:#fff}
/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{padding:32px;border-radius:16px;background:#fff;border:1px solid var(--border);transition:box-shadow .2s}
.review:hover{box-shadow:0 16px 40px rgba(10,37,64,.08)}
.review-stars{color:#ffb800;font-size:15px;margin-bottom:16px;letter-spacing:2px}
.review-quote{font-size:18px;color:var(--text);margin-bottom:24px;line-height:1.5;font-weight:500}
.review-author{display:flex;align-items:center;gap:12px}
.review-avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--brand),var(--mint));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.review-name{font-weight:600;font-size:15px;display:block;color:var(--text)}
.review-role{font-size:13px;color:var(--soft)}
/* FAQ */
.faq{max-width:760px;margin:0 auto}
.faq-item{border:1px solid var(--border);border-radius:12px;margin-bottom:12px;background:#fff;overflow:hidden;transition:box-shadow .2s}
.faq-item.active{box-shadow:0 8px 24px rgba(10,37,64,.06)}
.faq-q{width:100%;padding:22px 24px;background:none;border:none;text-align:left;font-size:16px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit}
.faq-q::after{content:'+';font-size:22px;color:var(--brand);transition:transform .3s;font-weight:400;line-height:1}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;padding:0 24px;line-height:1.6}
.faq-item.active .faq-a{max-height:280px;padding:0 24px 22px}
/* FOOTER — Stripe deep navy */
.footer{background:#0a2540;color:#fff;padding:96px 24px 32px}
.footer-cta{max-width:1080px;margin:0 auto 80px;text-align:center;padding-bottom:64px;border-bottom:1px solid rgba(255,255,255,.08)}
.footer-cta h2{font-size:clamp(34px,5vw,52px);font-weight:700;letter-spacing:-1.8px;margin-bottom:16px;color:#fff;background:linear-gradient(120deg,#fff,#a3f7bf 60%,#00d4ff);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.footer-cta p{font-size:18px;color:rgba(255,255,255,.7);max-width:560px;margin:0 auto 32px;line-height:1.5}
.footer-btn{display:inline-block;padding:14px 28px;border-radius:24px;background:linear-gradient(135deg,#635bff,#00d4ff);color:#fff;font-weight:600;font-size:15px;box-shadow:0 8px 24px rgba(99,91,255,.45);transition:transform .15s}
.footer-btn:hover{transform:translateY(-1px)}
.footer-cols{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:48px;padding-bottom:48px}
.footer-brand .logo{color:#fff;margin-bottom:12px}
.footer-brand p{color:rgba(255,255,255,.55);font-size:14px;max-width:280px;line-height:1.6}
.footer-col h4{font-size:13px;font-weight:600;color:#fff;text-transform:uppercase;letter-spacing:.6px;margin-bottom:18px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.footer-col a{color:rgba(255,255,255,.6);font-size:14px;transition:color .15s}
.footer-col a:hover{color:#fff}
.footer-copy{max-width:1080px;margin:0 auto;padding-top:24px;border-top:1px solid rgba(255,255,255,.08);font-size:13px;color:rgba(255,255,255,.5);text-align:center}
@media(max-width:880px){.steps-grid{grid-template-columns:1fr}.footer-cols{grid-template-columns:1fr 1fr;gap:32px}}
@media(max-width:640px){.nav-links,.nav-signin{display:none}.stats{gap:28px}.features-grid,.reviews-grid{grid-template-columns:1fr}.footer-cols{grid-template-columns:1fr}.section{padding:72px 24px}.hero{padding:72px 20px 72px}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner">
<a href="#" class="logo"><span class="logo-dot"></span>Eko</a>
<ul class="nav-links"><li><a href="#benefits">Products</a></li><li><a href="#how">Solutions</a></li><li><a href="#reviews">Customers</a></li><li><a href="#faq">Pricing</a></li><li><a href="#">Docs</a></li></ul>
<div class="nav-actions"><a href="#" class="nav-signin">Sign in</a><a href="#form" class="nav-cta">Contact sales &rsaquo;</a></div>
</div></nav>
<section class="hero" id="form">
<div class="mesh"><span class="m1"></span><span class="m2"></span><span class="m3"></span><span class="m4"></span></div>
<div class="hero-inner">
<div class="badge">{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Work email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Company website" required>
<button type="submit">{{CTA_BUTTON}} &rsaquo;</button>
</form>
<div class="stats">
<div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></div></section>
<section class="section section-alt" id="benefits"><div class="section-inner">
<div class="section-header"><span class="eyebrow">Platform</span><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div></div></section>
<section class="section" id="how"><div class="section-inner">
<div class="section-header"><span class="eyebrow">How it works</span><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="steps-list">
<div class="step"><div class="step-badge">1</div><div class="step-body"><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div></div>
<div class="step"><div class="step-badge">2</div><div class="step-body"><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div></div>
<div class="step"><div class="step-badge">3</div><div class="step-body"><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div></div>
</div>
<div class="code-preview" aria-hidden="true">
<div class="code-dots"><span></span><span></span><span></span></div>
<div class="code-line"><span class="cd-co">// Get started in minutes</span></div>
<div class="code-line"><span class="cd-kw">const</span> <span class="cd-pr">eko</span> = <span class="cd-kw">require</span>(<span class="cd-str">'eko'</span>);</div>
<div class="code-line"><span class="cd-kw">await</span> <span class="cd-pr">eko</span>.<span class="cd-fn">leads</span>.<span class="cd-fn">capture</span>({</div>
<div class="code-line">  <span class="cd-pr">email</span>: <span class="cd-str">'lead@acme.com'</span>,</div>
<div class="code-line">  <span class="cd-pr">source</span>: <span class="cd-str">'landing'</span>,</div>
<div class="code-line">  <span class="cd-pr">score</span>: <span class="cd-fn">auto</span>()</div>
<div class="code-line">});</div>
<div class="code-line"><span class="cd-co">// Webhook delivered &rarr; 99.99% uptime</span></div>
</div>
</div></div></section>
<section class="section section-alt" id="reviews"><div class="section-inner">
<div class="section-header"><span class="eyebrow">Customers</span><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</p><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</p><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div>
</div></div></section>
<section class="section" id="faq"><div class="section-inner">
<div class="section-header"><span class="eyebrow">FAQ</span><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div></div></section>
<footer class="footer">
<div class="footer-cta"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p><a href="#form" class="footer-btn">{{FOOTER_CTA}} &rsaquo;</a></div>
<div class="footer-cols">
<div class="footer-brand"><div class="logo" style="color:#fff"><span class="logo-dot"></span>Eko</div><p>Financial infrastructure for the modern internet business.</p></div>
<div class="footer-col"><h4>Products</h4><ul><li><a href="#">Payments</a></li><li><a href="#">Billing</a></li><li><a href="#">Connect</a></li><li><a href="#">Atlas</a></li></ul></div>
<div class="footer-col"><h4>Use cases</h4><ul><li><a href="#">SaaS</a></li><li><a href="#">Platforms</a></li><li><a href="#">Marketplaces</a></li><li><a href="#">Ecommerce</a></li></ul></div>
<div class="footer-col"><h4>Developers</h4><ul><li><a href="#">Docs</a></li><li><a href="#">API reference</a></li><li><a href="#">Status</a></li><li><a href="#">Changelog</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Customers</a></li><li><a href="#">Jobs</a></li><li><a href="#">Contact</a></li></ul></div>
</div>
<div class="footer-copy">&copy; {{YEAR}} Eko AI &middot; contact@biz.ekoaiautomation.com</div>
</footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 4: LINEAR DARK — Pure black bg, neon purple accents, sharp geometric
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_LINEAR_DARK = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#08080a;--surface:#0f0f12;--surface-2:#131318;--text:#fff;--muted:#a8a8b8;--soft:#71717a;--brand:#5e6ad2;--brand-glow:rgba(94,106,210,.4);--border:rgba(255,255,255,.06);--border-strong:rgba(255,255,255,.1);--divider:rgba(255,255,255,.08)}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:'Inter Display','Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--muted);line-height:1.6;-webkit-font-smoothing:antialiased;min-height:100vh;font-feature-settings:'cv11','ss01','ss03'}
a{color:var(--text);text-decoration:none}
img{max-width:100%;display:block}
.container{max-width:1200px;margin:0 auto;padding:0 32px}
/* NAV */
.nav{position:sticky;top:0;z-index:100;background:rgba(8,8,10,.72);backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid var(--divider)}
.nav-inner{max-width:1200px;margin:0 auto;padding:0 32px;height:64px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:17px;font-weight:600;color:var(--text);letter-spacing:-.4px;display:flex;align-items:center;gap:8px}
.logo-mark{width:22px;height:22px;border-radius:6px;background:linear-gradient(135deg,#5e6ad2,#8b5cf6);box-shadow:0 0 24px rgba(94,106,210,.4)}
.nav-links{display:flex;gap:28px;list-style:none;align-items:center}
.nav-links a{color:var(--muted);font-size:14px;font-weight:500;transition:color .15s}
.nav-links a:hover{color:var(--text)}
.nav-actions{display:flex;align-items:center;gap:12px}
.nav-signin{color:var(--muted);font-size:14px;font-weight:500;padding:8px 12px}
.nav-signin:hover{color:var(--text)}
.nav-cta{padding:7px 14px;border-radius:6px;background:#fff;color:#08080a!important;font-size:14px;font-weight:500;transition:opacity .15s}
.nav-cta:hover{opacity:.9}
/* HERO — Linear grid + purple glow */
.hero{position:relative;padding:140px 32px 120px;overflow:hidden;background:var(--bg);background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:64px 64px;background-position:center}
.hero::before{content:'';position:absolute;top:-200px;left:50%;transform:translateX(-50%);width:1000px;height:600px;background:radial-gradient(ellipse at center,rgba(94,106,210,.35) 0%,rgba(94,106,210,.15) 30%,transparent 65%);filter:blur(60px);pointer-events:none;z-index:0}
.hero::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 30%,var(--bg) 80%);pointer-events:none;z-index:0}
.hero-inner{max-width:980px;margin:0 auto;position:relative;z-index:1;text-align:center}
.badge{display:inline-flex;align-items:center;gap:8px;padding:5px 12px 5px 5px;border-radius:999px;background:rgba(255,255,255,.04);border:1px solid var(--border-strong);color:var(--muted);font-size:13px;font-weight:500;margin-bottom:32px;transition:border-color .2s}
.badge:hover{border-color:rgba(94,106,210,.4)}
.badge-pill{padding:2px 8px;border-radius:999px;background:var(--brand);color:#fff;font-size:11px;font-weight:600;letter-spacing:.2px}
h1{font-size:clamp(40px,5vw,72px);font-weight:600;line-height:1.05;letter-spacing:-2px;color:var(--text);margin-bottom:24px;font-feature-settings:'ss01'}
.hero p.sub{font-size:clamp(17px,1.6vw,20px);color:var(--muted);max-width:560px;margin:0 auto 40px;line-height:1.5;font-weight:400}
.hero-form{display:flex;flex-wrap:wrap;gap:8px;max-width:600px;margin:0 auto;padding:6px;background:rgba(255,255,255,.03);border:1px solid var(--border-strong);border-radius:8px;justify-content:center;backdrop-filter:blur(12px)}
.hero-form input{flex:1 1 200px;padding:11px 14px;border:1px solid transparent;border-radius:6px;font-size:14px;font-family:inherit;outline:none;background:rgba(255,255,255,.04);color:var(--text);transition:all .15s}
.hero-form input::placeholder{color:var(--soft)}
.hero-form input:focus{border-color:var(--brand);background:rgba(94,106,210,.08)}
.hero-form button{flex:0 0 auto;padding:11px 22px;border:none;border-radius:6px;background:#fff;color:#08080a;font-size:14px;font-weight:500;cursor:pointer;transition:opacity .15s}
.hero-form button:hover{opacity:.9}
.stats{display:flex;justify-content:center;gap:80px;margin-top:96px;flex-wrap:wrap;padding-top:64px;border-top:1px solid var(--divider)}
.stat-num{font-size:48px;font-weight:600;color:var(--text);letter-spacing:-1.8px}
.stat-label{font-size:13px;color:var(--soft);font-weight:500;margin-top:6px;text-transform:uppercase;letter-spacing:.4px}
/* SECTIONS */
.section{padding:128px 32px;position:relative}
.section-inner{max-width:1200px;margin:0 auto}
.section + .section{border-top:1px solid var(--divider)}
.section-header{text-align:center;margin-bottom:80px;max-width:680px;margin-left:auto;margin-right:auto}
.eyebrow{display:inline-block;font-size:13px;font-weight:500;color:var(--brand);margin-bottom:16px;letter-spacing:.2px}
.section-header h2{font-size:clamp(32px,4vw,56px);font-weight:600;letter-spacing:-1.5px;margin-bottom:16px;color:var(--text);line-height:1.1}
.section-header p{color:var(--muted);font-size:18px;line-height:1.55}
/* FEATURES */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1px;background:var(--border);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.feature{padding:36px 32px;background:var(--surface);transition:background .25s;position:relative}
.feature:hover{background:var(--surface-2)}
.feature-icon{display:inline-flex;width:36px;height:36px;border-radius:8px;background:rgba(94,106,210,.12);color:var(--brand);align-items:center;justify-content:center;font-size:18px;margin-bottom:20px;border:1px solid rgba(94,106,210,.2)}
.feature h3{font-size:16px;font-weight:600;margin-bottom:8px;color:var(--text);letter-spacing:-.2px}
.feature p{color:var(--muted);font-size:14.5px;line-height:1.6}
/* STEPS */
.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.step{padding:32px;background:var(--surface);border:1px solid var(--border);border-radius:12px;transition:border-color .2s,transform .2s}
.step:hover{border-color:rgba(94,106,210,.4);transform:translateY(-2px)}
.step-badge{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:6px;background:rgba(94,106,210,.12);color:var(--brand);font-weight:600;font-size:13px;margin-bottom:20px;border:1px solid rgba(94,106,210,.2);font-family:'SF Mono','Menlo',monospace}
.step h3{font-size:17px;font-weight:600;margin-bottom:8px;color:var(--text);letter-spacing:-.3px}
.step p{color:var(--muted);font-size:14.5px;line-height:1.55}
/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{padding:32px;border-radius:12px;background:var(--surface);border:1px solid var(--border);transition:border-color .2s}
.review:hover{border-color:rgba(94,106,210,.4)}
.review-stars{color:var(--brand);font-size:13px;margin-bottom:16px;letter-spacing:3px}
.review-quote{font-size:17px;color:var(--text);margin-bottom:24px;line-height:1.55;font-weight:400}
.review-author{display:flex;align-items:center;gap:12px;padding-top:20px;border-top:1px solid var(--divider)}
.review-avatar{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#5e6ad2,#8b5cf6);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:13px}
.review-name{font-weight:500;font-size:14px;display:block;color:var(--text)}
.review-role{font-size:13px;color:var(--soft)}
/* FAQ */
.faq{max-width:760px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--divider);background:transparent;overflow:hidden}
.faq-q{width:100%;padding:24px 0;background:none;border:none;text-align:left;font-size:16px;font-weight:500;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit;letter-spacing:-.2px}
.faq-q::after{content:'+';font-size:22px;color:var(--muted);transition:transform .3s,color .15s;font-weight:300;line-height:1}
.faq-item.active .faq-q::after{transform:rotate(45deg);color:var(--brand)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;line-height:1.6}
.faq-item.active .faq-a{max-height:280px;padding:0 0 24px}
/* FOOTER */
.footer{background:var(--bg);color:var(--muted);padding:96px 32px 32px;border-top:1px solid var(--divider);position:relative;overflow:hidden}
.footer::before{content:'';position:absolute;top:-100px;left:50%;transform:translateX(-50%);width:800px;height:300px;background:radial-gradient(ellipse at center,rgba(94,106,210,.15),transparent 70%);filter:blur(60px);pointer-events:none}
.footer-cta{max-width:1200px;margin:0 auto 80px;text-align:center;padding-bottom:80px;border-bottom:1px solid var(--divider);position:relative;z-index:1}
.footer-cta h2{font-size:clamp(36px,5vw,64px);font-weight:600;letter-spacing:-2px;margin-bottom:16px;color:var(--text);line-height:1.05}
.footer-cta p{font-size:18px;color:var(--muted);max-width:520px;margin:0 auto 36px;line-height:1.5}
.footer-btn{display:inline-block;padding:11px 22px;border-radius:6px;background:#fff;color:#08080a;font-weight:500;font-size:14px;transition:opacity .15s}
.footer-btn:hover{opacity:.9}
.footer-cols{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:48px;padding-bottom:48px;position:relative;z-index:1}
.footer-brand .logo{color:var(--text);margin-bottom:14px}
.footer-brand p{color:var(--soft);font-size:13.5px;max-width:280px;line-height:1.6}
.footer-col h4{font-size:13px;font-weight:600;color:var(--text);margin-bottom:16px;letter-spacing:-.1px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:10px}
.footer-col a{color:var(--soft);font-size:13.5px;transition:color .15s}
.footer-col a:hover{color:var(--brand)}
.footer-copy{max-width:1200px;margin:0 auto;padding-top:32px;border-top:1px solid var(--divider);font-size:13px;color:var(--soft);text-align:center;position:relative;z-index:1}
@media(max-width:880px){.steps-grid{grid-template-columns:1fr}.footer-cols{grid-template-columns:1fr 1fr;gap:32px}}
@media(max-width:640px){.nav-links,.nav-signin{display:none}.stats{gap:32px;margin-top:64px;padding-top:48px}.features-grid,.reviews-grid{grid-template-columns:1fr}.footer-cols{grid-template-columns:1fr}.section{padding:80px 24px}.hero{padding:96px 24px 80px}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner">
<a href="#" class="logo"><span class="logo-mark"></span>Eko</a>
<ul class="nav-links"><li><a href="#benefits">Features</a></li><li><a href="#how">Method</a></li><li><a href="#reviews">Customers</a></li><li><a href="#faq">Pricing</a></li><li><a href="#">Changelog</a></li><li><a href="#">Docs</a></li></ul>
<div class="nav-actions"><a href="#" class="nav-signin">Log in</a><a href="#form" class="nav-cta">Sign up</a></div>
</div></nav>
<section class="hero" id="form">
<div class="hero-inner">
<a href="#" class="badge"><span class="badge-pill">NEW</span>{{BADGE}} &rarr;</a>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Work email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Company URL" required>
<button type="submit">{{CTA_BUTTON}}</button>
</form>
<div class="stats">
<div><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></div></section>
<section class="section" id="benefits"><div class="section-inner">
<div class="section-header"><span class="eyebrow">Features</span><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div></div></section>
<section class="section" id="how"><div class="section-inner">
<div class="section-header"><span class="eyebrow">Method</span><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-badge">01</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-badge">02</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-badge">03</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div></div></section>
<section class="section" id="reviews"><div class="section-inner">
<div class="section-header"><span class="eyebrow">Customers</span><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</p><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</p><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div>
</div></div></section>
<section class="section" id="faq"><div class="section-inner">
<div class="section-header"><span class="eyebrow">FAQ</span><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
</div></div></section>
<footer class="footer">
<div class="footer-cta"><h2>{{FOOTER_HEADLINE}}</h2><p>{{FOOTER_SUBHEADLINE}}</p><a href="#form" class="footer-btn">{{FOOTER_CTA}}</a></div>
<div class="footer-cols">
<div class="footer-brand"><div class="logo"><span class="logo-mark"></span>Eko</div><p>Built for the modern workflow. Crafted with precision.</p></div>
<div class="footer-col"><h4>Product</h4><ul><li><a href="#">Features</a></li><li><a href="#">Integrations</a></li><li><a href="#">Pricing</a></li><li><a href="#">Changelog</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#">Documentation</a></li><li><a href="#">API</a></li><li><a href="#">Community</a></li><li><a href="#">Status</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Customers</a></li><li><a href="#">Careers</a></li><li><a href="#">Brand</a></li></ul></div>
<div class="footer-col"><h4>Legal</h4><ul><li><a href="#">Privacy</a></li><li><a href="#">Terms</a></li><li><a href="#">Security</a></li><li><a href="#">DPA</a></li></ul></div>
</div>
<div class="footer-copy">&copy; {{YEAR}} Eko AI &middot; contact@biz.ekoaiautomation.com</div>
</footer>
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
:root{--coral:#FF385C;--coral-hover:#E31C5F;--coral-2:#FF5A5F;--text:#222222;--muted:#717171;--bg:#fff;--surface:#f7f7f7;--border:#ebebeb;--star:#FF385C}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:"Cereal","Inter","Circular",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh}
a{color:var(--text);text-decoration:none}
.nav{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid var(--border)}
.nav-inner{max-width:1760px;margin:0 auto;padding:14px 40px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.logo{display:flex;align-items:center;gap:6px;font-size:22px;font-weight:800;color:var(--coral);letter-spacing:-.5px;flex-shrink:0}
.logo-mark{width:32px;height:32px;border-radius:50%;background:var(--coral);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:18px}
.nav-search{flex:1;max-width:560px;display:flex;align-items:center;border:1px solid var(--border);border-radius:40px;padding:8px 8px 8px 24px;box-shadow:0 1px 2px rgba(0,0,0,.08);cursor:pointer;transition:box-shadow .2s}
.nav-search:hover{box-shadow:0 2px 8px rgba(0,0,0,.12)}
.nav-search .pill{font-size:14px;font-weight:600;color:var(--text);padding-right:14px;border-right:1px solid var(--border)}
.nav-search .pill:last-of-type{border-right:none;color:var(--muted);font-weight:500}
.nav-search .pill+.pill{padding-left:14px}
.nav-search .search-btn{margin-left:auto;width:32px;height:32px;border-radius:50%;background:var(--coral);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;border:none;cursor:pointer}
.nav-right{display:flex;align-items:center;gap:6px;flex-shrink:0}
.nav-right a{padding:12px 14px;border-radius:24px;font-size:14px;font-weight:600;color:var(--text)}
.nav-right a:hover{background:var(--surface)}
.nav-profile{display:flex;align-items:center;gap:10px;padding:6px 6px 6px 14px;border:1px solid var(--border);border-radius:24px;cursor:pointer;transition:box-shadow .2s}
.nav-profile:hover{box-shadow:0 2px 6px rgba(0,0,0,.1)}
.nav-profile .lines{display:flex;flex-direction:column;gap:3px}
.nav-profile .lines span{width:14px;height:2px;background:var(--text);border-radius:2px}
.nav-profile .avatar{width:30px;height:30px;border-radius:50%;background:var(--text);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px}
.cat-strip{border-bottom:1px solid var(--border);background:#fff;overflow-x:auto;-webkit-overflow-scrolling:touch}
.cat-inner{max-width:1760px;margin:0 auto;padding:14px 40px;display:flex;gap:32px;align-items:center}
.cat{display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--muted);font-size:12px;font-weight:600;cursor:pointer;padding-bottom:14px;border-bottom:2px solid transparent;flex-shrink:0;transition:color .2s,border-color .2s}
.cat:hover,.cat.active{color:var(--text);border-bottom-color:var(--text)}
.cat-icon{font-size:24px;line-height:1}
.hero{padding:56px 40px 32px;text-align:center}
.hero-inner{max-width:920px;margin:0 auto}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:24px;background:#fff;border:1px solid var(--border);color:var(--text);font-size:13px;font-weight:600;margin-bottom:24px;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.badge::before{content:'★';color:var(--coral)}
h1{font-size:clamp(36px,5vw,58px);font-weight:700;line-height:1.1;letter-spacing:-1.2px;margin-bottom:20px;color:var(--text)}
.hero p.sub{font-size:clamp(16px,2vw,20px);color:var(--muted);max-width:640px;margin:0 auto 36px;line-height:1.45}
.booking-card{max-width:760px;margin:0 auto;background:#fff;border-radius:32px;border:1px solid var(--border);box-shadow:0 8px 28px rgba(0,0,0,.08);overflow:hidden}
.booking-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:0}
.booking-cell{padding:14px 24px;border-right:1px solid var(--border);border-bottom:1px solid var(--border);text-align:left;position:relative;transition:background .2s}
.booking-cell:hover{background:#f7f7f7}
.booking-cell:last-child{border-right:none}
.booking-cell label{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text);margin-bottom:4px}
.booking-cell input{width:100%;border:none;outline:none;background:transparent;font-size:14px;font-family:inherit;color:var(--text)}
.booking-cell input::placeholder{color:var(--muted)}
.booking-submit{padding:18px}
.booking-submit button{width:100%;padding:16px 28px;border:none;border-radius:24px;background:linear-gradient(135deg,#FF385C 0%,#E61E4D 50%,#BD1E59 100%);color:#fff;font-size:16px;font-weight:700;cursor:pointer;letter-spacing:.2px;display:flex;align-items:center;justify-content:center;gap:10px;transition:transform .15s}
.booking-submit button:hover{transform:translateY(-1px)}
.booking-submit button::before{content:'🔍';font-size:18px}
.trust-row{display:flex;justify-content:center;gap:48px;margin-top:48px;flex-wrap:wrap}
.trust{display:flex;align-items:center;gap:10px;color:var(--muted);font-size:14px}
.trust-icon{font-size:20px}
.stats{display:flex;justify-content:center;gap:64px;margin-top:48px;flex-wrap:wrap}
.stat{text-align:center}
.stat-num{font-size:clamp(36px,4vw,48px);font-weight:800;color:var(--coral);letter-spacing:-1.2px;line-height:1}
.stat-label{font-size:14px;color:var(--muted);margin-top:8px;font-weight:500}
.section{padding:80px 40px;max-width:1280px;margin:0 auto}
.section-alt{background:var(--surface);max-width:none}
.section-alt-inner{max-width:1280px;margin:0 auto}
.section-header{margin-bottom:48px}
.section-header h2{font-size:clamp(28px,3.5vw,40px);font-weight:700;letter-spacing:-.8px;margin-bottom:12px;color:var(--text)}
.section-header p{color:var(--muted);font-size:17px;max-width:640px;line-height:1.5}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature{padding:32px;border-radius:24px;background:#fff;border:1px solid var(--border);transition:transform .2s,box-shadow .2s}
.feature:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(0,0,0,.1)}
.feature-icon{width:56px;height:56px;border-radius:50%;background:rgba(255,56,92,.1);color:var(--coral);display:flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:18px}
.feature h3{font-size:18px;font-weight:700;margin-bottom:8px;color:var(--text);letter-spacing:-.3px}
.feature p{color:var(--muted);font-size:15px;line-height:1.55}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:48px}
.step{text-align:center;padding:24px 16px}
.step-circle{width:100px;height:100px;border-radius:50%;background:linear-gradient(135deg,#FF385C 0%,#E61E4D 100%);color:#fff;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:800;margin:0 auto 24px;box-shadow:0 8px 24px rgba(255,56,92,.25)}
.step h3{font-size:20px;font-weight:700;margin-bottom:10px;color:var(--text);letter-spacing:-.3px}
.step p{color:var(--muted);font-size:15px;line-height:1.55}
.reviews-header-row{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:32px}
.reviews-rating{display:flex;align-items:center;gap:12px;font-size:22px;font-weight:700;color:var(--text)}
.reviews-rating .star{color:var(--coral);font-size:22px}
.reviews-rating .dot{color:var(--muted);font-size:14px;font-weight:500}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{padding:28px;border-radius:24px;background:#fff;border:1px solid var(--border);transition:box-shadow .2s}
.review:hover{box-shadow:0 8px 24px rgba(0,0,0,.06)}
.review-stars{color:var(--coral);font-size:14px;margin-bottom:14px;letter-spacing:2px}
.review-quote{font-size:16px;color:var(--text);margin-bottom:24px;line-height:1.55;font-weight:400}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,var(--coral),#BD1E59);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px}
.review-name{font-weight:700;font-size:15px;display:block;color:var(--text)}
.review-role{font-size:13px;color:var(--muted)}
.faq{max-width:780px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--border)}
.faq-item:first-child{border-top:1px solid var(--border)}
.faq-q{width:100%;padding:24px 0;background:none;border:none;text-align:left;font-size:18px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit;letter-spacing:-.2px;transition:color .2s}
.faq-q:hover{color:var(--coral)}
.faq-q::after{content:'⌄';font-size:22px;color:var(--text);transition:transform .3s;margin-left:16px;line-height:.5}
.faq-item.active .faq-q::after{transform:rotate(180deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;line-height:1.6}
.faq-item.active .faq-a{max-height:320px;padding:0 0 24px}
.footer-cta{padding:96px 40px;background:linear-gradient(135deg,#FF385C 0%,#E61E4D 50%,#BD1E59 100%);text-align:center;color:#fff}
.footer-cta-inner{max-width:780px;margin:0 auto}
.footer-cta h2{font-size:clamp(32px,4vw,48px);font-weight:700;letter-spacing:-1px;margin-bottom:16px;color:#fff}
.footer-cta p{font-size:18px;color:rgba(255,255,255,.95);margin-bottom:32px;max-width:560px;margin-left:auto;margin-right:auto}
.cta-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;max-width:680px;margin:0 auto;background:#fff;padding:14px;border-radius:32px;box-shadow:0 12px 40px rgba(0,0,0,.18)}
.cta-form input{padding:14px 18px;border:1px solid var(--border);border-radius:24px;font-size:14px;font-family:inherit;outline:none;background:#fff;color:var(--text)}
.cta-form input:focus{border-color:var(--coral)}
.cta-form button{grid-column:1/-1;padding:16px 28px;border:none;border-radius:24px;background:linear-gradient(135deg,#FF385C 0%,#BD1E59 100%);color:#fff;font-size:15px;font-weight:700;cursor:pointer;letter-spacing:.2px}
.cta-form button:hover{filter:brightness(.95)}
.footer{padding:48px 40px 24px;background:var(--surface);color:var(--text);border-top:1px solid var(--border)}
.footer-cols{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;padding-bottom:32px;border-bottom:1px solid var(--border)}
.footer-col h4{font-size:14px;font-weight:700;margin-bottom:16px;color:var(--text)}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:10px}
.footer-col a{font-size:14px;color:var(--text);font-weight:400}
.footer-col a:hover{text-decoration:underline}
.footer-bottom{max-width:1280px;margin:0 auto;padding-top:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;font-size:14px;color:var(--text)}
.footer-bottom-links{display:flex;gap:16px;flex-wrap:wrap}
.footer-bottom-links span{display:flex;align-items:center;gap:6px;font-weight:600}
@media(max-width:900px){.nav-search{display:none}}
@media(max-width:640px){.nav-inner{padding:12px 20px;gap:10px}.cat-inner{gap:20px;padding:12px 20px}.nav-right a{display:none}.section,.footer-cta,.footer{padding-left:20px;padding-right:20px}.section{padding-top:56px;padding-bottom:56px}.features-grid,.reviews-grid,.steps-grid{grid-template-columns:1fr}.booking-cell{border-right:none}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner">
<a href="#" class="logo"><span class="logo-mark">e</span> eko</a>
<div class="nav-search" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">
<div class="pill">Anywhere</div><div class="pill">Any week</div><div class="pill">Add guests</div>
<button class="search-btn" type="button" aria-label="Search">🔍</button>
</div>
<div class="nav-right">
<a href="#form">Become a Host</a>
<a href="#" aria-label="Language">🌐</a>
<div class="nav-profile"><div class="lines"><span></span><span></span><span></span></div><div class="avatar">E</div></div>
</div>
</div></nav>
<div class="cat-strip"><div class="cat-inner">
<div class="cat active"><span class="cat-icon">🏠</span>Featured</div>
<div class="cat"><span class="cat-icon">🏖️</span>Beachfront</div>
<div class="cat"><span class="cat-icon">🏔️</span>Mountain</div>
<div class="cat"><span class="cat-icon">🌆</span>City</div>
<div class="cat"><span class="cat-icon">🏕️</span>Cabins</div>
<div class="cat"><span class="cat-icon">🏛️</span>Mansions</div>
<div class="cat"><span class="cat-icon">🌊</span>Lakefront</div>
<div class="cat"><span class="cat-icon">🌋</span>Trending</div>
<div class="cat"><span class="cat-icon">🏝️</span>Islands</div>
<div class="cat"><span class="cat-icon">⛷️</span>Skiing</div>
</div></div>
<section class="hero"><div class="hero-inner">
<div class="badge">{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="booking-card">
<div class="booking-form">
<div class="booking-cell"><label>Where</label><input type="text" placeholder="Search destinations" readonly></div>
<div class="booking-cell"><label>Check in</label><input type="text" placeholder="Add dates" readonly></div>
<div class="booking-cell"><label>Check out</label><input type="text" placeholder="Add dates" readonly></div>
<div class="booking-cell"><label>Who</label><input type="text" placeholder="Add guests" readonly></div>
</div>
<div class="booking-submit"><button type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">{{CTA_BUTTON}}</button></div>
</div>
<div class="stats">
<div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</div></section>
<section class="section" id="benefits">
<div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div>
</section>
<section class="section-alt"><div class="section-alt-inner section" style="background:transparent;padding-left:40px;padding-right:40px" id="how">
<div class="section-header" style="text-align:center"><h2>{{HOW_HEADLINE}}</h2><p style="margin:0 auto">{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-circle">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-circle">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-circle">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>
<section class="section" id="reviews">
<div class="reviews-header-row">
<div>
<h2 style="font-size:clamp(28px,3.5vw,40px);font-weight:700;letter-spacing:-.8px">{{REVIEWS_HEADLINE}}</h2>
<p style="color:var(--muted);font-size:17px;margin-top:6px">{{REVIEWS_SUBHEADLINE}}</p>
</div>
<div class="reviews-rating"><span class="star">★</span>4.92 <span class="dot">·</span> <span class="dot">12,439 reviews</span></div>
</div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div>
</div>
</section>
<section class="section-alt"><div class="section-alt-inner section" style="background:transparent;padding-left:40px;padding-right:40px" id="faq">
<div class="section-header" style="text-align:center"><h2>{{FAQ_HEADLINE}}</h2><p style="margin:0 auto">{{FAQ_SUBHEADLINE}}</p></div>
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
<div class="footer-col"><h4>Support</h4><ul><li><a href="#">Help Center</a></li><li><a href="#">AirCover</a></li><li><a href="#">Safety information</a></li><li><a href="#">Cancellation options</a></li></ul></div>
<div class="footer-col"><h4>Community</h4><ul><li><a href="#">Disaster relief</a></li><li><a href="#">Combating discrimination</a></li><li><a href="#">Diverse hosts</a></li></ul></div>
<div class="footer-col"><h4>Hosting</h4><ul><li><a href="#">Try hosting</a></li><li><a href="#">AirCover for Hosts</a></li><li><a href="#">Explore resources</a></li><li><a href="#">Community forum</a></li></ul></div>
<div class="footer-col"><h4>eko</h4><ul><li><a href="#">Newsroom</a></li><li><a href="#">New features</a></li><li><a href="#">Careers</a></li><li><a href="#">Investors</a></li></ul></div>
</div>
<div class="footer-bottom">
<div>&copy; {{YEAR}} eko, Inc. &middot; Privacy &middot; Terms &middot; Sitemap</div>
<div class="footer-bottom-links"><span>🌐 English (US)</span><span>$ USD</span></div>
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
:root{--bg:#fff;--cream:#f7f6f3;--text:#191919;--muted:#787774;--soft:#37352f;--blue:#2eaadc;--green:#0f7b6c;--border:#ebebeb;--border-soft:#f1f1ef}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:'Inter','Segoe UI','Helvetica Neue',Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;font-feature-settings:'ss01','cv11';min-height:100vh}
.serif{font-family:'Lyon','Lyon Display','Charter','Iowan Old Style','Apple Garamond','Baskerville','Times New Roman',Georgia,serif;font-feature-settings:'liga','dlig'}
a{color:var(--text);text-decoration:none}
.nav{position:sticky;top:0;z-index:9999;background:rgba(255,255,255,.96);backdrop-filter:saturate(180%) blur(8px);border-bottom:1px solid var(--border-soft)}
.nav-inner{max-width:1192px;margin:0 auto;padding:0 32px;height:64px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.logo{font-family:'Lyon','Charter','Georgia',serif;font-size:22px;font-weight:700;color:var(--text);letter-spacing:-.02em;display:flex;align-items:center;gap:8px}
.logo .glyph{width:22px;height:22px;background:var(--text);color:#fff;border-radius:4px;font-family:'Inter',sans-serif;font-weight:900;font-size:13px;display:inline-flex;align-items:center;justify-content:center;letter-spacing:0}
.nav-links{display:flex;gap:0;list-style:none;flex:1;justify-content:center}
.nav-links li{padding:0 14px}
.nav-links a{color:var(--text);font-size:14.5px;font-weight:500;opacity:.85;transition:opacity .15s}.nav-links a:hover{opacity:1}
.nav-utility{display:flex;align-items:center;gap:18px}
.nav-utility .link{font-size:14px;font-weight:500;color:var(--text);opacity:.85}.nav-utility .link:hover{opacity:1}
.nav-cta{padding:7px 14px;border-radius:6px;background:var(--text);color:#fff!important;font-size:14px;font-weight:600;border:1px solid var(--text);transition:background .15s}
.nav-cta:hover{background:#000}

.hero{padding:96px 32px 64px;max-width:1100px;margin:0 auto;text-align:center}
.hero-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 12px;border-radius:6px;background:var(--cream);border:1px solid var(--border);color:var(--text);font-size:13.5px;font-weight:500;margin-bottom:32px;font-family:'Inter',sans-serif}
.hero-badge .dot{width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block}
.hero h1{font-family:'Lyon','Charter','Iowan Old Style','Baskerville','Georgia',serif;font-size:clamp(36px,5vw,68px);font-weight:700;line-height:1.05;letter-spacing:-.025em;margin:0 auto 24px;max-width:920px;color:var(--text)}
.hero h1 em{font-style:italic;color:var(--text);font-weight:400}
.hero .sub{font-family:'Inter',sans-serif;font-size:clamp(17px,1.6vw,20px);color:var(--muted);max-width:620px;margin:0 auto 36px;line-height:1.5;font-weight:400}
.cta-form{display:flex;flex-wrap:wrap;gap:8px;max-width:560px;margin:0 auto 18px;justify-content:center}
.cta-form input{flex:1 1 220px;padding:12px 14px;border:1px solid var(--border);border-radius:6px;background:#fff;color:var(--text);font-size:14px;font-family:inherit;outline:none;transition:border-color .15s,box-shadow .15s}
.cta-form input::placeholder{color:#a0a0a0}
.cta-form input:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(46,170,220,.15)}
.cta-form button{flex:0 0 auto;padding:12px 22px;border:none;border-radius:6px;background:var(--text);color:#fff;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit;transition:background .15s}
.cta-form button:hover{background:#000}
.hero-meta{font-family:'Inter',sans-serif;font-size:13px;color:var(--muted);margin-top:8px}

.hero-screenshot{margin:64px auto 0;max-width:1080px;border-radius:12px;border:1px solid var(--border);background:#fff;overflow:hidden;box-shadow:0 10px 40px rgba(15,15,15,.06)}
.hs-bar{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid var(--border-soft);background:var(--cream)}
.hs-bar .d{width:11px;height:11px;border-radius:50%;background:#e0e0e0}
.hs-bar .t{margin-left:14px;font-size:12px;color:var(--muted);font-family:'Inter',sans-serif}
.hs-body{padding:32px 48px 56px;background:#fff;text-align:left;min-height:340px;display:flex;flex-direction:column;gap:14px}
.hs-h{font-family:'Lyon','Charter','Georgia',serif;font-size:36px;font-weight:700;letter-spacing:-.02em;color:var(--text)}
.hs-block{display:flex;gap:10px;align-items:flex-start;padding:6px 0;color:var(--text);font-size:15px}
.hs-block .b{width:18px;height:18px;flex-shrink:0;background:var(--cream);border-radius:4px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;color:var(--muted);margin-top:2px}
.hs-callout{padding:14px 16px;border-radius:6px;background:#f1f8fa;border-left:3px solid var(--blue);color:var(--soft);font-size:14.5px;line-height:1.55}

.stats{display:flex;justify-content:center;gap:96px;margin:96px auto 0;max-width:1100px;flex-wrap:wrap}
.stat{text-align:center}
.stat-num{font-family:'Lyon','Charter','Georgia',serif;font-size:48px;font-weight:700;color:var(--text);letter-spacing:-.025em;line-height:1}
.stat-label{font-family:'Inter',sans-serif;font-size:13px;color:var(--muted);margin-top:8px;font-weight:500}

.section{padding:120px 32px}
.section-inner{max-width:1100px;margin:0 auto}
.section-alt{background:var(--cream)}
.section-header{text-align:center;margin-bottom:64px}
.section-eyebrow{display:block;font-family:'Inter',sans-serif;font-size:13px;font-weight:600;color:var(--green);text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px}
.section-header h2{font-family:'Lyon','Charter','Georgia',serif;font-size:clamp(32px,4vw,52px);font-weight:700;letter-spacing:-.025em;line-height:1.08;margin-bottom:18px;color:var(--text)}
.section-header h2 em{font-style:italic;color:var(--text);font-weight:400}
.section-header p{font-family:'Inter',sans-serif;color:var(--muted);font-size:17px;max-width:580px;margin:0 auto;line-height:1.55}

.features-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.feature{padding:32px;border-radius:10px;background:#fff;border:1px solid var(--border);transition:transform .2s,box-shadow .2s}
.feature:hover{transform:translateY(-2px);box-shadow:0 6px 24px rgba(15,15,15,.06)}
.section-alt .feature{background:#fff}
.feature-icon{font-size:32px;line-height:1;margin-bottom:18px;display:inline-block;width:42px;height:42px;background:var(--cream);border-radius:6px;display:flex;align-items:center;justify-content:center}
.feature h3{font-family:'Lyon','Charter','Georgia',serif;font-size:22px;font-weight:700;margin-bottom:8px;letter-spacing:-.015em;color:var(--text);line-height:1.18}
.feature p{font-family:'Inter',sans-serif;color:var(--muted);font-size:15px;line-height:1.55}

.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
.step{padding:32px;border-radius:10px;background:#fff;border:1px solid var(--border)}
.step-num{display:inline-flex;width:32px;height:32px;border-radius:6px;background:var(--text);color:#fff;align-items:center;justify-content:center;font-family:'Inter',sans-serif;font-weight:700;font-size:14px;margin-bottom:16px}
.step h3{font-family:'Lyon','Charter','Georgia',serif;font-size:21px;font-weight:700;margin-bottom:8px;letter-spacing:-.015em;line-height:1.18}
.step p{font-family:'Inter',sans-serif;color:var(--muted);font-size:15px;line-height:1.55}

.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}
.review{padding:36px;border-radius:10px;background:#fff;border:1px solid var(--border)}
.review-stars{color:#f5a623;font-size:14px;margin-bottom:18px;letter-spacing:2px}
.review-quote{font-family:'Lyon','Charter','Georgia',serif;font-size:20px;color:var(--text);margin-bottom:24px;line-height:1.4;letter-spacing:-.012em;font-weight:400}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:40px;height:40px;border-radius:6px;background:linear-gradient(135deg,var(--blue),var(--green));color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Inter',sans-serif;font-weight:700;font-size:14px}
.review-name{font-family:'Inter',sans-serif;font-weight:600;font-size:14.5px;display:block;color:var(--text)}
.review-role{font-family:'Inter',sans-serif;font-size:13px;color:var(--muted)}

.faq{max-width:780px;margin:0 auto}
.faq-item{border-bottom:1px solid var(--border)}
.faq-item:first-child{border-top:1px solid var(--border)}
.faq-q{width:100%;padding:24px 8px;background:none;border:none;text-align:left;font-family:'Lyon','Charter','Georgia',serif;font-size:19px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);letter-spacing:-.015em;gap:24px;line-height:1.3}
.faq-q::after{content:'\203A';font-size:22px;color:var(--muted);transition:transform .25s;font-family:'Inter',sans-serif;flex-shrink:0}
.faq-item.active .faq-q::after{transform:rotate(90deg);color:var(--text)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;font-family:'Inter',sans-serif;color:var(--muted);font-size:15px;line-height:1.6;padding:0 8px}
.faq-item.active .faq-a{max-height:300px;padding:0 8px 24px}

.footer-cta{padding:120px 32px;text-align:center;background:var(--cream)}
.footer-cta h2{font-family:'Lyon','Charter','Georgia',serif;font-size:clamp(36px,5vw,60px);font-weight:700;letter-spacing:-.025em;margin-bottom:18px;color:var(--text);line-height:1.05}
.footer-cta h2 em{font-style:italic;font-weight:400}
.footer-cta p{font-family:'Inter',sans-serif;font-size:17px;color:var(--muted);max-width:580px;margin:0 auto 32px;line-height:1.55}
.footer-btn{display:inline-block;padding:13px 26px;border-radius:6px;background:var(--text);color:#fff;font-family:'Inter',sans-serif;font-weight:600;font-size:15px;border:none;transition:background .15s}
.footer-btn:hover{background:#000;color:#fff}

.footer{background:#000;color:#fff;padding:80px 32px 40px;font-family:'Inter',sans-serif}
.footer-inner{max-width:1100px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px;border-bottom:1px solid #2a2a2a}
.footer-brand{display:flex;flex-direction:column;gap:14px;max-width:260px}
.footer-brand .logo{color:#fff;font-family:'Lyon','Charter','Georgia',serif;font-size:24px;font-weight:700}
.footer-brand p{color:#9a9a9a;font-size:13px;line-height:1.55}
.footer-col h4{font-size:13px;font-weight:600;color:#fff;margin-bottom:14px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:10px}
.footer-col a{font-size:13px;color:#9a9a9a;text-decoration:none}.footer-col a:hover{color:#fff}
.footer-bottom{display:flex;justify-content:space-between;align-items:center;padding-top:32px;flex-wrap:wrap;gap:16px}
.copy{font-size:12px;color:#777}
.footer-legal{display:flex;gap:18px;font-size:12px}
.footer-legal a{color:#777;text-decoration:none}

@media(max-width:900px){.nav-links{display:none}.features-grid,.steps-grid,.reviews-grid{grid-template-columns:1fr}.stats{gap:40px}.section{padding:80px 24px}.footer-top{grid-template-columns:1fr 1fr;gap:32px}.hs-body{padding:24px 24px 36px}.hs-h{font-size:26px}}
@media(max-width:480px){.cta-form input,.cta-form button{flex:1 1 100%}.footer-top{grid-template-columns:1fr}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner">
<a href="#" class="logo"><span class="glyph">N</span>Eko</a>
<ul class="nav-links">
<li><a href="#benefits">Product</a></li>
<li><a href="#how">Templates</a></li>
<li><a href="#reviews">Customers</a></li>
<li><a href="#faq">Pricing</a></li>
<li><a href="#faq">Help</a></li>
</ul>
<div class="nav-utility">
<a href="#form" class="link">Log in</a>
<a href="#form" class="nav-cta">Get Eko free</a>
</div>
</div></nav>

<section class="hero" id="form">
<div class="hero-badge"><span class="dot"></span>{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="cta-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Enter your email" required>
<input type="tel" name="phone" placeholder="Phone" required>
<input type="url" name="website" placeholder="Website" required>
<button type="submit">{{CTA_BUTTON}}</button>
</form>
<div class="hero-meta">Free to try. No credit card required.</div>

<div class="hero-screenshot" aria-hidden="true">
<div class="hs-bar"><span class="d"></span><span class="d"></span><span class="d"></span><span class="t">eko.so / workspace</span></div>
<div class="hs-body">
<div class="hs-h">Welcome to your workspace</div>
<div class="hs-block"><span class="b">H</span><span>Organize everything, share with anyone, work in one place.</span></div>
<div class="hs-block"><span class="b">&middot;</span><span>Drag-and-drop blocks &mdash; text, tables, databases, embeds.</span></div>
<div class="hs-block"><span class="b">&middot;</span><span>Built-in collaboration that scales with your team.</span></div>
<div class="hs-callout">Tip: Use <strong>/</strong> to insert any block instantly &mdash; from headings to inline databases.</div>
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
<h2>{{FOOTER_HEADLINE}}</h2>
<p>{{FOOTER_SUBHEADLINE}}</p>
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
</section>

<footer class="footer">
<div class="footer-inner">
<div class="footer-top">
<div class="footer-brand">
<div class="logo">Eko</div>
<p>One connected workspace for your notes, docs, projects, and team.</p>
</div>
<div class="footer-col"><h4>Product</h4><ul><li><a href="#benefits">Features</a></li><li><a href="#how">Templates</a></li><li><a href="#form">Pricing</a></li><li><a href="#form">Download</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Careers</a></li><li><a href="#">Blog</a></li><li><a href="#">Press</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#faq">Help center</a></li><li><a href="#reviews">Customers</a></li><li><a href="#">Community</a></li><li><a href="#">Guides</a></li></ul></div>
<div class="footer-col"><h4>Connect</h4><ul><li><a href="#">Twitter</a></li><li><a href="#">LinkedIn</a></li><li><a href="#">YouTube</a></li><li><a href="mailto:contact@biz.ekoaiautomation.com">Contact</a></li></ul></div>
</div>
<div class="footer-bottom">
<div class="copy">&copy; {{YEAR}} Eko AI &middot; contact@biz.ekoaiautomation.com</div>
<div class="footer-legal"><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Security</a><a href="#">Cookies</a></div>
</div>
</div>
</footer>
__FORM_SUBMIT_JS__
</body></html>"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE 7: TESLA BOLD — Full-bleed dark hero, minimal nav, huge CTA
# ═══════════════════════════════════════════════════════════════════════════════
_TPL_TESLA_BOLD = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#fff;--surface:#f4f4f4;--surface-2:#e7e7e7;--text:#171a20;--muted:#5c5e62;--red:#cc0000;--blue:#3457b8;--blue-hover:#274a99;--border:#d0d1d2}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:"Gotham","Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh}
a{color:var(--text);text-decoration:none}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:14px 40px;display:flex;align-items:center;justify-content:space-between;background:transparent;transition:background .25s ease,color .25s ease}
.nav.scrolled{background:rgba(255,255,255,.92);backdrop-filter:blur(14px);box-shadow:0 1px 0 rgba(0,0,0,.05)}
.nav .logo{font-size:20px;font-weight:700;color:#fff;letter-spacing:4px;text-transform:uppercase;font-stretch:condensed}
.nav.scrolled .logo{color:var(--text)}
.nav-links{display:flex;gap:4px;list-style:none}
.nav-links a{color:#fff;font-size:14px;font-weight:500;padding:6px 14px;border-radius:4px;transition:background .2s}
.nav-links a:hover{background:rgba(255,255,255,.1)}
.nav.scrolled .nav-links a{color:var(--text)}
.nav.scrolled .nav-links a:hover{background:rgba(0,0,0,.06)}
.nav-right{display:flex;gap:8px;align-items:center}
.nav-pill{padding:8px 18px;border-radius:30px;background:rgba(255,255,255,.1);color:#fff!important;font-weight:500;font-size:14px;border:none}
.nav.scrolled .nav-pill{background:rgba(0,0,0,.06);color:var(--text)!important}
.nav-pill:hover{background:rgba(255,255,255,.2)}
.nav.scrolled .nav-pill:hover{background:rgba(0,0,0,.1)}
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;padding:120px 40px 80px;background:linear-gradient(180deg,#1a1a1a 0%,#0a0a0a 60%,#000 100%);overflow:hidden;color:#fff}
.hero::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 70%,rgba(50,60,80,.4) 0%,transparent 60%),radial-gradient(circle at 50% 100%,rgba(120,140,180,.15) 0%,transparent 40%);pointer-events:none}
.hero-inner{position:relative;z-index:2;text-align:center;max-width:1100px;width:100%}
.badge{display:inline-block;color:rgba(255,255,255,.7);font-size:12px;font-weight:500;letter-spacing:3px;text-transform:uppercase;margin-bottom:18px}
h1{font-size:clamp(40px,6vw,72px);font-weight:500;line-height:1.05;letter-spacing:1px;margin-bottom:14px;text-transform:uppercase;font-stretch:condensed;color:#fff}
.hero p.sub{font-size:clamp(14px,1.4vw,16px);color:rgba(255,255,255,.85);max-width:640px;margin:0 auto 36px;line-height:1.55;font-weight:400}
.hero p.sub a{color:#fff;text-decoration:underline;text-underline-offset:3px}
.hero-cta-row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-bottom:24px}
.btn{display:inline-block;padding:14px 32px;border-radius:4px;font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:1px;cursor:pointer;border:none;min-width:240px;text-align:center;transition:all .15s}
.btn-primary{background:var(--blue);color:#fff!important}
.btn-primary:hover{background:var(--blue-hover)}
.btn-outline{background:rgba(255,255,255,.1);color:#fff!important;border:1px solid rgba(255,255,255,.6);backdrop-filter:blur(4px)}
.btn-outline:hover{background:rgba(255,255,255,.25)}
.btn-dark{background:#171a20;color:#fff!important}
.btn-dark:hover{background:#000}
.scroll-cue{position:absolute;bottom:28px;left:50%;transform:translateX(-50%);color:rgba(255,255,255,.65);font-size:11px;letter-spacing:3px;text-transform:uppercase;z-index:2}
.scroll-cue::before{content:'';display:block;width:1px;height:32px;background:rgba(255,255,255,.4);margin:0 auto 10px}
.stats-strip{background:#fff;padding:64px 40px;border-bottom:1px solid var(--border)}
.stats-inner{max-width:1500px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:48px}
.stat{text-align:center}
.stat-num{font-size:clamp(40px,5vw,64px);font-weight:500;color:var(--red);letter-spacing:-1px;font-stretch:condensed;line-height:1;text-transform:uppercase}
.stat-label{font-size:12px;color:var(--muted);margin-top:10px;text-transform:uppercase;letter-spacing:2px;font-weight:500}
.section{padding:120px 40px;max-width:1500px;margin:0 auto;text-align:center}
.section-surface{background:var(--surface);max-width:none;padding-left:0;padding-right:0}
.section-surface .section-inner{max-width:1500px;margin:0 auto;padding:0 40px}
.section-header{margin-bottom:72px}
.section-header h2{font-size:clamp(32px,4.5vw,52px);font-weight:500;letter-spacing:1px;text-transform:uppercase;font-stretch:condensed;margin-bottom:16px;line-height:1.1;color:var(--text)}
.section-header p{color:var(--muted);font-size:17px;max-width:640px;margin:0 auto;line-height:1.55}
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:48px}
.feature{padding:32px 16px;background:transparent;text-align:center}
.feature-icon{font-size:42px;margin-bottom:20px;line-height:1}
.feature h3{font-size:15px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:14px;color:var(--text)}
.feature p{color:var(--muted);font-size:15px;line-height:1.6}
.lineup{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1px;background:var(--surface-2);margin-top:48px}
.lineup-card{background:#fff;padding:64px 32px;text-align:center;display:flex;flex-direction:column;align-items:center}
.lineup-img{width:100%;height:200px;border-radius:6px;background:linear-gradient(135deg,#e4e7ec 0%,#c0c5cc 100%);margin-bottom:24px;display:flex;align-items:center;justify-content:center;font-size:48px;color:#fff;box-shadow:inset 0 -40px 80px rgba(0,0,0,.15)}
.lineup-card h3{font-size:18px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;font-stretch:condensed}
.lineup-card p{color:var(--muted);font-size:14px;margin-bottom:16px}
.lineup-card .btn{min-width:160px;padding:10px 22px;font-size:12px}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:48px;margin-top:48px}
.step{text-align:center;padding:0 16px}
.step-num{display:inline-block;font-size:clamp(56px,7vw,88px);font-weight:500;color:var(--red);letter-spacing:-2px;margin-bottom:12px;font-stretch:condensed;line-height:1}
.step h3{font-size:16px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:14px}
.step p{color:var(--muted);font-size:15px;line-height:1.6}
.reviews-section{background:var(--surface);padding:120px 40px}
.reviews-section .section-header h2{color:var(--text)}
.reviews-inner{max-width:1100px;margin:0 auto}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:48px;text-align:center}
.review{padding:32px}
.review-stars{color:var(--red);font-size:14px;margin-bottom:20px;letter-spacing:3px}
.review-quote{font-family:Georgia,"Times New Roman",serif;font-size:22px;color:var(--text);margin-bottom:24px;line-height:1.4;font-style:italic;font-weight:400}
.review-author{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;display:inline-flex;align-items:center;gap:14px;justify-content:center}
.review-avatar{width:44px;height:44px;border-radius:50%;background:#171a20;color:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:600;font-size:13px;letter-spacing:0}
.review-name{font-weight:600;color:var(--text)}
.faq-section{padding:120px 40px}
.faq{max-width:820px;margin:0 auto;text-align:left}
.faq-item{border-bottom:1px solid var(--border)}
.faq-item:first-child{border-top:1px solid var(--border)}
.faq-q{width:100%;padding:28px 8px;background:none;border:none;text-align:left;font-size:17px;font-weight:500;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit}
.faq-q::after{content:'+';font-size:24px;color:var(--text);transition:transform .3s;font-weight:300;margin-left:16px}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;line-height:1.65;padding:0 8px}
.faq-item.active .faq-a{max-height:320px;padding:0 8px 28px}
.footer-cta{padding:160px 40px;text-align:center;background:linear-gradient(180deg,#000 0%,#1a1a1a 100%);color:#fff;position:relative;overflow:hidden}
.footer-cta::after{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(80,100,140,.3) 0%,transparent 60%);pointer-events:none}
.footer-cta-inner{position:relative;z-index:2;max-width:900px;margin:0 auto}
.footer-cta h2{font-size:clamp(40px,6vw,72px);font-weight:500;letter-spacing:1px;text-transform:uppercase;font-stretch:condensed;margin-bottom:20px;line-height:1.05}
.footer-cta p{font-size:17px;color:rgba(255,255,255,.85);max-width:600px;margin:0 auto 40px}
.cta-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px;max-width:720px;margin:0 auto 16px}
.cta-form input{padding:14px 18px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.05);color:#fff;font-size:14px;font-family:inherit;outline:none;border-radius:4px}
.cta-form input:focus{border-color:#fff;background:rgba(255,255,255,.1)}
.cta-form input::placeholder{color:rgba(255,255,255,.5)}
.cta-form button{grid-column:1/-1;padding:14px 32px;border:none;background:var(--blue);color:#fff;font-size:14px;font-weight:600;cursor:pointer;letter-spacing:1px;text-transform:uppercase;border-radius:4px}
.cta-form button:hover{background:var(--blue-hover)}
.footer{padding:48px 40px 32px;background:var(--surface);color:var(--muted)}
.footer-inner{max-width:1500px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
.footer-links{display:flex;gap:24px;flex-wrap:wrap;list-style:none}
.footer-links a{color:var(--muted);font-size:12px;font-weight:500}
.footer-links a:hover{color:var(--text)}
.copy{font-size:12px;color:var(--muted)}
@media(max-width:640px){.nav{padding:14px 20px}.nav-links{display:none}.nav-right .nav-pill{padding:6px 14px;font-size:12px}.hero{padding:100px 20px 60px}.section,.section-surface,.reviews-section,.faq-section,.footer-cta{padding-left:20px;padding-right:20px;padding-top:64px;padding-bottom:64px}.features-grid,.lineup,.reviews-grid,.steps-grid{grid-template-columns:1fr}.btn{min-width:0;width:100%}.footer-inner{flex-direction:column;text-align:center}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav" id="nav"><a href="#" class="logo">EKO</a>
<ul class="nav-links"><li><a href="#benefits">Model S</a></li><li><a href="#how">Model 3</a></li><li><a href="#benefits">Model X</a></li><li><a href="#how">Model Y</a></li><li><a href="#reviews">Owners</a></li><li><a href="#faq">Support</a></li></ul>
<div class="nav-right"><a href="#form" class="nav-pill">Order Now</a><a href="#form" class="nav-pill">Sign In</a></div></nav>
<section class="hero" id="top">
<div class="hero-inner">
<div class="badge">{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="hero-cta-row">
<a href="#form" class="btn btn-primary">{{CTA_BUTTON}}</a>
<a href="#benefits" class="btn btn-outline">Learn More</a>
</div>
</div>
<div class="scroll-cue">Scroll</div>
</section>
<div class="stats-strip"><div class="stats-inner">
<div class="stat"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div></div>
<section class="section" id="benefits">
<div class="section-header"><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="features-grid">
<div class="feature"><div class="feature-icon">{{BENEFIT_1_ICON}}</div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_2_ICON}}</div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_3_ICON}}</div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p></div>
<div class="feature"><div class="feature-icon">{{BENEFIT_4_ICON}}</div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p></div>
</div>
</section>
<section class="section-surface" id="how"><div class="section-inner">
<div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><span class="step-num">01</span><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><span class="step-num">02</span><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><span class="step-num">03</span><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>
<section class="reviews-section" id="reviews">
<div class="section-header"><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-inner"><div class="reviews-grid">
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span> &nbsp;·&nbsp; {{REVIEW_1_ROLE}}</div></div></div>
<div class="review"><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span> &nbsp;·&nbsp; {{REVIEW_2_ROLE}}</div></div></div>
</div></div>
</section>
<section class="faq-section" id="faq">
<div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
<div class="faq">
<div class="faq-item active"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_1_Q}}</button><div class="faq-a">{{FAQ_1_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_2_Q}}</button><div class="faq-a">{{FAQ_2_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_3_Q}}</button><div class="faq-a">{{FAQ_3_A}}</div></div>
<div class="faq-item"><button class="faq-q" onclick="this.parentElement.classList.toggle('active')">{{FAQ_4_Q}}</button><div class="faq-a">{{FAQ_4_A}}</div></div>
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
<footer class="footer"><div class="footer-inner">
<ul class="footer-links"><li><a href="#">Tesla &copy; {{YEAR}}</a></li><li><a href="#">Privacy & Legal</a></li><li><a href="#">Vehicle Recalls</a></li><li><a href="#">Contact</a></li><li><a href="#">News</a></li><li><a href="#">Locations</a></li></ul>
<div class="copy">EKO &middot; contact@biz.ekoaiautomation.com</div>
</div></footer>
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
<title>{{TITLE}}</title><style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--blue:#0046BE;--blue-dark:#003494;--blue-hover:#001E73;--yellow:#FFE000;--yellow-dark:#FFD200;--red:#C9242D;--red-dark:#A41C24;--text:#1d252c;--text-light:#2d3640;--muted:#6f7780;--bg:#fff;--surface:#f0f2f4;--surface-2:#e7eaee;--border:#d2d8df;--star:#FFB300}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:"Human BBY","Arial","Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh}
a{color:var(--blue);text-decoration:none}
a:hover{text-decoration:underline}
.utility-bar{background:var(--text);color:#fff;padding:6px 24px;text-align:right;font-size:12px}
.utility-bar a{color:#fff;margin-left:18px;font-weight:600}
.nav{background:var(--blue);padding:14px 24px;display:flex;align-items:center;gap:20px;color:#fff}
.nav-inner{max-width:1500px;margin:0 auto;width:100%;display:flex;align-items:center;gap:20px}
.logo{display:flex;align-items:center;gap:4px;flex-shrink:0;font-size:22px;font-weight:900;color:#fff;letter-spacing:-.5px}
.logo .tag{background:var(--yellow);color:var(--text);padding:6px 10px;border-radius:3px;font-size:13px;font-weight:900;letter-spacing:.5px;display:inline-block;transform:rotate(-2deg);box-shadow:0 2px 4px rgba(0,0,0,.15)}
.search{flex:1;display:flex;align-items:stretch;max-width:760px;background:#fff;border-radius:4px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.15)}
.search input{flex:1;padding:10px 16px;border:none;outline:none;font-size:14px;font-family:inherit;color:var(--text);background:#fff}
.search input::placeholder{color:var(--muted)}
.search button{padding:10px 18px;border:none;background:#fff;color:var(--blue);font-size:18px;cursor:pointer;border-left:1px solid var(--border)}
.nav-right{display:flex;align-items:center;gap:18px;flex-shrink:0;font-size:12px;font-weight:600}
.nav-right a{color:#fff;display:flex;flex-direction:column;align-items:center;gap:2px;line-height:1.2}
.nav-right a:hover{text-decoration:underline}
.nav-icon{font-size:18px}
.cart-pill{background:var(--yellow);color:var(--text)!important;padding:8px 14px;border-radius:4px;font-weight:700;display:inline-flex!important;flex-direction:row!important;gap:6px!important;align-items:center}
.shipping-ribbon{background:var(--yellow);color:var(--text);text-align:center;padding:8px 24px;font-size:14px;font-weight:700;letter-spacing:.2px}
.shipping-ribbon strong{font-weight:900}
.shipping-ribbon a{color:var(--blue);text-decoration:underline;margin-left:6px}
.subnav{background:#fff;border-bottom:1px solid var(--border);padding:0 24px}
.subnav-inner{max-width:1500px;margin:0 auto;display:flex;gap:24px;overflow-x:auto;padding:12px 0;-webkit-overflow-scrolling:touch}
.subnav a{color:var(--text);font-size:14px;font-weight:600;white-space:nowrap;padding:4px 0}
.subnav a:hover{color:var(--blue);text-decoration:none;border-bottom:2px solid var(--blue)}
.subnav .hot{color:var(--red)}
.hero{padding:48px 24px;background:linear-gradient(180deg,#fff 0%,#fff 60%,var(--surface) 100%);text-align:center}
.hero-inner{max-width:1280px;margin:0 auto}
.deal-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:4px;background:var(--yellow);color:var(--text);font-weight:900;font-size:13px;margin-bottom:20px;letter-spacing:.5px;text-transform:uppercase;box-shadow:0 2px 4px rgba(0,0,0,.12)}
h1{font-size:clamp(34px,5.5vw,52px);font-weight:900;line-height:1.1;letter-spacing:-1.4px;margin-bottom:14px;color:var(--text)}
h1 .accent{color:var(--blue)}
.hero p.sub{font-size:18px;color:var(--muted);max-width:680px;margin:0 auto 24px;line-height:1.5}
.rating-line{display:inline-flex;align-items:center;gap:10px;margin-bottom:24px;font-size:14px;color:var(--muted)}
.rating-line .stars{color:var(--star);font-size:16px;letter-spacing:1px}
.rating-line .num{font-weight:700;color:var(--text)}
.rating-line a{color:var(--blue);text-decoration:underline}
.cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-bottom:32px}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:14px 28px;border-radius:4px;font-size:15px;font-weight:700;cursor:pointer;border:none;font-family:inherit;text-decoration:none;min-width:200px}
.btn-primary{background:var(--blue);color:#fff!important}
.btn-primary:hover{background:var(--blue-hover);text-decoration:none}
.btn-outline{background:#fff;color:var(--blue)!important;border:2px solid var(--blue)}
.btn-outline:hover{background:var(--surface);text-decoration:none}
.deal-strip{display:inline-flex;align-items:center;gap:14px;margin:0 auto 24px;background:#fff;padding:14px 24px;border:2px dashed var(--yellow-dark);border-radius:8px}
.deal-strip .save{background:var(--red);color:#fff;padding:4px 12px;border-radius:3px;font-weight:900;font-size:12px;letter-spacing:.5px;text-transform:uppercase}
.deal-strip .was{text-decoration:line-through;color:var(--muted);font-size:16px}
.deal-strip .now{color:var(--red);font-size:30px;font-weight:900;letter-spacing:-.5px}
.deal-strip .reg{font-size:13px;color:var(--muted)}
.trust-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:0;max-width:1280px;margin:0 auto;background:#fff;border:1px solid var(--border);border-radius:6px;overflow:hidden;margin-top:32px}
.trust{padding:18px 16px;text-align:center;border-right:1px solid var(--border);display:flex;flex-direction:column;align-items:center;gap:6px}
.trust:last-child{border-right:none}
.trust-icon{font-size:22px}
.trust-text{font-size:13px;font-weight:700;color:var(--text);line-height:1.3}
.trust-sub{font-size:11px;color:var(--muted)}
.stats-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:32px;max-width:1280px;margin-left:auto;margin-right:auto}
.stat-tile{padding:24px;border-radius:6px;background:#fff;border:1px solid var(--border);border-top:4px solid var(--yellow);text-align:left;box-shadow:0 2px 8px rgba(0,0,0,.04)}
.stat-num{font-size:36px;font-weight:900;color:var(--blue);letter-spacing:-1px;line-height:1}
.stat-label{font-size:13px;color:var(--muted);margin-top:6px;text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.section{padding:64px 24px;max-width:1500px;margin:0 auto}
.section-alt{background:var(--surface);max-width:none}
.section-alt-inner{max-width:1500px;margin:0 auto;padding:0 24px}
.section-header{margin-bottom:36px;text-align:left}
.section-header h2{font-size:clamp(26px,4vw,38px);font-weight:900;letter-spacing:-1px;margin-bottom:8px;color:var(--text)}
.section-header h2 .accent{color:var(--blue)}
.section-header p{color:var(--muted);font-size:16px;max-width:680px}
.section-header .see-all{float:right;color:var(--blue);font-size:14px;font-weight:700}
.deals-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.deal-card{position:relative;padding:20px;border:1px solid var(--border);border-radius:6px;background:#fff;transition:box-shadow .2s,transform .15s;display:flex;flex-direction:column}
.deal-card:hover{box-shadow:0 6px 20px rgba(0,70,190,.12);transform:translateY(-2px)}
.deal-corner{position:absolute;top:0;left:0;background:var(--yellow);color:var(--text);padding:4px 12px 4px 10px;font-size:11px;font-weight:900;letter-spacing:.5px;text-transform:uppercase;border-radius:6px 0 8px 0;z-index:2}
.deal-icon{width:56px;height:56px;border-radius:6px;background:var(--surface);color:var(--blue);display:flex;align-items:center;justify-content:center;font-size:26px;margin:14px auto 16px}
.deal-card h3{font-size:16px;font-weight:700;margin-bottom:8px;color:var(--text);line-height:1.3}
.deal-card p{color:var(--muted);font-size:13.5px;line-height:1.5;margin-bottom:14px;flex:1}
.deal-stars{color:var(--star);font-size:12px;margin-bottom:8px;letter-spacing:1px}
.deal-stars .ct{color:var(--muted);margin-left:4px;font-size:12px}
.deal-price-row{margin-bottom:12px}
.deal-price{color:var(--red);font-size:22px;font-weight:900;letter-spacing:-.5px}
.deal-was{text-decoration:line-through;color:var(--muted);font-size:13px;margin-left:8px}
.deal-add{width:100%;padding:10px 16px;border:none;border-radius:4px;background:var(--blue);color:#fff;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit;letter-spacing:.2px}
.deal-add:hover{background:var(--blue-hover)}
.steps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.step{padding:28px;border-radius:6px;background:#fff;border:1px solid var(--border);position:relative;padding-top:56px}
.step-num{position:absolute;top:20px;left:20px;width:40px;height:40px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:18px}
.step h3{font-size:18px;font-weight:700;margin-bottom:8px}
.step p{color:var(--muted);font-size:14.5px;line-height:1.55}
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.review{padding:24px;border:1px solid var(--border);border-radius:6px;background:#fff}
.review-verified{display:inline-flex;align-items:center;gap:6px;background:#e8f4ec;color:#0d6e2a;padding:3px 8px;border-radius:3px;font-size:11px;font-weight:700;margin-bottom:10px;text-transform:uppercase;letter-spacing:.3px}
.review-stars{color:var(--star);font-size:16px;margin-bottom:10px;letter-spacing:1px}
.review-quote{font-size:15px;color:var(--text);margin-bottom:16px;line-height:1.55}
.review-author{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.review-avatar{width:36px;height:36px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.review-name{font-weight:700;font-size:14px;display:block;color:var(--text)}
.review-role{font-size:12px;color:var(--muted)}
.review-helpful{padding-top:12px;border-top:1px solid var(--border);font-size:12px;color:var(--muted);display:flex;justify-content:space-between;align-items:center}
.review-helpful button{padding:4px 10px;border:1px solid var(--border);background:#fff;color:var(--text);font-size:12px;font-weight:600;border-radius:3px;cursor:pointer;font-family:inherit}
.faq{max-width:920px;margin:0 auto}
.faq-item{border:1px solid var(--border);border-radius:4px;background:#fff;margin-bottom:8px;overflow:hidden}
.faq-q{width:100%;padding:18px 20px;background:none;border:none;text-align:left;font-size:16px;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit}
.faq-q:hover{background:var(--surface)}
.faq-q::after{content:'⌄';font-size:18px;color:var(--blue);transition:transform .3s;font-weight:700}
.faq-item.active .faq-q::after{transform:rotate(180deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:14.5px;padding:0 20px;line-height:1.6}
.faq-item.active .faq-a{max-height:280px;padding:0 20px 18px}
.footer-cta-block{background:var(--blue);padding:48px 24px;text-align:center;color:#fff}
.footer-cta-inner{max-width:880px;margin:0 auto}
.footer-cta-inner h2{font-size:clamp(28px,4vw,40px);font-weight:900;letter-spacing:-1px;margin-bottom:14px;color:#fff}
.footer-cta-inner h2 .accent{color:var(--yellow)}
.footer-cta-inner p{font-size:17px;margin-bottom:24px;color:rgba(255,255,255,.95);max-width:600px;margin-left:auto;margin-right:auto}
.cta-form{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px;max-width:760px;margin:0 auto;padding:16px;background:#fff;border:3px solid var(--yellow);border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.cta-form input{padding:12px 14px;border:1px solid var(--border);border-radius:4px;font-size:14px;font-family:inherit;outline:none;background:#fff;color:var(--text)}
.cta-form input:focus{border-color:var(--blue);box-shadow:0 0 0 2px rgba(0,70,190,.15)}
.cta-form button{grid-column:1/-1;padding:16px 28px;border:none;border-radius:4px;background:var(--blue);color:#fff;font-size:16px;font-weight:900;cursor:pointer;letter-spacing:.5px;text-transform:uppercase;font-family:inherit}
.cta-form button:hover{background:var(--blue-hover)}
.geek-row{background:#fff;padding:24px;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.geek-inner{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:24px;text-align:center}
.geek-badge{display:flex;flex-direction:column;align-items:center;gap:6px}
.geek-badge .ic{font-size:28px}
.geek-badge .ti{font-weight:700;font-size:14px;color:var(--text)}
.geek-badge .sb{font-size:12px;color:var(--muted)}
.footer{background:var(--text);color:#fff;padding:48px 24px 24px}
.footer-cols{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:32px;padding-bottom:32px;border-bottom:1px solid rgba(255,255,255,.15)}
.footer-col h4{font-size:14px;font-weight:900;margin-bottom:14px;color:var(--yellow);text-transform:uppercase;letter-spacing:.5px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:8px}
.footer-col a{font-size:13.5px;color:#fff;font-weight:400}
.footer-col a:hover{color:var(--yellow);text-decoration:underline}
.footer-bottom{max-width:1280px;margin:0 auto;padding-top:24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;font-size:12px;color:rgba(255,255,255,.7)}
.footer-bottom-links{display:flex;gap:14px;flex-wrap:wrap}
.footer-bottom-links a{color:rgba(255,255,255,.85);font-size:12px}
@media(max-width:900px){.search{display:none}}
@media(max-width:640px){.utility-bar{display:none}.nav{padding:12px 16px}.nav-right{gap:10px}.nav-right a span{display:none}.subnav,.shipping-ribbon{padding-left:16px;padding-right:16px;font-size:12px}.section,.section-alt-inner,.footer-cta-block,.footer{padding-left:16px;padding-right:16px}.section{padding-top:40px;padding-bottom:40px}.deals-grid,.reviews-grid,.steps-grid,.trust-strip,.stats-row{grid-template-columns:1fr}.trust{border-right:none;border-bottom:1px solid var(--border)}.btn{min-width:0;width:100%}}
</style></head>
<body>__TRACKING_PIXEL__
<div class="utility-bar"><a href="#">Order Status</a><a href="#">Saved Items</a><a href="#">My Account</a></div>
<nav class="nav"><div class="nav-inner">
<a href="#" class="logo">eko<span class="tag">AI</span></a>
<div class="search"><input type="text" placeholder="What can we help you find today?"><button type="button" aria-label="Search">🔍</button></div>
<div class="nav-right">
<a href="#"><span class="nav-icon">📍</span><span>Stores</span></a>
<a href="#"><span class="nav-icon">❤️</span><span>Saved</span></a>
<a href="#" class="cart-pill"><span class="nav-icon">🛒</span><span>Cart (0)</span></a>
</div>
</div></nav>
<div class="shipping-ribbon">⚡ <strong>FREE shipping</strong> on orders $35+ &nbsp;|&nbsp; Members get free shipping every day <a href="#">Learn more</a></div>
<nav class="subnav"><div class="subnav-inner">
<a href="#benefits">Top Deals</a>
<a href="#" class="hot">Deal of the Day</a>
<a href="#">Trending</a>
<a href="#">Best Sellers</a>
<a href="#">New Arrivals</a>
<a href="#">Outlet</a>
<a href="#">Credit Cards</a>
<a href="#">Gift Cards</a>
<a href="#">Geek Squad</a>
<a href="#">Recently Viewed</a>
</div></nav>
<section class="hero"><div class="hero-inner">
<div class="deal-badge">⚡ {{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<div class="rating-line"><span class="stars">★★★★★</span><span class="num">4.8</span> <a href="#reviews">(12,439 reviews)</a></div>
<div class="deal-strip">
<span class="save">Save $299</span>
<div><span class="was">Reg. $299.99</span> <span class="now">FREE</span></div>
<span class="reg">Today only</span>
</div>
<div class="cta-row">
<a href="#form" class="btn btn-primary">{{CTA_BUTTON}}</a>
<a href="#benefits" class="btn btn-outline">Compare Plans</a>
</div>
<div class="trust-strip">
<div class="trust"><span class="trust-icon">⭐</span><span class="trust-text">4.8 / 5</span><span class="trust-sub">50,000+ shoppers</span></div>
<div class="trust"><span class="trust-icon">🚚</span><span class="trust-text">Free Shipping</span><span class="trust-sub">on orders $35+</span></div>
<div class="trust"><span class="trust-icon">↩️</span><span class="trust-text">60-Day Returns</span><span class="trust-sub">no questions asked</span></div>
<div class="trust"><span class="trust-icon">💰</span><span class="trust-text">Price Match</span><span class="trust-sub">we'll match it</span></div>
<div class="trust"><span class="trust-icon">🛡️</span><span class="trust-text">Geek Squad</span><span class="trust-sub">24/7 support</span></div>
</div>
<div class="stats-row">
<div class="stat-tile"><div class="stat-num">{{STAT_1_NUM}}</div><div class="stat-label">{{STAT_1_LABEL}}</div></div>
<div class="stat-tile"><div class="stat-num">{{STAT_2_NUM}}</div><div class="stat-label">{{STAT_2_LABEL}}</div></div>
<div class="stat-tile"><div class="stat-num">{{STAT_3_NUM}}</div><div class="stat-label">{{STAT_3_LABEL}}</div></div>
</div>
</div></section>
<section class="section" id="benefits">
<div class="section-header"><a href="#form" class="see-all">See all deals ›</a><h2>{{BENEFITS_HEADLINE}}</h2><p>{{BENEFITS_SUBHEADLINE}}</p></div>
<div class="deals-grid">
<div class="deal-card"><div class="deal-corner">DEAL</div><div class="deal-icon">{{BENEFIT_1_ICON}}</div><div class="deal-stars">★★★★★ <span class="ct">(2,341)</span></div><h3>{{BENEFIT_1_TITLE}}</h3><p>{{BENEFIT_1_DESC}}</p><div class="deal-price-row"><span class="deal-price">FREE</span><span class="deal-was">$149.99</span></div><button class="deal-add" type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">Add to Cart</button></div>
<div class="deal-card"><div class="deal-corner">DEAL</div><div class="deal-icon">{{BENEFIT_2_ICON}}</div><div class="deal-stars">★★★★★ <span class="ct">(1,892)</span></div><h3>{{BENEFIT_2_TITLE}}</h3><p>{{BENEFIT_2_DESC}}</p><div class="deal-price-row"><span class="deal-price">FREE</span><span class="deal-was">$199.99</span></div><button class="deal-add" type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">Add to Cart</button></div>
<div class="deal-card"><div class="deal-corner">DEAL</div><div class="deal-icon">{{BENEFIT_3_ICON}}</div><div class="deal-stars">★★★★★ <span class="ct">(3,108)</span></div><h3>{{BENEFIT_3_TITLE}}</h3><p>{{BENEFIT_3_DESC}}</p><div class="deal-price-row"><span class="deal-price">FREE</span><span class="deal-was">$249.99</span></div><button class="deal-add" type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">Add to Cart</button></div>
<div class="deal-card"><div class="deal-corner">DEAL</div><div class="deal-icon">{{BENEFIT_4_ICON}}</div><div class="deal-stars">★★★★★ <span class="ct">(2,567)</span></div><h3>{{BENEFIT_4_TITLE}}</h3><p>{{BENEFIT_4_DESC}}</p><div class="deal-price-row"><span class="deal-price">FREE</span><span class="deal-was">$179.99</span></div><button class="deal-add" type="button" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'})">Add to Cart</button></div>
</div>
</section>
<section class="section-alt"><div class="section-alt-inner section" style="background:transparent;padding-left:24px;padding-right:24px;max-width:1280px" id="how">
<div class="section-header"><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-num">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-num">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-num">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div>
</div></section>
<section class="section" id="reviews">
<div class="section-header"><a href="#form" class="see-all">See all reviews ›</a><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-verified">✔ Verified Purchase</div><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_1_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div>
<div class="review-helpful"><span>Was this helpful? 142 of 158 found this helpful</span><button type="button">👍 Yes</button></div></div>
<div class="review"><div class="review-verified">✔ Verified Purchase</div><div class="review-stars">★★★★★</div><p class="review-quote">"{{REVIEW_2_QUOTE}}"</p>
<div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div>
<div class="review-helpful"><span>Was this helpful? 98 of 104 found this helpful</span><button type="button">👍 Yes</button></div></div>
</div>
</section>
<section class="section-alt"><div class="section-alt-inner section" style="background:transparent;padding-left:24px;padding-right:24px;max-width:1280px" id="faq">
<div class="section-header"><h2>{{FAQ_HEADLINE}}</h2><p>{{FAQ_SUBHEADLINE}}</p></div>
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
<button type="submit">⚡ {{FOOTER_CTA}}</button>
</form>
</div></section>
<div class="geek-row"><div class="geek-inner">
<div class="geek-badge"><span class="ic">🛡️</span><span class="ti">Geek Squad</span><span class="sb">Tech support 24/7</span></div>
<div class="geek-badge"><span class="ic">🚚</span><span class="ti">Free Shipping</span><span class="sb">Orders over $35</span></div>
<div class="geek-badge"><span class="ic">🏪</span><span class="ti">In-Store Pickup</span><span class="sb">Ready in 1 hour</span></div>
<div class="geek-badge"><span class="ic">💳</span><span class="ti">Flexible Payments</span><span class="sb">My eko Card</span></div>
<div class="geek-badge"><span class="ic">♻️</span><span class="ti">Recycling</span><span class="sb">Trade-in program</span></div>
</div></div>
<footer class="footer">
<div class="footer-cols">
<div class="footer-col"><h4>Customer Service</h4><ul><li><a href="#">Contact Us</a></li><li><a href="#">Help Center</a></li><li><a href="#">Order Status</a></li><li><a href="#">Returns & Exchanges</a></li><li><a href="#">Shipping & Delivery</a></li></ul></div>
<div class="footer-col"><h4>About Us</h4><ul><li><a href="#">Corporate Info</a></li><li><a href="#">Careers</a></li><li><a href="#">Sustainability</a></li><li><a href="#">Diversity</a></li><li><a href="#">Newsroom</a></li></ul></div>
<div class="footer-col"><h4>Investors</h4><ul><li><a href="#">Investor Relations</a></li><li><a href="#">Financial Reports</a></li><li><a href="#">Governance</a></li><li><a href="#">Stock Information</a></li></ul></div>
<div class="footer-col"><h4>Partnerships</h4><ul><li><a href="#">Affiliate Program</a></li><li><a href="#">Become a Vendor</a></li><li><a href="#">Developers</a></li><li><a href="#">Advertise</a></li></ul></div>
<div class="footer-col"><h4>eko Accounts</h4><ul><li><a href="#">My eko Card</a></li><li><a href="#">Rewards Program</a></li><li><a href="#">Gift Cards</a></li><li><a href="#">Membership</a></li></ul></div>
</div>
<div class="footer-bottom">
<div>&copy; {{YEAR}} eko AI &middot; contact@biz.ekoaiautomation.com</div>
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
:root{--bg:#000;--surface:#121212;--surface-2:#181818;--surface-3:#1f1f1f;--surface-hi:#282828;--text:#fff;--muted:#a7a7a7;--green:#1ed760;--green-bright:#3be477;--green-dark:#169c46;--pink:#ff4632;--blue:#4f9eff}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:'Spotify Circular','CircularSp','CircularSp-Arab','CircularSp-Hebr','CircularSp-Cyrl','CircularSp-Grek','CircularSp-Deva',Montserrat,var(--fallback-fonts,Helvetica,Arial,sans-serif);background:var(--bg);color:var(--text);line-height:1.5;-webkit-font-smoothing:antialiased;min-height:100vh;font-weight:400}
a{color:var(--text);text-decoration:none}

.nav{position:fixed;top:0;left:0;right:0;z-index:9999;background:#000;padding:0;height:80px;display:flex;align-items:center}
.nav-inner{max-width:1568px;margin:0 auto;padding:0 32px;width:100%;display:flex;align-items:center;justify-content:space-between;gap:24px}
.logo{display:flex;align-items:center;gap:8px;font-size:22px;font-weight:900;color:var(--green);letter-spacing:-.4px}
.logo svg{width:36px;height:36px;flex-shrink:0}
.nav-links{display:flex;gap:32px;list-style:none;flex:1;justify-content:flex-start;margin-left:32px}
.nav-links a{color:var(--muted);font-size:15px;font-weight:700;transition:color .15s,transform .15s}
.nav-links a:hover{color:#fff;transform:scale(1.04)}
.nav-utility{display:flex;align-items:center;gap:18px}
.nav-utility .link{color:var(--muted);font-size:15px;font-weight:700;transition:color .15s,transform .15s}
.nav-utility .link:hover{color:#fff;transform:scale(1.04)}
.nav-cta{padding:14px 32px;border-radius:500px;background:#fff;color:#000!important;font-weight:700;font-size:15px;letter-spacing:.1px;transition:transform .15s,background .15s}
.nav-cta:hover{transform:scale(1.04);background:#f0f0f0}

.hero{position:relative;padding:160px 32px 80px;background:linear-gradient(135deg,#1a3d2e 0%,#0f1e17 35%,#000 75%);overflow:hidden;min-height:88vh;display:flex;align-items:center}
.hero::before{content:'';position:absolute;top:-200px;right:-150px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(30,215,96,.25) 0%,transparent 70%);filter:blur(40px);pointer-events:none}
.hero::after{content:'';position:absolute;bottom:-150px;left:-100px;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(79,158,255,.18) 0%,transparent 70%);filter:blur(60px);pointer-events:none}
.hero-inner{position:relative;z-index:2;max-width:1180px;margin:0 auto;width:100%;display:grid;grid-template-columns:1.1fr .9fr;gap:64px;align-items:center}
.hero-text{text-align:left}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:500px;background:rgba(30,215,96,.12);border:1px solid rgba(30,215,96,.35);color:var(--green);font-size:13px;font-weight:700;margin-bottom:24px;letter-spacing:.3px;text-transform:uppercase}
.badge .pulse{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 0 0 rgba(30,215,96,.7);animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(30,215,96,.7)}70%{box-shadow:0 0 0 10px rgba(30,215,96,0)}100%{box-shadow:0 0 0 0 rgba(30,215,96,0)}}
.hero h1{font-size:clamp(48px,7vw,96px);font-weight:900;line-height:.95;letter-spacing:-3px;margin-bottom:24px;color:#fff;font-family:inherit}
.hero h1 .grad{background:linear-gradient(135deg,var(--green) 0%,var(--green-bright) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero .sub{font-size:clamp(17px,1.5vw,20px);color:var(--muted);max-width:540px;margin:0 0 32px;line-height:1.5;font-weight:400}
.hero-ctas{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:24px}
.btn-pill-green{display:inline-flex;align-items:center;justify-content:center;padding:16px 36px;border-radius:500px;background:var(--green);color:#000!important;font-size:15px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;border:none;cursor:pointer;transition:transform .15s,background .15s;font-family:inherit}
.btn-pill-green:hover{transform:scale(1.04);background:var(--green-bright)}
.btn-pill-outline{display:inline-flex;align-items:center;justify-content:center;padding:16px 36px;border-radius:500px;background:transparent;color:#fff;font-size:15px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;border:2px solid #fff;cursor:pointer;transition:transform .15s,background .15s;font-family:inherit}
.btn-pill-outline:hover{transform:scale(1.04);background:rgba(255,255,255,.08);color:#fff}
.hero-meta{font-size:13px;color:var(--muted);font-weight:500}

.hero-visual{position:relative;display:flex;align-items:center;justify-content:center;min-height:420px}
.album-stack{position:relative;width:100%;max-width:380px;aspect-ratio:1;perspective:1000px}
.album{position:absolute;border-radius:8px;box-shadow:0 16px 48px rgba(0,0,0,.6);overflow:hidden}
.album-1{inset:8% 18% 18% 8%;background:linear-gradient(135deg,#1ed760,#0a5d2a);transform:rotate(-6deg)}
.album-2{inset:18% 8% 8% 18%;background:linear-gradient(135deg,#ff4632,#7d1b10);transform:rotate(4deg)}
.album-3{inset:14% 14% 14% 14%;background:linear-gradient(135deg,#4f9eff,#1a3d8e);transform:rotate(-1deg)}
.album::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.15),transparent 60%)}

.cta-form{display:flex;flex-wrap:wrap;gap:10px;max-width:560px;margin:24px 0 0;justify-content:flex-start}
.cta-form input{flex:1 1 200px;padding:14px 20px;border:1px solid #2a2a2a;border-radius:500px;background:rgba(20,20,20,.85);color:#fff;font-size:14px;font-family:inherit;outline:none;transition:all .2s;font-weight:500}
.cta-form input::placeholder{color:#6a6a6a}
.cta-form input:focus{border-color:var(--green);background:#1a1a1a}
.cta-form button{flex:0 0 auto;padding:14px 32px;border:none;border-radius:500px;background:var(--green);color:#000;font-size:14px;font-weight:700;cursor:pointer;letter-spacing:1px;text-transform:uppercase;transition:transform .15s,background .15s;font-family:inherit}
.cta-form button:hover{background:var(--green-bright);transform:scale(1.04)}

.stats-strip{background:var(--surface);padding:48px 32px;border-top:1px solid #1a1a1a;border-bottom:1px solid #1a1a1a}
.stats{display:flex;justify-content:center;gap:96px;max-width:1180px;margin:0 auto;flex-wrap:wrap}
.stat{text-align:center}
.stat-num{font-size:clamp(40px,5vw,64px);font-weight:900;color:var(--green);letter-spacing:-2px;line-height:1;font-family:inherit}
.stat-label{font-size:13px;color:var(--muted);margin-top:10px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700}

.section{padding:120px 32px}
.section-inner{max-width:1280px;margin:0 auto}
.section-alt{background:var(--surface)}
.section-dark{background:linear-gradient(180deg,#000 0%,#0a0a0a 100%)}
.section-header{margin-bottom:64px;text-align:left;max-width:780px}
.section-header.center{text-align:center;margin-left:auto;margin-right:auto}
.section-eyebrow{display:inline-block;font-size:13px;color:var(--green);font-weight:700;text-transform:uppercase;letter-spacing:1.8px;margin-bottom:18px}
.section-header h2{font-size:clamp(40px,6vw,72px);font-weight:900;letter-spacing:-2.5px;line-height:.98;margin-bottom:20px;color:#fff;font-family:inherit}
.section-header h2 .grad{background:linear-gradient(135deg,var(--green),var(--green-bright));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.section-header p{color:var(--muted);font-size:18px;max-width:600px;line-height:1.5;font-weight:400}

.features-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.feature{padding:24px;border-radius:8px;background:var(--surface-2);transition:background .2s,transform .2s;cursor:pointer;position:relative}
.feature:hover{background:var(--surface-hi)}
.feature-art{width:100%;aspect-ratio:1;border-radius:6px;margin-bottom:18px;display:flex;align-items:center;justify-content:center;font-size:48px;box-shadow:0 8px 24px rgba(0,0,0,.5);position:relative;overflow:hidden}
.feature:nth-child(1) .feature-art{background:linear-gradient(135deg,#1ed760,#0a5d2a)}
.feature:nth-child(2) .feature-art{background:linear-gradient(135deg,#ff4632,#7d1b10)}
.feature:nth-child(3) .feature-art{background:linear-gradient(135deg,#4f9eff,#1a3d8e)}
.feature:nth-child(4) .feature-art{background:linear-gradient(135deg,#c44dff,#5a1d8e)}
.feature-art::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.18),transparent 65%)}
.feature-icon{position:relative;z-index:2;font-size:48px;line-height:1}
.feature h3{font-size:17px;font-weight:700;margin-bottom:6px;color:#fff;letter-spacing:-.3px;line-height:1.25}
.feature p{color:var(--muted);font-size:14px;line-height:1.45;font-weight:400}

.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.step{padding:32px;border-radius:8px;background:var(--surface-2);position:relative;transition:background .2s}
.step:hover{background:var(--surface-hi)}
.step-num{display:inline-flex;align-items:center;gap:10px;font-size:13px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:18px}
.step-num::before{content:'';display:inline-block;width:32px;height:32px;border-radius:50%;background:var(--green);color:#000;font-size:14px;font-weight:900;display:inline-flex;align-items:center;justify-content:center;font-family:inherit}
.step:nth-child(1) .step-num::before{content:'1'}
.step:nth-child(2) .step-num::before{content:'2'}
.step:nth-child(3) .step-num::before{content:'3'}
.step h3{font-size:22px;font-weight:900;margin-bottom:10px;letter-spacing:-.5px;color:#fff;line-height:1.15}
.step p{color:var(--muted);font-size:15px;line-height:1.5;font-weight:400}

.reviews-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.review{padding:36px;border-radius:8px;background:var(--surface-2);transition:background .2s;border:1px solid transparent}
.review:hover{background:var(--surface-hi);border-color:rgba(30,215,96,.2)}
.review-stars{color:var(--green);font-size:14px;margin-bottom:18px;letter-spacing:3px}
.review-quote{font-size:19px;color:#fff;margin-bottom:28px;line-height:1.45;font-weight:500;letter-spacing:-.3px}
.review-author{display:flex;align-items:center;gap:14px}
.review-avatar{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,var(--green),var(--green-bright));color:#000;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:16px;flex-shrink:0}
.review-name{font-weight:900;font-size:15px;display:block;color:#fff;letter-spacing:-.2px}
.review-role{font-size:13px;color:var(--muted);font-weight:500;margin-top:2px}

.faq{max-width:820px;margin:0 auto}
.faq-item{border-bottom:1px solid #1f1f1f}
.faq-item:first-child{border-top:1px solid #1f1f1f}
.faq-q{width:100%;padding:28px 8px;background:none;border:none;text-align:left;font-size:19px;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:#fff;letter-spacing:-.3px;gap:24px;font-family:inherit;transition:color .15s,background .15s}
.faq-q:hover{color:var(--green)}
.faq-q::after{content:'+';font-size:28px;color:var(--green);transition:transform .25s;font-weight:300;flex-shrink:0;line-height:1}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;line-height:1.6;padding:0 8px;font-weight:400}
.faq-item.active .faq-a{max-height:320px;padding:0 8px 28px}

.footer-cta{padding:140px 32px;text-align:center;background:linear-gradient(180deg,#000 0%,#0a3d22 100%);border-top:1px solid #0a1a12;position:relative;overflow:hidden}
.footer-cta::before{content:'';position:absolute;top:50%;left:50%;width:600px;height:600px;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(30,215,96,.18) 0%,transparent 60%);filter:blur(40px);pointer-events:none}
.footer-cta-inner{position:relative;z-index:1;max-width:780px;margin:0 auto}
.footer-cta h2{font-size:clamp(40px,6vw,72px);font-weight:900;letter-spacing:-2.5px;margin-bottom:24px;line-height:.95;color:#fff;font-family:inherit}
.footer-cta p{font-size:19px;color:var(--muted);max-width:580px;margin:0 auto 40px;line-height:1.45;font-weight:400}
.footer-btn{display:inline-block;padding:18px 48px;border-radius:500px;background:var(--green);color:#000;font-weight:900;font-size:15px;text-transform:uppercase;letter-spacing:1.5px;transition:transform .15s,background .15s;font-family:inherit;border:none;cursor:pointer}
.footer-btn:hover{background:var(--green-bright);transform:scale(1.04);color:#000}

.footer{background:#000;padding:80px 32px 40px;border-top:1px solid #1a1a1a}
.footer-inner{max-width:1280px;margin:0 auto}
.footer-top{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;gap:48px;padding-bottom:48px}
.footer-brand{display:flex;flex-direction:column;gap:14px}
.footer-brand .logo{color:var(--green);font-size:22px}
.footer-brand p{color:var(--muted);font-size:13px;line-height:1.55;max-width:280px;font-weight:400}
.footer-col h4{font-size:11px;font-weight:700;color:#fff;margin-bottom:18px;text-transform:uppercase;letter-spacing:1.5px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.footer-col a{font-size:14px;color:var(--muted);font-weight:500;transition:color .15s}.footer-col a:hover{color:#fff;text-decoration:underline}
.footer-bottom{padding-top:32px;border-top:1px solid #1a1a1a;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
.copy{font-size:12px;color:#6a6a6a;font-weight:500}
.footer-socials{display:flex;gap:12px}
.footer-socials a{width:40px;height:40px;border-radius:50%;background:var(--surface-2);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:14px;transition:background .15s}
.footer-socials a:hover{background:var(--surface-hi)}

@media(max-width:960px){.hero-inner{grid-template-columns:1fr;gap:48px;text-align:center}.hero-text{text-align:center}.hero-ctas{justify-content:center}.cta-form{justify-content:center}.nav-links{display:none}.features-grid{grid-template-columns:repeat(2,1fr)}.steps-grid,.reviews-grid{grid-template-columns:1fr}.stats{gap:48px}.section{padding:80px 24px}.footer-top{grid-template-columns:1fr 1fr;gap:32px}.section-header{text-align:center}}
@media(max-width:560px){.features-grid{grid-template-columns:1fr}.footer-top{grid-template-columns:1fr}.cta-form input,.cta-form button{flex:1 1 100%}.album-stack{max-width:280px}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner">
<a href="#" class="logo">
<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></svg>
Eko
</a>
<ul class="nav-links">
<li><a href="#benefits">Premium</a></li>
<li><a href="#how">Support</a></li>
<li><a href="#reviews">Download</a></li>
<li><a href="#faq">Sign up</a></li>
</ul>
<div class="nav-utility">
<a href="#form" class="link">Log in</a>
<a href="#form" class="nav-cta">Sign up free</a>
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
<div class="hero-meta" style="margin-top:18px">Free forever. Upgrade anytime.</div>
</div>
<div class="hero-visual" aria-hidden="true">
<div class="album-stack">
<div class="album album-1"></div>
<div class="album album-2"></div>
<div class="album album-3"></div>
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
<div class="step"><span class="step-num">Step</span><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><span class="step-num">Step</span><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><span class="step-num">Step</span><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
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
<div class="logo"><svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></svg>Eko</div>
<p>Sound for everyone. Discover, create, and share what moves you.</p>
</div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Jobs</a></li><li><a href="#">For the Record</a></li></ul></div>
<div class="footer-col"><h4>Communities</h4><ul><li><a href="#">For Artists</a></li><li><a href="#">Developers</a></li><li><a href="#">Advertising</a></li><li><a href="#">Vendors</a></li></ul></div>
<div class="footer-col"><h4>Useful Links</h4><ul><li><a href="#faq">Support</a></li><li><a href="#form">Free Mobile App</a></li><li><a href="#">Premium Plans</a></li></ul></div>
<div class="footer-col"><h4>Eko Plans</h4><ul><li><a href="#form">Premium Individual</a></li><li><a href="#form">Premium Duo</a></li><li><a href="#form">Premium Family</a></li><li><a href="#form">Premium Student</a></li><li><a href="#form">Eko Free</a></li></ul></div>
</div>
<div class="footer-bottom">
<div class="copy">&copy; {{YEAR}} Eko AI &middot; contact@biz.ekoaiautomation.com</div>
<div class="footer-socials"><a href="#" aria-label="Instagram">IG</a><a href="#" aria-label="Twitter">X</a><a href="#" aria-label="Facebook">FB</a></div>
</div>
</div>
</footer>
__FORM_SUBMIT_JS__
</body></html>"""


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
:root{--text:#33475b;--muted:#516f90;--soft:#7c98b6;--brand:#FF7A59;--brand-dark:#ff5c35;--teal:#0098d4;--teal-dark:#00709b;--bg:#fff;--surface:#f5f8fa;--border:#cbd6e2;--border-soft:#dfe3eb}
html{scroll-behavior:smooth;background:var(--bg);min-height:100vh}
body{font-family:'Lexend Deca','Lexend',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased;min-height:100vh}
a{color:var(--teal);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;display:block}
.container{max-width:1180px;margin:0 auto;padding:0 24px}
/* NAV */
.nav{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid var(--border-soft);box-shadow:0 1px 0 rgba(0,0,0,.02)}
.nav-inner{max-width:1180px;margin:0 auto;padding:0 24px;height:72px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:24px;font-weight:700;color:var(--text);letter-spacing:-.4px;display:flex;align-items:center;gap:8px}
.logo-mark{width:28px;height:28px;border-radius:50%;background:var(--brand);position:relative;display:inline-flex;align-items:center;justify-content:center}
.logo-mark::after{content:'';width:10px;height:10px;border-radius:50%;background:#fff}
.nav-links{display:flex;gap:28px;list-style:none;align-items:center}
.nav-links a{color:var(--text);font-size:15px;font-weight:500;transition:color .15s}
.nav-links a:hover{color:var(--brand);text-decoration:none}
.nav-actions{display:flex;align-items:center;gap:14px}
.nav-signin{color:var(--text);font-size:15px;font-weight:500;padding:8px 12px}
.nav-signin:hover{color:var(--brand);text-decoration:none}
.nav-cta{padding:11px 22px;border-radius:60px;background:var(--brand);color:#fff!important;font-size:14px;font-weight:600;transition:background .15s,transform .15s;border:2px solid var(--brand)}
.nav-cta:hover{background:var(--brand-dark);border-color:var(--brand-dark);text-decoration:none;transform:translateY(-1px)}
/* HERO */
.hero{position:relative;padding:96px 24px 88px;background:linear-gradient(180deg,#fff 0%,#f5f8fa 100%);overflow:hidden}
.hero::before{content:'';position:absolute;top:-100px;right:-100px;width:400px;height:400px;background:radial-gradient(circle,rgba(255,122,89,.12),transparent 70%);border-radius:50%;pointer-events:none}
.hero::after{content:'';position:absolute;bottom:-100px;left:-100px;width:400px;height:400px;background:radial-gradient(circle,rgba(0,152,212,.1),transparent 70%);border-radius:50%;pointer-events:none}
.hero-inner{max-width:880px;margin:0 auto;position:relative;z-index:1;text-align:center}
.badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:60px;background:rgba(255,122,89,.1);border:1px solid rgba(255,122,89,.25);color:var(--brand-dark);font-size:13px;font-weight:600;margin-bottom:24px}
.badge::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--brand)}
h1{font-size:clamp(36px,5vw,60px);font-weight:700;line-height:1.1;letter-spacing:-1.5px;color:var(--text);margin-bottom:20px}
h1 .accent{color:var(--brand)}
.hero p.sub{font-size:clamp(17px,1.6vw,20px);color:var(--muted);max-width:640px;margin:0 auto 36px;line-height:1.55;font-weight:400}
.hero-form{display:flex;flex-wrap:wrap;gap:10px;max-width:620px;margin:0 auto;padding:14px;background:#fff;border-radius:8px;box-shadow:0 12px 32px rgba(51,71,91,.12),0 2px 4px rgba(51,71,91,.04);border:1px solid var(--border-soft);justify-content:center}
.hero-form input{flex:1 1 220px;padding:12px 14px;border:1px solid var(--border);border-radius:4px;font-size:15px;font-family:inherit;outline:none;background:#fff;color:var(--text);transition:all .15s}
.hero-form input::placeholder{color:var(--soft)}
.hero-form input:focus{border-color:var(--teal);box-shadow:0 0 0 3px rgba(0,152,212,.18)}
.hero-form button{flex:0 0 auto;padding:13px 28px;border:none;border-radius:60px;background:var(--brand);color:#fff;font-size:15px;font-weight:600;cursor:pointer;transition:background .15s,transform .15s}
.hero-form button:hover{background:var(--brand-dark);transform:translateY(-2px)}
.hero-trust{margin-top:18px;font-size:13px;color:var(--soft);font-weight:500}
/* TRUST STRIP */
.trust-strip{background:#fff;padding:48px 24px;border-top:1px solid var(--border-soft);border-bottom:1px solid var(--border-soft)}
.trust-inner{max-width:1180px;margin:0 auto;text-align:center}
.trust-label{font-size:13px;color:var(--soft);font-weight:600;text-transform:uppercase;letter-spacing:1.2px;margin-bottom:24px}
.trust-logos{display:flex;justify-content:center;align-items:center;gap:56px;flex-wrap:wrap;opacity:.55}
.trust-logo{font-size:18px;font-weight:700;color:var(--soft);font-family:'Lexend',sans-serif;letter-spacing:-.3px}
.trust-logo.italic{font-style:italic}
.trust-logo.serif{font-family:Georgia,serif;letter-spacing:1px}
.trust-logo.upper{text-transform:uppercase;letter-spacing:2px;font-size:14px}
/* STATS */
.stats{background:var(--surface);padding:64px 24px}
.stats-inner{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:32px;text-align:center}
.stat{padding:24px}
.stat-num{font-size:52px;font-weight:700;color:var(--brand);letter-spacing:-1.5px;line-height:1}
.stat-label{font-size:15px;color:var(--muted);font-weight:500;margin-top:10px;line-height:1.4}
/* SECTIONS */
.section{padding:96px 24px;background:#fff}
.section-inner{max-width:1180px;margin:0 auto}
.section-alt{background:var(--surface)}
.section-header{text-align:center;margin-bottom:64px;max-width:720px;margin-left:auto;margin-right:auto}
.eyebrow{display:inline-block;font-size:13px;font-weight:700;color:var(--brand);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:14px}
.section-header h2{font-size:clamp(30px,4vw,44px);font-weight:700;letter-spacing:-1px;margin-bottom:16px;color:var(--text);line-height:1.15}
.section-header p{color:var(--muted);font-size:18px;line-height:1.55}
/* FEATURES */
.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
.feature{padding:32px 28px;border-radius:6px;background:#fff;border:1px solid var(--border);transition:transform .2s,box-shadow .2s,border-color .2s;text-align:left}
.feature:hover{transform:translateY(-4px);box-shadow:0 16px 32px rgba(51,71,91,.1);border-color:var(--brand)}
.feature-icon{display:inline-flex;width:56px;height:56px;border-radius:50%;background:var(--brand);color:#fff;align-items:center;justify-content:center;font-size:24px;margin-bottom:20px;box-shadow:0 6px 14px rgba(255,122,89,.3)}
.feature:nth-child(2) .feature-icon{background:var(--teal);box-shadow:0 6px 14px rgba(0,152,212,.3)}
.feature:nth-child(3) .feature-icon{background:#516f90;box-shadow:0 6px 14px rgba(81,111,144,.3)}
.feature:nth-child(4) .feature-icon{background:var(--brand);box-shadow:0 6px 14px rgba(255,122,89,.3)}
.feature h3{font-size:19px;font-weight:600;margin-bottom:10px;color:var(--text);letter-spacing:-.2px}
.feature p{color:var(--muted);font-size:15px;line-height:1.55}
/* STEPS */
.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;counter-reset:step}
.step{padding:32px;background:#fff;border:1px solid var(--border);border-radius:6px;border-top:4px solid var(--brand);position:relative;transition:transform .2s,box-shadow .2s}
.step:nth-child(2){border-top-color:var(--teal)}
.step:nth-child(3){border-top-color:#516f90}
.step:hover{transform:translateY(-4px);box-shadow:0 16px 32px rgba(51,71,91,.1)}
.step-badge{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:rgba(255,122,89,.12);color:var(--brand);font-weight:700;font-size:16px;margin-bottom:18px}
.step:nth-child(2) .step-badge{background:rgba(0,152,212,.12);color:var(--teal)}
.step:nth-child(3) .step-badge{background:rgba(81,111,144,.12);color:#516f90}
.step h3{font-size:20px;font-weight:600;margin-bottom:10px;color:var(--text);letter-spacing:-.2px}
.step p{color:var(--muted);font-size:15px;line-height:1.55}
/* REVIEWS */
.reviews-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.review{padding:36px 32px;border-radius:6px;background:#fff;border:1px solid var(--border);transition:box-shadow .2s,transform .2s;position:relative}
.review:hover{box-shadow:0 16px 32px rgba(51,71,91,.1);transform:translateY(-3px)}
.review-stars{color:#ffb800;font-size:16px;margin-bottom:16px;letter-spacing:2px}
.review-quote{font-size:18px;color:var(--text);margin-bottom:24px;line-height:1.55;font-weight:400}
.review-author{display:flex;align-items:center;gap:14px;padding-top:20px;border-top:1px solid var(--border-soft)}
.review-avatar{width:48px;height:48px;border-radius:50%;background:var(--brand);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px}
.review:nth-child(2) .review-avatar{background:var(--teal)}
.review-name{font-weight:600;font-size:15px;display:block;color:var(--text)}
.review-role{font-size:13px;color:var(--soft)}
/* FAQ */
.faq{max-width:780px;margin:0 auto}
.faq-item{border:1px solid var(--border);border-radius:6px;margin-bottom:12px;background:#fff;overflow:hidden;transition:border-color .2s,box-shadow .2s}
.faq-item.active{border-color:var(--brand);box-shadow:0 4px 12px rgba(255,122,89,.08)}
.faq-q{width:100%;padding:22px 24px;background:none;border:none;text-align:left;font-size:17px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:var(--text);font-family:inherit;gap:16px}
.faq-q::after{content:'+';font-size:24px;color:var(--brand);transition:transform .3s;font-weight:400;line-height:1;flex-shrink:0}
.faq-item.active .faq-q::after{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s ease;color:var(--muted);font-size:15px;padding:0 24px;line-height:1.6}
.faq-item.active .faq-a{max-height:300px;padding:0 24px 22px}
/* FOOTER CTA BAND */
.footer-band{background:linear-gradient(135deg,var(--brand) 0%,var(--brand-dark) 100%);padding:80px 24px;text-align:center;color:#fff}
.footer-band-inner{max-width:760px;margin:0 auto}
.footer-band h2{font-size:clamp(32px,4.5vw,48px);font-weight:700;letter-spacing:-1.2px;margin-bottom:16px;color:#fff;line-height:1.15}
.footer-band p{font-size:18px;color:rgba(255,255,255,.92);max-width:560px;margin:0 auto 32px;line-height:1.5}
.footer-btn{display:inline-block;padding:14px 32px;border-radius:60px;background:#fff;color:var(--brand-dark);font-weight:700;font-size:16px;transition:transform .15s,box-shadow .2s}
.footer-btn:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.15);text-decoration:none}
/* FOOTER */
.footer{background:var(--text);color:#fff;padding:72px 24px 32px}
.footer-cols{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:48px;padding-bottom:48px}
.footer-brand .logo{color:#fff;margin-bottom:14px}
.footer-brand .logo-mark{background:var(--brand)}
.footer-brand p{color:rgba(255,255,255,.65);font-size:14px;max-width:280px;line-height:1.6}
.footer-col h4{font-size:14px;font-weight:700;color:#fff;margin-bottom:18px;text-transform:uppercase;letter-spacing:.6px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.footer-col a{color:rgba(255,255,255,.7);font-size:14px;transition:color .15s}
.footer-col a:hover{color:var(--brand);text-decoration:none}
.footer-copy{max-width:1180px;margin:0 auto;padding-top:24px;border-top:1px solid rgba(255,255,255,.1);font-size:13px;color:rgba(255,255,255,.55);text-align:center}
@media(max-width:880px){.steps-grid,.stats-inner{grid-template-columns:1fr;gap:20px}.footer-cols{grid-template-columns:1fr 1fr;gap:32px}.trust-logos{gap:32px}}
@media(max-width:640px){.nav-links,.nav-signin{display:none}.features-grid,.reviews-grid{grid-template-columns:1fr}.footer-cols{grid-template-columns:1fr}.section{padding:64px 20px}.hero{padding:64px 20px 56px}}
</style></head>
<body>__TRACKING_PIXEL__
<nav class="nav"><div class="nav-inner">
<a href="#" class="logo"><span class="logo-mark"></span>Eko</a>
<ul class="nav-links"><li><a href="#benefits">Software</a></li><li><a href="#how">Solutions</a></li><li><a href="#reviews">Customers</a></li><li><a href="#faq">Pricing</a></li><li><a href="#">Resources</a></li></ul>
<div class="nav-actions"><a href="#" class="nav-signin">Contact sales</a><a href="#form" class="nav-cta">Get free CRM</a></div>
</div></nav>
<section class="hero" id="form"><div class="hero-inner">
<div class="badge">{{BADGE}}</div>
<h1>{{HERO_TITLE}}</h1>
<p class="sub">{{HERO_SUBTITLE}}</p>
<form class="hero-form" action="/api/v1/leads/public?landing_page_id={{LP_ID}}" method="POST">
<input type="text" name="first_name" placeholder="First name" required>
<input type="text" name="last_name" placeholder="Last name" required>
<input type="email" name="email" placeholder="Work email" required>
<input type="tel" name="phone" placeholder="Phone number" required>
<input type="url" name="website" placeholder="Company website" required>
<button type="submit">{{CTA_BUTTON}}</button>
</form>
<div class="hero-trust">Free forever &middot; No credit card required &middot; Setup in 5 minutes</div>
</div></section>
<section class="trust-strip"><div class="trust-inner">
<div class="trust-label">Trusted by 200,000+ growing teams worldwide</div>
<div class="trust-logos">
<span class="trust-logo">NORTHWIND</span>
<span class="trust-logo italic">Acme&middot;Co</span>
<span class="trust-logo serif">VERTEX</span>
<span class="trust-logo upper">Lumen</span>
<span class="trust-logo">Globex</span>
<span class="trust-logo italic">Initech</span>
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
</div></div></section>
<section class="section section-alt" id="how"><div class="section-inner">
<div class="section-header"><span class="eyebrow">How it works</span><h2>{{HOW_HEADLINE}}</h2><p>{{HOW_SUBHEADLINE}}</p></div>
<div class="steps-grid">
<div class="step"><div class="step-badge">1</div><h3>{{STEP_1_TITLE}}</h3><p>{{STEP_1_DESC}}</p></div>
<div class="step"><div class="step-badge">2</div><h3>{{STEP_2_TITLE}}</h3><p>{{STEP_2_DESC}}</p></div>
<div class="step"><div class="step-badge">3</div><h3>{{STEP_3_TITLE}}</h3><p>{{STEP_3_DESC}}</p></div>
</div></div></section>
<section class="section" id="reviews"><div class="section-inner">
<div class="section-header"><span class="eyebrow">Customer Stories</span><h2>{{REVIEWS_HEADLINE}}</h2><p>{{REVIEWS_SUBHEADLINE}}</p></div>
<div class="reviews-grid">
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_1_QUOTE}}&rdquo;</p><div class="review-author"><div class="review-avatar">{{REVIEW_1_INITIALS}}</div><div><span class="review-name">{{REVIEW_1_NAME}}</span><span class="review-role">{{REVIEW_1_ROLE}}</span></div></div></div>
<div class="review"><div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p class="review-quote">&ldquo;{{REVIEW_2_QUOTE}}&rdquo;</p><div class="review-author"><div class="review-avatar">{{REVIEW_2_INITIALS}}</div><div><span class="review-name">{{REVIEW_2_NAME}}</span><span class="review-role">{{REVIEW_2_ROLE}}</span></div></div></div>
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
<a href="#form" class="footer-btn">{{FOOTER_CTA}}</a>
</div></section>
<footer class="footer">
<div class="footer-cols">
<div class="footer-brand"><div class="logo"><span class="logo-mark"></span>Eko</div><p>The all-in-one platform built for growing teams. CRM, marketing, sales and service together.</p></div>
<div class="footer-col"><h4>Products</h4><ul><li><a href="#">Marketing Hub</a></li><li><a href="#">Sales Hub</a></li><li><a href="#">Service Hub</a></li><li><a href="#">CMS Hub</a></li></ul></div>
<div class="footer-col"><h4>Popular Features</h4><ul><li><a href="#">Free CRM</a></li><li><a href="#">Email Tracking</a></li><li><a href="#">Sales Sequences</a></li><li><a href="#">Reporting</a></li></ul></div>
<div class="footer-col"><h4>Resources</h4><ul><li><a href="#">Academy</a></li><li><a href="#">Blog</a></li><li><a href="#">Case Studies</a></li><li><a href="#">Templates</a></li></ul></div>
<div class="footer-col"><h4>Company</h4><ul><li><a href="#">About</a></li><li><a href="#">Careers</a></li><li><a href="#">Partners</a></li><li><a href="#">Contact</a></li></ul></div>
</div>
<div class="footer-copy">&copy; {{YEAR}} Eko AI &middot; contact@biz.ekoaiautomation.com</div>
</footer>
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
