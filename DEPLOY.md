# Guida Deploy — Sito Barbara Spica

## Visione d'insieme

```
[Tuo PC] → git push → [GitHub] → click "Update from Remote" su cPanel → [Sito online]
```

## Step 1 — Inizializza Git in locale (UNA SOLA VOLTA)

Apri PowerShell o cmd in `C:\Users\Intel\Documents\BarbaraSpica\sito` ed esegui:

```bash
git init
git config user.name "Laura"
git config user.email "gruppokosmos00@gmail.com"
git remote add origin https://github.com/lauruccia/barbaraspica-sito.git
git branch -M main
git add .
git commit -m "feat: prima versione sito vetrina con SEO completo"
git push -u origin main
```

> Se Git ti chiede credenziali GitHub, usa username `lauruccia` e come password un **Personal Access Token** (Settings → Developer settings → Personal access tokens → Generate new). Lo serve solo la prima volta.

## Step 2 — Configura cPanel (UNA SOLA VOLTA)

1. Accedi a cPanel del tuo hosting
2. Cerca e apri **Git™ Version Control**
3. Click **Create**
4. Compila:
   - **Clone URL**: `https://github.com/lauruccia/barbaraspica-sito.git`
   - **Repository Path**: lascia il default (es. `/home/USER/repositories/barbaraspica-sito`)
   - **Repository Name**: `barbaraspica-sito`
5. Click **Create**

Se il repo è privato, usa quest'URL invece:
```
https://lauruccia:GHP_TUO_TOKEN@github.com/lauruccia/barbaraspica-sito.git
```
(sostituisci `GHP_TUO_TOKEN` con il tuo Personal Access Token GitHub)

## Step 3 — Primo deploy

1. Su cPanel → **Git Version Control** → trova il repo → **Manage**
2. Tab **Pull or Deploy**
3. Click **Update from Remote** (scarica gli ultimi commit)
4. Click **Deploy HEAD Commit** (esegue `.cpanel.yml` → copia in `public_html`)
5. Apri `https://barbaraspica.it` → 🎉 dovrebbe essere online

## Step 4 — Configurazioni post-deploy

### A. Forza HTTPS
- cPanel → **SSL/TLS Status** → seleziona dominio → **Run AutoSSL** (se Let's Encrypt non è già attivo)
- Una volta attivo, l'`.htaccess` redirige automaticamente HTTP → HTTPS

### B. Crea l'email per il form
Il form usa `noreply@barbaraspica.it` come mittente. Crealo:
- cPanel → **Email Accounts** → **Create**
- Email: `noreply` · Domain: `barbaraspica.it` · password sicura
- Non serve consultarlo, serve solo perché esista come mittente

### C. Test del form
Compila il form su `/contatti` con un'email di test. Dovresti ricevere:
1. Una mail su `info@barbaraspica.it`
2. L'utente riceve un'auto-reply

Se non arriva: cPanel → **Track Delivery** → controlla i log di consegna

### D. Submit a Google Search Console
1. Vai su https://search.google.com/search-console
2. Aggiungi proprietà `barbaraspica.it`
3. Verifica con il metodo HTML file (Google ti dà un file da caricare in `public_html/`)
4. Una volta verificata, vai su **Sitemap** → invia: `sitemap.xml`

## Deploy successivi (workflow normale)

Dal tuo PC, dopo aver modificato qualcosa:
```bash
git add .
git commit -m "Descrizione modifica"
git push
```

Poi su cPanel → Git Version Control → **Update from Remote** → **Deploy HEAD Commit**.

**Scorciatoia**: doppio click su `carica-online.bat` esegue automaticamente add+commit+push.

## Troubleshooting

### "Il sito mostra ancora i vecchi contenuti"
- Cache browser: Ctrl+F5 (hard refresh)
- Cache CDN cPanel: cPanel → **Cache Manager** → Clear

### "Authentication failed" durante git push
- Assicurati di usare un Personal Access Token, non la password GitHub
- Crealo: github.com → Settings → Developer settings → Personal access tokens (classic) → scopes: `repo`

### "Errore 500 sul sito"
- 99% di volte è un errore in `.htaccess`. Confronta con la versione del repo
- Controlla cPanel → **Errors** per dettagli

### "Form non manda email"
- Verifica che esista `noreply@barbaraspica.it` come account email
- cPanel → **Track Delivery** per vedere se sono in coda
- Su alcuni hosting `mail()` di PHP è disabilitato: in tal caso passare a SMTP (PHPMailer)

### "Le immagini non si vedono"
- Verifica i permessi: cartelle 755, file 644 (lo script `.cpanel.yml` lo fa già)
- Controlla che la cartella `assets/` sia stata effettivamente copiata in `public_html`

## File da NON modificare manualmente in produzione

Quelli generati automaticamente:
- `blog/*.html` (rigenerati da `_articles/*.md`)
- `sitemap.xml` (rigenerato da `_tools/build_sitemap.py`)

Modifica sempre i sorgenti (`_articles/*.md`), poi rigenera con i `.bat`.

## Backup

Tutto è già su GitHub: ogni `git push` è un backup. Se vuoi un backup zip aggiuntivo:
- cPanel → **Backup** → **Download a Home Directory Backup**
