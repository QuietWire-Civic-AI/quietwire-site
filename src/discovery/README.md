# QuietWire Discovery candidate v0.1

This directory is a self-contained, static, browser-local discovery application.

## Operating boundary

- No backend.
- No accounts.
- No form submission.
- No third-party JavaScript, fonts, analytics, or CDNs.
- No `fetch`, `XMLHttpRequest`, `sendBeacon`, WebSocket, or EventSource calls.
- No automatic use of cookies, localStorage, sessionStorage, IndexedDB, or a service worker.
- Answers remain in JavaScript memory until the user explicitly downloads a working file or report.
- The page Content Security Policy sets `connect-src 'none'` and `form-action 'none'`.

The web server can still observe an ordinary request for the static page and assets. It does not receive the answers typed into the application.

## Files

- `index.html` — page shell and security policy.
- `discovery.css` — application styling.
- `report.css` — print styling.
- `discovery.js` — local application logic.
- `data/water-treatment-en-v1.js` — versioned English questionnaire corpus with 30 sections and 333 questions.
- `/assets/quietwire-mark.png` and the standard favicon set — canonical site assets copied by the repository build.

## Local preview

```bash
cd discovery
python3 -m http.server 8080 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8080/`.

## Working-file format

The Save action produces a local JSON file with schema:

```text
quietwire.discovery.responses
schema_version: 1.0
```

The import path validates the schema, survey ID, question IDs, status values, field lengths, and a five-megabyte size limit before accepting a file into browser memory.

## Repository integration

The application is maintained in `src/discovery/`. The canonical repository build copies it to `dist/discovery/`, producing `/discovery/` on the static site. Navigation paths and brand assets use the same canonical sources as the rest of the site.

Do not add a direct-send path until QuietWire has a separately governed intake service, explicit retention policy, operator access controls, deletion process, and a reviewed submission receipt.
