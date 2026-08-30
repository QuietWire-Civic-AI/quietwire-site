# QuietWire Site

A static, local-first public website for QuietWire.

## Design rules

- No framework or external runtime is required to serve the site.
- No advertising, trackers, external fonts, or third-party JavaScript.
- Locale-specific page fragments live in `src/content/<locale>/pages/`.
- Locale-specific shell strings live in `src/i18n/<locale>.json`.
- English (`en-CA`) is unprefixed; Arabic (`ar`) uses `/ar/` and RTL output.
- Language links connect equivalent routes without JavaScript or automatic redirects.
- Shared structure lives in `src/layout.html` and `site.config.json`.
- `dist/` is committed so a web server can serve it immediately.
- Builds are deterministic enough to package into content-addressed releases.
- Publications are generated from a fail-closed, public-safe manifest. The
  checked-in v1 input is now the current curated public handoff snapshot copied
  from an approved Internal export; the public repo and host still receive no
  private Internal credentials or provenance fields. Confirmed publication fact
  and explicit `listed` website visibility remain separate required decisions.
- QuietWire Editions is a separate first-party publishing lane. Its checked-in
  public-safe export is copied from the governed `editions-content` source lane;
  only records explicitly marked `release_state: approved` and
  `website_visibility: listed` can render.

## Build

```bash
make check
```

## Preview

```bash
make preview
```

Then open `http://127.0.0.1:8080`.

## Create a release bundle

```bash
make release
```

This produces a static archive and manifest under `releases/`. A later QWOS deployment module can attest and atomically activate that release on Teddy.

## Structure

```text
site.config.json      site metadata, ordinary routes, and locale registry
src/layout.html       shared document shell
src/content/en-CA/    default-locale page content
src/content/ar/       machine-assisted Arabic page drafts pending human review
src/i18n/en-CA.json   default-locale shell strings
src/assets/           CSS, JavaScript, and local graphics
scripts/build.py      dependency-free static builder
scripts/check.py      link, metadata, and tracker checks
scripts/publications.py public-safe external-publications validator and renderer
scripts/editions.py   public-safe first-party Editions validator and renderer
data/publications.dev.v1.json current curated public-safe Publications handoff snapshot (legacy first-slice filename)
data/editions-site.v1.json small website-side Editions collection configuration
exports/editions.v1.json approved public-safe Editions metadata handoff
exports/editions/      approved non-executable first-party body fragments
schemas/              machine-readable public manifest contracts
scripts/release.py    content-addressed release packager
dist/                 ready-to-serve output
deploy/               bounded Teddy hosting examples
```

## Publishing boundary

Models and companions may draft source changes and previews. Production publishing should remain an explicit human-approved release action.

Discovery remains English-only at `/discovery/`; it has no `/ar/discovery/`
route. Arabic translation governance is recorded in `docs/i18n/`.

Publications is an English-source collection at `/publications/`. It has no
fabricated localized counterparts. Its contract and synchronization handoff
boundary are documented in `docs/PUBLICATIONS_MANIFEST.md`.

QuietWire Editions is also an explicit English-source surface. `/editions/`
lists first-party originals and `/editions/<slug>/` carries their canonical
QuietWire pages. Editions source, approval, export, website merge, Teddy
activation, and downstream syndication remain separate powers. The website-side
boundary is documented in `docs/EDITIONS_V2.md`.
