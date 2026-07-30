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


def current_locale() -> dict:
    locales = CONFIG["locales"]
    for locale in locales:
        if locale["id"] == CONFIG["default_locale"]:
            return locale
    raise ValueError(f"default locale not found: {CONFIG['default_locale']}")


def navigation(active: str, shell: dict) -> str:
    links = []
    for item in CONFIG["nav"]:
        current = ' aria-current="page"' if item["key"] == active else ""
        label = shell["navigation"]["labels"][item["key"]]
        links.append(f'<a href="{escape(item["href"])}"{current}>{escape(label)}</a>')
    return "\n".join(links)


def canonical(output: str, locale: dict) -> str:
    prefix = locale["url_prefix"].strip("/")
    route_prefix = ("/" + prefix) if prefix else ""
    if output == "index.html":
        return CONFIG["base_url"] + route_prefix + "/"
    return CONFIG["base_url"] + route_prefix + "/" + output.removesuffix("index.html")


def structured_data(site_name: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": site_name,
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
    locale = current_locale()
    shell = json.loads((ROOT / locale["shell"]).read_text(encoding="utf-8"))
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(SRC / "assets", DIST / "assets")
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    year = str(datetime.now(timezone.utc).year)
    for page in locale["pages"]:
        body = (ROOT / locale["content_dir"] / "pages" / page["source"]).read_text(encoding="utf-8")
        output = DIST / page["output"]
        output.parent.mkdir(parents=True, exist_ok=True)
        html = replace(layout, {
            "page_title": escape(page["title"]),
            "page_description": escape(page["description"]),
            "page_key": escape(page["key"]),
            "canonical_url": canonical(page["output"], locale),
            "base_url": CONFIG["base_url"],
            "structured_data": structured_data(shell["metadata"]["site_name"]),
            "site_name": shell["metadata"]["site_name"],
            "navigation": navigation(page["key"], shell),
            "skip_to_content": shell["accessibility"]["skip_to_content"],
            "home_label": shell["navigation"]["home_label"],
            "toggle_label": shell["navigation"]["toggle_label"],
            "primary_label": shell["navigation"]["primary_label"],
            "cta": shell["navigation"]["cta"],
            "cta_subject": shell["navigation"]["cta_subject"],
            "brand_subtitle": shell["brand"]["subtitle"],
            "footer_subtitle": shell["brand"]["footer_subtitle"],
            "footer_description": shell["footer"]["description"],
            "begin": shell["footer"]["begin"],
            "node_appliances": shell["footer"]["node_appliances"],
            "pilot": shell["footer"]["pilot"],
            "patterns": shell["footer"]["patterns"],
            "explore": shell["footer"]["explore"],
            "what_we_build": shell["footer"]["what_we_build"],
            "method": shell["footer"]["method"],
            "field": shell["footer"]["field"],
            "about": shell["footer"]["about"],
            "connect": shell["footer"]["connect"],
            "privacy": shell["footer"]["privacy"],
            "copyright": shell["footer"]["copyright"].replace("{{year}}", year),
            "quiet_principles": shell["footer"]["quiet_principles"],
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
    urls = [canonical(page["output"], locale) for page in locale["pages"]]
    urls.extend(CONFIG["base_url"] + "/" + app["output"].strip("/") + "/" for app in CONFIG.get("static_apps", []))
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
        + '\n</urlset>\n',
        encoding="utf-8"
    )
    manifest = {
        "name": shell["metadata"]["manifest_name"],
        "short_name": shell["metadata"]["manifest_short_name"],
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
    built_locale = current_locale()
    print(
        f"Built {len(built_locale['pages'])} pages and "
        f"{len(CONFIG.get('static_apps', []))} static app(s) in {DIST}"
    )
