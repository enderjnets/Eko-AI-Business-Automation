SPA_PROPOSAL_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Propuesta Eko AI — The Pampering Place</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Segoe UI',system-ui,sans-serif;background:#f8f9fa;color:#1a1a2e;line-height:1.6}
  .container{max-width:720px;margin:0 auto;background:#fff}
  .hero{background:linear-gradient(135deg,#0B4FD8 0%,#1e3a5f 100%);color:#fff;padding:48px 32px;text-align:center}
  .hero h1{font-size:2rem;font-weight:700;margin-bottom:8px}
  .hero p{font-size:1.1rem;opacity:.9}
  .brand-row{display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:16px}
  .brand-logo{width:48px;height:48px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;color:#0B4FD8}
  .section{padding:40px 32px}
  .section.alt{background:#f8f9fa}
  .section h2{font-size:1.5rem;color:#0B4FD8;margin-bottom:20px}
  .section h3{font-size:1.15rem;color:#1a1a2e;margin:24px 0 12px}
  .challenge-card{background:#fff;border-left:4px solid #e74c3c;padding:20px 24px;margin:16px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,.06)}
  .solution-card{background:#fff;border-left:4px solid #0B4FD8;padding:20px 24px;margin:16px 0;border-radius:0 8px 8px 0;box-shadow:0 2px 8px rgba(0,0,0,.06)}
  .icon{font-size:1.5rem;margin-right:8px}
  .highlight{background:linear-gradient(120deg,#ffeaa7 0%,#ffeaa7 100%);background-repeat:no-repeat;background-size:100% 40%;background-position:0 88%;padding:0 4px}
  .pricing-table{width:100%;border-collapse:collapse;margin:24px 0}
  .pricing-table th,.pricing-table td{padding:14px 16px;text-align:left;border-bottom:1px solid #e9ecef}
  .pricing-table th{background:#f8f9fa;font-weight:600;color:#495057}
  .pricing-table tr:hover{background:#f8f9fa}
  .check{color:#27ae60;font-weight:700}
  .cross{color:#e74c3c;font-weight:700}
  .best-value{border:2px solid #0B4FD8;border-radius:12px;padding:4px;margin:-4px;position:relative}
  .best-value::before{content:"⭐ Best Value";position:absolute;top:-12px;left:16px;background:#0B4FD8;color:#fff;font-size:.7rem;font-weight:600;padding:2px 10px;border-radius:20px}
  .cta-section{text-align:center;padding:48px 32px;background:linear-gradient(135deg,#0B4FD8 0%,#1e3a5f 100%);color:#fff}
  .cta-button{display:inline-block;background:#fff;color:#0B4FD8;font-weight:700;padding:16px 40px;border-radius:50px;text-decoration:none;font-size:1.1rem;margin:8px;transition:transform .2s}
  .cta-button:hover{transform:translateY(-2px)}
  .cta-button.secondary{background:transparent;color:#fff;border:2px solid #fff}
  .stats{display:flex;justify-content:center;gap:32px;margin:32px 0;flex-wrap:wrap}
  .stat{text-align:center}
  .stat-number{font-size:2rem;font-weight:700;color:#0B4FD8}
  .stat-label{font-size:.85rem;color:#6c757d}
  .footer{text-align:center;padding:24px;font-size:.8rem;color:#6c757d}
  .step{display:flex;gap:16px;margin:20px 0;align-items:flex-start}
  .step-number{min-width:36px;height:36px;border-radius:50%;background:#0B4FD8;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0}
  .step-content h4{font-weight:600;margin-bottom:4px}
  .step-content p{font-size:.9rem;color:#495057}
  @media(max-width:600px){.section{padding:28px 20px}.hero h1{font-size:1.5rem}.stats{gap:16px}}
</style>
</head>
<body>
<div class="container">

  <div class="hero">
    <div class="brand-row">
      <div class="brand-logo">E</div>
      <span style="font-size:1.5rem">×</span>
      <div style="font-weight:600;font-size:1.1rem">The Pampering Place</div>
    </div>
    <h1>Propuesta Confidencial de Automatización con IA</h1>
    <p>Libere a su equipo de la recepción. Elimine las citas perdidas. Haga crecer el spa mientras duerme.</p>
    <div class="stats" style="margin-top:28px">
      <div class="stat" style="color:#fff"><div class="stat-number" style="color:#fff">2–3 hrs</div><div class="stat-label" style="color:rgba(255,255,255,.8)">Ahorradas diarias</div></div>
      <div class="stat" style="color:#fff"><div class="stat-number" style="color:#fff">24/7</div><div class="stat-label" style="color:rgba(255,255,255,.8)">Recepción bilingüe</div></div>
      <div class="stat" style="color:#fff"><div class="stat-number" style="color:#fff">Mes 1</div><div class="stat-label" style="color:rgba(255,255,255,.8)">ROI positivo</div></div>
    </div>
  </div>

  <div class="section">
    <h2>🎯 El Desafío</h2>
    <p>Hoy, <strong>The Pampering Place</strong> depende de que su equipo atienda cada llamada, confirme cada cita manualmente y pierda horas en tareas administrativas que la IA puede hacer automáticamente.</p>

    <div class="challenge-card">
      <span class="icon">📞</span><strong>El teléfono nunca para</strong>
      <p style="margin-top:6px">Cada llamada interrumpe a su terapeuta o recepcionista en medio de un tratamiento. Clientes en sala de espera ven al personal distraído contestando el teléfono.</p>
    </div>

    <div class="challenge-card">
      <span class="icon">📅</span><strong>Citas perdidas por no-shows</strong>
      <p style="margin-top:6px">Sin recordatorios automáticos, los clientes olvidan sus citas. Un hueco vacío en el calendario = ingresos perdidos que no se recuperan.</p>
    </div>

    <div class="challenge-card">
      <span class="icon">🌙</span><strong>Cero reservas después de horas</strong>
      <p style="margin-top:6px">Si alguien quiere agendar a las 9 PM después del trabajo, no hay quien conteste. Ese cliente reserva en otro spa.</p>
    </div>

    <div class="challenge-card">
      <span class="icon">💸</span><strong>Pago de propinas manual</strong>
      <p style="margin-top:6px">Las propinas se anotan en papel. No hay totales, no hay resúmenes — la nómina se convierte en un dolor de cabeza semanal.</p>
    </div>

    <p style="margin-top:20px"><strong>El verdadero costo no es solo dinero.</strong> Es su equipo perdiendo horas cada día en tareas administrativas que un sistema de IA maneja automáticamente, liberándolos para enfocarse en lo que mejor saben hacer: consentir a sus clientes.</p>
  </div>

  <div class="section alt">
    <h2>✨ La Solución Eko AI para The Pampering Place</h2>
    <p>Tres componentes interconectados que trabajan juntos para automatizar las operaciones diarias del spa — sin nuevo hardware, funciona con cualquier teléfono.</p>

    <div class="solution-card">
      <h3><span class="icon">🤖</span>Recepcionista de IA</h3>
      <p><strong>Impulsado por VAPI Phone Agent</strong></p>
      <ul style="margin:10px 0 0 20px">
        <li>Atiende llamadas <strong>24/7</strong> — en <strong>inglés y español</strong></li>
        <li>Agenda, reagenda y cancela citas automáticamente</li>
        <li>Responde preguntas frecuentes: horarios, precios, servicios, dirección</li>
        <li>Envía confirmación por SMS instantánea a cada cliente</li>
        <li>Nunca ocupado, nunca cansado, nunca fuera de servicio</li>
        <li>Incluido en la tarifa mensual — sin costo extra por llamada</li>
      </ul>
    </div>

    <div class="solution-card">
      <h3><span class="icon">📅</span>Gestión Inteligente de Citas</h3>
      <p><strong>Calendario Digital con Recordatorios</strong></p>
      <ul style="margin:10px 0 0 20px">
        <li>Reemplaza la libreta de papel con un calendario digital real</li>
        <li>Recordatorio automático por SMS <strong>24 horas antes</strong> de cada cita</li>
        <li>Los clientes confirman o cancelan por texto — llena huecos antes de que ocurran</li>
        <li>Resumen diario enviado a usted cada mañana</li>
        <li>Funciona en cualquier smartphone — sin computadora, sin tablet</li>
      </ul>
    </div>

    <div class="solution-card">
      <h3><span class="icon">💰</span>Seguimiento de Ingresos y Propinas</h3>
      <p><strong>Inteligencia de Negocio Simple</strong></p>
      <ul style="margin:10px 0 0 20px">
        <li>Registro digital de propinas por terapeuta, por día — toma segundos registrar</li>
        <li>Resumen semanal de propinas enviado automáticamente para nómina</li>
        <li>Reporte mensual de ingresos con tendencias y destacados</li>
        <li>Sin hojas de cálculo, sin matemáticas manuales — todo calculado automáticamente</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>💎 Inversión</h2>
    <p>Precios transparentes y simples. Elija el plan que mejor se adapte a The Pampering Place:</p>

    <table class="pricing-table">
      <thead>
        <tr><th>Característica</th><th>Starter</th><th>Growth</th><th class="best-value">Premium</th></tr>
      </thead>
      <tbody>
        <tr><td>Agente de Teléfono IA (EN + ES)</td><td class="check">✓</td><td class="check">✓</td><td class="check">✓</td></tr>
        <tr><td>Agenda de Citas Digital</td><td class="check">✓</td><td class="check">✓</td><td class="check">✓</td></tr>
        <tr><td>SMS de Confirmación</td><td class="check">✓</td><td class="check">✓</td><td class="check">✓</td></tr>
        <tr><td>Recordatorios Automáticos (24h)</td><td class="cross">✗</td><td class="check">✓</td><td class="check">✓</td></tr>
        <tr><td>Reportes Diarios a Usted</td><td class="cross">✗</td><td class="check">✓</td><td class="check">✓</td></tr>
        <tr><td>Seguimiento de Propinas</td><td class="cross">✗</td><td class="check">✓</td><td class="check">✓</td></tr>
        <tr><td>Acceso Email + Calendario</td><td class="cross">✗</td><td class="cross">✗</td><td class="check">✓</td></tr>
        <tr><td><strong>Precio mensual</strong></td><td><strong>$199/mes</strong></td><td><strong>$299/mes</strong></td><td><strong>$399/mes</strong></td></tr>
      </tbody>
    </table>

    <p style="text-align:center;color:#6c757d;font-size:.9rem">Setup inicial: <strong>$499</strong> (configuración, entrenamiento de IA, integración). Primer mes de servicio incluido.</p>
  </div>

  <div class="section alt">
    <h2>📈 Retorno de Inversión</h2>
    <p>Por qué esto se paga solo en el primer mes:</p>
    <ul style="margin:12px 0 0 20px">
      <li><strong>Ingresos protegidos:</strong> Un spa mediano en Denver genera <strong>$15,000–$40,000/mes</strong>. Eko protege y hace crecer esa base.</li>
      <li><strong>No-shows recuperados:</strong> Reducir no-shows un 20% = aprox. <strong>$300–$800/mes ahorrados</strong> solo en citas recuperadas.</li>
      <li><strong>Tiempo liberado:</strong> Su equipo recupera <strong>2–3 horas diarias</strong> actualmente gastadas en llamadas. Ese tiempo se convierte en atención a clientes o descanso.</li>
      <li><strong>Después de horas:</strong> La IA agenda citas a medianoche si es necesario. <strong>Cero ingresos perdidos</strong> por llamadas no atendidas en la noche.</li>
    </ul>
    <p style="margin-top:16px;text-align:center;font-size:1.1rem"><strong>Ahorro estimado mensual:</strong> <span style="color:#0B4FD8;font-size:1.3rem;font-weight:700">$300–$800+</span> <span style="color:#6c757d">vs. $299–$399/mes de costo</span></p>
  </div>

  <div class="section">
    <h2>🚀 Próximos Pasos</h2>
    <p>De hoy a operativo en 7 días:</p>

    <div class="step">
      <div class="step-number">1</div>
      <div class="step-content">
        <h4>Agende una Demo Gratuita</h4>
        <p>30 minutos con Ender — vea la IA atender una llamada en vivo, agendar una cita de demo y enviar una confirmación por SMS en tiempo real. Sin compromiso.</p>
      </div>
    </div>

    <div class="step">
      <div class="step-number">2</div>
      <div class="step-content">
        <h4>Personalice y Configure</h4>
        <p>Recolectamos los servicios, precios, horarios y preguntas frecuentes de The Pampering Place. La IA se entrena para sonar como su recepcionista — pero sin el salario.</p>
      </div>
    </div>

    <div class="step">
      <div class="step-number">3</div>
      <div class="step-content">
        <h4>Pruebe Juntos</h4>
        <p>Usted llama al sistema, refinamos la voz, el guion y las respuestas juntos. Nada se activa hasta que se sienta bien.</p>
      </div>
    </div>

    <div class="step">
      <div class="step-number">4</div>
      <div class="step-content">
        <h4>Vaya en Vivo — Su Equipo Descansa</h4>
        <p>La IA atiende la primera llamada real. Las citas se agendan solas. Los recordatorios SMS salen automáticamente. Usted recibe un reporte matutino y sigue con su día.</p>
      </div>
    </div>
  </div>

  <div class="cta-section">
    <h2 style="color:#fff;margin-bottom:12px">¿Listo para que su spa trabaje las 24 horas?</h2>
    <p style="opacity:.9;margin-bottom:24px">Sin costo de setup hoy. Pague solo cuando esté listo para activar.</p>
    <a href="https://ender-rog.tail25dc73.ts.net/book-demo?email=margie240478@gmail.com&name=The+Pampering+Place" class="cta-button">Agendar Demo Gratuita →</a>
    <a href="mailto:contact@biz.ekoaiautomation.com?subject=Me interesa el plan Premium" class="cta-button secondary">Responder por Email</a>
    <p style="margin-top:20px;font-size:.8rem;opacity:.7">Eko AI · Denver, CO · contact@biz.ekoaiautomation.com</p>
  </div>

  <div class="footer">
    <p>Esta propuesta es confidencial y personalizada para The Pampering Place Day Wellness Spa.</p>
    <p style="margin-top:4px">Generada por Eko AI · {date}</p>
  </div>

</div>
</body>
</html>"""
