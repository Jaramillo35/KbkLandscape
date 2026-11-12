import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { SplitText } from 'gsap/SplitText';
import Lenis from 'lenis';

gsap.registerPlugin(ScrollTrigger, SplitText);

const root = document.documentElement;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
const desktop = matchMedia('(min-width: 64rem)');
const saveData = navigator.connection && navigator.connection.saveData;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const lineSplit = (el) => new SplitText(el, { type: 'lines', mask: 'lines', linesClass: 'split-line', aria: 'none' });

// Everything below the first screen is set up in small slices after first
// paint, so no single task blocks the main thread.
const tasks = [];
const defer = (fn) => tasks.push(fn);

/* ---------- Smooth scroll: desktop fine pointers only ---------- */
let lenis = null;
if (fine && !reduce) {
  lenis = new Lenis({ duration: 1.1, anchors: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
}

/* ---------- Video: load when near, play in view, pause off-screen ---------- */
const small = matchMedia('(max-width: 47.99rem)').matches;
function prime(v) { if (v.dataset.poster && !v.poster) v.poster = v.dataset.poster; }
function playVideo(v) {
  prime(v);
  if (reduce || saveData) return;
  if (v.dataset.src && !v.src) { v.src = (small && v.dataset.srcSm) || v.dataset.src; v.load(); }
  const p = v.play();
  if (p) p.catch(() => {});
}
$$('video').forEach((v) => v.addEventListener('playing', () => v.classList.add('is-playing'), { once: true }));
// film starts only once the page itself has finished loading
const startFilm = () => $$('[data-video], video[data-auto]').forEach((v) => {
  new IntersectionObserver(([e]) => (e.isIntersecting ? playVideo(v) : v.pause()), { threshold: 0.05 }).observe(v);
});
const afterLoad = (fn) => (document.readyState === 'complete' ? fn() : addEventListener('load', fn, { once: true }));
afterLoad(() => setTimeout(startFilm, 1200));

/* ---------- Header ---------- */
const hdr = $('[data-hdr]');
const burger = $('.burger');
const nav = $('#nav');
const callbar = $('.callbar');
const first = $('main > *');
const darkTop = first && first.matches('.hero, .phero');
let lastY = 0;
function onScroll() {
  const y = window.scrollY;
  const edge = darkTop ? first.offsetHeight - hdr.offsetHeight : -1;
  hdr.classList.toggle('is-solid', y > edge);
  // hide on the way down, return on the way up
  hdr.classList.toggle('is-hidden', y > window.innerHeight * 0.9 && y > lastY + 4 && !nav.classList.contains('is-open'));
  if (y < lastY - 4) hdr.classList.remove('is-hidden');
  callbar.classList.toggle('is-on', !first.matches('.hero') || y > window.innerHeight * 0.5);
  lastY = y;
}
addEventListener('scroll', onScroll, { passive: true });
onScroll();

function setMenu(open) {
  nav.classList.toggle('is-open', open);
  hdr.classList.toggle('menu-open', open);
  burger.setAttribute('aria-expanded', String(open));
  document.body.style.overflow = open ? 'hidden' : '';
  if (lenis) open ? lenis.stop() : lenis.start();
}
burger.addEventListener('click', () => setMenu(!nav.classList.contains('is-open')));
addEventListener('keydown', (e) => e.key === 'Escape' && setMenu(false));
desktop.addEventListener('change', () => setMenu(false));

/* ---------- Page intro: headline rises, drawing draws ---------- */
// Text is hidden here, at once and under cover, then revealed after `delay`.
function pageIn(delay = 0) {
  const h1 = $('main [data-split]');
  const ins = $$('main [data-in]');
  if (reduce || !h1) return root.classList.add('ready');

  const split = lineSplit(h1);
  gsap.set(split.lines, { yPercent: 108 });
  gsap.set(ins, { autoAlpha: 0, y: 18 });
  root.classList.add('ready');

  gsap.timeline({ delay, defaults: { ease: 'expo.out' } })
    .to(split.lines, { yPercent: 0, duration: 1.25, stagger: 0.09 }, 0.05)
    .to(ins, { autoAlpha: 1, y: 0, duration: 0.9, stagger: 0.07 }, 0.4)
    .to($$('.hero-plan [pathLength], .phero-art [pathLength]'), { strokeDashoffset: 0, duration: 1.8, stagger: 0.12, ease: 'power2.inOut' }, 0.4)
    .add(() => split.revert()); // release the masks so descenders are never clipped

  const hero = $('[data-hero]');
  if (hero) {
    // depth: film drifts slower than the page, copy lifts away
    gsap.to('[data-hero-media]', { yPercent: 9, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.hero-in', { yPercent: -8, autoAlpha: 0.2, ease: 'none', scrollTrigger: { trigger: hero, start: '35% top', end: 'bottom top', scrub: true } });
  }
}

/* ---------- Load sequence (first visit) and page transitions (after) ---------- */
const wipe = $('.wipe');
function boot() {
  const loader = $('.loader');
  if (reduce || root.classList.contains('no-anim')) return pageIn();
  if (root.classList.contains('seen')) {
    // arriving from another page: the green sheet lifts away
    gsap.to(wipe, { clipPath: 'inset(0 0 100% 0)', duration: 0.7, ease: 'expo.inOut' });
    return pageIn(0.25);
  }
  try { sessionStorage.setItem('kbk-seen', '1'); } catch (e) {}
  const tl = gsap.timeline()
    .to($$('[pathLength]', loader), { strokeDashoffset: 0, duration: 0.7, stagger: 0.08, ease: 'power2.inOut' })
    .to(loader, { clipPath: 'inset(0 0 100% 0)', duration: 0.85, ease: 'expo.inOut' }, '+=0.1')
    .set(loader, { display: 'none' });
  pageIn(tl.duration() - 0.55);
}
(document.fonts && document.fonts.ready ? Promise.race([document.fonts.ready, new Promise((r) => setTimeout(r, 1200))]) : Promise.resolve()).then(boot);

if (!reduce && wipe) {
  document.addEventListener('click', (e) => {
    const a = e.target.closest && e.target.closest('a[href]');
    if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.target || a.hasAttribute('download')) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || !/^https?:$/.test(url.protocol)) return;
    if (url.pathname === location.pathname && url.hash) return; // in-page anchor
    e.preventDefault();
    setMenu(false);
    try { sessionStorage.setItem('kbk-seen', '1'); } catch (err) {}
    gsap.fromTo(wipe, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: 0.5, ease: 'expo.inOut', onComplete: () => (location.href = url.href) });
  });
  // back/forward cache: never come back to a covered page
  addEventListener('pageshow', (e) => e.persisted && gsap.set(wipe, { clipPath: 'inset(0 0 100% 0)' }));
}

/* ---------- Scroll reveals ---------- */
if (!reduce) {
  defer(() => {
  $$('[data-split-scroll]').forEach((el) => {
    const s = lineSplit(el);
    gsap.from(s.lines, { yPercent: 108, duration: 1.15, stagger: 0.09, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 88%', once: true }, onComplete: () => s.revert() });
  });

  });
  defer(() => {
  const rises = $$('[data-rise]');
  gsap.set(rises, { autoAlpha: 0, y: 22 });
  ScrollTrigger.batch(rises, { start: 'top 93%', once: true, onEnter: (b) => gsap.to(b, { autoAlpha: 1, y: 0, duration: 0.9, ease: 'expo.out', stagger: 0.07, overwrite: true }) });

  });
  defer(() => {
  // image reveals: the frame opens upward, the picture settles
  $$('[data-clip]').forEach((el) => {
    const st = { trigger: el, start: 'top 90%', once: true };
    gsap.fromTo(el, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: 1.3, ease: 'expo.inOut', scrollTrigger: st });
    const m = $('img:not([data-parallax-img]), video', el);
    if (m) gsap.fromTo(m, { scale: 1.16 }, { scale: 1, duration: 1.9, ease: 'expo.out', scrollTrigger: st });
  });
  $$('[data-parallax-img]').forEach((img) => {
    gsap.fromTo(img, { yPercent: -5, scale: 1.12 }, { yPercent: 5, scale: 1.12, ease: 'none', scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  $$('[data-parallax]').forEach((el) => {
    gsap.to(el, { yPercent: +el.dataset.parallax, ease: 'none', scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  });
  defer(() => {
  // philosophy: the sentence comes into focus word by word as you read down
  $$('[data-words]').forEach((el) => {
    const s = new SplitText(el, { type: 'words', wordsClass: 'w', aria: 'none' });
    gsap.fromTo(s.words, { opacity: 0.5 }, { opacity: 1, stagger: 0.1, ease: 'none', scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 48%', scrub: true } });
  });

  });
  defer(() => {
  // drawings that draw themselves
  $$('[data-draw-scroll]').forEach((svg) => {
    gsap.fromTo($$('[pathLength]', svg), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 2.2, stagger: 0.25, ease: 'power2.inOut', scrollTrigger: { trigger: svg, start: 'top 80%', once: true } });
  });
  const pavers = $$('[data-paver]');
  if (pavers.length) {
    gsap.fromTo(pavers, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.4, ease: 'power2.out', stagger: { each: 0.008, from: 'end' }, scrollTrigger: { trigger: '[data-promise]', start: 'top 75%', once: true } });
  }
  });
  defer(() => {
  const proc = $('[data-process] .steps');
  if (proc) {
    gsap.fromTo('[data-line]', { strokeDashoffset: 1 }, { strokeDashoffset: 0, ease: 'none', scrollTrigger: { trigger: proc, start: 'top 78%', end: 'top 30%', scrub: 0.6 } });
    gsap.fromTo('[data-rail]', { scaleY: 0 }, { scaleY: 1, ease: 'none', scrollTrigger: { trigger: proc, start: 'top 75%', end: 'bottom 60%', scrub: 0.4 } });
    $$('[data-step]', proc).forEach((li, i) => {
      gsap.from(li, { autoAlpha: 0, y: 26, duration: 0.9, ease: 'expo.out', delay: desktop.matches ? i * 0.12 : 0, scrollTrigger: { trigger: desktop.matches ? proc : li, start: 'top 80%', once: true } });
    });
  }
  });
  defer(() => {
  const map = $('.map');
  if (map) {
    const st = { trigger: map, start: 'top 80%', once: true };
    gsap.fromTo($$('.map-lines [pathLength]:not(.dash)', map), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.8, stagger: 0.15, ease: 'power2.inOut', scrollTrigger: st });
    gsap.from($$('.map-pt circle', map), { scale: 0.2, autoAlpha: 0, transformOrigin: 'center', duration: 0.6, stagger: 0.04, ease: 'back.out(2)', delay: 0.6, scrollTrigger: st });
    gsap.from($$('text, .dash', map), { autoAlpha: 0, duration: 0.8, delay: 1, scrollTrigger: st });
  }
  const rows = $$('.svc-row');
  if (rows.length) gsap.from(rows, { autoAlpha: 0, y: 28, duration: 0.9, stagger: 0.07, ease: 'expo.out', scrollTrigger: { trigger: '.svc-list', start: 'top 84%', once: true } });
  });
}

/* ---------- Services: six rows, one stage ---------- */
defer(function services() {
  const sec = $('[data-services]');
  if (!sec) return;
  const list = $('.svc-list', sec);
  const rows = $$('.svc-row', sec);
  const layers = $$('.svc-layer', sec);
  const caps = $$('[data-cap]', sec);
  const count = $('[data-count]', sec);
  let active = -1;

  function media(i, on) {
    const v = desktop.matches ? $('video', layers[i]) : $('.svc-inline video', rows[i]);
    if (v) on ? playVideo(v) : v.pause();
  }
  function setActive(i) {
    if (i === active) return;
    const prev = active;
    active = i;
    rows.forEach((r, n) => {
      r.classList.toggle('is-active', n === i);
      $('.svc-btn', r).setAttribute('aria-expanded', String(n === i));
    });
    list.classList.toggle('has-active', i > -1);
    layers.forEach((l, n) => {
      l.classList.remove('is-prev');
      if (n === prev && i > -1) l.classList.add('is-prev');
      l.classList.toggle('is-active', n === i);
    });
    caps.forEach((c, n) => c.classList.toggle('is-active', n === i));
    if (count && i > -1) count.textContent = String(i + 1).padStart(2, '0');
    if (prev > -1) media(prev, false);
    if (i > -1) media(i, true);
    setTimeout(() => ScrollTrigger.refresh(), 620); // panel height changed
  }
  rows.forEach((row, i) => {
    const btn = $('.svc-btn', row);
    if (fine) row.addEventListener('pointerenter', () => desktop.matches && setActive(i));
    btn.addEventListener('focus', () => desktop.matches && setActive(i));
    btn.addEventListener('click', () => {
      if (desktop.matches && fine) {
        // on desktop the row is already open from hover: a click goes through to the service
        if (active === i) return $('.lnk-arrow', row).click();
        return setActive(i);
      }
      setActive(active === i ? -1 : i);
    });
  });
  // posters are fetched only when the section is near, and only for the layout in use
  new IntersectionObserver(([e], io) => {
    if (!e.isIntersecting) return;
    $$('video', sec).forEach((v) => (desktop.matches ? !v.closest('.svc-inline') : !!v.closest('.svc-inline')) && prime(v));
    io.disconnect();
  }, { rootMargin: '800px' }).observe(sec);
  let primed = false;
  new IntersectionObserver(([e]) => {
    if (e.isIntersecting && !primed) { primed = true; if (desktop.matches) setActive(0); }
    if (active > -1) media(active, e.isIntersecting);
  }, { threshold: 0.15 }).observe(sec);
});

/* ---------- Featured work: blueprint to built, then a pinned horizontal walk ---------- */
defer(function work() {
  const sec = $('[data-work]');
  if (!sec || reduce) return;
  const track = $('[data-track]', sec);
  const plan = $('[data-plan]', sec);
  const planImg = plan && $('img', plan.parentElement);
  const tagA = $('[data-tag-a]', sec), tagB = $('[data-tag-b]', sec);
  const built = (on) => { tagA.classList.toggle('is-on', !on); tagB.classList.toggle('is-on', on); };

  // 1) the drawing draws itself as the section arrives
  gsap.set(planImg, { clipPath: 'inset(0 0 100% 0)' });
  gsap.set('.plan-tag', { opacity: 1 });
  built(false);
  const draw = gsap.timeline({ paused: true })
    .set(plan, { opacity: 1 })
    .fromTo($$('.plan-main [pathLength]', plan), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.3, stagger: 0.14, ease: 'power2.inOut' })
    .fromTo($$('.plan-thin [pathLength]', plan), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.3, stagger: 0.2, ease: 'power2.inOut' }, '-=0.9');
  ScrollTrigger.create({ trigger: sec, start: 'top 65%', once: true, onEnter: () => draw.play() });

  const mm = gsap.matchMedia();
  mm.add('(min-width: 64rem)', () => {
    // 2) pinned: the photo rises through the drawing, then the gallery travels
    const dist = () => Math.max(0, track.scrollWidth - window.innerWidth);
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: sec, pin: $('.work-pin', sec), start: 'top top', end: () => `+=${dist() + window.innerHeight * 0.7}`,
        scrub: 0.6, invalidateOnRefresh: true, anticipatePin: 1,
        onUpdate: (self) => built(self.progress > 0.09),
      },
    });
    tl.to(planImg, { clipPath: 'inset(0 0 0% 0)', duration: 0.7, ease: 'none' }, 0)
      .to(plan, { opacity: 0, duration: 0.35, ease: 'none' }, 0.45)
      .to(track, { x: () => -dist(), duration: 3, ease: 'none' }, 0.8)
      .to('[data-bar]', { scaleX: 1, duration: 3.8, ease: 'none' }, 0);
    $$('[data-card]', sec).forEach((card, i) => {
      const img = $('img', card);
      if (i > 0) tl.fromTo(img, { xPercent: -5, scale: 1.12 }, { xPercent: 5, scale: 1.12, duration: 3, ease: 'none' }, 0.8);
    });
    return () => { gsap.set([track, '[data-bar]'], { clearProps: 'all' }); };
  });
  mm.add('(max-width: 63.99rem)', () => {
    // phones and tablets: native swipe; the morph simply plays after the drawing
    const t = gsap.timeline({ scrollTrigger: { trigger: sec, start: 'top 40%', once: true }, delay: 1.6, onStart: () => built(true) })
      .to(planImg, { clipPath: 'inset(0 0 0% 0)', duration: 1.4, ease: 'expo.inOut' })
      .to(plan, { opacity: 0, duration: 0.8 }, '-=0.6');
    return () => t.kill();
  });
});

/* ---------- Day to dusk: drag to bring the lights on ---------- */
defer(function dusk() {
  const stage = $('[data-stage]');
  if (!stage) return;
  const range = $('[data-range]', stage);
  const state = { p: 0.2 };
  let touched = false, grab = 0;
  const render = () => { stage.style.setProperty('--p', state.p.toFixed(4)); range.value = Math.round(state.p * 100); };
  const set = (v) => { state.p = clamp(v, 0.03, 0.97); render(); };
  const at = (e) => { const r = stage.getBoundingClientRect(); return (e.clientX - r.left - grab) / r.width; };

  stage.addEventListener('pointerdown', (e) => {
    if (e.button) return;
    touched = true;
    gsap.killTweensOf(state);
    const r = stage.getBoundingClientRect();
    const hx = r.left + state.p * r.width;
    grab = Math.abs(e.clientX - hx) < 36 ? e.clientX - hx : 0; // respect where the handle was grabbed
    stage.setPointerCapture(e.pointerId);
    stage.classList.add('is-drag');
    set(at(e));
  });
  stage.addEventListener('pointermove', (e) => stage.hasPointerCapture(e.pointerId) && set(at(e)));
  const end = (e) => { stage.classList.remove('is-drag'); if (stage.hasPointerCapture(e.pointerId)) stage.releasePointerCapture(e.pointerId); };
  stage.addEventListener('pointerup', end);
  stage.addEventListener('pointercancel', end);
  range.addEventListener('input', () => { touched = true; gsap.killTweensOf(state); set(range.value / 100); });

  if (reduce) return set(0.6);
  // a hint: the lights come part-way on by themselves, once
  ScrollTrigger.create({ trigger: stage, start: 'top 62%', once: true, onEnter: () => !touched && gsap.to(state, { p: 0.62, duration: 1.8, ease: 'power3.inOut', onUpdate: render }) });
});

/* ---------- Reviews: one at a time, slow crossfade ---------- */
defer(function reviews() {
  const sec = $('[data-reviews]');
  if (!sec) return;
  const quotes = $$('[data-quote]', sec), dots = $$('[data-dot]', sec);
  let i = 0, timer = null, visible = false, held = false;
  const go = (n) => {
    i = (n + quotes.length) % quotes.length;
    quotes.forEach((q, k) => { q.classList.toggle('is-active', k === i); q.setAttribute('aria-hidden', String(k !== i)); });
    dots.forEach((d, k) => d.setAttribute('aria-pressed', String(k === i)));
  };
  const tick = () => { clearInterval(timer); if (visible && !held && !reduce) timer = setInterval(() => go(i + 1), 7000); };
  dots.forEach((d, k) => d.addEventListener('click', () => { go(k); tick(); }));
  sec.addEventListener('pointerenter', () => { held = true; tick(); });
  sec.addEventListener('pointerleave', () => { held = false; tick(); });
  sec.addEventListener('focusin', () => { held = true; tick(); });
  sec.addEventListener('focusout', () => { held = false; tick(); });
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; tick(); }, { threshold: 0.3 }).observe(sec);
});

/* ---------- Service area: town list and map point light each other ---------- */
defer(function area() {
  const sec = $('[data-area]');
  if (!sec) return;
  const on = (i, v) => { $(`[data-town="${i}"]`, sec)?.classList.toggle('is-on', v); $(`[data-pt="${i}"]`, sec)?.classList.toggle('is-on', v); };
  $$('[data-town], [data-pt]', sec).forEach((el) => {
    const i = el.dataset.town ?? el.dataset.pt;
    el.addEventListener('pointerenter', () => on(i, true));
    el.addEventListener('pointerleave', () => on(i, false));
  });
});

/* ---------- Our work: filters and lightbox ---------- */
defer(function gallery() {
  const gal = $('[data-gallery]');
  if (!gal) return;
  const items = $$('.gal-item', gal), filters = $$('[data-filter]', gal), box = $('[data-lightbox]');
  filters.forEach((b) => b.addEventListener('click', () => {
    filters.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    items.forEach((it) => { it.hidden = b.dataset.filter !== 'all' && it.dataset.cat !== b.dataset.filter; });
    ScrollTrigger.refresh();
  }));
  items.filter((it) => it.dataset.full).forEach((it) => it.addEventListener('click', () => {
    const img = $('img', it);
    $('img', box).src = it.dataset.full;
    $('img', box).alt = img.alt;
    $('p', box).textContent = img.alt;
    box.showModal();
  }));
  box.addEventListener('click', (e) => e.target === box && box.close());
});

/* ---------- Quote form: inline validation, JSON post, email fallback ---------- */
defer(function quoteForm() {
  const form = $('[data-form]');
  if (!form) return;
  const msg = $('.form-msg', form), btn = $('button[type=submit]', form), label = $('span', btn);
  const fields = $$('input[data-msg]', form);
  const check = (f) => {
    const v = f.value.trim();
    const bad = (f.required && !v) || (v && !f.checkValidity());
    f.setAttribute('aria-invalid', String(!!bad));
    $(`#${f.id}-e`, form).textContent = bad ? f.dataset.msg : '';
    return !bad;
  };
  fields.forEach((f) => {
    f.addEventListener('blur', () => (f.value || f.dataset.touched) && check(f));
    f.addEventListener('input', () => { f.dataset.touched = '1'; if (f.getAttribute('aria-invalid') === 'true') check(f); });
  });
  // previews (anything that is not the live domain) post to a local KBK Office, never the real one
  let action = form.action;
  if (!location.hostname.endsWith('kbklandscape.com')) action = `http://${location.hostname}:8800/kbk-api/leads`;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const ok = fields.map(check);
    if (ok.includes(false)) return fields[ok.indexOf(false)].focus();
    if ($('.hp input', form).value) return; // honeypot: bots fill it, people don't
    const data = Object.fromEntries(new FormData(form).entries());
    data.services = $$('input[name=services]:checked', form).map((i) => i.value);
    data.lang = root.lang; data.page = location.pathname;
    delete data.website;
    const text = label.textContent;
    btn.disabled = true; label.textContent = form.dataset.sending;
    msg.textContent = ''; msg.className = 'form-msg';
    try {
      const key = form.dataset.key;
      const r = await fetch(key ? 'https://api.web3forms.com/submit' : action, {
        method: 'POST', headers: { 'content-type': 'application/json', accept: 'application/json' },
        body: JSON.stringify(key ? { access_key: key, subject: `Quote request: ${data.name}`, from_name: 'kbklandscape.com', ...data, services: data.services.join(', ') } : data),
      });
      if (!r.ok) throw new Error(r.status);
      msg.textContent = form.dataset.ok;
      form.reset();
      fields.forEach((f) => f.removeAttribute('aria-invalid'));
    } catch (err) {
      const body = encodeURIComponent(`${data.name}\n${data.phone}\n${data.address || ''}\n\n${data.services.join(', ')}\n\n${data.details || ''}`);
      msg.textContent = `${form.dataset.err} `;
      const a = document.createElement('a');
      a.href = `mailto:josechavarin@kbklandscape.com?subject=Quote%20request&body=${body}`;
      a.textContent = 'Email';
      msg.append(a);
      msg.className = 'form-msg is-err';
    } finally { btn.disabled = false; label.textContent = text; }
  });
});

