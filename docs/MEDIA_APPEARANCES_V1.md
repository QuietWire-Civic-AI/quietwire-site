# Media / Appearances v1

Status: first framework and bounded web implementation, grounded in the public corpus recovered 2026-08-30.

This document defines the first website-side framework for QuietWire media, appearances, recurring series, and related public records. It preserves provenance, distinguishes origin from distribution, and makes a reviewed slice of the existing corpus navigable without pretending QuietWire owns externally published media.

## First principle

When QuietWire owns the work, own the origin.

When another venue owns the recording or publication surface, witness the origin.

A media record therefore describes a public event or artifact without changing its publication authority.

## Implemented web slice

The first web slice is implemented on the draft media branch and remains unmerged/unreleased until separately reviewed.

It adds:

- a bounded three-card `Watch & Listen` shelf inside `/library/`;
- `/library/media/` as the English-source collection landing page;
- `/library/media/the-inevitability-curve/` as a 20-episode series page;
- `/library/media/techstrong-gang/` as a selected-appearances series page;
- native QuietWire witness/catalog pages for the 2026 Parliament civic-resilience testimony, the 2026 Still Cyber panel, and the 2023 RSAC `The World on SBOMs` session;
- external source links rather than embedded third-party video players;
- a fail-closed public-safe media manifest separate from the richer research index;
- build and CI checks for route integrity, provenance boundaries, no localized leakage, no tracker/player embeds, and deterministic committed build output.

The web implementation consumes only `data/media-appearances.v1.json`. The research files `data/media-appearances.index.v0.json` and `data/media-appearances.techstrong-backfill-20260830.json` do not become runtime publication authority.

No top-level navigation item is added. Media remains a Library lane.

## Scope

The research corpus includes:

- recurring Techstrong Gang appearances in 2025 and 2026;
- the 20-episode `The Inevitability Curve` series published by Techstrong in 2025;
- Parliamentary testimony;
- conference and webinar appearances including RSA Conference, OASIS Borderless Cyber, CS2AI, Cybeats/Scryb, Security Weekly, and ICS-ISAC;
- future QuietWire-owned original video and audio works;
- transcripts, captions, clips, and derivatives when rights and source evidence permit.

The public web manifest is deliberately smaller than the research corpus. Inclusion in research is not publication approval.

## Current corpus checkpoint

The research index plus its additive backfill currently account for **92 effective Techstrong records** recovered during the 2026-08-30 source-first pass:

- **20** `The Inevitability Curve` episodes, completing the canonical 2025 Techstrong series;
- **41** Techstrong Gang records from 2025: 40 publisher-explicit Chris Blask identifications plus one weaker candidate identity record;
- **31** source-confirmed or source-identified Techstrong Gang records from 2026 through 2026-08-30.

The count is a research checkpoint, not a claim that the Gang census is permanently complete. Records whose exact dates, canonical URLs, or identity details still need source confirmation remain explicitly marked as such. Known publisher metadata conflicts remain in the research index rather than being normalized away.

The public-safe v1 web manifest currently promotes all 20 confirmed Inevitability Curve episode records, a restrained selected subset of source-confirmed Techstrong Gang appearances, and three standalone appearance/testimony records.

## Historical lineage: The Inevitability Curve

Chris's current first-person recollection places the origin of the term `The Inevitability Curve` in approximately **1991–1992**. He recalls coining it while trying to persuade his boss that everyone on Earth was going to get on the Internet. The premise was that if that connected future was effectively inevitable, a line already joined the present to that notional future; people in the future would be able to look backward and see the exact shape of the path. The immediate engineering conclusion was that the organization should go ahead and build a firewall.

Chris recalls using the term and underlying concept continuously ever since. The 2025 Techstrong series is therefore treated as a later public expression of that longstanding concept, not as the origin of the phrase.

This is historical recollection, not yet an independently documented 1991/1992 artifact. The exact year must remain uncertain until underlying evidence supports greater precision. The complete captured recollection and evidence posture are preserved in `docs/INEVITABILITY_CURVE_ORIGIN_NOTE.md`.

That history is represented as provenance rather than collapsed into a single publication date. The 2025 series has its own publication record; the concept lineage has an earlier origin recollection that should eventually be tied to underlying documentary evidence where available.

## Object model

### 1. Series

A `series` groups recurring media with a durable editorial identity.

Examples:

- `the-inevitability-curve`
- `techstrong-gang`

A series record does not imply QuietWire ownership. It may be externally published.

Public-safe series fields include stable ID, publication/visibility state, title, publisher, summary, a native QuietWire Library path, external source URL, role label, and an optional bounded lineage note.

### 2. Appearance / episode

An `appearance` records participation in a public event or externally published media item. An `episode` is an appearance that belongs to a recurring series.

Public-safe records carry only reviewed metadata such as title, date, venue, participants, external canonical URL, optional series/episode identity, and optional media/transcript pointers.

Research-only ambiguity and source conflicts stay in the research index until resolved or deliberately represented by a future public contract.

### 3. QuietWire-owned media work

A first-party QuietWire video or audio work is a different authority class. Its canonical page belongs on `quietwire.ai`, while YouTube, LinkedIn, StreamYard, Vimeo, or other hosts are distribution channels.

