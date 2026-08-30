# Media / Appearances v1

Status: first framework, grounded in the public corpus recovered 2026-08-30.

This document defines the first website-side framework for QuietWire media, appearances, recurring series, and related public records. It is intentionally narrower than a finished implementation. The goal is to preserve provenance, distinguish origin from distribution, and make the existing corpus navigable without pretending QuietWire owns externally published media.

## First principle

When QuietWire owns the work, own the origin.

When another venue owns the recording or publication surface, witness the origin.

A media record therefore describes a public event or artifact without changing its publication authority.

## Scope

The first corpus includes:

- recurring Techstrong Gang appearances in 2025 and 2026;
- the 20-episode `The Inevitability Curve` series published by Techstrong in 2025;
- Parliamentary testimony;
- conference and webinar appearances including RSA Conference, OASIS Borderless Cyber, CS2AI, Cybeats/Scryb, Security Weekly, and ICS-ISAC;
- future QuietWire-owned original video and audio works;
- transcripts, captions, clips, and derivatives when rights and source evidence permit.

This v1 framework does not claim the current index is exhaustive.

## Historical lineage: The Inevitability Curve

Chris states that he coined the term `The Inevitability Curve` in 1992. The 2025 Techstrong series is therefore not treated as a newly invented title or an accidental recurrence. It is a later public expression of a concept with an intentional, linear history extending back to 1992.

That history should be represented as provenance rather than collapsed into a single publication date. The 2025 series has its own publication record; the concept lineage has an earlier origin claim that should eventually be tied to underlying documentary evidence where available.

## Object model

### 1. Series

A `series` groups recurring media with a durable editorial identity.

Examples:

- `the-inevitability-curve`
- `techstrong-gang`

A series record does not imply QuietWire ownership. It may be externally published.

Suggested fields:

```json
{
  "id": "the-inevitability-curve",
  "kind": "series",
  "title": "The Inevitability Curve",
  "publisher": "Techstrong",
  "canonical_url": "https://techstrong.tv/videos/the-inevitability-curve",
  "ownership": "external",
  "access": "public",
  "website_visibility": "listed"
}
```

### 2. Appearance / episode

An `appearance` records participation in a public event or externally published media item. An `episode` is an appearance that belongs to a recurring series.

Suggested fields:

```json
{
  "id": "2026-08-18-techstrong-gang",
  "kind": "episode",
  "series_id": "techstrong-gang",
  "title": "...",
  "event_date": "2026-08-18",
  "publisher": "Techstrong",
  "participants": ["Chris Blask"],
  "roles": ["panelist"],
  "canonical_url": "...",
  "media_url": "...",
  "access": "public",
  "rights": "external",
  "record_state": "confirmed",
  "website_visibility": "listed"
}
```

### 3. QuietWire-owned media work

A first-party QuietWire video or audio work is a different authority class. Its canonical page belongs on `quietwire.ai`, while YouTube, LinkedIn, StreamYard, Vimeo, or other hosts are distribution channels.

Suggested distinction:

```json
{
  "kind": "quietwire_media",
  "ownership": "quietwire",
  "canonical_path": "/library/media/<slug>/",
  "distribution": [
    {"platform": "youtube", "url": "..."}
  ]
}
```

### 4. Derivative

Short clips, social excerpts, trailers, captions, and transcript-derived pieces are derivatives rather than independent canonical works unless separately approved as such.

They should carry a `derived_from` link to the parent work or appearance.

## Provenance and evidence

Media metadata is often inconsistent across publishers. The record must preserve uncertainty instead of normalizing it away.

Suggested fields:

```json
{
  "event_date": null,
  "source_published_at": null,
  "verified_date": null,
  "source_evidence": [],
  "record_state": "confirmed",
  "metadata_notes": []
}
```

Recommended `record_state` values:

- `confirmed`
- `needs_media_id`
- `metadata_conflict`
- `member_access`
- `recording_unconfirmed`
- `candidate`

A record may be historically real while its recording remains unavailable or access-restricted.

## Authority boundary

The media system must preserve these distinctions:

```text
participation fact != publication ownership
external canonical URL != QuietWire canonical URL
recording exists != recording is publicly accessible
series membership != editorial feature selection
manifest inclusion != homepage inclusion
repo merge != Teddy production release
```

External appearances remain canonical at the external venue. QuietWire may render a public-safe record containing title, date, venue, participants, summary, topics, transcript pointers, and source links.

QuietWire-owned media can receive first-party canonical pages and first-party transcripts/captions.

## Techstrong Gang corpus posture

Chris reports that Techstrong Gang has run essentially every Tuesday through 2025 and 2026, with Chris participating pretty well every Tuesday. Public search confirms a large recurring corpus, but the exact episode-by-episode census should be completed from Techstrong's own archive rather than inferred solely from search-engine indexing.

