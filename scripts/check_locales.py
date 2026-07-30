#!/usr/bin/env python3
"""Validate the locale registry without requiring translated output."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
errors: list[str] = []
locales = CONFIG.get("locales", [])
default_id = CONFIG.get("default_locale")
if not locales:
    errors.append("locale: no locales configured")
if sum(bool(locale.get("default")) for locale in locales) != 1:
    errors.append("locale: expected exactly one default locale")
if sum(locale.get("id") == default_id for locale in locales) != 1:
    errors.append(f"locale: default_locale {default_id!r} must identify exactly one locale")
ids = [locale.get("id") for locale in locales]
prefixes = [locale.get("url_prefix") for locale in locales]
if len(ids) != len(set(ids)):
    errors.append("locale: identifiers are not unique")
if len(prefixes) != len(set(prefixes)):
    errors.append("locale: URL prefixes are not unique")

required_shell = {
    "navigation.primary_label", "navigation.toggle_label", "navigation.home_label",
    "navigation.cta", "navigation.cta_subject", "navigation.language_label", "navigation.labels", "brand.subtitle",
    "brand.footer_subtitle", "accessibility.skip_to_content", "footer.description",
    "footer.begin", "footer.node_appliances", "footer.pilot", "footer.patterns",
    "footer.explore", "footer.what_we_build", "footer.method", "footer.field",
    "footer.about", "footer.connect", "footer.privacy", "footer.copyright",
    "footer.quiet_principles",
    "metadata.site_name", "metadata.manifest_name", "metadata.manifest_short_name",
}

def value_at(document: dict, path: str):
    value = document
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value

route_sets: list[set[str]] = []
for locale in locales:
    locale_id = locale.get("id", "<missing>")
    if not locale.get("language_name"):
        errors.append(f"locale {locale_id}: missing language_name")
    if locale.get("direction") not in {"ltr", "rtl"}:
        errors.append(f"locale {locale_id}: direction must be ltr or rtl")
    if not isinstance(locale.get("url_prefix"), str):
        errors.append(f"locale {locale_id}: url_prefix must be a string")
    shell_path = ROOT / locale.get("shell", "")
    content_dir = ROOT / locale.get("content_dir", "")
    if not shell_path.is_file():
        errors.append(f"locale {locale_id}: missing shell file {shell_path}")
        shell = {}
    else:
        shell = json.loads(shell_path.read_text(encoding="utf-8"))
    for key in required_shell:
        if value_at(shell, key) in (None, ""):
            errors.append(f"locale {locale_id}: missing required shell key {key}")
    labels = value_at(shell, "navigation.labels") or {}
    for item in CONFIG.get("nav", []):
        if item["key"] not in labels:
            errors.append(f"locale {locale_id}: missing navigation label {item['key']}")
    routes = []
    keys = []
    for page in locale.get("pages", []):
        route = page.get("output")
        key = page.get("key")
        if route in routes:
            errors.append(f"locale {locale_id}: duplicate generated route {route}")
        if key in keys:
            errors.append(f"locale {locale_id}: duplicate page key {key}")
        routes.append(route)
        keys.append(key)
        source = content_dir / "pages" / page.get("source", "")
        if not source.is_file():
            errors.append(f"locale {locale_id}: missing page source {source}")
    route_sets.append(set(page.get("key") for page in locale.get("pages", [])))
if route_sets and any(routes != route_sets[0] for routes in route_sets[1:]):
    errors.append("locale: page route identity coverage differs between locales")
if route_sets and set(route_sets[0]) != {"home", "work", "appliances", "pilot", "patterns", "method", "field", "about", "privacy"}:
    errors.append("locale: ordinary page key set is incomplete or drifting")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"PASS: locale integrity ({len(locales)} locale, {len(route_sets[0]) if route_sets else 0} equivalent page routes)")
print("PASS: complete shell keys, unique IDs/prefixes, valid directions, and no silent page fallback")
