"""Render index.html to the downloadable CV PDFs (English + French).

Usage:  python tools/build_pdfs.py
Needs:  pip install playwright   (uses the locally installed Google Chrome)
Writes: assets/Ziad-Ouariachi-CV-EN.pdf, assets/Ziad-Ouariachi-CV-FR.pdf
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "index.html").as_uri()

VIEWPORT_W = 1200            # desktop layout width rendered onto the page
A4_W_PX = 210 / 25.4 * 96    # A4 width in CSS px
SCALE = round(A4_W_PX / VIEWPORT_W, 3)


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": VIEWPORT_W, "height": 1000})
        page.emulate_media(media="screen")
        for lang in ("en", "fr"):
            page.goto(f"{PAGE}?pdf=1&lang={lang}", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 0)")
            out = ROOT / "assets" / f"Ziad-Ouariachi-CV-{lang.upper()}.pdf"
            page.pdf(path=str(out), format="A4", print_background=True, scale=SCALE,
                     margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
        browser.close()


if __name__ == "__main__":
    main()
