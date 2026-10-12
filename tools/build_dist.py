"""Package the site for any static host, with its final public URL baked in.

Usage:  python tools/build_dist.py https://ziadouariachi.github.io/
Writes: dist/            (upload this folder, or point the host at it)
        dist.zip         (same, zipped: for drag-and-drop hosts)

The source files keep their current URL; only the copy in dist/ is rewritten
(canonical, og:url, og:image, twitter:image, JSON-LD, sitemap).
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
PUBLISH = ["index.html", "site.webmanifest", "sitemap.xml", ".nojekyll", "assets"]
CURRENT = re.search(r'<link rel="canonical" href="([^"]+)"', (ROOT / "index.html").read_text(encoding="utf-8")).group(1)


def main():
    if len(sys.argv) != 2 or not sys.argv[1].startswith("https://"):
        raise SystemExit("usage: python tools/build_dist.py https://your-site/")
    url = sys.argv[1].rstrip("/") + "/"

    shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir()
    for item in PUBLISH:
        src = ROOT / item
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, DIST / item)

    for name in ("index.html", "sitemap.xml"):
        p = DIST / name
        p.write_text(p.read_text(encoding="utf-8").replace(CURRENT, url), encoding="utf-8")

    # Cache headers for Cloudflare Pages / Netlify (ignored elsewhere)
    (DIST / "_headers").write_text(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
        "/assets/*\n  Cache-Control: public, max-age=604800\n", encoding="utf-8")

    archive = shutil.make_archive(str(ROOT / "dist"), "zip", DIST)
    print(f"dist/ ready for {url}  ({sum(f.stat().st_size for f in DIST.rglob('*') if f.is_file()) // 1024} KB)")
    print(f"zip: {Path(archive).name}")


if __name__ == "__main__":
    main()
