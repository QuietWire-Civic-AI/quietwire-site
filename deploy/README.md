# Teddy hosting and release boundary

The QuietWire website is deployed as a separate static module. It is not Teddy's chat surface and receives no access to companion memory, model credentials, attestation keys, work orders, or loopback APIs.

## Custody layout

```text
/var/lib/qwos/sites/quietwire/
├── releases/<release-id>/
│   ├── public/
│   ├── files.sha256
│   └── release.txt
├── current -> releases/<release-id>/public
└── provenance/<release-id>/
    ├── files.sha256
    └── release.txt
```

Caddy serves only the `current` symlink. Releases are immutable deployment units. Activation is an atomic symlink change after local validation, uploaded-file hash verification, and Teddy-origin verification.

## Canonical release command

Run from Moose with a clean `main` checkout and the Teddy SSH alias available:

```bash
cd ~/quietwire-site
bash deploy/release-site.sh
```

Optional environment overrides:

```bash
TEDDY_SSH=root@teddy.quietwire.ai \
QUIETWIRE_SITE_BASE=/var/lib/qwos/sites/quietwire \
QUIETWIRE_PUBLIC_ORIGIN=https://www.quietwire.ai \
QUIETWIRE_ORIGIN_HOST=www.quietwire.ai \
bash deploy/release-site.sh
```

The release tool performs the following bounded sequence:

1. Requires the current branch to be `main` and the working tree to be clean.
2. Fetches and fast-forwards from `origin/main`.
3. Runs `make check` and refuses to release if the build changes committed output.
4. Creates a timestamped release archive and a SHA-256 manifest for every generated file.
5. Records the Git commit, build time, builder host, archive hash, target, and previous release.
6. Uploads the archive and manifests to Teddy.
7. Verifies the uploaded archive hash and every extracted file before activation.
8. Activates the new release with an atomic `current` symlink replacement.
9. Requests every generated `index.html` route directly from Teddy's Caddy origin and compares the served bytes with the staged files.
10. Restores the previous release automatically if origin verification fails.
11. Requests every public HTML route through `www.quietwire.ai` and compares it byte-for-byte with the approved local build.
12. Leaves the new release active with exit code `2` when Teddy is correct but an external cache or edge has not converged within the verification window.

The tool does not pass translated phrases through nested shell quoting. Meaning and publication approval are checked during `make check`; deployment identity is then verified with hashes and byte comparison.

## Exit meanings

- `0`: Teddy and the public website match the approved build.
- `1`: preflight, build, upload, staging, or other local failure; inspect the printed boundary before retrying.
- `2`: Teddy origin is verified and the new release remains active, but the public edge did not return identical files within the configured window.
- remote staging failures restore the previous release before returning nonzero.

## Rollback

The release command prints both the active and previous release paths. To restore a known release manually, use an atomic symlink replacement on Teddy:

```bash
TARGET=/var/lib/qwos/sites/quietwire/releases/<release-id>/public
BASE=/var/lib/qwos/sites/quietwire

ssh teddy bash -s -- "$BASE" "$TARGET" <<'REMOTE'
set -euo pipefail
BASE="$1"
TARGET="$2"

if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
else
  SUDO="sudo"
fi

LINK="$BASE/.rollback-current-$$"
$SUDO rm -f "$LINK"
$SUDO ln -s "$TARGET" "$LINK"
$SUDO mv -Tf "$LINK" "$BASE/current"
readlink "$BASE/current"
REMOTE
```

Verify the restored public route before closing the operation.

## Retention

Do not delete releases during an active deployment or immediately after a successful change. Preserve at least the current release and its immediate predecessor. Adopt and run a separate retention procedure only after the release history is no longer operationally warm.

## Security boundary

- Teddy serves static output only.
- The site receives no runtime access to QWOS internals or companion state.
- Caddy's root remains the read-only `current` release path.
- DNS, TLS, mail records, monitoring, backup, and rollback remain separate operational boundaries.
- A repository merge is not a production deployment; production activation remains an explicit authorized action.
