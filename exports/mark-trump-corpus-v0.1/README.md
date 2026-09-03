# Mark Trump / Cyber Research Library — QuietWire First Tranche

**Version:** 0.1  
**Prepared:** 2026-09-02  
**Purpose:** A small `Recent / Relevant / Ready` source set that Mark Trump's Cyber Research Library can ingest or stage without waiting for a comprehensive historical archive.

This package is deliberately a **manifest of canonical sources**, not a bulk mirror of third-party content.

Mark's current workflow already distinguishes searchable full text from metadata-only references based on source, provenance, rights, and publication status. QuietWire wants to preserve that boundary.

## Start here

- [`manifest.csv`](manifest.csv) — machine-friendly first tranche, 25 records.
- [`dbom-apache2-pins.csv`](dbom-apache2-pins.csv) — immutable source/license pins for the three DBoM records that Mark's intake classified as separate full-text candidates.
- Canonical source links are preferred over copied third-party content.

## Intake feedback — 2026-09-02

Mark returned a rights-aware intake report for this tranche. His system classified all 25 records as body-free `Future References`, with **0 Corpus imports** from the first pass. It identified the three DBoM documents as candidates for separate full-text review once the source revision and Apache-2.0 license were pinned together.

QuietWire therefore verified the following DBoM revision and license as one immutable source state:

- repository: `QuietWire-Civic-AI/dbom-core`
- revision: `110c804fea79302d3d0c59bf6300a91518e75313`
- license at that revision: `Apache-2.0`

The three pinned candidates are recorded in `dbom-apache2-pins.csv`. This pin makes the source/license state inspectable; Mark's library remains responsible for its own admission/publication decision.

## What is in v0.1

The first tranche spans:

- current writing by Chris Blask on AI security, bounded authority, local stewardship, provenance, narrative security, and human confirmation;
- selected public conversations on critical infrastructure, information warfare, marine/OT cyber conflict, software supply chains, SBOMs, DBoM, and AI security;
- public QuietWire repositories and documents for DBoM / SCITT / SBOM attestation and provenance-oriented governance.

This is **not** the comprehensive Chris Blask historical corpus. It is the first useful box.

## Rights / provenance posture

`publicly reachable` is not the same thing as `licensed for republication`.

The `ingest_mode` and `rights_note` fields in the manifest are intentionally conservative:

- **External publisher / platform:** ingest metadata + canonical link by default. Mark's own verification process should decide whether full text or transcripts can be retained and republished.
- **QuietWire public GitHub:** public visibility does not automatically imply reuse rights. Follow the repository's current license; where a license is restrictive or unclear, keep metadata/link-only until verified.
- **NIDP:** the current public repository explicitly carries a restrictive all-rights-reserved placeholder license, so the manifest recommends metadata/link-only unless permission is separately established.

## Next tranche

If this first set ingests cleanly, the next pass should broaden from `Recent / Relevant / Ready` toward the historical compendium:

1. early firewall / Internet-inevitability material and surviving presentations;
2. information-sharing / ISAC history;
3. OT / ICS and critical-infrastructure work;
4. SBOM / software-supply-chain / DBoM / SCITT history;
5. interviews, panels, podcasts, and conference recordings with recoverable transcripts;
6. public repositories with stable canonical URLs; and
7. source notes that distinguish Chris's present recollection from contemporaneous documentary evidence.

The goal is not to make Mark's library trust QuietWire because the material came from QuietWire. The goal is to give his verification machinery **better source material to inspect**.
