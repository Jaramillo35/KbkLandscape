// Single source of truth. Business facts and every sentence of body copy come
// from copy.json (exported from the previous site's build.py, EN + ES) and the
// photo manifest. Only short interface labels are added here.
import copy from './copy.json';
import manifest from '../../public/assets/img/projects/manifest.json';

export const biz = {
  name: 'KBK Landscape & Beyond',
  legal: 'KBK Landscape & Beyond LLC',
  url: 'https://kbklandscape.com',
  tel: '+15864895613',
  telText: '(586) 489-5613',
  email: 'josechavarin@kbklandscape.com',
  street: '20752 Miles St S',
  city: 'Clinton Township',
  region: 'MI',
  zip: '48036',
  google: 'https://www.google.com/maps?cid=13843601923157048672',
  facebook: 'https://www.facebook.com/kbkoutdoorservices',
  mapEmbed: copy.MAP_EMBED,
};

// Contact form. Default is the existing KBK Office lead endpoint (already live).
// To use Web3Forms instead, paste its access key here; the form then posts to
// https://api.web3forms.com/submit with the same fields.
export const form = {
  endpoint: copy.LEADS_URL,
  web3formsKey: '',
};

// The six featured projects (brief), in gallery order. `svc` = index into services.
export const featured = [
  { id: 'patio-grand-stairs', svc: 0 },
  { id: 'kitchen-bar', svc: 2, video: 'kitchen' },
  { id: 'firepit-pavers', svc: 1, video: 'firepit' },
  { id: 'garden-front', svc: 4, video: 'garden' },
  { id: 'lighting-facade', svc: 5, video: 'dusk-lights' },
  { id: 'pool-modern', svc: 0, video: 'pool' },
];

// Media shown for each of the six home-page service rows.
const svcMedia = [
  { type: 'img', id: 'patio-grand-stairs' },
  { type: 'video', src: 'firepit', id: 'firepit-pavers' },
  { type: 'video', src: 'kitchen', id: 'kitchen-bar' },
  { type: 'img', id: 'garden-terraces' },
  { type: 'video', src: 'garden', id: 'garden-front' },
  { type: 'video', src: 'dusk-lights', id: 'lighting-facade' },
];

const ui = {
  en: {
    skip: 'Skip to content', menu: 'Menu', scroll: 'Scroll', view: 'View', drag: 'Drag', call: 'Call',
    philosophy: 'How we work', project: 'Project', viewProject: 'View project', next: 'Next project', back: 'All projects',
    dusk: 'Dusk', lit: 'Lights on', duskHint: 'Drag to bring the lights on', duskLabel: 'Lighting level',
    blueprint: 'Drawn', built: 'Built', hoursShort: 'Mon–Fri 7:30–6:30 · Sat 8–3',
    hoursRows: ['Mon–Fri 7:30–6:30', 'Sat 8–3'], office: 'Office', email: 'Email', also: 'Also',
    included: 'What it includes', close: 'Close', prevNext: 'Reviews', lake: 'Lake St. Clair',
    oakland: 'Oakland County', macomb: 'Macomb County', location: 'Location', service: 'Service',
    sending: 'Sending…', ok: 'Thanks! Jose will get back to you within one business day.',
    err: 'Sorry, that did not go through. Please call (586) 489-5613 or email josechavarin@kbklandscape.com.',
    vName: 'Please enter your name.', vPhone: 'Please enter a phone number we can reach you at.', vEmail: 'That email address does not look right.',
    stats: [['4.9', 'from 600+ reviews', true], ['2009', 'Family-owned since'], ['3-year', 'paver warranty']],
  },
  es: {
    skip: 'Ir al contenido', menu: 'Menú', scroll: 'Bajar', view: 'Ver', drag: 'Arrastre', call: 'Llamar',
    philosophy: 'Cómo trabajamos', project: 'Proyecto', viewProject: 'Ver proyecto', next: 'Siguiente proyecto', back: 'Todos los proyectos',
    dusk: 'Atardecer', lit: 'Luces encendidas', duskHint: 'Arrastre para encender las luces', duskLabel: 'Nivel de iluminación',
    blueprint: 'Dibujado', built: 'Construido', hoursShort: 'Lun–Vie 7:30–6:30 · Sáb 8–3',
    hoursRows: ['Lun–Vie 7:30–6:30', 'Sáb 8–3'], office: 'Oficina', email: 'Correo', also: 'También',
    included: 'Qué incluye', close: 'Cerrar', prevNext: 'Reseñas', lake: 'Lago St. Clair',
    oakland: 'Condado de Oakland', macomb: 'Condado de Macomb', location: 'Ubicación', service: 'Servicio',
    sending: 'Enviando…', ok: '¡Gracias! Jose se comunicará con usted en un día hábil.',
    err: 'No se pudo enviar. Por favor llame al (586) 489-5613 o escriba a josechavarin@kbklandscape.com.',
    vName: 'Escriba su nombre.', vPhone: 'Escriba un teléfono donde podamos llamarle.', vEmail: 'Ese correo no parece correcto.',
    stats: [['4.9', 'en más de 600 reseñas', true], ['2009', 'Empresa familiar desde'], ['3 años', 'de garantía en adoquín']],
  },
};

const byId = Object.fromEntries(manifest.map((m) => [m.id, m]));
export const photos = manifest;

export function getT(lang = 'en') {
  const c = copy.C[lang];
  const u = ui[lang];
  const p = lang === 'es' ? '/es' : '';
  const href = (page) => (page === 'index' ? `${p}/` : `${p}/${page}.html`);
  const photo = (id) => ({ ...byId[id], label: byId[id][lang] });

  const services = c.services.map(([img, name, text, list], i) => ({ i, slug: `s${i}`, img, name, text, list }));

  return {
    lang, c, u, href, photo, prefix: p,
    home: href('index'),
    alt: lang === 'es'
      ? { prefix: '', label: 'EN', title: 'English', hreflang: 'en' }
      : { prefix: '/es', label: 'ES', title: 'Español', hreflang: 'es' },
    nav: ['services', 'projects', 'about', 'contact'].map((k) => [c.nav[k], href(k), k]),
    quote: c.quote,
    services,
    homeServices: services.slice(0, 6).map((s, i) => ({ ...s, media: svcMedia[i], photo: photo(svcMedia[i].id) })),
    featured: featured.map((f, n) => ({ ...f, n, photo: photo(f.id), service: services[f.svc], href: `${p}/projects/${f.id}.html` })),
    reviews: c.reviews.items.map(([text, name, what]) => ({ text, name, what })),
    title: (page) => c.titles[page],
    desc: (page) => c.desc[page],
  };
}

// Approximate town positions (lat, lon) for the hand-drawn service-area map.
export const towns = [
  ['Clinton Township', 42.587, -82.92, true], ['Macomb', 42.7, -82.96], ['Shelby Twp', 42.671, -83.033], ['Sterling Heights', 42.58, -83.03],
  ['Rochester Hills', 42.658, -83.15], ['Rochester', 42.681, -83.134], ['Troy', 42.58, -83.143], ['Bloomfield Hills', 42.584, -83.245],
  ['Birmingham', 42.547, -83.211], ['Royal Oak', 42.49, -83.145], ['Farmington Hills', 42.485, -83.377], ['Grosse Pointe', 42.386, -82.912],
  ['St. Clair Shores', 42.497, -82.889], ['Warren', 42.49, -83.03], ['Utica', 42.626, -83.033], ['Washington Twp', 42.724, -83.036],
  ['Chesterfield', 42.663, -82.842], ['West Bloomfield', 42.569, -83.383],
];
