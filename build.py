#!/usr/bin/env python3
"""Generates the site: English pages at the root, Spanish pages under /es/.

    python3 build.py

Edit the copy in the C dict below, run the script, commit the generated HTML.
Photos and captions come from assets/img/projects/manifest.json.
"""
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent
# Preview builds: KBK_BASE=/kbk-preview KBK_OUT=/path python3 build.py  (paths rebased, noindex)
BASE = os.environ.get("KBK_BASE", "").rstrip("/")
OUT = Path(os.environ.get("KBK_OUT", ROOT))
SITE = "https://kbklandscape.com"
PHONE = "(586) 489-5613"
TEL = "+15864895613"
EMAIL = "josechavarin@kbklandscape.com"
ADDRESS = "20752 Miles St S, Clinton Township, MI 48036"
FACEBOOK = "https://www.facebook.com/kbkoutdoorservices"
GOOGLE = "https://www.google.com/maps?cid=13843601923157048672"
# Lead endpoint: KBK Office on the Pi, published with Tailscale Funnel.
LEADS_URL = "https://raspberrypi-1.tail0107e4.ts.net/kbk-api/leads"
MAP_EMBED = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2937.723192444613!2d-82.91382498458115!3d42.58239747917254"
             "!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8824df67db270921%3A0xc01e5a9a41b0bd60"
             "!2sKBK%20Landscape%20%26%20Beyond%20LLC!5e0!3m2!1sen!2sus!4v1680016573812!5m2!1sen!2sus")

MANIFEST = json.loads((ROOT / "assets/img/projects/manifest.json").read_text())
PAGES = ["index", "services", "projects", "about", "contact"]

