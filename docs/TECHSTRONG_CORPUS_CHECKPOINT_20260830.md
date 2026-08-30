# Techstrong corpus checkpoint — 2026-08-30

Status: research checkpoint plus bounded public-web promotion. The research corpus is not itself a public manifest or a production-release act.

## Where the corpus lives

The media work is deliberately split by authority:

- `data/media-appearances.index.v0.json` — primary research index populated during the first source pass;
- `data/media-appearances.techstrong-backfill-20260830.json` — corrections and records found during the subsequent full-season/release-page sweep;
- `data/media-appearances.v1.json` — separately curated, fail-closed public-safe subset consumed by the website;
- `data/media-site.v1.json` — explicit website curation, including the three-card Library shelf;
- `docs/MEDIA_APPEARANCES_V1.md` — media/appearance architecture and authority boundary;
- `docs/INEVITABILITY_CURVE_ORIGIN_NOTE.md` — Chris Blask's approximately 1991–1992 first-person origin recollection, kept separate from later documentary/publication evidence.

The research backfill remains additive/corrective so the research history stays inspectable. The website does **not** read either research file at build/runtime. Promotion to `data/media-appearances.v1.json` is an explicit curation boundary.

## Effective Techstrong research checkpoint

After applying the backfill to the primary research index:

| Corpus | Effective records | Evidence posture |
|---|---:|---|
| The Inevitability Curve (2025) | 20 | complete against canonical Techstrong series page |
| Techstrong Gang (2025) | 41 | 40 source-explicit Chris Blask identifications + 1 candidate identity record |
| Techstrong Gang (2026 through Aug. 30) | 31 | source-confirmed partial census; more archive inspection may add records |
| **Total Techstrong records** | **92** | research checkpoint |

## Public web promotion

The first public-safe web slice promotes:

- all 20 `The Inevitability Curve` episodes, with conservative handling of unresolved guest metadata;
- a deliberately selected subset of source-confirmed Techstrong Gang appearances rather than all recovered Gang research records;
- three standalone external records: the 2026 Parliament civic-resilience testimony, `Surviving the Cyber Core Collapse`, and the 2023 RSAC session `The World on SBOMs`.

The generated web surface is under `/library/media/`, with a bounded `Watch & Listen` shelf inside `/library/`. External venues remain canonical. There are no embedded third-party video players in v1.

## 2025 Gang sweep

All ten paginated pages of the 2025 Techstrong Gang season archive were inspected for Chris Blask participation.

The full sweep exposed one record missed in the first pass:

- `Navigating IT Spending and AI's Impact on Enterprise Software` — TSG Ep. 906.

The publisher description spells the name `Chis Blask`. The research record treats this as an apparent source typo while preserving the typo in metadata notes. Its exact event date and canonical episode URL remain unresolved rather than inferred from episode sequence.

One existing 2025 record remains deliberately weaker:

- TSG Ep. 926, `AI in HR: Workday’s Big Bet on Automation & the Future of Work`, where the recovered publisher text identifies only `Chris`. It remains a candidate identity record until the source establishes that this is Chris Blask.

The effective 2025 posture is therefore **40 explicit + 1 candidate**, not 41 equally strong confirmations.

## 2026 corrections and additions

The release-date archive supplied three additional source-explicit Chris appearances that were not in the primary index:

- `AI Regulation Fight, Women Engineers and Anthropic Security Signals`;
- `Apple Pushes AI, OpenAI Files and SpaceX Teams With Google`;
- `Anthropic Goes Big, NVIDIA Expands AI and Microsoft’s Security Fight Escalates`.

Their canonical OTT routes are recovered, but their exact event dates remain pending. The dates are intentionally left null rather than inferred from neighboring episodes.

Three existing primary-index records were also sharpened without creating duplicates:

- 2026-06-30: the generic date placeholder resolves to `Open Source AI, OpenAI Copyright Fight and PACT Protocol` with Kate Scarcella and Chris Blask;
- 2026-07-01: the generic date placeholder resolves to `AI Job Interviews, AI Coding Costs and Human Creativity` with Andi Mann, Jeff Reich, Chris Blask and Jon Swartz;
- `OpenAI Cuts Prices, Huang Calls Out CEOs and Cyber Hits $521B` resolves to 2026-06-16 from Techstrong's publisher-controlled YouTube distribution.

## Cadence: recollection versus publisher evidence

Chris recalls his Gang participation as essentially weekly through 2025 and 2026, mostly Tuesdays.

Techstrong currently describes the program as a Monday-through-Friday daily roundtable, and source-confirmed Chris appearances occur across multiple weekdays. The corpus therefore stores Chris's cadence recollection as continuity evidence but never generates an episode from a Tuesday on the calendar. Individual records are governed by publisher evidence.

This is a useful example of the intended provenance model: recollection and source evidence can both be useful without being flattened into one claim.

## The Inevitability Curve

All 20 published 2025 Techstrong episodes are in the research index and the first public-safe web manifest.

The series remains a 2025 publication corpus. Its conceptual origin is a separate historical lineage: Chris recalls coining `The Inevitability Curve` around 1991–1992 while arguing that universal Internet connectivity was an inevitable future state whose path could already be anticipated, with the immediate practical conclusion that the organization should build a firewall.

That recollection is preserved in `docs/INEVITABILITY_CURVE_ORIGIN_NOTE.md`. Earliest documentary evidence remains a separate provenance task; the 2025 series is not backdated.

## Known source anomalies preserved

The research corpus deliberately retains rather than silently repairs several publisher inconsistencies:

- February 24 and 26, 2025 Gang pages have 2025 in their titles but display internal page metadata dated 27-Feb-2024;
- Inevitability Curve episode 20 has `Amelie Karan` in publisher guest metadata while body copy says `Emily`;
- Techstrong has overlapping/mixed season/archive surfaces and at least one apparent duplicate episode-number condition around TSG 999;
- publisher feed/archive ordering can differ from event-date chronology.

These are reasons to keep `event_date`, `source_published_at`, canonical URL, and evidence source as distinct fields in research. The public-safe manifest omits unresolved details rather than exporting them as settled fact.

## Next corpus work

1. Resolve exact dates and canonical URLs for remaining source-identified Gang records rather than inferring them.
2. Continue the 2026 archive census as useful.
3. Backfill the other confirmed media collections as individual research records: Parliament, Still Cyber, RSA Conference, OASIS Borderless Cyber, Cybeats/Scryb, CS2AI, Security Weekly and ICS-ISAC.
4. Promote only deliberately reviewed public-safe records into the website manifest.
5. Recover documentary evidence for the early Inevitability Curve lineage where available.

The current draft branch changes generated website output, but no merge or Teddy production release is implied. Production activation remains a separate explicit release act.
