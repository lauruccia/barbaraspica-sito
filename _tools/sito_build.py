#!/usr/bin/env python3
"""Build all HTML pages for barbaraspica.it static site."""
import os, json

OUT = '/sessions/exciting-youthful-hamilton/mnt/BarbaraSpica/sito'
SITE_URL = "https://barbaraspica.it"
SITE_NAME = "Barbara Spica"
TEL_DISPLAY = "+39 349 7543276"
TEL_E164 = "+393497543276"
TEL_HREF = "tel:+393497543276"
WA_HREF = "https://wa.me/393497543276?text=Salve%20Dott.ssa%20Spica%2C%20le%20scrivo%20dal%20suo%20sito%20web."
EMAIL = "info@barbaraspica.it"
ADDRESS_STREET = "Via Diego Malara 4, Traversa I"
ADDRESS_CITY = "89133 Reggio Calabria"
PIVA = "03719660833"

ICON = {
  "phone": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.86 19.86 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.86 19.86 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
  "mail": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
  "pin": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
  "whatsapp": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163A11.867 11.867 0 0 1 .002 11.79C.005 5.281 5.286 0 11.794 0a11.83 11.83 0 0 1 8.413 3.488 11.74 11.74 0 0 1 3.476 8.405c-.003 6.508-5.286 11.793-11.794 11.793h-.005a11.81 11.81 0 0 1-5.643-1.437L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884a9.86 9.86 0 0 0 1.51 5.26l-.999 3.648 3.978-1.607zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.521.074-.793.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.71.306 1.263.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413z"/></svg>',
  "clock": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
  "instagram": '<svg viewBox="0 0 24 24"><path d="M12 2.16c3.2 0 3.58.012 4.85.07 1.17.054 1.8.249 2.23.413.56.218.96.477 1.38.896.42.42.68.823.9 1.382.16.43.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.43.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.43-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.43-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16zm0-2.16C8.74 0 8.33.014 7.05.072c-1.28.058-2.16.26-2.92.55-.79.31-1.46.71-2.13 1.38C1.34 2.67.93 3.34.62 4.13c-.29.76-.49 1.64-.55 2.92C.01 8.33 0 8.74 0 12s.014 3.67.072 4.95c.058 1.28.26 2.16.55 2.92.31.79.71 1.46 1.38 2.13.67.67 1.34 1.07 2.13 1.38.76.29 1.64.49 2.92.55C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.28-.06 2.16-.26 2.92-.55.79-.31 1.46-.71 2.13-1.38.67-.67 1.07-1.34 1.38-2.13.29-.76.49-1.64.55-2.92.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.28-.26-2.16-.55-2.92-.31-.79-.71-1.46-1.38-2.13C21.33 1.34 20.66.93 19.87.62c-.76-.29-1.64-.49-2.92-.55C15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 12 18.16 6.16 6.16 0 0 0 12 5.84zm0 10.16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.41-10.4a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/></svg>',
  "facebook": '<svg viewBox="0 0 24 24"><path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073c0 6.025 4.388 11.02 10.125 11.927v-8.435H7.078v-3.492h3.047V9.41c0-3.026 1.792-4.697 4.533-4.697 1.312 0 2.686.235 2.686.235v2.97H15.83c-1.491 0-1.956.93-1.956 1.886v2.27h3.328l-.532 3.492h-2.796v8.435C19.612 23.094 24 18.1 24 12.073z"/></svg>',
  "check": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
  "heart": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
  "users": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
  "compass": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
  "leaf": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/></svg>',
  "sparkle": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3Z"/></svg>',
  "smile": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>',
  "shield": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/></svg>',
  "book": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>',
  "calendar": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
  "puzzle": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/></svg>',
  "arrow": '<svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
}