C = {
"en": {
  "nav": {"index": "Home", "services": "Services", "projects": "Our work", "about": "About", "contact": "Contact"},
  "quote": "Get a free quote", "call": "Call", "lang_btn": "ES", "lang_label": "Español",
  "hours": "Mon–Fri 7:30–6:30 · Sat 8–3",
  "area_line": "Clinton Township · Macomb & Oakland counties",
  "titles": {
    "index": "KBK Landscape & Beyond | Paver patios, fire pits & landscaping in Clinton Township, MI",
    "services": "Services | KBK Landscape & Beyond",
    "projects": "Our work | KBK Landscape & Beyond",
    "about": "About Jose and the crew | KBK Landscape & Beyond",
    "contact": "Get a free quote | KBK Landscape & Beyond",
  },
  "desc": {
    "index": "Family-owned hardscape and landscape company in Clinton Township, MI since 2009. Paver patios, fire pits, outdoor kitchens, retaining walls and planting, with a 3-year paver warranty. 4.9 stars from 600+ reviews.",
    "services": "Paver patios and walkways, fire pits, outdoor kitchens, retaining walls, landscape design, lighting, irrigation and paver sealing in Macomb and Oakland counties.",
    "projects": "Photos of patios, fire pits, outdoor kitchens, lighting and landscapes built by KBK Landscape & Beyond across metro Detroit.",
    "about": "Jose Chavarin has led KBK Landscape & Beyond since 2009. Meet the crew behind 600+ five-star reviews.",
    "contact": "Request a free on-site estimate from KBK Landscape & Beyond. Call (586) 489-5613 or send us your project details.",
  },
  "hero": {
    "h1": "Outdoor spaces built to last, by a crew that shows up.",
    "lede": "Paver patios, fire pits, outdoor kitchens and landscapes across Macomb and Oakland counties. Jose is on every job, from the first estimate to the last sweep.",
    "cta2": "See our work",
    "proof": [("4.9 ★", "600+ customer reviews"), ("2009", "Family-owned since"), ("3 yrs", "Paver warranty")],
  },
  "services_intro": {"eyebrow": "What we do", "h2": "One crew for the whole backyard", "p": "Design, hardscape and planting under one roof, so nothing gets lost between contractors."},
  "services": [
    ("patio-modern", "Paver patios & walkways", "Brick, concrete and porcelain pavers laid on a proper compacted base, with borders and inlays that make it yours.", ["Patios, walkways and porches", "Driveways and driveway aprons", "Steps and landings", "Circle kits, inlays and borders"]),
    ("fire-pit-patio", "Fire pits & fireplaces", "Gas or wood, round or square, with seating walls so the whole family fits around it.", ["Gas and wood-burning fire pits", "Outdoor fireplaces", "Seating walls and columns", "Natural-stone caps"]),
    ("kitchen-grill", "Outdoor kitchens & bars", "Built-in grills, counters and bars in stone or block, sized for how you actually cook outside.", ["Built-in grill islands", "Bars and counters", "Pizza ovens and smokers", "Lighting and power"]),
    ("garden-terraces", "Retaining walls & steps", "Walls that hold a slope for decades, with proper drainage behind them, plus steps that are safe at night.", ["Block, boulder and timber walls", "Terracing on slopes", "Garden walls and edging", "Drainage and grading"]),
    ("garden-path", "Landscape design & planting", "Beds, trees, shrubs and perennials picked for Michigan winters, planted right, and mulched to finish.", ["Front and back yard design", "Trees, shrubs and perennials", "Sod and seeding", "Mulch, river rock and edging"]),
    ("lighting-steps", "Landscape lighting", "Low-voltage LED lighting for paths, steps, trees and the front of the house. Safer, and it looks great from the street.", ["Path and step lights", "Up-lighting for trees and facades", "Paver-integrated lights", "Timers and smart controls"]),
    ("patio-sealed", "Paver cleaning, sealing & repair", "Bring an old patio back: power washing, re-sanding, sealing and re-levelling sunken sections.", ["Power washing and re-sanding", "Sealing (wet look or natural)", "Re-levelling and repairs", "Weed and moss control"]),
    ("garden-drybed", "Irrigation, drainage & maintenance", "Sprinkler systems, drainage fixes for soggy yards, and seasonal cleanups to keep everything looking new.", ["Sprinkler installation and repair", "French drains and dry creek beds", "Spring and fall cleanups", "Shrub trimming and bed care"]),
  ],
  "more": "Learn more",
  "why": {"eyebrow": "Why homeowners pick KBK", "h2": "The owner is on your job, every day",
    "p": "Jose Chavarin started KBK in 2009 and still runs the crew himself. You get one person who answers the phone, remembers what you asked for, and is there when the last paver goes in.",
    "list": ["Free on-site estimates with a clear written price", "Clean job sites and honest timelines, usually a patio in under a week", "Fully insured, with warranties in writing", "Fair pricing: customers often tell us we came in well under other quotes"]},
  "warranty": {"eyebrow": "Our promise", "h2": "Warranties that mean something",
    "items": [("3 years", "on every new paver installation"), ("1 year", "on every tree and plant we install"), ("Free", "on-site estimates, no pressure")]},
  "steps": {"eyebrow": "How it works", "h2": "From idea to finished backyard", "items": [
    ("Call or send photos", "Tell us what you have in mind. A few phone photos of the space are enough to start."),
    ("On-site visit", "Jose measures, listens, and suggests what will work with your yard and budget."),
    ("Written quote", "A clear price with materials named, usually within a few days. No surprises later."),
    ("We build it", "A tidy crew, a realistic schedule, and a walkthrough with you at the end."),
  ]},
  "work": {"eyebrow": "Recent work", "h2": "Built in your neighborhood", "all": "See all projects"},
  "reviews": {"eyebrow": "Reviews", "h2": "What customers say", "src": "Reviews from Google", "items": [
    ("Hiring KBK for a complete renovation of our front yard was a great decision. From the estimate to the design to the finished job, Jose was professional, accommodating and open to changes. We've been getting so many compliments.", "Priya S.", "Front-yard renovation"),
    ("They worked their butts off to complete our patio in 5 days, starting promptly at 8am. Jose made sure we were satisfied at every step. We'll recommend Jose and his team in a heartbeat.", "Sandesh S.", "Paver patio"),
    ("Hard-working team that made sure we were happy with the finished product. Impressed with their efficiency and commitment to keeping the area clean as they installed my paver patio.", "David D.", "Paver patio"),
    ("Jose and his crew deserve 10 stars. Seven Canadian hemlocks, burning bushes and two star magnolias, all so organized, trustworthy and professional.", "Carlos L.", "Planting"),
  ]},
  "areas": {"eyebrow": "Where we work", "h2": "Serving Macomb and Oakland counties", "p": "Based in Clinton Township. If your town is not listed, ask; we probably cover it.",
    "list": ["Clinton Township", "Macomb", "Shelby Township", "Sterling Heights", "Rochester Hills", "Rochester", "Troy", "Bloomfield Hills", "Birmingham", "Royal Oak", "Farmington Hills", "Grosse Pointe", "St. Clair Shores", "Warren", "Utica", "Washington Township", "Chesterfield", "West Bloomfield"]},
  "cta": {"h2": "Ready to plan your patio?", "p": "Free estimates. Jose answers the phone.", "btn": "Request a free quote"},
  "footer": {"about": "Family-owned hardscape and landscape company serving metro Detroit since 2009. Licensed Michigan LLC, fully insured.",
    "links": "Pages", "services": "Services", "contact": "Contact", "rights": "All rights reserved.", "privacy": "Privacy notice & terms"},
  "page_services": {"eyebrow": "Services", "h1": "Everything for the outside of your home", "lede": "From a single walkway to a full backyard with kitchen, fire pit and lighting. Here is what we build and what each job includes."},
  "page_projects": {"eyebrow": "Our work", "h1": "Patios, fire pits and gardens we've built", "lede": "Real projects from real backyards in Macomb and Oakland counties. Tap a photo to see it larger.",
    "cats": [("all", "All"), ("patios", "Patios & walkways"), ("firepits", "Fire pits"), ("kitchens", "Outdoor kitchens"), ("landscape", "Landscaping"), ("lighting", "Lighting"), ("pools", "Pool decks"), ("maintenance", "Sealing & repair")]},
  "page_about": {"eyebrow": "About", "h1": "A company created to serve and transform", "lede": "That was the idea when Jose Chavarin registered KBK Landscape & Beyond in April 2009. Seventeen years and hundreds of backyards later, it still is.",
    "blocks": [
      ("Jose is the company", "Jose is not a salesman who hands you off to a crew you never met. He does the estimate, designs the layout, orders the material, and is on site with the crew. Customers mention it in almost every review: he answers the phone, he listens, and he remembers what you asked for."),
      ("Built the right way", "A patio is only as good as the base under it. We excavate to the right depth, compact in lifts, use proper edge restraint and polymeric sand, and set drainage before we lay a single paver. That is why we can put 3 years in writing."),
      ("Plants that survive Michigan", "We pick trees, shrubs and perennials that handle zone 6 winters and clay soil, plant them at the right depth, and guarantee them for a year."),
      ("Family-owned, minority-owned", "KBK is a family business based in Clinton Township. Estimates are free, seniors get 5% off, and we speak English and Spanish."),
    ],
    "stats": [("2009", "Founded"), ("600+", "Reviews"), ("4.9", "Average rating"), ("3 yr", "Paver warranty")]},
  "page_contact": {"eyebrow": "Free estimate", "h1": "Tell us about your project", "lede": "Send a few details and Jose will call you back, usually the same day. Or skip the form and call.",
    "f": {"name": "Your name", "phone": "Phone", "email": "Email (optional)", "address": "Project address or town", "services": "What are you thinking about?", "budget": "Rough budget", "budget_opts": ["Not sure yet", "Under $5,000", "$5,000 – $15,000", "$15,000 – $30,000", "$30,000+"],
          "when": "When would you like it done?", "when_opts": ["As soon as possible", "In the next 1–3 months", "This year", "Just planning"],
          "details": "Anything else? Size, materials you like, photos you've seen…", "send": "Send my request", "note": "No spam, no sharing your details. Jose will reach out directly.",
          "chips": ["Paver patio", "Walkway or driveway", "Fire pit or fireplace", "Outdoor kitchen", "Retaining wall", "Landscaping & planting", "Lighting", "Sealing or repair", "Irrigation or drainage", "Cleanup or maintenance"]},
    "side": {"call": "Call or text", "email": "Email", "visit": "Shop", "hours": "Hours", "hours_v": "Mon–Fri 7:30 am – 6:30 pm<br>Sat 8 am – 3 pm<br>Sun closed", "social": "Find us on"}},
  "privacy_page": {"title": "Privacy notice & terms | KBK Landscape & Beyond", "desc": "How KBK Landscape & Beyond LLC uses the information you send through this website, and the terms that apply to estimates and quotes.",
    "eyebrow": "Legal", "h1": "Privacy notice & website terms", "updated": "Last updated: September 15, 2026",
    "consent": "By sending this form you agree that KBK Landscape & Beyond LLC may contact you by phone, text message or email about your request, and you accept our <a href=\"/privacy.html\">privacy notice and terms</a>. Message and data rates may apply. Reply STOP to any text to opt out.",
    "sections": [
      ("Who we are", "<p>This website is operated by KBK Landscape &amp; Beyond LLC, a Michigan limited liability company located at 20752 Miles St S, Clinton Township, MI 48036 (\"KBK\", \"we\", \"us\"). Questions about this notice: <a href=\"mailto:josechavarin@kbklandscape.com\">josechavarin@kbklandscape.com</a> or (586) 489-5613.</p>"),
      ("What we collect", "<p>When you request a quote we collect what you type into the form: your name, phone number, email address (optional), the project address or town, the services you are interested in, your budget range, timing, and any details you add. We also record the date and time, the page you sent it from, the language you used, your IP address and browser type, which we use to block spam and abuse.</p><p>If you call, text or email us, we keep the contact details and notes needed to respond and, if you hire us, to do the work.</p><p>We do not ask for and do not want payment card numbers, Social Security numbers or other sensitive personal information through this website. Please do not send them.</p>"),
      ("How we use it", "<ul><li>To answer your request, schedule a site visit and prepare a quote.</li><li>To contact you about your project by phone, text message or email. You agree to this when you send the form. Text messages are about your request only; we will not send marketing texts unless you separately agree to them, and you can stop at any time by replying STOP.</li><li>To keep records of estimates, quotes, projects and warranties, which we need in order to honor our warranties.</li><li>To protect the website and our business from spam, fraud and abuse.</li></ul><p>We do not sell, rent or trade your personal information. We do not use it for advertising by third parties.</p>"),
      ("Who can see it", "<p>Your information is stored on systems controlled by KBK and seen only by the owner and the people who help run the business, such as our website administrator. We share it only when needed to do the work (for example a supplier delivering material to your address), when required by law, or to protect our legal rights. If KBK is ever sold, customer records may transfer to the new owner under the same rules.</p><p>The website is hosted by GitHub Pages and uses Google Fonts and an embedded Google Map. Those providers receive your IP address and standard browser information when the page loads, under their own privacy policies. We do not set advertising or analytics cookies. The site stores your language preference in your browser only.</p>"),
      ("How long we keep it", "<p>Quote requests that do not lead to a project are deleted or anonymized within 24 months. Records of completed projects are kept for as long as a warranty applies and as required for tax and legal purposes, then deleted.</p>"),
      ("Your choices", "<p>You can ask us at any time what information we hold about you, ask us to correct it, or ask us to delete it, unless we need to keep it for a warranty, a contract or the law. Email <a href=\"mailto:josechavarin@kbklandscape.com\">josechavarin@kbklandscape.com</a> and we will respond within 30 days. You can also ask us to stop contacting you.</p>"),
      ("Security", "<p>We use reasonable technical and organizational measures to protect your information, including encrypted connections to this website and access limited to the people who need it. No method of transmission or storage is completely secure, and we cannot guarantee absolute security.</p>"),
      ("Children", "<p>This website is for adults arranging work on their property. We do not knowingly collect information from anyone under 18.</p>"),
      ("Estimates, quotes and website content", "<p>Information on this website, including service descriptions, photos and any price ranges we may publish, is general information and not an offer. Every property is different. A quote is only binding once it is issued in writing by KBK and accepted by you, and it is subject to the conditions stated in it, such as site access, soil conditions and material availability. Free estimates may be limited to our service area.</p><p>Project photos on this site show work performed by KBK. Customer reviews are quoted from public review platforms and reflect those customers' own opinions.</p><p>Warranties are as stated in your written quote or contract: currently 3 years on new paver installations and 1 year on plants and trees we install, covering workmanship and plant health under normal care. They do not cover damage from misuse, neglect, extreme weather, settling caused by others' work, or products excluded by the manufacturer.</p>"),
      ("Limitation of liability", "<p>To the extent permitted by Michigan law, KBK is not liable for any indirect, incidental or consequential damages arising from use of this website or reliance on its content. Nothing in this notice limits rights you have under applicable consumer protection law.</p>"),
      ("Changes and governing law", "<p>We may update this notice from time to time; the date at the top shows the current version. This notice and any dispute relating to this website are governed by the laws of the State of Michigan.</p>"),
    ]},
  "notfound": {"h1": "Page not found", "p": "That page moved when we rebuilt the site.", "btn": "Go to the home page"},
},
"es": {
  "nav": {"index": "Inicio", "services": "Servicios", "projects": "Proyectos", "about": "Nosotros", "contact": "Contacto"},
  "quote": "Cotización gratis", "call": "Llamar", "lang_btn": "EN", "lang_label": "English",
  "hours": "Lun–Vie 7:30–6:30 · Sáb 8–3",
  "area_line": "Clinton Township · Condados de Macomb y Oakland",
  "titles": {
    "index": "KBK Landscape & Beyond | Patios de adoquín, fogatas y jardinería en Clinton Township, MI",
    "services": "Servicios | KBK Landscape & Beyond",
    "projects": "Proyectos | KBK Landscape & Beyond",
    "about": "Sobre Jose y su equipo | KBK Landscape & Beyond",
    "contact": "Cotización gratis | KBK Landscape & Beyond",
  },
  "desc": {
    "index": "Empresa familiar de hardscape y jardinería en Clinton Township, MI desde 2009. Patios de adoquín, fogatas, cocinas exteriores, muros de contención y plantación, con 3 años de garantía. 4.9 estrellas en más de 600 reseñas.",
    "services": "Patios y caminos de adoquín, fogatas, cocinas exteriores, muros de contención, diseño de jardines, iluminación, riego y sellado de adoquín en los condados de Macomb y Oakland.",
    "projects": "Fotos de patios, fogatas, cocinas exteriores, iluminación y jardines construidos por KBK Landscape & Beyond en el área metropolitana de Detroit.",
    "about": "Jose Chavarin dirige KBK Landscape & Beyond desde 2009. Conozca al equipo detrás de más de 600 reseñas de cinco estrellas.",
    "contact": "Solicite un presupuesto gratis a domicilio de KBK Landscape & Beyond. Llame al (586) 489-5613 o envíenos los detalles de su proyecto.",
  },
  "hero": {
    "h1": "Espacios exteriores hechos para durar, por un equipo que sí llega.",
    "lede": "Patios de adoquín, fogatas, cocinas exteriores y jardines en los condados de Macomb y Oakland. Jose está en cada obra, desde el presupuesto hasta la última barrida.",
    "cta2": "Ver proyectos",
    "proof": [("4.9 ★", "Más de 600 reseñas"), ("2009", "Empresa familiar desde"), ("3 años", "Garantía en adoquín")],
  },
  "services_intro": {"eyebrow": "Qué hacemos", "h2": "Un solo equipo para todo el patio", "p": "Diseño, hardscape y plantación bajo un mismo techo, para que nada se pierda entre contratistas."},
  "services": [
    ("patio-modern", "Patios y caminos de adoquín", "Adoquín de ladrillo, concreto o porcelana sobre una base bien compactada, con bordes e incrustaciones a su gusto.", ["Patios, caminos y porches", "Entradas de autos", "Escalones y descansos", "Círculos, incrustaciones y bordes"]),
    ("fire-pit-patio", "Fogatas y chimeneas", "De gas o leña, redondas o cuadradas, con muros de asiento para que quepa toda la familia.", ["Fogatas de gas y de leña", "Chimeneas exteriores", "Muros de asiento y columnas", "Remates de piedra natural"]),
    ("kitchen-grill", "Cocinas y barras exteriores", "Asadores empotrados, barras y cubiertas en piedra o bloque, del tamaño que usted realmente usa.", ["Islas con asador empotrado", "Barras y cubiertas", "Hornos de pizza y ahumadores", "Iluminación y electricidad"]),
    ("garden-terraces", "Muros de contención y escalones", "Muros que sostienen una pendiente por décadas, con buen drenaje detrás, y escalones seguros de noche.", ["Muros de bloque, roca y madera", "Terrazas en pendientes", "Muros de jardín y bordes", "Drenaje y nivelación"]),
    ("garden-path", "Diseño de jardín y plantación", "Jardineras, árboles, arbustos y perennes escogidos para el invierno de Michigan, bien plantados y con mulch.", ["Diseño de jardín frontal y trasero", "Árboles, arbustos y perennes", "Pasto en rollo y semilla", "Mulch, roca de río y bordes"]),
    ("lighting-steps", "Iluminación de jardín", "Luces LED de bajo voltaje para caminos, escalones, árboles y fachada. Más seguro y se ve muy bien desde la calle.", ["Luces de camino y escalón", "Iluminación de árboles y fachadas", "Luces integradas en adoquín", "Temporizadores y control inteligente"]),
    ("patio-sealed", "Limpieza, sellado y reparación de adoquín", "Recupere un patio viejo: lavado a presión, arena nueva, sellado y nivelación de secciones hundidas.", ["Lavado a presión y arena nueva", "Sellado (efecto mojado o natural)", "Nivelación y reparaciones", "Control de maleza y musgo"]),
    ("garden-drybed", "Riego, drenaje y mantenimiento", "Sistemas de riego, soluciones para patios encharcados y limpiezas de temporada para que todo siga como nuevo.", ["Instalación y reparación de riego", "Drenajes franceses y cauces secos", "Limpiezas de primavera y otoño", "Poda de arbustos y cuidado de jardineras"]),
  ],
  "more": "Ver más",
  "why": {"eyebrow": "Por qué eligen a KBK", "h2": "El dueño está en su obra, todos los días",
    "p": "Jose Chavarin fundó KBK en 2009 y sigue dirigiendo la cuadrilla personalmente. Usted trata con una sola persona que contesta el teléfono, recuerda lo que pidió y está ahí cuando se coloca el último adoquín.",
    "list": ["Presupuesto gratis a domicilio, con precio claro por escrito", "Obra limpia y plazos honestos: un patio normalmente en menos de una semana", "Asegurados, con garantías por escrito", "Precio justo: muchos clientes nos dicen que quedamos muy por debajo de otras cotizaciones"]},
  "warranty": {"eyebrow": "Nuestra promesa", "h2": "Garantías que sí valen",
    "items": [("3 años", "en cada instalación nueva de adoquín"), ("1 año", "en cada árbol y planta que instalamos"), ("Gratis", "presupuesto a domicilio, sin presión")]},
  "steps": {"eyebrow": "Cómo funciona", "h2": "De la idea al patio terminado", "items": [
    ("Llame o mande fotos", "Cuéntenos qué tiene en mente. Con unas fotos del espacio desde el celular es suficiente para empezar."),
    ("Visita a domicilio", "Jose mide, escucha y sugiere lo que funciona con su patio y su presupuesto."),
    ("Cotización por escrito", "Un precio claro con los materiales especificados, normalmente en pocos días. Sin sorpresas."),
    ("Lo construimos", "Una cuadrilla ordenada, un calendario realista y un recorrido final con usted."),
  ]},
  "work": {"eyebrow": "Trabajos recientes", "h2": "Construido en su vecindario", "all": "Ver todos los proyectos"},
  "reviews": {"eyebrow": "Reseñas", "h2": "Lo que dicen los clientes", "src": "Reseñas de Google (traducidas)", "items": [
    ("Contratar a KBK para renovar todo nuestro jardín frontal fue una gran decisión. Desde el presupuesto hasta el diseño y la obra terminada, Jose fue profesional, flexible y abierto a cambios. Nos han llegado muchísimos cumplidos.", "Priya S.", "Renovación de jardín frontal"),
    ("Trabajaron durísimo para terminar nuestro patio en 5 días, empezando puntual a las 8 am. Jose se aseguró de que estuviéramos satisfechos en cada paso. Recomendamos a Jose y su equipo sin dudarlo.", "Sandesh S.", "Patio de adoquín"),
    ("Un equipo muy trabajador que se aseguró de que quedáramos contentos con el resultado. Me impresionó su eficiencia y lo limpio que mantuvieron el área mientras instalaban mi patio.", "David D.", "Patio de adoquín"),
    ("Jose y su equipo merecen 10 estrellas. Siete hemlocks canadienses, arbustos y dos magnolias estrella; todo organizado, confiable y muy profesional.", "Carlos L.", "Plantación"),
  ]},
  "areas": {"eyebrow": "Dónde trabajamos", "h2": "Condados de Macomb y Oakland", "p": "Estamos en Clinton Township. Si su ciudad no aparece, pregunte; seguramente la cubrimos.",
    "list": ["Clinton Township", "Macomb", "Shelby Township", "Sterling Heights", "Rochester Hills", "Rochester", "Troy", "Bloomfield Hills", "Birmingham", "Royal Oak", "Farmington Hills", "Grosse Pointe", "St. Clair Shores", "Warren", "Utica", "Washington Township", "Chesterfield", "West Bloomfield"]},
  "cta": {"h2": "¿Listo para planear su patio?", "p": "Presupuesto gratis. Jose contesta el teléfono, en español o inglés.", "btn": "Pedir cotización gratis"},
  "footer": {"about": "Empresa familiar de hardscape y jardinería en el área de Detroit desde 2009. LLC registrada en Michigan, asegurada.",
    "links": "Páginas", "services": "Servicios", "contact": "Contacto", "rights": "Todos los derechos reservados.", "privacy": "Aviso de privacidad y términos"},
  "page_services": {"eyebrow": "Servicios", "h1": "Todo para el exterior de su casa", "lede": "Desde un camino sencillo hasta un patio completo con cocina, fogata e iluminación. Esto es lo que construimos y lo que incluye cada trabajo."},
  "page_projects": {"eyebrow": "Proyectos", "h1": "Patios, fogatas y jardines que hemos construido", "lede": "Proyectos reales en patios reales de los condados de Macomb y Oakland. Toque una foto para verla más grande.",
    "cats": [("all", "Todos"), ("patios", "Patios y caminos"), ("firepits", "Fogatas"), ("kitchens", "Cocinas exteriores"), ("landscape", "Jardinería"), ("lighting", "Iluminación"), ("pools", "Terrazas de piscina"), ("maintenance", "Sellado y reparación")]},
  "page_about": {"eyebrow": "Nosotros", "h1": "Una empresa creada para servir y transformar", "lede": "Esa fue la idea cuando Jose Chavarin registró KBK Landscape & Beyond en abril de 2009. Diecisiete años y cientos de patios después, lo sigue siendo.",
    "blocks": [
      ("Jose es la empresa", "Jose no es un vendedor que lo pasa a una cuadrilla que nunca conoció. Él hace el presupuesto, diseña el trazo, pide el material y está en la obra con el equipo. Los clientes lo mencionan en casi cada reseña: contesta el teléfono, escucha y recuerda lo que usted pidió."),
      ("Construido como debe ser", "Un patio vale lo que vale la base que tiene debajo. Excavamos a la profundidad correcta, compactamos por capas, usamos borde de contención y arena polimérica, y resolvemos el drenaje antes de colocar el primer adoquín. Por eso podemos dar 3 años por escrito."),
      ("Plantas que sobreviven a Michigan", "Elegimos árboles, arbustos y perennes que aguantan el invierno de la zona 6 y el suelo arcilloso, los plantamos a la profundidad correcta y los garantizamos por un año."),
      ("Empresa familiar, de propietario hispano", "KBK es un negocio familiar con base en Clinton Township. El presupuesto es gratis, los adultos mayores tienen 5% de descuento, y atendemos en español e inglés."),
    ],
    "stats": [("2009", "Fundada"), ("600+", "Reseñas"), ("4.9", "Calificación promedio"), ("3 años", "Garantía en adoquín")]},
  "page_contact": {"eyebrow": "Presupuesto gratis", "h1": "Cuéntenos de su proyecto", "lede": "Mande unos detalles y Jose le devolverá la llamada, normalmente el mismo día. O sáltese el formulario y llame.",
    "f": {"name": "Su nombre", "phone": "Teléfono", "email": "Correo (opcional)", "address": "Dirección o ciudad del proyecto", "services": "¿Qué tiene en mente?", "budget": "Presupuesto aproximado", "budget_opts": ["Todavía no sé", "Menos de $5,000", "$5,000 – $15,000", "$15,000 – $30,000", "Más de $30,000"],
          "when": "¿Para cuándo lo quiere?", "when_opts": ["Lo antes posible", "En los próximos 1–3 meses", "Este año", "Solo estoy planeando"],
          "details": "¿Algo más? Medidas, materiales que le gustan, fotos que ha visto…", "send": "Enviar solicitud", "note": "Sin spam y sin compartir sus datos. Jose se comunicará directamente.",
          "chips": ["Patio de adoquín", "Camino o entrada de autos", "Fogata o chimenea", "Cocina exterior", "Muro de contención", "Jardinería y plantación", "Iluminación", "Sellado o reparación", "Riego o drenaje", "Limpieza o mantenimiento"]},
    "side": {"call": "Llame o mande mensaje", "email": "Correo", "visit": "Taller", "hours": "Horario", "hours_v": "Lun–Vie 7:30 am – 6:30 pm<br>Sáb 8 am – 3 pm<br>Dom cerrado", "social": "Encuéntrenos en"}},
  "privacy_page": {"title": "Aviso de privacidad y términos | KBK Landscape & Beyond", "desc": "Cómo usa KBK Landscape & Beyond LLC la información que usted envía por este sitio, y los términos que aplican a presupuestos y cotizaciones.",
    "eyebrow": "Legal", "h1": "Aviso de privacidad y términos del sitio", "updated": "Última actualización: 15 de septiembre de 2026",
    "consent": "Al enviar este formulario acepta que KBK Landscape & Beyond LLC se comunique con usted por teléfono, mensaje de texto o correo sobre su solicitud, y acepta nuestro <a href=\"/es/privacy.html\">aviso de privacidad y términos</a>. Pueden aplicar tarifas de mensajes y datos. Responda STOP a cualquier texto para cancelar.",
    "sections": [
      ("Quiénes somos", "<p>Este sitio es operado por KBK Landscape &amp; Beyond LLC, una sociedad de responsabilidad limitada de Michigan ubicada en 20752 Miles St S, Clinton Township, MI 48036 (\"KBK\", \"nosotros\"). Preguntas sobre este aviso: <a href=\"mailto:josechavarin@kbklandscape.com\">josechavarin@kbklandscape.com</a> o (586) 489-5613.</p>"),
      ("Qué información recopilamos", "<p>Cuando pide una cotización recopilamos lo que escribe en el formulario: nombre, teléfono, correo (opcional), la dirección o ciudad del proyecto, los servicios que le interesan, su rango de presupuesto, el plazo y los detalles que agregue. También registramos la fecha y hora, la página desde la que envió, el idioma, su dirección IP y el tipo de navegador, que usamos para bloquear spam y abusos.</p><p>Si nos llama, escribe o manda un mensaje, guardamos los datos de contacto y las notas necesarias para responder y, si nos contrata, para hacer el trabajo.</p><p>No pedimos ni queremos números de tarjeta, números de Seguro Social ni otra información sensible por este sitio. Por favor no los envíe.</p>"),
      ("Cómo la usamos", "<ul><li>Para responder a su solicitud, programar la visita y preparar una cotización.</li><li>Para comunicarnos con usted sobre su proyecto por teléfono, mensaje de texto o correo. Usted lo acepta al enviar el formulario. Los mensajes de texto son solo sobre su solicitud; no enviaremos textos publicitarios salvo que usted lo acepte por separado, y puede cancelar en cualquier momento respondiendo STOP.</li><li>Para llevar registro de presupuestos, cotizaciones, proyectos y garantías, que necesitamos para cumplir nuestras garantías.</li><li>Para proteger el sitio y el negocio contra spam, fraude y abusos.</li></ul><p>No vendemos, rentamos ni intercambiamos su información personal. No la usamos para publicidad de terceros.</p>"),
      ("Quién puede verla", "<p>Su información se guarda en sistemas controlados por KBK y solo la ven el propietario y las personas que ayudan a operar el negocio, como el administrador del sitio web. La compartimos solo cuando hace falta para el trabajo (por ejemplo, un proveedor que entrega material en su dirección), cuando la ley lo exige o para proteger nuestros derechos legales. Si KBK se vendiera, los registros de clientes pasarían al nuevo propietario bajo las mismas reglas.</p><p>El sitio está alojado en GitHub Pages y usa Google Fonts y un mapa de Google incrustado. Esos proveedores reciben su dirección IP e información estándar del navegador al cargar la página, bajo sus propias políticas de privacidad. No usamos cookies de publicidad ni de analítica. El sitio guarda su preferencia de idioma solo en su navegador.</p>"),
      ("Cuánto tiempo la conservamos", "<p>Las solicitudes que no terminan en un proyecto se eliminan o anonimizan en un plazo de 24 meses. Los registros de proyectos terminados se conservan mientras aplique una garantía y lo exijan fines fiscales y legales, y después se eliminan.</p>"),
      ("Sus opciones", "<p>Puede pedirnos en cualquier momento qué información tenemos sobre usted, pedir que la corrijamos o que la eliminemos, salvo que debamos conservarla por una garantía, un contrato o la ley. Escriba a <a href=\"mailto:josechavarin@kbklandscape.com\">josechavarin@kbklandscape.com</a> y responderemos en un plazo de 30 días. También puede pedirnos que dejemos de contactarlo.</p>"),
      ("Seguridad", "<p>Usamos medidas técnicas y organizativas razonables para proteger su información, incluyendo conexiones cifradas a este sitio y acceso limitado a quienes lo necesitan. Ningún método de transmisión o almacenamiento es totalmente seguro y no podemos garantizar seguridad absoluta.</p>"),
      ("Menores", "<p>Este sitio es para adultos que contratan trabajos en su propiedad. No recopilamos a sabiendas información de menores de 18 años.</p>"),
      ("Presupuestos, cotizaciones y contenido del sitio", "<p>La información de este sitio, incluidas descripciones de servicios, fotos y cualquier rango de precios que publiquemos, es información general y no una oferta. Cada propiedad es distinta. Una cotización solo es vinculante cuando KBK la emite por escrito y usted la acepta, y está sujeta a las condiciones que indique, como acceso al sitio, condiciones del suelo y disponibilidad de materiales. Los presupuestos gratis pueden limitarse a nuestra zona de servicio.</p><p>Las fotos de proyectos muestran trabajos realizados por KBK. Las reseñas de clientes se citan de plataformas públicas y reflejan la opinión de esos clientes.</p><p>Las garantías son las que indique su cotización o contrato por escrito: actualmente 3 años en instalaciones nuevas de adoquín y 1 año en plantas y árboles que instalamos, y cubren mano de obra y salud de la planta con cuidado normal. No cubren daños por mal uso, descuido, clima extremo, hundimientos causados por trabajos de terceros ni productos excluidos por el fabricante.</p>"),
      ("Limitación de responsabilidad", "<p>En la medida que lo permita la ley de Michigan, KBK no es responsable de daños indirectos, incidentales o consecuentes derivados del uso de este sitio o de confiar en su contenido. Nada en este aviso limita los derechos que usted tenga bajo las leyes de protección al consumidor aplicables.</p>"),
      ("Cambios y ley aplicable", "<p>Podemos actualizar este aviso; la fecha al inicio muestra la versión vigente. Este aviso y cualquier disputa relacionada con este sitio se rigen por las leyes del Estado de Michigan.</p>"),
    ]},
  "notfound": {"h1": "Página no encontrada", "p": "Esa página cambió de lugar cuando rediseñamos el sitio.", "btn": "Ir al inicio"},
},
}


