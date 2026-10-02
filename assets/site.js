(function () {
  var mobileButton = document.querySelector('.hamburger');
  var mobileMenu = document.getElementById('mobile-nav');
  if (mobileButton && mobileMenu) {
    mobileButton.addEventListener('click', function () {
      var open = mobileButton.getAttribute('aria-expanded') === 'true';
      mobileButton.setAttribute('aria-expanded', String(!open));
      mobileButton.classList.toggle('active', !open);
      mobileMenu.hidden = open;
      mobileMenu.classList.toggle('active', !open);
    });
    mobileMenu.querySelectorAll('a').forEach(function (link) { link.addEventListener('click', function () { mobileButton.setAttribute('aria-expanded', 'false'); mobileButton.classList.remove('active'); mobileMenu.hidden = true; mobileMenu.classList.remove('active'); }); });
  }
  var scrollPending = false;
  var mainNav = document.querySelector('nav');
  var readProgress = document.getElementById('read-progress');
  function updateScroll() {
    /* Read layout first, then write styles to avoid a forced synchronous reflow. */
    var scrollTop = window.scrollY;
    var height = document.documentElement.scrollHeight - window.innerHeight;
    var ratio = height > 0 ? Math.min(1, scrollTop / height) : 0;
    if (mainNav) mainNav.classList.toggle('nav-scrolled', scrollTop > 24);
    if (readProgress) readProgress.style.transform = 'scaleX(' + ratio + ')';
    scrollPending = false;
  }
  window.addEventListener('scroll', function () { if (!scrollPending) { scrollPending = true; requestAnimationFrame(updateScroll); } }, {passive:true});
  window.addEventListener('resize', updateScroll, {passive:true});
  updateScroll();
  function closeMobile(returnFocus) { if (!mobileButton || !mobileMenu) return; mobileButton.setAttribute('aria-expanded','false'); mobileButton.classList.remove('active'); mobileMenu.hidden = true; mobileMenu.classList.remove('active'); if(returnFocus)mobileButton.focus(); }
  window.matchMedia('(min-width:1181px)').addEventListener('change', function(e){if(e.matches)closeMobile(false);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape' && mobileButton && mobileButton.getAttribute('aria-expanded')==='true')closeMobile(true);});
  var journey = Array.prototype.find.call(document.querySelectorAll('.steps'), function (group) { return group.parentElement.textContent.indexOf('De la primera factura') !== -1; }); if (journey) journey.classList.add('growth-path');
  var animated = document.querySelectorAll('.steps > article, .resource-cards > a, .pain-grid article, .testimonial-card, .bridge'); var board = document.querySelector('.control-board'); if (board) { board.classList.add('board-ready'); }
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) { var reveal = new IntersectionObserver(function(entries){ entries.forEach(function(entry){ if(entry.isIntersecting){ entry.target.classList.add('is-visible'); reveal.unobserve(entry.target); } }); }, {threshold:.12}); animated.forEach(function(el,index){ el.classList.add('reveal-on-scroll'); el.style.transitionDelay = (index % 3) * 70 + 'ms'; reveal.observe(el); }); if(board) reveal.observe(board); } else { animated.forEach(function(el){el.classList.add('is-visible');}); if(board)board.classList.add('is-visible'); }
  var contact = document.getElementById('contact-form');
  if (contact) {
    contact.querySelectorAll('[required]').forEach(function(input){ input.addEventListener('input',function(){input.setCustomValidity('');}); });
    contact.addEventListener('input',function(){document.getElementById('contact-preview').hidden=true;});
    contact.addEventListener('submit',function(event){
      event.preventDefault();
      contact.querySelectorAll('[required]').forEach(function(input){input.setCustomValidity(input.value.trim() ? '' : 'Completa este campo.');});
      if(!contact.reportValidity())return;
      var name=contact.elements.nombre.value.trim(), email=contact.elements.email.value.trim(), message=contact.elements.mensaje.value.trim();
      var text='Hola, soy '+name+'.\nInterés: '+contact.dataset.topic+'.\n'+(email?'Email: '+email+'\n':'')+'\n'+message;
      var preview=document.getElementById('contact-preview'); preview.hidden=false; preview.querySelector('pre').textContent=text;
      var link=preview.querySelector('a'); link.href='https://wa.me/56961314436?text='+encodeURIComponent(text); link.focus();
    });
  }
  var finders = document.querySelectorAll('[data-route-finder]');
  if (finders.length) {
    var modal = document.createElement('dialog'); modal.className = 'route-modal'; modal.setAttribute('aria-labelledby','route-modal-title');
    modal.innerHTML = '<div class="route-modal__panel"><button class="route-modal__close" type="button" aria-label="Cerrar">×</button><div class="section-label">Orientación rápida</div><h2 id="route-modal-title">¿Qué necesita hoy tu negocio?</h2><p>Elige la situación que más se parece a la tuya. Te llevaremos a la información y al siguiente paso adecuados.</p><div class="route-modal__options"><a href="/emprendedores/"><strong>Ordenar mi contabilidad</strong><span>Impuestos, obligaciones y apoyo para emprender o ponerse al día.</span></a><a href="/control-financiero/"><strong>Entender y controlar mis finanzas</strong><span>Caja, cobranza, pagos, resultados y diagnóstico financiero.</span></a></div></div>';
    document.body.appendChild(modal); var priorFocus;
    function closeRouteModal(){ modal.close(); }
    modal.addEventListener('close',function(){document.body.classList.remove('dialog-open'); if(priorFocus)(priorFocus.closest('#mobile-nav')?mobileButton:priorFocus).focus();});
    finders.forEach(function(link){ link.addEventListener('click',function(e){ if(typeof modal.showModal!=='function')return; e.preventDefault(); priorFocus=link; modal.showModal(); document.body.classList.add('dialog-open'); modal.querySelector('.route-modal__close').focus(); }); });
    modal.querySelector('.route-modal__close').addEventListener('click',closeRouteModal); modal.addEventListener('click',function(e){ if(e.target===modal) closeRouteModal(); });
  }
  if(location.pathname==='/' || location.pathname==='/index.html'){
    var legacy=['#servicios','#planes','#testimonios','#faq'];
    function routeLegacy(){if(legacy.indexOf(location.hash)!==-1)location.replace('/emprendedores/'+location.hash);}
    window.addEventListener('hashchange',routeLegacy);routeLegacy();
  }
  var form = document.getElementById('diagnostic-form');
  if (!form) return;
  form.hidden = false;
  var groups = [
    {area:'Tesorería', questions:['¿Tienes una proyección actualizada de ingresos y pagos para las próximas 8 semanas?','¿Sabes cuánto puedes pagar esta semana sin afectar tus próximas obligaciones?']},
    {area:'Cobranza', questions:['¿Revisas con frecuencia las cuentas por cobrar vencidas?','¿Tienes un proceso claro para recordar y gestionar pagos pendientes?']},
    {area:'Proveedores y pagos', questions:['¿Conoces los próximos pagos a proveedores y sus fechas de vencimiento?','¿Priorizas pagos según caja disponible y compromisos de la empresa?']},
    {area:'Presupuesto y resultados', questions:['¿Comparas tus resultados reales con un presupuesto o meta mensual?','¿Puedes identificar las principales razones cuando un resultado se desvía de lo esperado?']},
    {area:'Información gerencial', questions:['¿Puedes revisar indicadores clave sin reunir manualmente varias planillas?','¿Sabes qué áreas, clientes o líneas necesitan más atención para mejorar el resultado?']}
  ];
  var state = 0, answers = Array(10).fill(null);
  var fields = document.getElementById('quiz-fields'), title = document.getElementById('quiz-title'), step = document.getElementById('quiz-step'), progress = document.getElementById('quiz-progress'), error = document.getElementById('quiz-error'), back = document.getElementById('quiz-back'), next = document.getElementById('quiz-next'), result = document.getElementById('quiz-result');
  function draw() { var g = groups[state], start = state * 2; step.textContent = 'PASO ' + (state + 1) + ' DE ' + groups.length + ' · ' + g.area.toUpperCase(); progress.value = state + 1; title.textContent = g.area; fields.innerHTML = g.questions.map(function (q,i) { var n=start+i; return '<fieldset class="quiz-question"><legend>' + q + '</legend><div class="answer-group">' + [[0,'No, hoy no'],[5,'Parcialmente'],[10,'Sí, con claridad']].map(function (choice) { return '<label><input type="radio" name="q'+n+'" value="'+choice[0]+'" '+(answers[n]===choice[0]?'checked':'')+'>'+choice[1]+'</label>'; }).join('') + '</div></fieldset>'; }).join(''); back.hidden = state === 0; next.textContent = state === groups.length-1 ? 'Ver mi resultado →' : 'Continuar →'; error.textContent=''; }
  function saveCurrent() { var valid = true; fields.querySelectorAll('fieldset').forEach(function (fieldset,i) { var selected = fieldset.querySelector('input:checked'); if (!selected) valid=false; else answers[state*2+i] = Number(selected.value); }); return valid; }
  form.addEventListener('submit', function (e) { e.preventDefault(); if (!saveCurrent()) { error.textContent='Elige una respuesta para cada pregunta antes de continuar.'; var missing=Array.from(fields.querySelectorAll('fieldset')).find(function(f){return !f.querySelector(':checked');}); if(missing)missing.querySelector('input').focus(); return; } if (state < groups.length-1) { state++; draw(); title.focus(); } else showResult(); });
  fields.addEventListener('change',function(e){if(e.target.matches('input[type=radio]')){answers[Number(e.target.name.slice(1))]=Number(e.target.value);error.textContent='';}});
  back.addEventListener('click', function () { if (state) { saveCurrent(); state--; draw(); title.focus(); } });
  function level(score) { return score <= 5 ? 'Bajo' : score <= 15 ? 'Medio' : 'Alto'; }
  function showResult() { form.hidden=true; result.hidden=false; var scores=groups.map(function (_,i) { return answers.slice(i*2,i*2+2).reduce(function(a,b){return a+b;},0); }), total=scores.reduce(function(a,b){return a+b;},0), ranked=scores.map(function(s,i){return {score:s,index:i};}).sort(function(a,b){return a.score-b.score;}); document.getElementById('score-total').textContent=total; document.getElementById('result-title').textContent='Control financiero: '+total+'/100'; document.getElementById('score-summary').textContent= total < 40 ? 'Hoy hay varias áreas que pueden requerir orden y visibilidad. Empieza por las dos prioridades que aparecen abajo.' : total < 70 ? 'Tienes algunas prácticas de control, con oportunidades claras de fortalecer tu información para decidir.' : 'Tu percepción indica una base sólida. La conversación puede enfocarse en consolidar y profundizar el control.'; document.getElementById('score-areas').innerHTML=scores.map(function(s,i){return '<div class="score-area"><span>'+groups[i].area+'</span><div class="score-bar"><i style="width:'+(s/20*100)+'%"></i></div><strong>'+level(s)+'</strong></div>';}).join(''); document.getElementById('score-priorities').innerHTML=ranked.slice(0,2).map(function(r){var label=groups[r.index].area; var advice={Tesorería:'Revisar la proyección de ingresos y pagos para las próximas semanas.','Cobranza':'Revisar cuentas vencidas y mantener un seguimiento periódico.','Proveedores y pagos':'Reunir vencimientos y priorizar pagos según caja disponible.','Presupuesto y resultados':'Comparar el resultado del mes con una meta o presupuesto inicial.','Información gerencial':'Definir pocos indicadores y una fuente regular para revisarlos.'}[label];return '<li><strong>'+label+':</strong> '+advice+'</li>';}).join(''); document.getElementById('priorities-title').textContent=total===100?'Dos áreas para seguir fortaleciendo':'Dos prioridades para revisar'; var text='Hola, completé el Diagnóstico de Control Financiero.\nPuntaje: '+total+'/100.\n'+scores.map(function(s,i){return groups[i].area+': '+level(s);}).join('\n')+'\n\nMe gustaría solicitar una revisión.'; document.getElementById('result-contact').href='https://wa.me/56961314436?text='+encodeURIComponent(text); result.querySelector('#result-title').focus(); }
  document.getElementById('quiz-restart').addEventListener('click', function () { state=0; answers=Array(10).fill(null); result.hidden=true; form.hidden=false; draw(); title.focus(); }); draw();
})();
