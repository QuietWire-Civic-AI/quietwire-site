# Publications manifest boundary

`quietwire.publications-manifest.v1` is the website-side contract for a
public-safe, deliberately curated list of confirmed publications. Its structural reference is
`schemas/publications-manifest-v1.schema.json`; `scripts/publications.py` is
the dependency-free, fail-closed validator used by the build.

The checked-in `data/publications.dev.v1.json` path retains its first-slice
filename for compatibility, but its content is no longer merely a one-record
development fixture. It is the current public-safe handoff snapshot copied from
an explicitly curated Internal export. The copy is intentional: this public
repository and the public host do not receive credentials for the private
Internal repository. A later deterministic synchronization mechanism may
replace the manual handoff while preserving the same contract and authority
boundary.

## Public-safe record

Every record contains only:

- a lowercase, stable ID;
- the factual publication state `confirmed_public`;
- the separate website visibility value `listed`;
- title, author names, venue, ISO publication date, and artifact type;
- an optional short plain-text summary (at most 500 characters); and
- one public, external, canonical HTTPS URL.

The contract deliberately has no article-body, draft, candidate, internal
note, source-repository, credential, or review-workflow field. Unknown fields
fail validation instead of being ignored. The build also rejects any state
other than `confirmed_public`, any website visibility other than `listed`,
markup in text fields, non-public or internal URLs, duplicate stable IDs, and
duplicate canonical URLs (including hostname case, default-port, and
trailing-slash aliases). Missing `website_visibility` fails closed.

Publication fact and website visibility are separate decisions. QuietWire
Internal may preserve broad historical evidence that an artifact was genuinely
published, while this public website remains deliberately curated. In v1, a
record is exportable to the website only when:

```text
publication_state == confirmed_public
AND website_visibility == listed
AND required public fields validate
```

There are no automatic age rules, and `unlisted` is not accepted by this
public-manifest contract.

The renderer sorts validated records by publication date and stable ID,
newest first. It copies only the allowlisted metadata and summary into static
HTML; full works remain at their canonical venues.

## Handoff boundary

The current batch is prepared in Internal as one-record-per-publication source
records plus a sanitized export containing exactly the website allowlist fields.
The site repository receives only that sanitized JSON snapshot. Internal
curation notes, evidence notes, credentials, private history, and draft material
remain outside this repository.

Updating the handoff snapshot does not itself activate production. The normal
site checks, review/merge boundary, and explicit immutable Teddy release remain
separate steps.

## Locale boundary

`/publications/` is an English-source collection route, like the existing
English-only `/discovery/` application. It does not create translated routes
or claim translation review. The four-locale ordinary-page registry,
reciprocal language links, and translation manifests remain unchanged. A
future localized publications shell requires separately reviewed interface
language and an explicit locale-scope decision; publication titles and
bylines should not be silently translated.
