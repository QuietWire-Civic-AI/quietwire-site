# vNext delegated implementation — release and locale checklist (2026-10-19)

**Status:** source implementation underway; not validated or published.
**Website decision owner:** Chris Beall / Nexus. **Authority:** [Oct 19 direct delegation](https://github.com/QuietWire-Civic-AI/Internal/blob/main/01_Projects/Website/2026-10-19_Chris_Beall_Website_Publication_Delegation_Arabic_First_Locale_Gate.md).
**Release executor:** an existing authorized Teddy operator; name and privilege to be verified, not inferred from GitHub admin.
**Source preview:** [Internal draft PR #284](https://github.com/QuietWire-Civic-AI/Internal/pull/284) remains provenance, not an approval queue.

## Scope in this branch
- Bring the owner-selected **lean English homepage** and responsive styles into canonical site source.
- Preserve exactly one `{{home_library_shelf}}` marker and the three-item Library contract.
- Reconcile privacy/geography About and Field redlines before declaring the website-wide vNext complete.
- Reconcile claim repair [site PR #40](https://github.com/QuietWire-Civic-AI/quietwire-site/pull/40) and Library curation [site PR #41](https://github.com/QuietWire-Civic-AI/quietwire-site/pull/41); neither is silently merged here.
- Use the April 2026 **original approved QuietWire logo**. Do not redraw, recolor or invent an identity mark.
- Requalify old claims rather than treating existing website language as ready-to-use evidence.

## Arabic included at source PR time
**English changed route:** `/`.
**Arabic corresponding route:** `/ar/`.
**Human language counterpart:** Ali Adnan / Khalil, using the glossary and manifest; review not yet attested.

- [ ] Diff English source against `src/content/ar/pages/index.html` (or actual Arabic home route) and update `src/i18n/ar.json` / `docs/i18n/ar-glossary.md` and manifest as appropriate.
- [ ] Document English revision, Arabic revision, reviewer, state and changed routes in `docs/i18n/ar-translation-manifest.json`.
- [ ] Preserve approved prior Arabic text; no unreviewed machine replacement.
- [ ] Test Arabic RTL, navigation, links, metadata, hreflang, and rendered equivalence; accurately hold affected materially drifted route if not ready.
- [ ] Prove this source/reviewer/check/release loop with Ali before copying it to French or Spanish workflows.

## Technical claim gates
Avoid global guarantees for local processing, data never leaving, security, model/provider independence, backup/recovery and support. Consult Ashraf/Raasid for **material new** technical/data/security claims, not for general editorial signoff. See [technical claim review](https://github.com/QuietWire-Civic-AI/companion-wire/blob/main/inbox/Chris-Beall-Nexus/2026-10-07__CW-2026-10-07-AR-003__Website_vNext_technical_claim_review.md).

## Build and release — not passed merely because commits exist
- [ ] Integrate About and Field redlines from the Oct 17 Internal source.
- [ ] Confirm official logo is packaged from approved source.
- [ ] Reconcile #40 and #41 with current main and rebuild generated `dist/`.
- [ ] Run `make check` and validate generated parity; inspect mobile and accessibility.
- [ ] Record Ali's Arabic receipt or an explicitly honest route exclusion.
- [ ] Review exact Git SHA, changed claims and all locale effects.
- [ ] Chris Beall records website publication go/no-go within delegated scope.
- [ ] Authorized Teddy operator runs `deploy/release-site.sh` on clean main.
- [ ] Preserve previous immutable release, release hashes, source commit and rollback path.
- [ ] Verify Teddy origin **and public edge** bytes. Exit 2 is **not** public cutover proof.
- [ ] Record public verification and send Chris/Lumina an exception-only report, not an approval request.

**Boundary:** This checklist is an implementation aid, not proof of completion, new runtime rights, or a waiver of legal/security/custody requirements.

## Verified implementation update — 2026-10-19
- English claim-discipline changes from PR #40 were copied into `about.html`, `patterns.html`, and `work.html`, retaining conditional wording rather than unconditional guarantees. English generated pages were rebuilt; resulting Git blobs match checked laptop build: About `834dcf75a4ed4dbb1fe873eed0dab54cb31a97cb`, Patterns `54b258ec305ddcf6b3193bd82ad112d258775ee7`, Work `42f3b0dee771d2b9de31608d5ded3c0565e5f33b`.
- Entire `make check` suite passed after English change, including existing locale structural checks. **This does not attest semantic parity or human approval for the new English changes.** The corresponding Arabic, French, and Spanish claim corrections in PR #40 remain unintegrated pending language stewardship; do not misrepresent locale coherence.
- Research & Advisory edits exist as **uncommitted work in the user's separate laptop working tree**. These were inspected but intentionally not imported or overwritten. They can be brought into the source PR once reviewed for current English claim boundaries and source/build contract.
- PR #41 Library/publications is still separate. Its curated records and generated shelves must be reconciled before website-wide release.
- **Release status remains HOLD:** About/Field privacy-source redlines, translated material route review, official logo, and operator proof remain incomplete. This is not a launch receipt.

## English reconciliation triage — 2026-10-19 (current pass)
- **Research & Advisory:** Current PR #42 already contains the changed hero and applied-research framing; current site config already labels navigation and metadata `Research & Advisory`. The user's local uncommitted edits were inspected against this branch. Do not overwrite the local checkout or duplicate this work.
- **CIGI/Library:** PR #41's `data/publications.dev.v1.json` is byte-identical to PR #42's manifest; the two CIGI record additions therefore do **not** need another manifest insertion. Generated publications/author pages differ between branches; use the build system on the final integrated source instead of copying stale `dist/` across branches. PR #41 remains a distinct open provenance artifact.
- **Claims:** English source repairs from PR #40 are integrated; the translated variants from PR #40 are *not* and require human semantic parity review. This does not block continuing English work, but does block claiming website-wide locale completion.
- **Privacy/geography:** Existing About top copy still says `Canadian-held. Globally rooted.` That phrase should be treated as a provenance/custody claim needing substantiation or conservative revision before publication, rather than taken as a guaranteed hosting fact. Oct 17 source redlines are still to be reconciled.
- **Operator boundary:** No website publication go/no-go, merge or Teddy release is implied by this source reconciliation.
