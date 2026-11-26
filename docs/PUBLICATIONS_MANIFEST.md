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
Internal repository. The bounded deterministic synchronization command is now
`scripts/sync_publications.py`. It accepts an explicitly supplied approved
public-safe export, validates it with the same fail-closed contract, no-ops when
the bytes already match, updates only the checked-in publication snapshot when
they differ, and emits `data/publications-sync-receipt.v1.json` containing
source/destination SHA-256 hashes, record count, and validation state. It
performs no network access and no production activation.

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

Normal bounded handoff:

```bash
python3 scripts/sync_publications.py /path/to/approved/publications.v1.json
make check
```

The source path is supplied by the human/companion operating context; the site
repository does not gain private-Internal credentials. The sync receipt is
deterministic and contains hashes only, so repeating an unchanged handoff does
not create data-file churn.

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
