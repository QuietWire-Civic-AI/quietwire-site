# Arabic website revision 2 — source integration map (2026-10-29)

**State:** `DRAFT / REVIEW ONLY`, not a rendered or published preview.  
**Source:** Ali Adnan and Khalil, `QuietWire_Arabic_Website_Review_Revision2_2026-10-26.docx`, sent October 26 to Chris Beall, Chris Blask and Lumina. The document explicitly says its wording is proposed for review and does not authorize a technical change or publication.  
**English editorial source:** Chris Beall / Nexus, website vNext [draft PR #43](https://github.com/QuietWire-Civic-AI/quietwire-site/pull/43), source commit `3bacd1e991f37051a2c1588603ec62a69755a13e`, stacked on [draft PR #42](https://github.com/QuietWire-Civic-AI/quietwire-site/pull/42).  
**Technical integrator:** Lumina, temporarily at Chris Blask's direct request on October 29, with Beall/Nexus remaining the ongoing operational and publication owner.  
**Arabic language owner:** Ali Adnan with Khalil. **Go/no-go:** Chris Beall / Nexus; real Teddy deployment by existing authorized site operator only.

## What is staged in this child branch

- `src/content/ar/pages/index.html`: replace the older Arabic node/pilot-first homepage with Ali/Khalil's October 26 **proposed** lean-homepage language. Keep the English lean homepage's corresponding sections: hero, three questions, Research & Advisory / Work paths, responsibility, Labs/Library, People & projects, and contact.
- Retain exactly one `{{home_library_shelf}}` marker.
- Keep Labs, Library and People routes pointing to the **existing English pages**, clearly labeled `(بالإنجليزية)`; do not invent `/ar/labs/`, `/ar/library/` or `/ar/people/` endpoints.
- Remove the obsolete Arabic homepage invitation to the 60-day node pilot. Do not imply a fixed offer, integration, pricing, node deployment guarantee or production-readiness claim.
- Maintain Arabic direction from the existing site shell; isolate digits and external identifiers using existing markup conventions.
- Initial static source checks: one H1, one Library marker, expected working route strings, no retired pilot link, and no Yemen/Sana'a references in this source page. These are **source-only checks**, not a replacement for a rendered RTL/mobile/link audit.

**Not yet implemented or verified:** Other Arabic routes, rendered `dist/` parity, full `make check`, actual screenshots, customer-visible preview, complete RTL/mobile review, updated global translation manifest, publication or release receipt. Existing Arabic Advisory language approved in August remains untouched; October 26 proposed replacements require fresh semantic review before adoption.

## Mapping of the Oct 26 reviewer package

| Reviewer topic | Proposed destination | State / next check |
| --- | --- | --- |
| Home: approved-for-review headline and three questions | `src/content/ar/pages/index.html` | Staged as **draft**; verify exact wording, graphic truncation (full questions retained in attributes), RTL, card sizes and mobile |
| Home: Research & Advisory / Work cards | Arabic homepage links to `/ar/advisory/` and `/ar/work/` | Staged as draft; ensure it matches Beall's two-path editorial intention |
| Home: Labs / Library | English-only URLs with Arabic language disclosure | Staged as draft; review label and bidi behavior |
| Home: People & projects | English-only `/people/`, no invented Arabic route | Staged as draft; rights / relationship claims still need Beall's review |
| Work | `src/content/ar/pages/work.html` | **Pending** technical integration and subsequent Ali/Khalil review; old appliance-first source remains in source at this stage |
| Research & Advisory | `src/content/ar/pages/advisory.html` | **Pending** Oct 26 delta; preserve the independently approved Aug 6 human translation until explicit revision acceptance |
| About | `src/content/ar/pages/about.html` | **Pending**; distinguish institutional memory from knowledge and avoid equating local stewardship with fixed geographic hosting |
| Method, Labs, Library, People | Existing method route / English-only routes where Arabic unavailable | **Pending** page-by-page content / relationship review; no fabricated translated pages |
| Nav/footer, legacy offer routes | `src/i18n/ar.json`, shared shell, retired route handling | **Pending**; do not resurrect appliances pricing, 60-day pilot or old Field claims |
| Glossary / manifest | `docs/i18n/ar-glossary.md`, `docs/i18n/ar-translation-manifest.json` | **Pending** reviewer confirmation. Especially `الذاكرة المؤسسية` vs `المعرفة المؤسسية`, authority, provenance, receipt, local stewardship |

## How Chris Beall and Nexus can own the ongoing process

1. Work from this child source branch and review proposed changes **against PR #43**, not the current production `main`. The PR #43 stack remains draft and must be reconciled with current main before any eventual release.
2. For each changed English page, identify the corresponding Arabic source, human reviewer, terms touched, claim risk, and hold state. Use **one source PR** per coherent batch with precise reviewer comments.
3. On an authorized development checkout, run:
   ```bash
   git fetch origin
   git switch lumina/ar-vnext-rev2-preview-20261029
   make check
   make preview
   ```
   Then review `http://127.0.0.1:8080/ar/` at desktop and mobile widths, including RTL, navigation, metadata, hreflang, footer and link targets. **These commands are instructions; they have not been run or passed in this branch.** A build can change committed `dist/` bytes; include verified rebuilt output in the eventual release PR.
4. Ask Ali/Khalil to mark exact proposed Arabic wording `approved / needs correction / hold`. Do not silently replace historically approved Arabic with a machine-generated translation or claim new approval because the draft arrived.
5. Chris Beall performs the editorial/claim review and decides website publish/rollback. The technical operator should use the [canonical Teddy release procedure](../../deploy/README.md), retaining old immutable releases and actual origin/public-byte receipts. GitHub admin authority is **not** Teddy privilege.

**Relevant governing record:** [Internal October 19 delegation](https://github.com/QuietWire-Civic-AI/Internal/blob/main/01_Projects/Website/2026-10-19_Chris_Beall_Website_Publication_Delegation_Arabic_First_Locale_Gate.md).

## Boundaries / review gates

This branch records **source integration in progress**, not finished Arabization of the site. No live website change, legal/commercial promise, new translation sign-off, or operational privilege follows from its existence.

The current organization-wide GitHub Actions runner problem can prevent CI from starting, independent of the source quality. Use a clean local `make check` as interim evidence but **do not merge a changed site without complete build/parity and human language checks**.
