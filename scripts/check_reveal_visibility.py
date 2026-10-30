#!/usr/bin/env python3
"""Check that decorative animations cannot hide published reading content."""
from pathlib import Path
import re
import json

root = Path(__file__).resolve().parents[1]
css_source = (root / "src/assets/site.css").read_text(encoding="utf-8")
js_source = (root / "src/assets/site.js").read_text(encoding="utf-8")
layout = (root / "src/layout.html").read_text(encoding="utf-8")

def rule(css, selector):
    pattern = r"(?m)^" + re.escape(selector) + r"[ ]*[{]([^}]*)[}]"
    result = re.search(pattern, css)
    assert result is not None, f"missing CSS rule: {selector}"
    return result.group(1)

def declaration(block, name):
    match = re.search(r"(?:^|;)[ ]*" + re.escape(name) + r"[ ]*:[ ]*([^;]+)", block)
    return match.group(1).strip() if match else None

base = rule(css_source, "[data-reveal]")
js_enabled = rule(css_source, ".has-js [data-reveal]")
visible = rule(css_source, ".has-js [data-reveal].is-visible")
assert declaration(base, "opacity") == "1", "plain HTML must be visible"
assert declaration(js_enabled, "opacity") == "1", "JS must never hide content pending observer"
assert declaration(visible, "opacity") == "1", "observed content must stay visible"
assert declaration(js_enabled, "transform") == "translateY(18px)"
assert declaration(visible, "transform") == "none"
assert re.search(r"threshold:[ ]*0(?=[ ,}])", js_source), "tall groups need a zero threshold"
assert "entry.isIntersecting" in js_source
assert "site.css?v=20261030-reveal" in layout
assert "site.js?v=20261030-reveal" in layout

for name, text in (("site.css", css_source), ("site.js", js_source)):
    served = (root / "dist/assets" / name).read_text(encoding="utf-8")
    assert text == served, name + ": source/build mismatch"

publication = (root / "dist/publications/index.html").read_text(encoding="utf-8")
manifest = json.loads((root / "data/publications.dev.v1.json").read_text(encoding="utf-8"))
assert publication.count('class="publication-card"') == len(manifest["publications"]), "published cards differ from approved manifest"
assert 'class="shell publication-list" data-reveal' in publication
assert "site.css?v=20261030-reveal" in publication
assert "site.js?v=20261030-reveal" in publication
print("PASS: reveal content stays visible even if animation JS fails")
print("PASS: tall publication list animates on first intersection")
print("PASS: changed CSS/JS use cache-busted public URLs")