def head(title, description, path, og_image=None, schema_extra=None):
    canonical = SITE_URL + path
    full_title = f"{title} | Dott.ssa Barbara Spica"
    if path == "/" or path == "/index.html":
        full_title = "Dott.ssa Barbara Spica | TNPEE & Psicologa a Reggio Calabria"
    og_img = og_image or "/assets/img/og/og-image.jpg"
    person_schema = {
        "@context": "https://schema.org", "@type": "Person",
        "name": "Dott.ssa Barbara Spica", "givenName": "Barbara", "familyName": "Spica",
        "honorificPrefix": "Dott.ssa",
        "jobTitle": "TNPEE - Terapista della Neuro e Psicomotricità dell'Età Evolutiva, Psicologa",
        "url": SITE_URL,
        "image": SITE_URL + "/assets/img/photos/hero-barbara.jpg",
        "telephone": TEL_E164, "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS_STREET,
                    "addressLocality": "Reggio Calabria", "postalCode": "89133",
                    "addressCountry": "IT", "addressRegion": "Calabria"},
        "knowsAbout": ["Disturbi del neurosviluppo", "Psicomotricità infantile",
                       "DIR/Floortime", "Early Start Denver Model (ESDM)",
                       "Disturbo dello spettro autistico", "ADHD", "Disprassia", "Sindrome di Down"]
    }
    business_schema = {
        "@context": "https://schema.org", "@type": ["MedicalBusiness", "LocalBusiness"],
        "@id": SITE_URL + "/#business",
        "name": "Dott.ssa Barbara Spica - TNPEE e Psicologa",
        "image": SITE_URL + "/assets/img/photos/hero-barbara.jpg",
        "url": SITE_URL, "telephone": TEL_E164, "email": EMAIL, "priceRange": "€€",
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS_STREET,
                    "addressLocality": "Reggio Calabria", "postalCode": "89133",
                    "addressCountry": "IT", "addressRegion": "Calabria"},
        "geo": {"@type": "GeoCoordinates", "latitude": 38.0793, "longitude": 15.6486},
        "openingHoursSpecification": [
            {"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"19:00"}
        ],
        "medicalSpecialty": ["Psychiatric", "Pediatric"], "vatID": PIVA
    }
    schemas = [person_schema, business_schema]
    if schema_extra: schemas.append(schema_extra)
    schema_json = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)

    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<meta name="author" content="Dott.ssa Barbara Spica">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{full_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}{og_img}">
<meta name="theme-color" content="#2F6B5E">
<link rel="icon" type="image/svg+xml" href="/assets/img/icons/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/icons/favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/img/icons/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{schema_json}
</head>
<body>
<a class="skip-link" href="#content">Vai al contenuto</a>
'''

def header_html(active=""):
    def cls(k):
        return ' class="is-active"' if k == active else ''
    return f'''<header class="site-header">
  <div class="container nav-row">
    <a href="/" class="brand" aria-label="Home - Dott.ssa Barbara Spica">
      <img src="/assets/img/icons/logo-header.png" alt="Logo Barbara Spica TNPEE Psicologa" width="240" height="60" loading="eager">
    </a>
    <nav class="main-nav" aria-label="Navigazione principale">
      <a href="/"{cls('home')}>Home</a>
      <a href="/chi-sono.html"{cls('chi-sono')}>Chi sono</a>
      <a href="/servizi.html"{cls('servizi')}>Servizi</a>
      <a href="/aree-di-intervento.html"{cls('aree')}>Aree di intervento</a>
      <a href="/approccio.html"{cls('approccio')}>Approccio</a>
      <a href="/blog/"{cls('blog')}>Blog</a>
      <a href="/contatti.html"{cls('contatti')}>Contatti</a>
    </nav>
    <div class="nav-cta">
      <a href="{TEL_HREF}" class="nav-tel" aria-label="Chiama ora">
        {ICON["phone"]} <span class="nav-tel-text">{TEL_DISPLAY}</span>
      </a>
      <a href="/contatti.html" class="btn btn-primary">Prenota</a>
      <button class="nav-toggle" aria-label="Apri menu" aria-controls="main-nav" aria-expanded="false"><span></span></button>
    </div>
  </div>
