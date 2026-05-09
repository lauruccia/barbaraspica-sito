#!/usr/bin/env python3
"""Build a blog article from a Markdown file.

Usage:
  python _tools/build_article.py _articles/nome-articolo.md

Markdown frontmatter (YAML):
---
title: Il mio nuovo articolo
description: Riassunto in 1-2 frasi (per Google)
category: Approccio
date: 2026-05-12
read_min: 5
image: /assets/img/photos/attivita-1.jpg
---

# Eventuale H1 (verrà ignorato, usato il title)
Contenuto in markdown qui...
"""
import sys, os, re, html as html_lib

# Bootstrap path so we can import sito_build
HERE = os.path.dirname(os.path.abspath(__file__))
SITO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

# Import shared module via exec
exec(open(os.path.join(HERE, 'sito_build.py')).read(), globals())

# Override OUT to current sito root
OUT = SITO  # noqa: F811

# ---------------------- minimal markdown converter ----------------------
def md_to_html(md):
    """Very small but solid Markdown converter sufficient for blog articles."""
    md = md.replace('\r\n', '\n')

    # Code blocks (fenced)
    code_blocks = []
    def stash_code(m):
        code_blocks.append(m.group(1))
        return f'@@@CODE{len(code_blocks)-1}@@@'
    md = re.sub(r'```(?:\w+)?\n(.*?)\n```', stash_code, md, flags=re.S)

    # Blockquotes (lines starting with >)
    def conv_block(text):
        blocks = re.split(r'\n{2,}', text.strip())
        out = []
        i = 0
        while i < len(blocks):
            b = blocks[i].strip()
            if not b:
                i += 1; continue

            # Heading
            mh = re.match(r'^(#{1,6})\s+(.+)$', b)
            if mh and '\n' not in b:
                level = len(mh.group(1))
                txt = inline(mh.group(2))
                out.append(f'<h{level}>{txt}</h{level}>')
                i += 1; continue

            # Blockquote
            if b.startswith('>'):
                lines = [re.sub(r'^>\s?', '', l) for l in b.split('\n')]
                inner = inline('\n'.join(lines).strip())
                out.append(f'<blockquote>{inner}</blockquote>')
                i += 1; continue

            # Unordered list
            if re.match(r'^[\*\-]\s+', b):
                items = re.split(r'\n(?=[\*\-]\s+)', b)
                _re_li = re.compile(r'^[\*\-]\s+')
                lis = ''.join(f'<li>{inline(_re_li.sub("", it).strip())}</li>' for it in items)
                out.append(f'<ul>{lis}</ul>')
                i += 1; continue

            # Ordered list
            if re.match(r'^\d+\.\s+', b):
                items = re.split(r'\n(?=\d+\.\s+)', b)
                _re_oli = re.compile(r'^\d+\.\s+')
                lis = ''.join(f'<li>{inline(_re_oli.sub("", it).strip())}</li>' for it in items)
                out.append(f'<ol>{lis}</ol>')
                i += 1; continue

            # Image-only block
            mim = re.match(r'^!\[(.*?)\]\((.+?)\)\s*$', b)
            if mim:
                alt, src = mim.group(1), mim.group(2)
                out.append(f'<p><img src="{src}" alt="{html_lib.escape(alt)}" loading="lazy"></p>')
                i += 1; continue

            # Horizontal rule
            if re.match(r'^-{3,}$|^_{3,}$|^\*{3,}$', b):
                out.append('<hr>')
                i += 1; continue

            # Paragraph
            out.append(f'<p>{inline(b)}</p>')
            i += 1
        return '\n'.join(out)

    def inline(s):
        # Restore code first as inline placeholder (later)
        # Bold + italic
        s = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'__(.+?)__', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'<em>\1</em>', s)
        s = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<em>\1</em>', s)
        # Inline code
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        # Links [text](url)
        s = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)',
                   r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', s)
        # Images inside text
        s = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1" loading="lazy">', s)
        # Linebreaks: 2 spaces at end of line
        s = re.sub(r'  +\n', '<br>', s)
        return s

    html_out = conv_block(md)

    # Re-insert code blocks
    for idx, cb in enumerate(code_blocks):
        cb_esc = html_lib.escape(cb)
        html_out = html_out.replace(f'@@@CODE{idx}@@@', f'<pre><code>{cb_esc}</code></pre>')

    return html_out