def href(lang, page):
    base = "/es/" if lang == "es" else "/"
    return base if page == "index" else f"{base}{page}.html"


def other(lang):
    return "en" if lang == "es" else "es"


def head(lang, page, t):
    alt = other(lang)
    if page == "privacy":
        t = {**t, "titles": {**t["titles"], "privacy": t["privacy_page"]["title"]}, "desc": {**t["desc"], "privacy": t["privacy_page"]["desc"]}}
    ld = ""
    if page == "index":
        ld = json.dumps({
            "@context": "https://schema.org", "@type": "LandscapeContractor" if False else "HomeAndConstructionBusiness",
            "name": "KBK Landscape & Beyond LLC", "url": SITE, "telephone": TEL, "email": EMAIL, "image": f"{SITE}/assets/img/og.jpg",
            "foundingDate": "2009-04-24", "founder": {"@type": "Person", "name": "Jose Chavarin"},
            "address": {"@type": "PostalAddress", "streetAddress": "20752 Miles St S", "addressLocality": "Clinton Township", "addressRegion": "MI", "postalCode": "48036", "addressCountry": "US"},
            "geo": {"@type": "GeoCoordinates", "latitude": 42.5823975, "longitude": -82.9116363},
            "openingHoursSpecification": [
                {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:30", "closes": "18:30"},
                {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "15:00"}],
            "areaServed": ["Macomb County, MI", "Oakland County, MI"], "priceRange": "$$",
            "sameAs": [FACEBOOK, GOOGLE],
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "614"},
        })
        ld = f'<script type="application/ld+json">{ld}</script>'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t['titles'][page]}</title>