</header>
'''

def footer_html():
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="brand" style="text-decoration:none">
          <span class="brand-text">
            <strong>Dott.ssa Barbara Spica</strong>
            <span>TNPEE · Psicologa</span>
          </span>
        </a>
        <p>Percorsi terapeutici personalizzati per accompagnare bambini e famiglie nello sviluppo emotivo, relazionale e motorio, nel rispetto dei tempi e dell'unicità di ciascuno.</p>
        <div class="social-row" aria-label="Social media">
          <a href="https://www.instagram.com/" target="_blank" rel="noopener" aria-label="Instagram">{ICON["instagram"]}</a>
          <a href="https://www.facebook.com/" target="_blank" rel="noopener" aria-label="Facebook">{ICON["facebook"]}</a>
        </div>
      </div>
      <div>
        <h4>Sito</h4>
        <ul class="footer-list">
          <li><a href="/">Home</a></li>
          <li><a href="/chi-sono.html">Chi sono</a></li>
          <li><a href="/servizi.html">Servizi</a></li>
          <li><a href="/aree-di-intervento.html">Aree di intervento</a></li>
          <li><a href="/approccio.html">Approccio</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/contatti.html">Contatti</a></li>
        </ul>
      </div>
      <div>
        <h4>Contatti</h4>
        <ul class="footer-list">
          <li>{ICON["phone"]} <a href="{TEL_HREF}">{TEL_DISPLAY}</a></li>
          <li>{ICON["mail"]} <a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ICON["whatsapp"]} <a href="{WA_HREF}" target="_blank" rel="noopener">WhatsApp</a></li>
        </ul>
      </div>
      <div>
        <h4>Sede</h4>
        <ul class="footer-list">
          <li>{ICON["pin"]} <a href="https://maps.google.com/?q=via+Diego+Malara+4+Reggio+Calabria" target="_blank" rel="noopener">{ADDRESS_STREET}<br>{ADDRESS_CITY}</a></li>
          <li>{ICON["clock"]} Lun-Ven 9:00-19:00<br>(su appuntamento)</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© <span data-year>2026</span> Dott.ssa Barbara Spica · P.IVA {PIVA}</div>
      <nav aria-label="Note legali">
        <a href="/privacy.html">Privacy</a>
        <a href="/cookie.html">Cookie Policy</a>
        <a href="/note-legali.html">Note legali</a>
      </nav>
    </div>
  </div>
</footer>
<aside id="cookie-banner" class="cookie-banner" role="dialog" aria-label="Informativa cookie">
  <p>Questo sito utilizza solo cookie tecnici essenziali al funzionamento. Non vengono usati cookie di profilazione né di terze parti. <a href="/cookie.html">Maggiori informazioni</a>.</p>
  <div class="actions">
    <button class="reject" data-cookie="rejected">Solo necessari</button>
    <button class="accept" data-cookie="accepted">Ho capito</button>
  </div>
</aside>
<div class="float-actions" aria-label="Contatti rapidi">
  <a href="{WA_HREF}" target="_blank" rel="noopener" class="fab-wa" aria-label="Contattami su WhatsApp">{ICON["whatsapp"]}</a>
  <a href="{TEL_HREF}" class="fab-tel" aria-label="Chiamami">{ICON["phone"]}</a>
</div>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''

def page_hero(title, subtitle, breadcrumbs):
    crumbs = ['<a href="/">Home</a>']
    for label, href in breadcrumbs[:-1]:
        crumbs.append(f'<span aria-hidden="true">›</span><a href="{href}">{label}</a>')
    crumbs.append(f'<span aria-hidden="true">›</span><span aria-current="page">{breadcrumbs[-1][0]}</span>')
    crumbs_html = ' '.join(crumbs)
    return f'''<section class="page-hero">
  <div class="container container-narrow">
    <nav class="breadcrumb" aria-label="Briciole di pane">{crumbs_html}</nav>
    <h1>{title}</h1>
    <p class="lede">{subtitle}</p>
  </div>
</section>
'''

def cta_band():
    return f'''<section class="section-cream">
  <div class="container">
    <div class="cta-banner">
      <span class="eyebrow" style="color:#FCEEE8">Insieme nel percorso di crescita</span>
      <h2>Un lavoro condiviso, passo dopo passo</h2>
      <p>Ogni percorso terapeutico è una collaborazione fatta di ascolto, fiducia e obiettivi condivisi.<br>Se senti il bisogno di un confronto, di una valutazione o di maggiori informazioni, contattami per iniziare insieme un percorso pensato su misura.</p>
      <div class="actions">
        <a href="/contatti.html" class="btn btn-light">Prenota un colloquio {ICON["arrow"]}</a>
        <a href="{WA_HREF}" target="_blank" rel="noopener" class="btn btn-whatsapp">{ICON["whatsapp"]} Scrivimi su WhatsApp</a>
      </div>
    </div>
  </div>
</section>
'''

def write(path, content):
    full = os.path.join(OUT, path.lstrip('/'))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {path} ({len(content)//1024} KB)")

# Save module helpers for re-use
print("module ready")