This first v1 implementation does not yet introduce a QuietWire-owned video master or player. Large audio/video masters should remain outside ordinary static site releases in QuietWire-controlled media/object storage.

### 4. Derivative

Short clips, social excerpts, trailers, captions, and transcript-derived pieces are derivatives rather than independent canonical works unless separately approved as such.

They should eventually carry a `derived_from` link to the parent work or appearance.

## Provenance and evidence

Media metadata is often inconsistent across publishers. Research records preserve uncertainty instead of normalizing it away.

Recommended research `record_state` values include:

- `confirmed`
- `needs_media_id`
- `metadata_conflict`
- `member_access`
- `recording_unconfirmed`
- `candidate`

A record may be historically real while its recording remains unavailable or access-restricted.

Promotion to the public-safe manifest is a separate curation act. The current web validator accepts only `confirmed_public` + `listed` records and rejects unknown fields, malformed paths, unsafe/non-public URLs, duplicates, and invalid series references.

## Authority boundary

The media system preserves these distinctions:

```text
participation fact != publication ownership
external canonical URL != QuietWire canonical URL
recording exists != recording is publicly accessible
series membership != editorial feature selection
research-index inclusion != public-manifest inclusion
public-manifest inclusion != homepage inclusion
repo merge != Teddy production release
```

External appearances remain canonical at the external venue. QuietWire renders a public-safe catalog/witness page containing reviewed title, date, venue, participants, summary, transcript pointers where appropriate, and source links.

QuietWire-owned media can later receive first-party canonical pages and first-party transcripts/captions.

## Techstrong Gang corpus posture

Chris recalls his Techstrong Gang participation as essentially weekly through 2025 and 2026, mostly Tuesdays.

Techstrong currently describes the program as a weekday/daily roundtable, and source-confirmed Chris appearances occur across multiple weekdays. The corpus therefore stores Chris's cadence recollection as continuity evidence but never generates an episode from a Tuesday on the calendar. Individual records are governed by publisher evidence.

The complete research census remains richer than the public web page. The v1 public series page intentionally shows only a selected source-confirmed subset instead of flooding the visitor-facing Library with every recovered appearance.

## The Inevitability Curve corpus posture

The canonical Techstrong series page enumerates 20 published episodes in 2025. The public-safe manifest represents:

- one series object: `the-inevitability-curve`;
- twenty child episode records;
- Techstrong as external canonical publisher for those recordings;
- a separate historical-lineage note recording Chris's approximately 1991–1992 origin recollection, pending attachment of earliest documentary evidence.

The historical-lineage note does not rewrite the 2025 publication dates.

Where guest metadata remains conflicted in the research source, the public record is conservative rather than exporting unresolved names as fact.

## Public Library behavior

The Library remains curated rather than becoming a feed.

The v1 visitor-facing lane uses:

- `Series`
- `Public Testimony`
- `Panel`
- `Conference Session`
- source-linked `Episode` records inside series pages.

The Library shelf is exactly three explicitly curated records in `data/media-site.v1.json`: `The Inevitability Curve`, `Techstrong Gang`, and the Parliament civic-resilience testimony. It does not select newest-N records automatically.

External cards/pages use source-oriented language such as `Watch at source`, `Watch at Techstrong`, or `Series at source`.

No autoplay or third-party player embeds are introduced in v1.

## Transcript posture

Where a transcript exists, treat it as a companion artifact with its own provenance.

Possible authority classes:

- official transcript supplied by publisher or public institution;
- publisher captions/subtitles;
- QuietWire-owned transcript from a QuietWire-owned recording;
- QuietWire-derived transcript of external media, only where rights and policy permit.

The Parliament seed record links the official House of Commons transcript. A transcript must not silently become evidence for words not present in the recording/source.

## Repository layout

The implemented slice uses:

```text
docs/MEDIA_APPEARANCES_V1.md
docs/INEVITABILITY_CURVE_ORIGIN_NOTE.md
docs/TECHSTRONG_CORPUS_CHECKPOINT_20260830.md
schemas/media-appearances-manifest-v1.schema.json
data/media-site.v1.json
data/media-appearances.v1.json
data/media-appearances.index.v0.json
data/media-appearances.techstrong-backfill-20260830.json
scripts/media_appearances.py
scripts/build_media.py
scripts/check_media_appearances.py
```

Generated outputs are committed under `dist/library/media/` plus the bounded Library shelf and sitemap entries, following the site's existing reproducible-dist convention.

## Next evidence / product work

1. Continue resolving exact dates and canonical URLs for source-identified Gang research records rather than inferring them.
2. Continue the 2026 Gang publisher-archive census as useful.
3. Backfill confirmed Parliament, RSAC, OASIS, Cybeats/Scryb, CS2AI, Security Weekly, and ICS-ISAC records into the research lane, promoting only a deliberately curated subset to public-safe metadata.
4. Recover earliest surviving documentary evidence for the approximately 1991–1992 `The Inevitability Curve` concept origin and store it in the appropriate historical/provenance lane.
5. Add QuietWire-owned media only when a first-party custody/storage path is explicitly designed.
6. Consider thumbnails/stills later only where rights, privacy, performance, and provenance are clear.

## Release boundary

The implemented v1 slice is still a draft branch/PR until separately reviewed and merged. A merge is not itself a production release. Teddy activation remains an explicit separate Moose → Teddy release act with normal verification and receipt.
