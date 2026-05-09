# barbaraspica.it — Sito vetrina

Sito statico professionale della **Dott.ssa Barbara Spica** (TNPEE & Psicologa, Reggio Calabria).
HTML5 + CSS + un singolo file PHP per il form contatti. Nessun database.

## 📁 Struttura

```
sito/
├── index.html, chi-sono.html, servizi.html, …  # Pagine HTML
├── blog/                                       # Articoli (auto-generati da _articles/)
├── webapp/                                     # Landing area riservata (linka alla WebApp Medica)
├── assets/
│   ├── css/style.css      # Stylesheet (palette teal brand)
│   ├── js/main.js         # JS minimo: nav mobile, cookie banner
│   └── img/               # Immagini, logo, favicon, OG image
├── contact.php            # Handler form contatti (mail() + anti-spam)
├── .htaccess              # Redirect HTTPS, cache, sicurezza, URL puliti
├── .cpanel.yml            # Deploy automatico su cPanel via Git
├── manifest.webmanifest   # PWA manifest
├── robots.txt + sitemap.xml
├── _articles/             # Sorgenti markdown degli articoli (NON pubblicati)
└── _tools/                # Script di build (Python)
```

## 🚀 Avvio in locale (anteprima sul tuo PC)

**Modo veloce — Windows**: doppio click su `serve.bat` → si apre il browser.

**Da terminale**:
```bash
cd sito
php -S localhost:8000          # se hai PHP (consigliato, testa anche il form)
# oppure
python -m http.server 8000     # se hai Python
```

## ✍️ Scrivere un nuovo articolo del blog

Vedi **`GUIDA-ARTICOLI.md`** per la procedura completa. In sintesi:
1. Doppio click su `nuovo-articolo.bat` → si apre Notepad con un template
2. Modifica e salva
3. Doppio click su `pubblica-articoli.bat` → genera l'HTML
4. Doppio click su `carica-online.bat` → push su GitHub → deploy cPanel

## 🌐 Deploy su cPanel via GitHub

### Setup iniziale (una sola volta)

```bash
cd sito
git init
git remote add origin https://github.com/lauruccia/barbaraspica-sito.git
git branch -M main
git add .
git commit -m "feat: sito vetrina iniziale"
git push -u origin main
```

### Configurazione cPanel
1. Login cPanel → **Git Version Control**
2. **Create** → URL del Clone: `https://github.com/lauruccia/barbaraspica-sito.git`
3. Repository Path: `/home/USER/repositories/barbaraspica-sito` (default)
4. Repository Name: `barbaraspica-sito`
5. **Create**
6. Una volta creato → click su **Manage** → tab **Pull or Deploy** → **Update from Remote** → **Deploy HEAD Commit**

Lo script `.cpanel.yml` copia tutti i file in `~/public_html/`.

### Deploy successivi (ogni volta che modifichi)
```bash
git add .
git commit -m "descrizione modifica"
git push
```
poi vai su cPanel → Git Version Control → **Update from Remote** → **Deploy HEAD Commit**.

> Suggerimento: usa **`carica-online.bat`** per fare git add+commit+push in un solo doppio click.

## 🔐 Form contatti — configurazione

`contact.php` invia email via PHP `mail()`. Apri il file e verifica:

```php
'to'   => 'info@barbaraspica.it',                    // ← destinatario
'from' => 'noreply@barbaraspica.it',                 // ← deve essere un indirizzo del DOMINIO
```

Su cPanel crea l'account email `noreply@barbaraspica.it` (anche un alias va bene) per evitare blocchi SPF/DKIM.

## 🎨 Palette colori (brand)

| Variabile | Hex | Uso |
|---|---|---|
| `--c-primary` | `#2A6F73` | testo, header, bottoni |
| `--c-brand` | `#88C8C8` | teal del logo |
| `--c-brand-light` | `#A3DDDE` | sfondi delicati |
| `--c-accent` | `#E59076` | CTA, evidenziazioni |
| `--c-cream` | `#FAF7F2` | sfondi sezioni |
| `--c-dark` | `#1F2A37` | titoli scuri |

## 📋 Checklist post-deploy

- [ ] HTTPS attivo (certificato Let's Encrypt da cPanel → SSL/TLS Status)
- [ ] Account email `noreply@` creato per il form
- [ ] Sitemap inviata a Google Search Console: `https://barbaraspica.it/sitemap.xml`
- [ ] Sito verificato con [PageSpeed Insights](https://pagespeed.web.dev/)
- [ ] Sito verificato con [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- [ ] Redirect dal vecchio sito WordPress impostati (vedi `.htaccess`)

## 📞 Contatti

Dott.ssa Barbara Spica · TNPEE & Psicologa · P.IVA 03719660833
Via Diego Malara 4, Trav. I — 89133 Reggio Calabria
+39 349 7543276 · info@barbaraspica.it
