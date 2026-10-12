# Ziad Ouariachi — CV website

Single-page, bilingual (EN / FR) CV site for Ziad Ouariachi, Senior Equity Research Analyst (Casablanca).
Plain HTML/CSS/JS — no build step, no framework. Hosted on GitHub Pages.

**Live:** https://matsmiersen.github.io/ZiadCV/

## Features
- English ↔ French toggle and light ↔ dark toggle (both remembered in `localStorage`)
- Downloadable CV PDFs (EN and FR) rendered from this same page
- Responsive from 320 px phones to desktop; accessible (keyboard, screen readers, reduced motion)
- Social preview card, favicons, structured data (schema.org `Person`)

## Structure
```
index.html                  the whole site (styles, markup, translations, script)
assets/
  ziad-ouariachi.jpg        headshot
  og-image.jpg              social preview card (1200×630)
  Ziad-Ouariachi-CV-EN.pdf  generated — do not edit by hand
  Ziad-Ouariachi-CV-FR.pdf  generated — do not edit by hand
  icons/                    favicons + app icons (generated)
  logos/                    employer / school logos (official sources)
tools/
  build_pdfs.py             index.html → the two CV PDFs
  build_brand.py            favicons + og-image.jpg
  brand/og-image.html       template for the social card
site.webmanifest, sitemap.xml, .nojekyll
```

## Editing content
All text lives in `index.html`:
- **Markup** carries the English default text with a `data-i18n="key"` attribute.
- **Translations** are in the `I18N` object near the bottom (`en: {…}` and `fr: {…}`). Change a key in **both** languages.
- Attributes (placeholders, aria-labels, alt text) use `data-i18n-attr="attr:key"`.

URL overrides (not saved): `?lang=fr`, `?theme=dark`, `?pdf=1` (print layout used for the PDFs).

## After editing — regenerate the PDFs
The download buttons serve PDFs of this page, so rebuild them whenever content changes:

```bash
pip install playwright pillow
python tools/build_pdfs.py      # writes assets/Ziad-Ouariachi-CV-EN.pdf and -FR.pdf
python tools/build_brand.py     # only if the name/title/photo changed (og image, icons)
```
Both scripts use the locally installed Google Chrome. Each PDF should be 4 A4 pages; if new content
pushes a section onto a 5th page, tighten the `.pdf-mode` spacing rules in `index.html`.

## Preview locally
```bash
python -m http.server 5173
```
then open http://localhost:5173/.

## Deploying
GitHub Pages serves the `main` branch root. Push to `main` and the site updates in about a minute.
If the site moves to another URL, update the absolute URLs in `index.html` (`canonical`, `og:*`, `twitter:*`,
JSON-LD) and `sitemap.xml`.
