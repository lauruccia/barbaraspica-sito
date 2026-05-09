#!/usr/bin/env python3
"""Rigenera /blog/index.html scansionando tutti gli articoli HTML del sito."""
import os, sys, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
SITO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
exec(open(os.path.join(HERE, 'sito_build.py')).read(), globals())
OUT = SITO

BLOG = os.path.join(SITO, 'blog')

def parse_meta(html_text):
    """Estrae i metadati di un articolo dall'<head> e dal corpo."""
    def find(pat, default=''):
        m = re.search(pat, html_text)
        return html.unescape(m.group(1)) if m else default

    title = find(r'<title>([^<|]+)\|')
    title = title.strip() or find(r'<title>([^<]+)</title>').replace('| Dott.ssa Barbara Spica','').strip()
    desc = find(r'<meta name="description" content="([^"]+)"')
    img = find(r'<meta property="og:image" content="[^"]*?(/assets/img/photos/[^"]+)"', '/assets/img/photos/attivita-1.jpg')
    cat = find(r'<span class="pill is-accent">([^<]+)</span>', 'Articolo')
    date = find(r'datePublished":\s*"([^"]+)"')
    read_min = find(r'⏱\s*(\d+)\s*min', '5')
    return {'title': title, 'description': desc, 'image': img, 'category': cat,
            'date': date, 'read_min': read_min}

articles = []
for f in sorted(os.listdir(BLOG)):
    if f == 'index.html' or not f.endswith('.html'):
        continue
    with open(os.path.join(BLOG, f), encoding='utf-8') as fp:
        meta = parse_meta(fp.read())
    meta['slug'] = f[:-5]
    articles.append(meta)

# Newest first
articles.sort(key=lambda a: a['date'], reverse=True)

# Build cards
cards_html = ''
for a in articles:
    cards_html += f'''
      <article class="article-card" data-reveal>
        <a href="/blog/{a['slug']}.html" class="thumb"><img src="{a['image']}" alt="{html.escape(a['title'])}" loading="lazy" width="1000" height="750"></a>
        <div class="body">
          <div class="meta">{html.escape(a['category'])} · {a['read_min']} min · {a['date']}</div>
          <h3><a href="/blog/{a['slug']}.html">{html.escape(a['title'])}</a></h3>
          <p>{html.escape(a['description'])}</p>
          <a href="/blog/{a['slug']}.html" class="read-more">Leggi {ICON["arrow"]}</a>
        </div>
      </article>
'''

h = head("Blog",
    "Blog della Dott.ssa Barbara Spica: articoli su screening neuropsicomotorio, DIR/Floortime, ESDM, autismo, ADHD, sviluppo del bambino. Reggio Calabria.",
    "/blog/")
body = header_html("blog")
body += page_hero("Blog",
    "Articoli e approfondimenti sui disturbi del neurosviluppo, l'intervento precoce, l'approccio DIR/Floortime ed ESDM. Per famiglie, insegnanti e professionisti.",
    [("Blog", "/blog/")])
body += f'''
<main id="content">
<section>
  <div class="container">
    <div class="grid grid-3">
      {cards_html}
    </div>
  </div>
</section>
{cta_band()}
</main>
'''
out = os.path.join(BLOG, 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(h + body + footer_html())
print(f"✅ Blog index aggiornato con {len(articles)} articoli → {out}")