/* ---------- Cursor: a brass disc that names the action ---------- */
defer(function cursor() {
  const el = $('.cursor');
  if (!el || !fine || reduce) return;
  const label = $('.cursor-label', el);
  const xTo = gsap.quickTo(el, 'x', { duration: 0.45, ease: 'power3.out' });
  const yTo = gsap.quickTo(el, 'y', { duration: 0.45, ease: 'power3.out' });
  gsap.set(el, { x: -100, y: -100, scale: 0.12 });
  let over = null;
  addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'mouse') return;
    xTo(e.clientX); yTo(e.clientY);
    const t = e.target.closest ? e.target.closest('[data-cursor]') : null;
    if (t === over) return;
    over = t;
    el.classList.toggle('is-on', !!t);
    el.classList.toggle('has-label', !!t);
    if (t) label.textContent = t.dataset.cursor;
    gsap.to(el, { scale: t ? 1 : 0.12, duration: 0.45, ease: 'expo.out', overwrite: 'auto' });
  }, { passive: true });
  document.addEventListener('pointerleave', () => el.classList.remove('is-on'));
});

(async () => {
  await new Promise((r) => setTimeout(r, 0));
  for (const fn of tasks) { fn(); await new Promise((r) => setTimeout(r, 0)); }
  ScrollTrigger.refresh();
})();
addEventListener('load', () => ScrollTrigger.refresh());
