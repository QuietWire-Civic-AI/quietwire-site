# QuietWire multilingual foundation

The canonical internal locale identifier is `en-CA`. Arabic (`ar`) is the
second enabled locale and is machine-drafted pending human review. English is
the default locale. Its `url_prefix` is empty,
so its public routes remain `/`, `/work/`, `/appliances/`, and the other
existing unprefixed routes. English is not duplicated under `/en/` or
`/en-ca/`.

## Source and build model

- `site.config.json` owns the site-wide routing inventory and locale registry.
- `src/content/en-CA/pages/` owns substantial English page markup and prose.
- `src/i18n/en-CA.json` owns shared shell strings, accessibility labels, and
  shared metadata strings.
- `src/layout.html` remains the shared document shell; the builder injects the
  selected locale's shell values without changing their current output.
- The builder emits both enabled locales. English keeps its empty URL prefix;
  Arabic uses `/ar/` and the same route identities.

Every locale must have exactly one registry entry, a unique identifier and URL
prefix, a direction of `ltr` or `rtl`, complete shell keys, and one content
entry for every equivalent page route. Missing strings are errors: there is no
silent fallback to another locale.

## Routing and language choice

English remains unprefixed for continuity with the existing public site,
stable links, and the captured English baseline. Browser-language redirects,
cookies, runtime language detection, and duplicate English routes are
intentionally absent. Locale selection is explicit URL/build behavior.
Equivalent pages expose ordinary keyboard-accessible links to one another and
never redirect automatically. Arabic pages use `dir="rtl"`; English remains
`dir="ltr"`.

## Discovery

Discovery's current corpus and application remain byte-for-byte unchanged.
Its canonical question IDs, role and area mappings, response schema, and
local-first browser boundary are language-independent working data. The next
safe extraction step is to keep a locale-neutral survey structure and IDs,
place section/question text and interface strings in locale-specific content,
and serialize each selected locale to the existing application corpus shape.
Working response files must continue to contain stable survey and question IDs,
not translated labels, so a file can be reopened across interface languages.

Any such extraction must be proven against the existing generated Discovery
files before it is enabled.

## Publications

The generated `/publications/` collection is English-source-only in its first
bounded slice. It sits outside the equivalent ordinary-page inventory, just
as `/discovery/` does, and therefore does not add unreviewed `/ar/`, `/es/`, or
`/fr/` routes. Its language selector and hreflang metadata expose only
`en-CA` plus `x-default`. Localizing the collection shell requires reviewed
interface language; titles and bylines from external venues are not silently
translated.

## Arabic and translation review

Arabic has `url_prefix: "ar"`, `direction: "rtl"`, a complete shell, and
equivalent ordinary page keys. Discovery remains English-only at
`/discovery/`; Arabic may link to it only with a clear English-availability
label. The Arabic translation manifest is `machine_draft` and must not be
treated as publishable until a human reviewer verifies terminology, cultural
meaning, accessibility, and right-to-left presentation.
