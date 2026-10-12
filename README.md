# Ziad Ouariachi — CV website

Single-page, bilingual (EN / FR) CV site for Ziad Ouariachi, Senior Equity Research Analyst (Casablanca).
Plain HTML/CSS/JS — no build step, no framework. Hosted on GitHub Pages.

**Live:** https://ziad-ouariachi.github.io/

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
  build_dist.py             upload-ready copy for any host, final URL baked in
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

## Deploying to any host
```bash
python tools/build_dist.py https://your-final-url/
```
This writes `dist/` and `dist.zip`, a clean copy of only the public files with the final URL baked into
the canonical, social preview and sitemap tags. Upload `dist.zip` to Netlify Drop or Cloudflare Pages, or serve `dist/` anywhere.

## Deploying (GitHub Pages)
GitHub Pages serves the `main` branch root. Push to `main` and the site updates in about a minute.
If the site moves to another URL, update the absolute URLs in `index.html` (`canonical`, `og:*`, `twitter:*`,
JSON-LD) and `sitemap.xml`.

## Ownership & handover
The site lives in the GitHub organization **ziad-ouariachi** (repo `ziad-ouariachi.github.io`, served at the root URL).
To hand over: invite Ziad's GitHub account as an organization **Owner**
(Organization → People → Invite member → role *Owner*). Once he accepts, the previous owner can leave the organization.
