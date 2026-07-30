# QuietWire Site

A static, local-first public website for QuietWire.

## Design rules

- No framework or external runtime is required to serve the site.
- No advertising, trackers, external fonts, or third-party JavaScript.
- Locale-specific page fragments live in `src/content/<locale>/pages/`.
- Locale-specific shell strings live in `src/i18n/<locale>.json`.
- Shared structure lives in `src/layout.html` and `site.config.json`.
- `dist/` is committed so a web server can serve it immediately.
- Builds are deterministic enough to package into content-addressed releases.

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
site.config.json      site metadata, routes, and locale registry
src/layout.html       shared document shell
src/content/en-CA/    default-locale page content
src/i18n/en-CA.json    default-locale shell strings
src/assets/           CSS, JavaScript, and local graphics
scripts/build.py      dependency-free static builder
scripts/check.py      link, metadata, and tracker checks
scripts/release.py    content-addressed release packager
dist/                 ready-to-serve output
deploy/               bounded Teddy hosting examples
```

## Publishing boundary

Models and companions may draft source changes and previews. Production publishing should remain an explicit human-approved release action.
