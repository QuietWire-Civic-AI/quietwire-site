# Ask QuietWire — conversational homepage specification (proposal)

Status: design review only. No current route, hosting contract or release has changed.

## User experience

A clean first-party landing page with a prominent question input, optional example prompts, language choice and discreet links to Advisory, Labs, Work, Library and About. Asking a question expands into a multi-turn conversation with links to the published source pages. Identify the assistant as AI, state uncertainty, and offer a normal contact path. No login for public questions. Keep deep links and ordinary navigation fully usable without inference or JavaScript. Proposed text and layout need editorial and locale review.

## Integration contract

- Preserve deterministic static build, committed dist output, current locale manifests, tracker-free design and immutable static release/rollback mechanism. Add no third-party scripts or client-side model keys.
- A separately admitted public chat API is a proposal, not an existing static-site capability. Browser traffic must reach only a narrowly scoped first-party endpoint. Keep static release and gateway deployment identities, filesystems, credentials and rollback separate.
- Gateway retrieval uses an explicitly approved, versioned public-only corpus of released website content and listed publications/editions. Include source links and release/freshness metadata. No access to private repositories, mail, companion memory, internal APIs or execution tools.
- Use isolated short-lived sessions, an explicit privacy notice, bounded request and output sizes, rate/concurrency/cost limits, safe rendering, validated source links and timeout/circuit breaker. Treat visitor input and retrieved text as untrusted. Provider adapter selection and data-handling policy need separate review.
- No autonomous commitment, financial quote, confidential intake or customer data. An optional later human handoff must be consented and separate from anonymous chat.

## Acceptance sequence

1. Review responsive mockup and source selection with editorial owner. Preserve reviewed locale variants, including human-reviewed Arabic as required by the current website-change gate.
2. Private prototype against public or fictional sources. Prove a visitor can ask, follow up, receive a source-backed answer, and reach the ordinary page.
3. Test unknowns, false/unsupported claims, citation validation, prompt injection, fictional restricted-record refusal, cross-session isolation, quotas, timeouts, accessibility, no private data access and no tool authority.
4. Prove static and contact fallback with API down. Verify build/link/locale checks and gateway tests. Independently approve technical hosting, privacy and deployment scope; publish only through approved release mechanism with exact artifacts, public verification and rollback.

The website stays static and useful until a separate service is qualified. This document proposes an interface, not an advertised product or production launch.
