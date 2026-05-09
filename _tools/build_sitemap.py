#!/usr/bin/env python3
"""Genera sitemap.xml + robots.txt scansionando tutti gli HTML del sito."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SITO = os.path.dirname(HERE)
SITE_URL = "https://barbaraspica.it"
TODAY = "2026-05-09"

# Pages: (path, priority, freq)
priorities = {
    '/': (1.0, 'monthly'),
    '/chi-sono.html': (0.9, 'monthly'),
    '/servizi.html': (0.9, 'monthly'),
    '/aree-di-intervento.html': (0.9, 'monthly'),
    '/approccio.html': (0.9, 'monthly'),
    '/contatti.html': (0.9, 'monthly'),
    '/blog/': (0.8, 'weekly'),
}

urls = []
# Static pages
for p, (prio, freq) in priorities.items():
    urls.append((SITE_URL + p, TODAY, freq, prio))

# Blog articles
blog_dir = os.path.join(SITO, 'blog')
for f in sorted(os.listdir(blog_dir)):
    if f.endswith('.html') and f != 'index.html':
        urls.append((f'{SITE_URL}/blog/{f}', TODAY, 'monthly', 0.7))

# Legal pages (lower prio)
for p in ['/privacy.html', '/cookie.html', '/note-legali.html']:
    if os.path.exists(os.path.join(SITO, p.lstrip('/'))):
        urls.append((SITE_URL + p, TODAY, 'yearly', 0.3))

xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url, lastmod, freq, prio in urls:
    xml.append(f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>')
xml.append('</urlset>')

with open(os.path.join(SITO, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml))
print(f"✅ sitemap.xml generato con {len(urls)} URL")