# ---------------------- frontmatter parser ----------------------
def parse_frontmatter(text):
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 3)
    if end < 0:
        return {}, text
    fm = text[3:end].strip()
    body = text[end+4:].lstrip('\n')
    meta = {}
    for line in fm.split('\n'):
        if ':' in line:
            k, _, v = line.partition(':')
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


# ---------------------- main ----------------------
def build_one(md_path):
    with open(md_path, encoding='utf-8') as f:
        raw = f.read()
    meta, body_md = parse_frontmatter(raw)

    slug = meta.get('slug') or os.path.splitext(os.path.basename(md_path))[0]
    title = meta.get('title') or slug.replace('-', ' ').capitalize()
    description = meta.get('description', title)
    category = meta.get('category', 'Articolo')
    date = meta.get('date', '2026-05-09')
    read_min = meta.get('read_min', '5')
    image = meta.get('image', '/assets/img/photos/attivita-1.jpg')

    # Strip the first <h1> from rendered md if present (we use the title)
    body_md = re.sub(r'^\s*#\s+.*\n', '', body_md, count=1)
    content_html = md_to_html(body_md)

    # Build full article page using shared head/header/footer
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "image": SITE_URL + image,
        "datePublished": date,
        "dateModified": date,
        "author": {"@type": "Person", "name": "Dott.ssa Barbara Spica",
                   "url": SITE_URL + "/chi-sono.html"},
        "publisher": {"@type": "Person", "name": "Dott.ssa Barbara Spica",
                      "logo": {"@type": "ImageObject",
                               "url": SITE_URL + "/assets/img/icons/favicon-512.png"}},
        "mainEntityOfPage": {"@type": "WebPage",
                             "@id": f"{SITE_URL}/blog/{slug}.html"}
    }

    h = head(title, description, f"/blog/{slug}.html",
             og_image=image, schema_extra=article_schema)
    body = header_html("blog")
    body += f'''
<section class="page-hero">
  <div class="container container-narrow">
    <nav class="breadcrumb"><a href="/">Home</a> › <a href="/blog/">Blog</a> › <span aria-current="page">{html_lib.escape(title)}</span></nav>
    <span class="pill is-accent">{html_lib.escape(category)}</span>
    <h1 style="margin-top:1rem">{html_lib.escape(title)}</h1>
    <div class="article-meta-bar" style="justify-content:center; border:0; padding:0; margin-top:1rem;">
      <span>📅 {date}</span><span>·</span>
      <span>⏱ {read_min} min</span><span>·</span>
      <span>✍️ Dott.ssa Barbara Spica</span>
    </div>
  </div>
</section>
<main id="content">
<section style="padding-top:0;">
  <div class="container container-narrow">
    <picture><img src="{image}" alt="{html_lib.escape(title)}" style="width:100%; border-radius:var(--radius-md); margin-bottom:2rem;"></picture>
    <div class="article-body">
{content_html}
    </div>
    <div style="margin-top:3rem;padding:1.6rem 1.8rem;background:var(--c-cream);border-radius:var(--radius-md);">
      <strong>Hai dubbi o vuoi un confronto?</strong>
      <p style="margin:.5rem 0 1rem;color:var(--c-text-soft)">Contattami: posso darti indicazioni più precise sulla situazione del tuo bambino.</p>
      <a href="/contatti.html" class="btn btn-primary">Prenota un colloquio →</a>
    </div>
    <p style="margin-top:2rem"><a href="/blog/">← Torna a tutti gli articoli</a></p>
  </div>
</section>
</main>
'''
    out_path = os.path.join(SITO, 'blog', f'{slug}.html')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(h + body + footer_html())
    print(f'  ✅ {slug}.html  ({len(content_html)//1024} KB)')
    return slug, title, description, category, date, read_min, image


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python _tools/build_article.py _articles/nome.md  (oppure --all)')
        sys.exit(1)

    if sys.argv[1] == '--all':
        files = sorted([os.path.join(SITO, '_articles', f)
                       for f in os.listdir(os.path.join(SITO, '_articles'))
                       if f.endswith('.md')])
    else:
        files = sys.argv[1:]

    print(f'\n📝 Genero {len(files)} articolo/i...\n')
    for f in files:
        if not os.path.exists(f):
            f2 = os.path.join(SITO, f)
            if os.path.exists(f2): f = f2
        if os.path.exists(f):
            build_one(f)
        else:
            print(f'  ❌ Non trovato: {f}')
    print('\n✨ Fatto! Ricorda di aggiornare blog/index.html se hai aggiunto un nuovo articolo.\n')