For this reason the first manifest should distinguish:

- episodes individually confirmed from Techstrong source pages;
- expected recurring Tuesday slots still awaiting exact source-page backfill;
- dates where there was no episode, Chris was absent, publication moved, or metadata differs.

Do not synthesize an appearance merely because a Tuesday exists on the calendar.

The recurring-series record may carry a human-supplied cadence note such as:

```json
{
  "cadence_note": "Historically weekly, usually Tuesday; individual appearances require source confirmation."
}
```

## The Inevitability Curve corpus posture

The recovered Techstrong series page enumerates 20 published episodes in 2025. These should be represented as:

- one series object: `the-inevitability-curve`;
- twenty child episode records;
- Techstrong as external canonical publisher for those recordings;
- a separate historical-lineage note recording Chris's 1992 origin of the term, pending attachment of the earliest documentary evidence available.

The historical-lineage note must not rewrite the 2025 publication dates.

## First recovered corpus index

The following collections are known and suitable for structured backfill.

| Collection | Current evidence | Target classification |
|---|---|---|
| The Inevitability Curve | 20 Techstrong episodes, 2025 | series + episodes |
| Techstrong Gang | recurring 2025-2026 appearances; exact census pending | external recurring series + episodes |
| Parliament of Canada PROC | 2026 civic resilience testimony with official video/transcript | public testimony |
| Still Cyber / Techstrong | 2026 panel appearance | panel appearance |
| RSA Conference | multiple 2018, 2021, 2023 sessions | conference appearances |
| OASIS Borderless Cyber | 2021 DBoM supply-chain session | conference appearance |
| Cybeats / Scryb State of Cybersecurity | multiple 2021-2022 webinars; several media IDs recovered | webinar appearances |
| CS2AI | multiple seminars/panels; some recordings member-only | seminar/panel appearances |
| Security Weekly / SC Media | 2021 DBoM interview | video podcast/interview |
| ICS-ISAC | 2013-2014 historical webinar archive | historical institutional media |

## Public Library behavior

The Library should remain curated rather than become a feed.

Recommended visitor-facing distinctions:

- `QuietWire Video`
- `Appearance`
- `Panel`
- `Public Testimony`
- `Webinar`
- `Series`

A series may have one Library landing page with episodes beneath it. Individual episodes remain addressable/searchable but need not flood the top-level Library.

External cards should use `Watch at source` or equivalent language. First-party QuietWire works may use `Watch`.

No autoplay or unreviewed third-party embeds should be introduced in the first slice.

## Transcript posture

Where a transcript exists, treat it as a companion artifact with its own provenance.

Possible authority classes:

- official transcript supplied by publisher or public institution;
- publisher captions/subtitles;
- QuietWire-owned transcript from a QuietWire-owned recording;
- QuietWire-derived transcript of external media, only where rights and policy permit.

A transcript must not silently become evidence for words not present in the recording/source.

## First implementation tranche

A sensible first website tranche is:

1. The Inevitability Curve series + 20 episodes.
2. Parliament of Canada civic resilience testimony.
3. Still Cyber / Techstrong 2026 panel.
4. A bounded set of representative Techstrong Gang appearances from 2025 and 2026 while the full census is being backfilled.
5. RSA Conference sessions.
6. OASIS Borderless Cyber 2021.
7. Confirmed Cybeats/Scryb webinar records with recovered video IDs.
8. A small historical ICS-ISAC set.

The complete Techstrong Gang census can then be added as a data backfill without redesigning the schema.

## Suggested repository layout

If implemented, prefer a parallel public-safe contract rather than overloading Publications v1:

```text
docs/MEDIA_APPEARANCES_V1.md
schemas/media-appearances-manifest-v1.schema.json
data/media-appearances.v1.json
scripts/media_appearances.py
```

Later rendering can feed `/library/` and any dedicated media/series pages from the same validated in-memory records.

The public manifest should contain only public-safe metadata. Research notes, ambiguous candidates, private recordings, credentials, and internal curation history belong outside the public website repository.

## Next evidence work

1. Enumerate Techstrong Gang source pages for every 2025 and 2026 Tuesday/episode, confirming Chris's participation per episode.
2. Capture exact title, source date, canonical URL, participants, and media URL/ID.
3. Enumerate all 20 Inevitability Curve episode records from the canonical Techstrong series page.
4. Recover earliest surviving documentary evidence for the 1992 `The Inevitability Curve` concept origin and store that in the appropriate historical/provenance lane, not as a fabricated 1992 media publication.
5. Continue source-first backfill for Parliament, RSAC, OASIS, Cybeats/Scryb, CS2AI, Security Weekly, and ICS-ISAC.

## Release boundary

This document is a design/index checkpoint only. It does not create public routes, change Library rendering, authorize publication of any candidate, or activate Teddy production.
