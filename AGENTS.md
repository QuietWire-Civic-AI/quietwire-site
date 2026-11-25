# Guidance for Nexus working with Chris Beall

## Scope

These instructions apply to work performed by Nexus for Chris Beall in this
repository. They preserve Chris's artifact destinations and working conventions;
they do not impose those preferences on other maintainers or companions.

Read `README.md` before changing the site. Preserve its static, local-first
design, locale review states, public-safe content rules, and publishing boundary.

## Source and verification

- Edit maintained site source under `src/` and the relevant configuration or
  data. Regenerate `dist/` through the existing build when site source changes;
  `dist/` is committed release output.
- Run `make check` for site source or configuration changes, together with
  focused checks for changed behavior. Do not weaken a gate to obtain a pass.
  For documentation-only work, verify the affected references and the diff
  without regenerating unrelated output.
- Verify contact links, document destinations, and access for the intended
  audience. Keep private material and private document links out of public
  website pages.

## Artifact destinations for Chris's work

- Before creating or converting a deliverable, resolve its intended destination
  and any existing maintained version. Follow the destination specified in the
  current task; update the maintained item instead of creating a competing copy.
- Maintain collaborative narrative, strategy, scope, and working documents in
  native Google Docs/Drive through the established G: workflow.
- Keep code, repository operating instructions, and approved release snapshots
  in GitHub. Repository build and release documentation remains with its source.
- Create Word, PDF, ZIP, or other document exports only when requested or agreed.
  Exports are snapshots; they do not replace the maintained native document.
  Do not restore superseded exports to public download directories.
- Verify a document's approved version and distribution audience before linking
  or serving it publicly. Access through an owner-private preview is not public
  distribution approval.

## Publishing authority

Models and companions may prepare source changes and previews. Production
publishing remains an explicit human-approved release action, as set out in
`README.md` and `deploy/README.md`. A repository merge establishes maintained
source; it does not authorize production activation.