<meta name="description" content="{t['desc'][page]}">
<link rel="canonical" href="{SITE}{href(lang, page)}">
<link rel="alternate" hreflang="en" href="{SITE}{href('en', page)}">
<link rel="alternate" hreflang="es" href="{SITE}{href('es', page)}">
<link rel="alternate" hreflang="x-default" href="{SITE}{href('en', page)}">
<meta property="og:title" content="{t['titles'][page]}">
<meta property="og:description" content="{t['desc'][page]}">
<meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{href(lang, page)}">
<meta name="theme-color" content="#1f3d2b">
<link rel="icon" href="/assets/img/icon-32.png" sizes="32x32">
<link rel="icon" href="/assets/img/logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Source+Sans+3:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
{ld}
</head>
<body>
"""


def header(lang, page, t):
    links = "".join(f'<li><a href="{href(lang, p)}"{" aria-current=\"page\"" if p == page else ""}>{t["nav"][p]}</a></li>' for p in PAGES)
    return f"""<div class="topbar"><div class="wrap">
  <span class="hours">{t['hours']} · {t['area_line']}</span>
  <span><a href="tel:{TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
</div></div>
<header class="site"><div class="wrap">
  <a class="brand" href="{href(lang, 'index')}"><img src="/assets/img/logo.svg" alt="" width="46" height="46"><span><b>KBK</b><small>Landscape &amp; Beyond</small></span></a>
  <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="main" id="nav" aria-label="Main"><ul>{links}
    <li><a class="lang" href="{href(other(lang), page)}" hreflang="{other(lang)}" title="{t['lang_label']}">{t['lang_btn']}</a></li>
    <li><a class="btn btn-primary" href="{href(lang, 'contact')}">{t['quote']}</a></li></ul></nav>
