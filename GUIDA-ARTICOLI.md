# Come scrivere un nuovo articolo del blog (in 4 click)

> Tutto è ottimizzato per scrivere senza pensare al codice.
> Tu scrivi in **Markdown** (semplicissimo formato testuale), gli script trasformano in HTML SEO-ottimizzato.

## Passo 1 — Crea l'articolo
Doppio click su **`nuovo-articolo.bat`** → digita un nome (es. `autismo-segnali-precoci`) → si apre Notepad con un template pronto.

## Passo 2 — Modifica i metadati in alto
Le prime righe tra `---` sono i metadati. Cambia title, description, category, image:

```yaml
---
title: Autismo: 7 segnali precoci da non sottovalutare
description: I principali segnali nei primi 24 mesi di vita che meritano un consulto specialistico.
category: Autismo
date: 2026-05-15
read_min: 5
image: /assets/img/photos/attivita-1.jpg
slug: autismo-segnali-precoci
---
```

**Linee guida**:
- `title`: 50-65 caratteri ideali per Google
- `description`: 130-160 caratteri (compare nei risultati Google)
- `category`: una parola, libera (es. Autismo, Approccio, Famiglia)
- `image`: una delle immagini in `/assets/img/photos/` (vedi cartella)

## Passo 3 — Scrivi il contenuto

Sotto i metadati, scrivi normalmente. Esempi rapidi:

```markdown
## Un titolo di sezione

Testo normale con **grassetto** e *corsivo*.

> Una citazione importante che vuoi evidenziare.

### Un sottotitolo

- Lista puntata
- Secondo elemento
- Terzo

1. Lista numerata
2. Secondo passo

[Link a una pagina del sito](/contatti.html)
[Link a un sito esterno](https://www.iss.it)
```

**Suggerimenti SEO**:
- Inizia con un paragrafo breve che riassuma di cosa parla l'articolo
- Usa `##` (H2) per le sezioni principali, `###` (H3) per i sotto-titoli
- Inserisci la parola chiave principale almeno 1-2 volte nei sottotitoli
- Lunghezza ideale: 600-1500 parole
- Concludi con un invito al contatto (la CTA è già aggiunta automaticamente in fondo)

## Passo 4 — Pubblica

1. **Salva** il file in Notepad (Ctrl+S)
2. Doppio click su **`pubblica-articoli.bat`** → genera l'HTML e aggiorna l'indice del blog
3. Doppio click su **`serve.bat`** → apri il browser per vedere come viene
4. Quando sei contenta: doppio click su **`carica-online.bat`** → invia tutto su GitHub
5. Vai sul tuo cPanel → "Git Version Control" → "Update from Remote" → "Deploy HEAD Commit"

🎉 Fatto. L'articolo è online.

## Modificare un articolo esistente
1. Apri il file `.md` corrispondente in `_articles/`
2. Modifica e salva
3. `pubblica-articoli.bat` → `carica-online.bat`

## Suggerimenti per le immagini
- Le immagini disponibili sono in `assets/img/photos/`
- Per usarne una nuova: copiala dentro quella cartella, poi nel markdown usa `image: /assets/img/photos/nomefile.jpg`
- Dimensioni ideali: 1000×750 px, JPG o WebP, < 200 KB

## Lista comandi
| Doppio click | Cosa fa |
|---|---|
| `nuovo-articolo.bat` | Crea un nuovo articolo dal template |
| `pubblica-articoli.bat` | Rigenera tutti gli articoli HTML |
| `serve.bat` | Anteprima del sito in `localhost:8000` |
| `carica-online.bat` | Pubblica online via GitHub |

