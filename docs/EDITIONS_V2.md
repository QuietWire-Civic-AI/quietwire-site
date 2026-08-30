# QuietWire Editions v2 website boundary

QuietWire Editions is the first-party publishing lane for works QuietWire owns
and deliberately publishes under its own custody.

This website repository is the renderer and release implementation. It is not
the private editorial source of truth and it does not receive unpublished
Editorial or Internal material.

## Source and handoff

The governed source lane is:

`QuietWire-Civic-AI/editions-content`

The first website handoff consists of exact public-safe export artifacts:

- `exports/editions.v1.json`
- `exports/editions/<slug>.html`

The current seed artifacts are copied byte-for-byte from the approved
`editions-content` export. The website then independently validates them before
rendering.

The website never clones the private editorial repository at runtime and Teddy
does not need credentials for it.

## Public-safe contract

`quietwire.editions-manifest.v1` allows only:

- stable Edition ID;
- explicit `release_state: approved`;
- explicit `website_visibility: listed`;
- title and slug;
- public author names;
- source date;
- artifact type;
- short public summary;
- canonical `/editions/<slug>/` path; and
- one approved body-fragment path.

Unknown fields fail closed.

A body fragment is also fail-closed. The renderer accepts only a small
non-executable HTML subset:

`p`, `h2`, `h3`, `ul`, `ol`, `li`, `blockquote`, `strong`, `em`, `a`, `hr`

Arbitrary attributes, scripts, styles, event handlers, comments/declarations,
embedded objects, unsafe links, and executable markup are rejected.

The public export must not contain private editorial notes, Internal paths,
credentials, unpublished attachments, customer/source details, or private
provenance.

## Routes

The initial English-source routes are:

- `/editions/`
- `/editions/<slug>/`

Like `/publications/` and `/discovery/`, Editions does not fabricate translated
copies. A localized Editions interface or translated work requires a separate
review and locale-scope decision.

## Canonical-first semantics

An approved Edition record means the artifact is approved to be rendered by the
website. It does **not** mean production has been activated.

The sequence remains:

```text
editions-content source
  -> editorial approval
  -> public-safe export
  -> quietwire-site validation and PR
  -> explicit Teddy immutable release
  -> public verification
  -> Internal publication-event / release receipt
  -> optional downstream syndication
```

A merged website change is therefore not itself a publication receipt.

## Work versus publication event

QuietWire Editions holds the canonical first-party page for a QuietWire-owned
work. External cross-posts or adaptations are separate publication events tied
to that same underlying work.

External-only appearances remain canonical at their external venue and belong
in the broader Publications system rather than being copied into Editions as
though QuietWire owned them.

The current Publications v1 contract intentionally allows only external
canonical URLs. This first Editions slice does not silently widen that contract.
A later work/event model will connect first-party Editions and external
publication events cleanly.

## First seed: Foundry Wakes

The first v2 seed is the existing historical source artifact `Foundry Wakes`,
dated 2025-09-11 in `editions-content`.

The page labels that date as the **source artifact date**. It does not assert
that the new `quietwire.ai/editions/foundry-wakes/` URL was publicly live in
2025.

Once the Teddy release is explicitly activated and verified, Internal can
record the new canonical QuietWire web publication event and its release
receipt.

## Media

Text and modest web assets can travel through the static Git/release path.

Large audio/video masters should remain outside ordinary site releases in
QuietWire-controlled media/object storage. Editions pages can carry metadata,
transcripts/captions, provenance, and owned media URLs while external platforms
remain optional distribution channels.