</div></header>
"""


def footer(lang, t):
    f = t["footer"]
    svc = "".join(f'<li><a href="{href(lang, "services")}#s{i}">{s[1]}</a></li>' for i, s in enumerate(t["services"][:6]))
    pages = "".join(f'<li><a href="{href(lang, p)}">{t["nav"][p]}</a></li>' for p in PAGES)
    return f"""<footer class="site"><div class="wrap">
  <div class="cols">
    <div><a class="brand" href="{href(lang, 'index')}" style="color:var(--cream)"><img src="/assets/img/logo.svg" alt="" width="46" height="46"><span><b>KBK</b><small style="color:var(--leaf)">Landscape &amp; Beyond LLC</small></span></a>
      <p style="margin-top:16px">{f['about']}</p></div>
    <div><h4>{f['links']}</h4><ul>{pages}</ul></div>
    <div><h4>{f['services']}</h4><ul>{svc}</ul></div>
    <div><h4>{f['contact']}</h4><ul>
      <li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li>{ADDRESS.replace(', ', '<br>', 1)}</li>
      <li><a href="{FACEBOOK}" rel="noopener" target="_blank">Facebook</a> · <a href="{GOOGLE}" rel="noopener" target="_blank">Google</a></li></ul></div>
  </div>
  <div class="legal"><span>© <span data-year>2026</span> KBK Landscape &amp; Beyond LLC. {f['rights']}</span><a href="{href(lang, 'privacy')}">{f['privacy']}</a></div>
