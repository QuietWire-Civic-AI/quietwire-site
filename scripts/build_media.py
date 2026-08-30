#!/usr/bin/env python3
"""Build the English-only media layer after the base static site build."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import build as site_build
from media_appearances import (
    load_manifest,
    render_item,
    render_library_shelf,
    render_media_landing,
    render_series,
)

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MEDIA_CONFIG_PATH = ROOT / "data" / "media-site.v1.json"
MARKER = "<!-- quietwire-media-shelf -->"


def _output_for_path(path: str) -> Path:
    return DIST / path.lstrip("/") / "index.html"


def _page_for_path(path: str, title: str, description: str) -> dict:
    return {
        "output": path.lstrip("/") + "index.html",
        "key": "library",
        "title": title,
        "description": description,
    }


def _write_document(layout: str, locale: dict, shell: dict, page: dict, body: str, year: str) -> str:
    output = DIST / page["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    html = site_build.render_document(
        layout,
        page,
        locale,
        shell,
        body,
        year,
        site_build.single_locale_language_data(page, locale),
    )
    output.write_text(html.rstrip() + "\n", encoding="utf-8")
    return site_build.canonical_url(page, locale)


def _inject_library_shelf(config: dict, series: list[dict], items: list[dict]) -> None:
    library_path = DIST / "library" / "index.html"
    if not library_path.is_file():
        raise RuntimeError("media build requires the base /library/ route")
    text = library_path.read_text(encoding="utf-8")
    if text.count(MARKER) != 1:
        raise RuntimeError("media build requires exactly one Library media shelf marker")
    shelf = render_library_shelf(config, series, items)
    library_path.write_text(text.replace(MARKER, shelf), encoding="utf-8")


def _extend_sitemap(urls: list[str]) -> None:
    sitemap_path = DIST / "sitemap.xml"
    text = sitemap_path.read_text(encoding="utf-8")
    closing = "</urlset>\n"
    if text.count(closing) != 1:
        raise RuntimeError("unexpected sitemap structure")
    additions = []
    for url in urls:
        if f"<loc>{url}</loc>" in text:
            continue
        additions.append(f"  <url><loc>{url}</loc></url>")
    if additions:
        text = text.replace(closing, "\n".join(additions) + "\n" + closing)
        sitemap_path.write_text(text, encoding="utf-8")


def build_media() -> None:
    config = json.loads(MEDIA_CONFIG_PATH.read_text(encoding="utf-8"))
    expected_fields = {"manifest", "locale", "output", "title", "description", "library_shelf"}
    if set(config) != expected_fields:
        raise RuntimeError("media-site.v1.json fields do not match the v1 website contract")
    series, items = load_manifest(ROOT / config["manifest"])

    locale = next((value for value in site_build.locales() if value["id"] == config["locale"]), None)
    if locale is None or locale["id"] != site_build.CONFIG["default_locale"]:
        raise RuntimeError("media v1 must remain on the default English locale")
    shell = json.loads((ROOT / locale["shell"]).read_text(encoding="utf-8"))
    layout = (ROOT / "src" / "layout.html").read_text(encoding="utf-8")
    year = str(datetime.now(timezone.utc).year)
    urls: list[str] = []

    landing_page = {
        "output": config["output"],
        "key": "library",
        "title": config["title"],
        "description": config["description"],
    }
    urls.append(_write_document(layout, locale, shell, landing_page, render_media_landing(series, items), year))

    for record in series:
        page = _page_for_path(
            record["canonical_path"],
            f'{record["title"]} — QuietWire Watch & Listen',
            record["summary"],
        )
        if site_build.locale_path(page, locale) != record["canonical_path"]:
            raise RuntimeError(f'media series route mismatch for {record["series_id"]}')
        urls.append(_write_document(layout, locale, shell, page, render_series(record, items), year))

    standalone = [record for record in items if "canonical_path" in record]
    for record in standalone:
        page = _page_for_path(
            record["canonical_path"],
            f'{record["title"]} — QuietWire Watch & Listen',
            record.get("summary", f'{record["venue"]} appearance indexed by QuietWire.'),
        )
        if site_build.locale_path(page, locale) != record["canonical_path"]:
            raise RuntimeError(f'media item route mismatch for {record["stable_id"]}')
        urls.append(_write_document(layout, locale, shell, page, render_item(record), year))

    _inject_library_shelf(config, series, items)
    _extend_sitemap(urls)
    print(
        f"Built media landing, {len(series)} series route(s), {len(standalone)} standalone appearance route(s), "
        f"and injected the bounded Library media shelf"
    )


if __name__ == "__main__":
    build_media()
