# QuietWire multilingual foundation

The canonical internal locale identifier is `en-CA`. It is the sole enabled
locale in this milestone and is the default locale. Its `url_prefix` is empty,
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
- The builder currently emits only the enabled default locale and keeps its
  empty URL prefix. Future prefixed locales will use the same route identities.

Every locale must have exactly one registry entry, a unique identifier and URL
prefix, a direction of `ltr` or `rtl`, complete shell keys, and one content
entry for every equivalent page route. Missing strings are errors: there is no
silent fallback to another locale.

## Routing and language choice

English remains unprefixed for continuity with the existing public site,
stable links, and the captured English baseline. Browser-language redirects,
cookies, runtime language detection, and duplicate English routes are
intentionally absent. Locale selection will be an explicit URL/build concern
when additional locales are enabled.

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

## Arabic and translation review

The next locale can add `ar` (or another agreed canonical identifier) with
`url_prefix`, `direction: rtl`, a complete shell, equivalent page keys, and a
locale-specific Discovery text layer. RTL layout changes belong in a later
reviewed output change, not in this foundation. Machine-drafted translations
must be marked as drafts and must not be treated as publishable until a human
reviewer verifies terminology, cultural meaning, accessibility, and right-to-
left presentation.