</div></footer>
<div class="callbar"><a class="btn btn-ghost" style="color:var(--cream)" href="tel:{TEL}">☎ {t['call']}</a><a class="btn btn-primary" href="{href(lang, 'contact')}">{t['quote']}</a></div>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def cta(lang, t):
    return f"""<section class="cta-band"><div class="wrap">
  <h2>{t['cta']['h2']}</h2><p class="lede" style="margin:0 auto">{t['cta']['p']}</p>
  <a class="btn btn-primary" href="{href(lang, 'contact')}">{t['cta']['btn']}</a>
  <a class="btn btn-ghost" href="tel:{TEL}">☎ {PHONE}</a>
</div></section>
"""


def pic(pid, lang, cls="", lazy=True):
    m = next(x for x in MANIFEST if x["id"] == pid)
    return (f'<img src="/assets/img/projects/{pid}-800.webp" srcset="/assets/img/projects/{pid}-800.webp 800w, /assets/img/projects/{pid}.webp 1600w" '
            f'sizes="(max-width: 700px) 100vw, 33vw" alt="{m[lang]}" {"loading=\"lazy\" decoding=\"async\"" if lazy else ""} class="{cls}">')


def page_index(lang, t):
    h = t["hero"]
    proof = "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in h["proof"])
    cards = "".join(f"""<a class="card reveal" href="{href(lang, 'services')}#s{i}">{pic(s[0], lang)}<div class="body"><h3>{s[1]}</h3><p>{s[2]}</p><div class="more">{t['more']} →</div></div></a>""" for i, s in enumerate(t["services"][:6]))
    w = t["why"]
    checks = "".join(f"<li>{x}</li>" for x in w["list"])
    war = "".join(f"<div><b>{b}</b>{s}</div>" for b, s in t["warranty"]["items"])
    steps = "".join(f"<div><h3>{a}</h3><p class='muted'>{b}</p></div>" for a, b in t["steps"]["items"])
    work_ids = ["patio-grand-stairs", "kitchen-bar", "firepit-pavers", "garden-front", "lighting-facade", "pool-modern"]
    work = "".join(f'<figure data-cat="x">{pic(i, lang)}<figcaption><b>{next(x for x in MANIFEST if x["id"]==i)[lang]}</b>{next(x for x in MANIFEST if x["id"]==i)["town"]}</figcaption></figure>' for i in work_ids)
    revs = "".join(f'<blockquote class="review reveal"><span class="stars">★★★★★</span><p>“{q}”</p><footer><b>{n}</b> · {s}</footer></blockquote>' for q, n, s in t["reviews"]["items"])
    areas = "".join(f"<li>{a}</li>" for a in t["areas"]["list"])
    return f"""<section class="hero">
  <picture><source media="(max-width: 700px)" srcset="/assets/img/hero-800.webp"><img class="bg" src="/assets/img/hero.webp" alt="" fetchpriority="high"></picture>
  <div class="wrap">
    <p class="eyebrow">{t['area_line']}</p>
    <h1>{h['h1']}</h1>
    <p class="lede">{h['lede']}</p>
    <div class="cta"><a class="btn btn-primary" href="{href(lang, 'contact')}">{t['quote']}</a><a class="btn btn-ghost" href="{href(lang, 'projects')}">{h['cta2']}</a></div>
    <div class="proof">{proof}</div>
  </div>
</section>

<section><div class="wrap">
  <p class="eyebrow">{t['services_intro']['eyebrow']}</p><h2>{t['services_intro']['h2']}</h2><p class="lede muted">{t['services_intro']['p']}</p>
  <div class="grid grid-3" style="margin-top:36px">{cards}</div>
</div></section>

<section style="padding-top:0"><div class="wrap split">
  <img src="/assets/img/about.webp" alt="" loading="lazy" width="1200" height="900">
  <div><p class="eyebrow">{w['eyebrow']}</p><h2>{w['h2']}</h2><p class="lede muted">{w['p']}</p><ul class="checks">{checks}</ul></div>
</div></section>

<section class="band"><div class="wrap">
  <p class="eyebrow">{t['warranty']['eyebrow']}</p><h2>{t['warranty']['h2']}</h2>
  <div class="warranty" style="margin-top:32px">{war}</div>
</div></section>

<section><div class="wrap">
  <p class="eyebrow">{t['steps']['eyebrow']}</p><h2>{t['steps']['h2']}</h2>
  <div class="steps" style="margin-top:32px">{steps}</div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <p class="eyebrow">{t['work']['eyebrow']}</p><h2>{t['work']['h2']}</h2>
  <div class="gallery" style="margin-top:28px">{work}</div>
  <p style="margin-top:28px"><a class="btn btn-dark" href="{href(lang, 'projects')}">{t['work']['all']} →</a></p>
</div></section>

<section style="background:var(--cream-2)"><div class="wrap">
  <p class="eyebrow">{t['reviews']['eyebrow']}</p><h2>{t['reviews']['h2']}</h2>
  <div class="reviews" style="margin-top:32px">{revs}</div>
  <p class="muted" style="margin-top:20px;font-size:.9rem"><a href="{GOOGLE}" rel="noopener" target="_blank">{t['reviews']['src']} →</a></p>
</div></section>

<section><div class="wrap">
  <p class="eyebrow">{t['areas']['eyebrow']}</p><h2>{t['areas']['h2']}</h2><p class="lede muted">{t['areas']['p']}</p>
  <ul class="areas" style="margin-top:24px">{areas}</ul>
</div></section>
{cta(lang, t)}"""


