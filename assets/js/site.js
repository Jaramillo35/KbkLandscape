// KBK Landscape & Beyond — shared behaviour. No dependencies.
(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const lang = document.documentElement.lang.startsWith('es') ? 'es' : 'en';
  const T = {
    en: { sending: 'Sending…', ok: 'Thanks! Jose will get back to you within one business day.',
          err: 'Sorry, that did not go through. Please call (586) 489-5613 or email josechavarin@kbklandscape.com.',
          all: 'All', close: 'Close' },
    es: { sending: 'Enviando…', ok: '¡Gracias! Jose se comunicará con usted en un día hábil.',
          err: 'No se pudo enviar. Por favor llame al (586) 489-5613 o escriba a josechavarin@kbklandscape.com.',
          all: 'Todos', close: 'Cerrar' },
  }[lang];

  // Mobile nav
  const burger = $('.burger'), nav = $('nav.main');
  if (burger && nav) burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });

  // Remember language choice; offer the other language on first visit
  try {
    const saved = localStorage.getItem('kbk-lang');
    if (!saved) localStorage.setItem('kbk-lang', lang);
    else if (saved !== lang && !sessionStorage.getItem('kbk-lang-switched')) {
      const alt = $('.lang');
      if (alt) { sessionStorage.setItem('kbk-lang-switched', '1'); location.replace(alt.href); }
    }
    $$('.lang').forEach(a => a.addEventListener('click', () => localStorage.setItem('kbk-lang', lang === 'en' ? 'es' : 'en')));
  } catch (e) { /* storage blocked: fine */ }

  // Reveal on scroll
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    $$('.reveal').forEach(el => io.observe(el));
  } else $$('.reveal').forEach(el => el.classList.add('in'));

  // Gallery: filters + lightbox
  const gallery = $('.gallery');
  if (gallery) {
    const figs = $$('figure', gallery);
    $$('.filters button').forEach(b => b.addEventListener('click', () => {
      $$('.filters button').forEach(x => x.setAttribute('aria-pressed', x === b));
      const cat = b.dataset.cat;
      figs.forEach(f => f.hidden = cat !== 'all' && f.dataset.cat !== cat);
    }));
    const dlg = document.createElement('dialog'); dlg.className = 'lightbox';
    dlg.innerHTML = `<button type="button" aria-label="${T.close}">×</button><img alt=""><p></p>`;
    document.body.append(dlg);
    $('button', dlg).addEventListener('click', () => dlg.close());
    dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
    figs.forEach(f => f.addEventListener('click', () => {
      const img = $('img', f);
      $('img', dlg).src = img.dataset.full || img.src;
      $('img', dlg).alt = img.alt;
      $('p', dlg).textContent = $('figcaption', f)?.textContent || '';
      dlg.showModal();
    }));
  }

  // Quote form → KBK Office on the Pi; falls back to a pre-filled email
  const form = $('form.quote');
  // Preview copies of the site (not on kbklandscape.com) talk to KBK Office on the same host.
  if (form && !location.hostname.endsWith('kbklandscape.com')) form.action = `http://${location.hostname}:8800/kbk-api/leads`;
  if (form) form.addEventListener('submit', async e => {
    e.preventDefault();
    const msg = $('.form-msg', form), btn = $('button[type=submit]', form);
    if ($('.hp input', form)?.value) return;            // honeypot: bots fill it, people don't
    const data = Object.fromEntries(new FormData(form).entries());
    data.services = $$('input[name=services]:checked', form).map(i => i.value);
    data.lang = lang; data.page = location.pathname;
    btn.disabled = true; const label = btn.textContent; btn.textContent = T.sending;
    msg.className = 'form-msg';
    try {
      const r = await fetch(form.action, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(data) });
      if (!r.ok) throw new Error(r.status);
      msg.textContent = T.ok; msg.className = 'form-msg ok'; form.reset();
    } catch (err) {
      const body = encodeURIComponent(`${data.name}\n${data.phone}\n${data.address || ''}\n\n${data.services.join(', ')}\n\n${data.details || ''}`);
      msg.innerHTML = `${T.err} <a href="mailto:josechavarin@kbklandscape.com?subject=Quote%20request&body=${body}">Email</a>`;
      msg.className = 'form-msg err';
    } finally { btn.disabled = false; btn.textContent = label; }
  });

  // Current year
  $$('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
