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

## Public information architecture

The English public frame is organized around four operating lanes:

- **Advisory** — define the decision, objective, authority, trust boundary, and conditions for success.
- **Labs** — test consequential uncertainty and preserve evidence before an experiment becomes a supported promise.
- **Work** — deploy supported capability around real work.
- **Library** — publish selected thinking, field lessons, media, and first-party material.

`About` remains top-level institutional context.

The deeper implementation surfaces remain intact: Appliances, Pilot, Patterns, Method, Field, Discovery, Publications, and Editions. Hardware is an implementation configuration beneath Work rather than the public starting ontology of QuietWire.

Labs is currently an English-only first-party surface under `src/labs/`, copied as a static app. This intentionally avoids fabricating translated Labs pages while Arabic, Spanish, and Canadian-French review states remain distinct. Existing localized route bodies are preserved; their translation manifests record the English Home/Work information-architecture drift introduced on 2026-09-06.

## Build

```bash
make check
```

## Sync an approved Publications export

The public site never reads the private Internal repository directly. After an
authorized steward has produced the sanitized `publications.v1.json` export,
sync it explicitly:

```bash
python3 scripts/sync_publications.py /path/to/publications.v1.json
make check
```

The sync command validates the fail-closed public contract, no-ops when the
approved export already matches the checked-in site snapshot, and writes a
deterministic hash receipt at `data/publications-sync-receipt.v1.json`. It
performs no network access and no Teddy production activation.

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
site.config.json      site metadata, ordinary routes, locale registry, navigation, and static surfaces
src/layout.html       shared document shell
src/content/en-CA/    default-locale page content
src/content/ar/       machine-assisted Arabic page drafts with partial human review
src/content/es/       machine-assisted Spanish page drafts pending human review
src/content/fr-CA/    machine-assisted Canadian-French page drafts pending human review
src/i18n/             locale-specific shell strings
src/labs/             English-only QuietWire Labs public surface
src/assets/           CSS, JavaScript, and local graphics
scripts/build.py      dependency-free static builder
scripts/check.py      link, metadata, locale, and tracker checks
scripts/publications.py public-safe external-publications validator and renderer
scripts/sync_publications.py bounded approved-export -> site snapshot sync with hash receipt
scripts/check_sync_publications.py self-checks for the bounded sync path
scripts/editions.py   public-safe first-party Editions validator and renderer
data/publications.dev.v1.json current curated public-safe Publications handoff snapshot (legacy first-slice filename)
data/publications-sync-receipt.v1.json deterministic sync receipt after the sync command is run
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

A repository merge establishes maintained website source. It does not, by itself, establish authority to activate that source in production.

Discovery remains English-only at `/discovery/`; it has no localized Discovery route. Arabic translation governance is recorded in `docs/i18n/`.

QuietWire Labs is English-only at `/labs/` in this first refit. It has no fabricated localized counterpart. The investigation frames on that surface are research questions, not claims of completed capability or certification.

Publications is an English-source collection at `/publications/`. It has no
fabricated localized counterparts. Its contract and synchronization handoff
boundary are documented in `docs/PUBLICATIONS_MANIFEST.md`.

QuietWire Editions is also an explicit English-source surface. `/editions/`
lists first-party originals and `/editions/<slug>/` carries their canonical
QuietWire pages. Editions source, approval, export, website merge, Teddy
activation, and downstream syndication remain separate powers. The website-side
boundary is documented in `docs/EDITIONS_V2.md`.