def page_services(lang, t):
    p = t["page_services"]
    blocks = "".join(f"""<article class="service" id="s{i}">
  <div class="media">{pic(s[0], lang)}</div>
  <div><h2>{s[1]}</h2><p class="lede muted">{s[2]}</p><ul>{"".join(f"<li>{x}</li>" for x in s[3])}</ul>
    <a class="btn btn-dark" href="{href(lang, 'contact')}">{t['quote']}</a></div>
</article>""" for i, s in enumerate(t["services"]))
    return f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">{p['eyebrow']}</p><h1>{p['h1']}</h1><p class="lede">{p['lede']}</p></div></section>
<div class="wrap">{blocks}</div>
{cta(lang, t)}"""


def page_projects(lang, t):
    p = t["page_projects"]
    filters = "".join(f'<button type="button" data-cat="{c}" aria-pressed="{"true" if c == "all" else "false"}">{n}</button>' for c, n in p["cats"])
    figs = "".join(f'<figure data-cat="{m["cat"]}"><img src="/assets/img/projects/{m["id"]}-800.webp" data-full="/assets/img/projects/{m["id"]}.webp" alt="{m[lang]}" loading="lazy" decoding="async"><figcaption><b>{m[lang]}</b>{m["town"]}</figcaption></figure>' for m in MANIFEST)
    return f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">{p['eyebrow']}</p><h1>{p['h1']}</h1><p class="lede">{p['lede']}</p></div></section>
<section><div class="wrap"><div class="filters">{filters}</div><div class="gallery">{figs}</div></div></section>
{cta(lang, t)}"""


