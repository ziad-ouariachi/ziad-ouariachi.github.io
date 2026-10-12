"""Render brand assets: social preview image and favicons.

Usage:  python tools/build_brand.py
Needs:  pip install playwright pillow   (uses the locally installed Google Chrome)
Writes: assets/og-image.jpg, assets/icons/*
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "assets" / "icons"

# "ZO" monogram: navy tile, gold Fraunces letters (same as the header brand mark)
ICON_HTML = """<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500&display=block" rel="stylesheet">
<style>
  html, body {{ margin: 0; width: {s}px; height: {s}px; background: transparent; }}
  div {{ width: {s}px; height: {s}px; border-radius: {r}px; background: #0f1c33; color: #dcbb76;
        display: grid; place-items: center; font: 500 {f}px/1 Fraunces, Georgia, serif; letter-spacing: .01em; }}
</style></head><body><div>ZO</div></body></html>"""

# SVG favicon for modern browsers (letters as text; falls back to Georgia)
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#0f1c33"/>
  <text x="32" y="33" text-anchor="middle" dominant-baseline="middle" font-family="Georgia, 'Times New Roman', serif" font-size="27" fill="#dcbb76">ZO</text>
</svg>
"""


def render_icon(page, size, path, rounded=True):
    page.set_viewport_size({"width": size, "height": size})
    page.set_content(ICON_HTML.format(s=size, r=round(size * .22) if rounded else 0, f=round(size * .44)),
                     wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    page.screenshot(path=str(path), omit_background=True)
    print("wrote", path.relative_to(ROOT))


def main():
    ICONS.mkdir(parents=True, exist_ok=True)
    (ICONS / "favicon.svg").write_text(FAVICON_SVG, encoding="utf-8")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page()
        render_icon(page, 32, ICONS / "favicon-32.png")
        render_icon(page, 180, ICONS / "apple-touch-icon.png", rounded=False)  # iOS rounds it itself
        render_icon(page, 192, ICONS / "icon-192.png")
        render_icon(page, 512, ICONS / "icon-512.png")

        page.set_viewport_size({"width": 1200, "height": 630})
        page.goto((ROOT / "tools" / "brand" / "og-image.html").as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        out = ROOT / "assets" / "og-image.jpg"
        page.screenshot(path=str(out), type="jpeg", quality=88)
        print("wrote", out.relative_to(ROOT))
        browser.close()

    # Re-encode PNGs compactly
    from PIL import Image
    for p in ICONS.glob("*.png"):
        Image.open(p).save(p, optimize=True)


if __name__ == "__main__":
    main()
