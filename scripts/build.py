#!/usr/bin/env python3
from __future__ import annotations
import json, shutil
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"
CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))


def replace(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def navigation(active: str) -> str:
    links = []
    for item in CONFIG["nav"]:
        current = ' aria-current="page"' if item["key"] == active else ""
        links.append(f'<a href="{escape(item["href"])}"{current}>{escape(item["label"])}</a>')
    return "\n".join(links)


def canonical(output: str) -> str:
    if output == "index.html":
        return CONFIG["base_url"] + "/"
    return CONFIG["base_url"] + "/" + output.removesuffix("index.html")


def structured_data() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "QuietWire",
        "url": CONFIG["base_url"],
        "email": CONFIG["email"],
        "description": CONFIG["description"],
        "sameAs": [
            "https://github.com/QuietWire-Civic-AI",
            "https://www.linkedin.com/company/quietwire/"
        ]
    }
    return json.dumps(data, separators=(",", ":"))


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(SRC / "assets", DIST / "assets")
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    year = str(datetime.now(timezone.utc).year)
    for page in CONFIG["pages"]:
        body = (SRC / "pages" / page["source"]).read_text(encoding="utf-8")
        output = DIST / page["output"]
        output.parent.mkdir(parents=True, exist_ok=True)
        html = replace(layout, {
            "page_title": escape(page["title"]),
            "page_description": escape(page["description"]),
            "page_key": escape(page["key"]),
            "canonical_url": canonical(page["output"]),
            "base_url": CONFIG["base_url"],
            "structured_data": structured_data(),
            "navigation": navigation(page["key"]),
            "content": body,
            "year": year,
        })
        output.write_text(html.rstrip() + "\n", encoding="utf-8")

    for app in CONFIG.get("static_apps", []):
        source = SRC / app["source"]
        output = DIST / app["output"]
        shutil.copytree(source, output)

    (DIST / "404.html").write_text((DIST / "index.html").read_text(encoding="utf-8").replace(
        "Coherence infrastructure for organizations with a story to protect.",
        "This wire does not lead anywhere yet."
    ).replace(
        "QuietWire — Coherence Infrastructure",
        "Page not found — QuietWire"
    ), encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f'User-agent: *\nAllow: /\n\nSitemap: {CONFIG["base_url"]}/sitemap.xml\n', encoding="utf-8"
    )
    urls = [canonical(page["output"]) for page in CONFIG["pages"]]
    urls.extend(CONFIG["base_url"] + "/" + app["output"].strip("/") + "/" for app in CONFIG.get("static_apps", []))
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
        + '\n</urlset>\n',
        encoding="utf-8"
    )
    manifest = {
        "name": "QuietWire",
        "short_name": "QuietWire",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a1212",
        "theme_color": "#0a1212",
        "icons": [
            {"src": "/assets/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}
        ]
    }
    (DIST / "site.webmanifest").write_text(json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    (DIST / "CNAME").write_text("www.quietwire.ai\n", encoding="utf-8")

if __name__ == "__main__":
    build()
    print(
        f"Built {len(CONFIG['pages'])} pages and "
        f"{len(CONFIG.get('static_apps', []))} static app(s) in {DIST}"
    )