def page_about(lang, t):
    p = t["page_about"]
    stats = "".join(f"<div><b>{b}</b>{s}</div>" for b, s in p["stats"])
    blocks = "".join(f'<div class="card reveal"><div class="body"><h3>{a}</h3><p>{b}</p></div></div>' for a, b in p["blocks"])
    return f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">{p['eyebrow']}</p><h1>{p['h1']}</h1><p class="lede">{p['lede']}</p></div></section>
<section><div class="wrap split">
  {pic('firepit-pavers', lang, lazy=False)}
  <div class="grid grid-2" style="gap:16px">{blocks}</div>
</div></section>
<section class="band" style="padding-top:48px;padding-bottom:48px"><div class="wrap warranty">{stats}</div></section>
{cta(lang, t)}"""


def page_contact(lang, t):
    p, f, s = t["page_contact"], t["page_contact"]["f"], t["page_contact"]["side"]
    chips = "".join(f'<label><input type="checkbox" name="services" value="{c}"><span>{c}</span></label>' for c in f["chips"])
    opt = lambda xs: "".join(f"<option>{x}</option>" for x in xs)
    return f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">{p['eyebrow']}</p><h1>{p['h1']}</h1><p class="lede">{p['lede']}</p></div></section>
<section><div class="wrap split" style="align-items:start">
  <form class="quote" action="{LEADS_URL}" method="post" novalidate>
    <div><label for="name">{f['name']}</label><input id="name" name="name" required autocomplete="name"></div>
    <div><label for="phone">{f['phone']}</label><input id="phone" name="phone" type="tel" required autocomplete="tel"></div>
    <div><label for="email">{f['email']}</label><input id="email" name="email" type="email" autocomplete="email"></div>
    <div><label for="address">{f['address']}</label><input id="address" name="address" autocomplete="street-address"></div>
    <div class="full"><label>{f['services']}</label><div class="chips">{chips}</div></div>
    <div><label for="budget">{f['budget']}</label><select id="budget" name="budget">{opt(f['budget_opts'])}</select></div>
    <div><label for="when">{f['when']}</label><select id="when" name="when">{opt(f['when_opts'])}</select></div>
    <div class="full"><label for="details">{f['details']}</label><textarea id="details" name="details"></textarea></div>
    <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
    <div class="form-msg" role="status"></div>
    <div class="full"><button class="btn btn-primary" type="submit">{f['send']}</button><p class="form-note" style="margin-top:12px">{t['privacy_page']['consent']}</p></div>
  </form>
  <aside class="contact-side">
    <dl><dt>{s['call']}</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd></dl>
    <dl><dt>{s['email']}</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></dl>
    <dl><dt>{s['visit']}</dt><dd>{ADDRESS}</dd></dl>
    <dl><dt>{s['hours']}</dt><dd>{s['hours_v']}</dd></dl>
    <dl><dt>{s['social']}</dt><dd><a href="{FACEBOOK}" rel="noopener" target="_blank">Facebook</a> · <a href="{GOOGLE}" rel="noopener" target="_blank">Google</a></dd></dl>
    <div class="map"><iframe src="{MAP_EMBED}" loading="lazy" title="Map" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
  </aside>
</div></section>"""


def page_privacy(lang, t):
    p = t["privacy_page"]
    body = "".join(f"<h2 style='font-size:1.4rem;margin-top:1.8em'>{h}</h2>{html}" for h, html in p["sections"])
    return f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">{p['eyebrow']}</p><h1>{p['h1']}</h1><p class="lede">{p['updated']}</p></div></section>
<section><div class="wrap" style="max-width:820px">{body}</div></section>"""


BUILDERS = {"index": page_index, "privacy": page_privacy, "services": page_services, "projects": page_projects, "about": page_about, "contact": page_contact}


def finish(html):
    """Preview builds live under a sub-path and must not be indexed."""
    if not BASE:
        return html
    html = re.sub(r'((?:href|src|data-full)=")/(?!/)', rf'\1{BASE}/', html)
    html = re.sub(r'(srcset="[^"]*?)(?<=[", ])/(?=assets/)', rf'\1{BASE}/', html)
    html = re.sub(r'(srcset="[^"]*)', lambda m: m.group(1).replace(", /assets", f", {BASE}/assets"), html)
    return html.replace("<head>\n", '<head>\n<meta name="robots" content="noindex, nofollow">\n', 1)


def build():
    for lang in ("en", "es"):
        t = C[lang]
        out = OUT / ("es" if lang == "es" else ".")
        out.mkdir(parents=True, exist_ok=True)
        for page in PAGES + ["privacy"]:
            html = head(lang, page, t) + header(lang, page, t) + f'<main>{BUILDERS[page](lang, t)}</main>\n' + footer(lang, t)
            (out / f"{page}.html").write_text(finish(html), encoding="utf-8")
    # 404 (GitHub Pages serves /404.html for missing paths)
    t = C["en"]; n = t["notfound"]
    (OUT / "404.html").write_text(finish(head("en", "index", t).replace(t["titles"]["index"], "Page not found | KBK Landscape & Beyond") + header("en", "index", t)
        + f'<main><section class="page-hero"><div class="wrap"><h1>{n["h1"]} / {C["es"]["notfound"]["h1"]}</h1><p class="lede">{n["p"]}</p><a class="btn btn-primary" href="/">{n["btn"]}</a> <a class="btn btn-ghost" href="/es/">{C["es"]["notfound"]["btn"]}</a></div></section></main>\n' + footer("en", t)), encoding="utf-8")
    # Old URL kept alive
    (OUT / "project.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/projects.html"><link rel="canonical" href="https://kbklandscape.com/projects.html"><title>Redirecting</title><a href="/projects.html">Projects</a>\n')
    urls = [f"{SITE}{href(l, p)}" for l in ("en", "es") for p in PAGES + ["privacy"]]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\n{'Disallow: /' if BASE else 'Allow: /'}\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(PAGES) * 2 + 1, "pages")


if __name__ == "__main__":
    build()
