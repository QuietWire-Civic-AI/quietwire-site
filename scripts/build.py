#!/usr/bin/env python3
from __future__ import annotations
import json, shutil
from datetime import datetime, timezone
from html import escape
from pathlib import Path

from editions import load_manifest as load_editions_manifest, render_edition, render_editions_landing
from home_library import render_home_library
from library import render_library
from publications import load_manifest, render_publications

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"
CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
EDITIONS_CONFIG = json.loads((ROOT / "data" / "editions-site.v1.json").read_text(encoding="utf-8"))


def replace(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def locales() -> list[dict]:
    return CONFIG["locales"]


def locale_path(page: dict, locale: dict) -> str:
    prefix = locale["url_prefix"].strip("/")
    route_prefix = ("/" + prefix) if prefix else ""
    if page["output"] == "index.html":
        return route_prefix + "/"
    return route_prefix + "/" + page["output"].removesuffix("index.html")


def canonical_url(page: dict, locale: dict) -> str:
    return CONFIG["base_url"] + locale_path(page, locale)


def page_for_key(locale: dict, key: str, required: bool = True) -> dict | None:
    for page in locale["pages"]:
        if page["key"] == key:
            return page
    if required:
        raise ValueError(f"locale {locale['id']} has no page key {key}")
    return None


def navigation(active: str, shell: dict, locale: dict) -> str:
    links = []
    for item in CONFIG["nav"]:
        if item.get("locales") and locale["id"] not in item["locales"]:
            continue
        page = page_for_key(locale, item["key"], required=False)
        if page is None and not item.get("href"):
            continue
        current = ' aria-current="page"' if item["key"] == active else ""
        label = shell["navigation"]["labels"][item["key"]]
        href = item["href"] if page is None and item.get("href") else locale_path(page, locale)
        links.append(f'<a href="{escape(href)}"{current}>{escape(label)}</a>')
    return "\n".join(links)


def language_links(page: dict, locale: dict) -> tuple[str, str]:
    links = []
    alternates = []
    available = []
    for other in locales():
        equivalent = page_for_key(other, page["key"], required=False)
        if equivalent is None:
            continue
        available.append((other, equivalent))
        href = locale_path(equivalent, other)
        name = other["language_name"]
        current = ' aria-current="true"' if other["id"] == locale["id"] else ""
        links.append(
            f'<a href="{escape(href)}" hreflang="{escape(other["id"])}" '
            f'lang="{escape(other["id"])}" dir="auto"{current}>{escape(name)}</a>'
        )
        alternates.append(f'<link rel="alternate" hreflang="{escape(other["id"])}" href="{escape(canonical_url(equivalent, other))}">')
    default_locale = next(l for l in locales() if l["id"] == CONFIG["default_locale"])
    default_page = page_for_key(default_locale, page["key"], required=False)
    if default_page is not None:
        alternates.append(f'<link rel="alternate" hreflang="x-default" href="{escape(canonical_url(default_page, default_locale))}">')
    return " ".join(links), "\n  ".join(alternates)


def single_locale_language_data(page: dict, locale: dict) -> tuple[str, str]:
    path = locale_path(page, locale)
    url = canonical_url(page, locale)
    return (
        f'<a href="{escape(path)}" hreflang="{escape(locale["id"])}" '
        f'lang="{escape(locale["id"])}" dir="auto" aria-current="true">'
        f'{escape(locale["language_name"])}</a>',
        f'<link rel="alternate" hreflang="{escape(locale["id"])}" href="{escape(url)}">\n  '
        f'<link rel="alternate" hreflang="x-default" href="{escape(url)}">',
    )


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


def render_document(
    layout: str,
    page: dict,
    locale: dict,
    shell: dict,
    body: str,
    year: str,
    language_data: tuple[str, str] | None = None,
) -> str:
    links, alternates = language_data if language_data is not None else language_links(page, locale)
    urls = {item["key"]: locale_path(item, locale) for item in locale["pages"]}
    return replace(layout, {
        "lang": escape(locale["id"]),
        "direction": escape(locale["direction"]),
        "hreflang": alternates,
        "language_links": links,
        "language_label": shell["navigation"]["language_label"],
        "current_language": locale["language_name"],
        "home_url": urls["home"],
        "work_url": urls["work"],
        "advisory_url": urls.get("advisory", "/advisory/"),
        "appliances_url": urls["appliances"], "pilot_url": urls["pilot"],
        "patterns_url": urls["patterns"], "method_url": urls["method"], "field_url": urls["field"],
        "about_url": urls["about"], "privacy_url": urls["privacy"],
        "page_title": escape(page["title"]),
        "page_description": escape(page["description"]),
        "page_key": escape(page["key"]),
        "canonical_url": canonical_url(page, locale),
        "base_url": CONFIG["base_url"],
        "structured_data": structured_data(shell["metadata"]["site_name"]),
        "site_name": shell["metadata"]["site_name"],
        "navigation": navigation(page["key"], shell, locale),
        "skip_to_content": shell["accessibility"]["skip_to_content"],
        "home_label": shell["navigation"]["home_label"],
        "toggle_label": shell["navigation"]["toggle_label"],
        "primary_label": shell["navigation"]["primary_label"],
        "cta": shell["navigation"]["cta"], "cta_subject": shell["navigation"]["cta_subject"],
        "brand_subtitle": shell["brand"]["subtitle"], "footer_subtitle": shell["brand"]["footer_subtitle"],
        "footer_description": shell["footer"]["description"], "begin": shell["footer"]["begin"],
        "advisory": shell["footer"].get("advisory", "QuietWire Advisory"),
        "node_appliances": shell["footer"]["node_appliances"], "pilot": shell["footer"]["pilot"],
        "patterns": shell["footer"]["patterns"], "explore": shell["footer"]["explore"],
        "what_we_build": shell["footer"]["what_we_build"], "method": shell["footer"]["method"],
        "field": shell["footer"]["field"], "about": shell["footer"]["about"],
        "library_link": '\n        <a href="/library/">Library</a>' if locale["id"] == CONFIG["default_locale"] else "",
        "connect": shell["footer"]["connect"], "privacy": shell["footer"]["privacy"],
        "copyright": shell["footer"]["copyright"].replace("{{year}}", year),
        "quiet_principles": shell["footer"]["quiet_principles"], "content": body, "year": year,
    })


def build() -> None:
    collection = CONFIG["publications_collection"]
    publication_records = load_manifest(ROOT / collection["manifest"])
    editions_collection = EDITIONS_CONFIG
    edition_records = load_editions_manifest(ROOT / editions_collection["manifest"])

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(SRC / "assets", DIST / "assets")
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    year = str(datetime.now(timezone.utc).year)
    default_locale = next(locale for locale in locales() if locale["id"] == CONFIG["default_locale"])
    default_shell = json.loads((ROOT / default_locale["shell"]).read_text(encoding="utf-8"))
    home_library_shelf = ""

    for locale in locales():
        shell = json.loads((ROOT / locale["shell"]).read_text(encoding="utf-8"))
        for page in locale["pages"]:
            body = (ROOT / locale["content_dir"] / "pages" / page["source"]).read_text(encoding="utf-8")
            if locale["id"] == default_locale["id"] and page["key"] == "home":
                marker = "{{home_library_shelf}}"
                if marker not in body:
                    raise ValueError("English home page is missing the home Library shelf marker")
                home_library_shelf = render_home_library(CONFIG["home_library"], edition_records, publication_records)
                body = body.replace(marker, home_library_shelf)
            relative_output = (Path(locale["url_prefix"]) / page["output"] if locale["url_prefix"] else Path(page["output"]))
            output = DIST / relative_output
            output.parent.mkdir(parents=True, exist_ok=True)
            html = render_document(layout, page, locale, shell, body, year)
            output.write_text(html.rstrip() + "\n", encoding="utf-8")

    collection_locale = next(locale for locale in locales() if locale["id"] == collection["locale"])
    collection_shell = json.loads((ROOT / collection_locale["shell"]).read_text(encoding="utf-8"))
    collection_page = {
        "output": collection["output"], "key": collection["key"],
        "title": collection["title"], "description": collection["description"],
    }
    collection_url = canonical_url(collection_page, collection_locale)
    collection_output = DIST / collection["output"]
    collection_output.parent.mkdir(parents=True, exist_ok=True)
    collection_html = render_document(
        layout, collection_page, collection_locale, collection_shell,
        render_publications(publication_records), year, single_locale_language_data(collection_page, collection_locale),
    )
    collection_output.write_text(collection_html.rstrip() + "\n", encoding="utf-8")

    editions_locale = next(locale for locale in locales() if locale["id"] == editions_collection["locale"])
    editions_shell = json.loads((ROOT / editions_locale["shell"]).read_text(encoding="utf-8"))
    editions_page = {
        "output": editions_collection["output"],
        "key": editions_collection["key"],
        "title": editions_collection["title"],
        "description": editions_collection["description"],
    }
    editions_url = canonical_url(editions_page, editions_locale)
    editions_output = DIST / editions_collection["output"]
    editions_output.parent.mkdir(parents=True, exist_ok=True)
    editions_html = render_document(
        layout, editions_page, editions_locale, editions_shell,
        render_editions_landing(edition_records), year, single_locale_language_data(editions_page, editions_locale),
    )
    editions_output.write_text(editions_html.rstrip() + "\n", encoding="utf-8")

    library_collection = CONFIG["library_collection"]
    library_page = {
        "output": library_collection["output"], "key": library_collection["key"],
        "title": library_collection["title"], "description": library_collection["description"],
    }
    library_output = DIST / library_collection["output"]
    library_output.parent.mkdir(parents=True, exist_ok=True)
    library_html = render_document(
        layout, library_page, editions_locale, editions_shell,
        render_library(edition_records, publication_records), year,
        single_locale_language_data(library_page, editions_locale),
    )
    library_output.write_text(library_html.rstrip() + "\n", encoding="utf-8")

    edition_urls: list[str] = []
    for record in edition_records:
        relative_output = record["canonical_path"].lstrip("/") + "index.html"
        edition_page = {
            "output": relative_output,
            "key": "edition",
            "title": f'{record["title"]} — QuietWire Editions',
            "description": record["summary"],
        }
        if locale_path(edition_page, editions_locale) != record["canonical_path"]:
            raise ValueError(f'Edition route mismatch for {record["edition_id"]}')
        edition_output = DIST / relative_output
        edition_output.parent.mkdir(parents=True, exist_ok=True)
        edition_html = render_document(
            layout, edition_page, editions_locale, editions_shell,
            render_edition(record, CONFIG["base_url"]), year, single_locale_language_data(edition_page, editions_locale),
        )
        edition_output.write_text(edition_html.rstrip() + "\n", encoding="utf-8")
        edition_urls.append(canonical_url(edition_page, editions_locale))

    for app in CONFIG.get("static_apps", []):
        source = SRC / app["source"]
        output = DIST / app["output"]
        shutil.copytree(source, output)

    (DIST / "404.html").write_text((DIST / "index.html").read_text(encoding="utf-8").replace(
        "\n\n" + home_library_shelf + "\n\n",
        "\n\n"
    ).replace(
        "Coherence infrastructure for organizations with a story to protect.",
        "This wire does not lead anywhere yet."
    ).replace(
        "QuietWire — Coherence Infrastructure",
        "Page not found — QuietWire"
    ), encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f'User-agent: *\nAllow: /\n\nSitemap: {CONFIG["base_url"]}/sitemap.xml\n', encoding="utf-8"
    )
    urls = [canonical_url(page, locale) for locale in locales() for page in locale["pages"]]
    urls.append(collection_url)
    urls.append(editions_url)
    urls.append(CONFIG["base_url"] + "/library/")
    urls.extend(edition_urls)
    urls.extend(CONFIG["base_url"] + "/" + app["output"].strip("/") + "/" for app in CONFIG.get("static_apps", []))
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{url}</loc></url>" for url in urls)
        + '\n</urlset>\n', encoding="utf-8"
    )
    manifest = {
        "name": default_shell["metadata"]["manifest_name"],
        "short_name": default_shell["metadata"]["manifest_short_name"],
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
        f"Built {sum(len(locale['pages']) for locale in locales())} pages, "
        f"1 publications collection, 1 Editions collection, and "
        f"{len(CONFIG.get('static_apps', []))} static app(s) in {DIST}"
    )
