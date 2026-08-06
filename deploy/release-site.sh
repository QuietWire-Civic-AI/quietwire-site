#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C.UTF-8

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

T="${TEDDY_SSH:-teddy}"
BASE="${QUIETWIRE_SITE_BASE:-/var/lib/qwos/sites/quietwire}"
PUBLIC_ORIGIN="${QUIETWIRE_PUBLIC_ORIGIN:-https://www.quietwire.ai}"
ORIGIN_HOST="${QUIETWIRE_ORIGIN_HOST:-www.quietwire.ai}"
PUBLIC_ATTEMPTS="${QUIETWIRE_PUBLIC_ATTEMPTS:-6}"
PUBLIC_DELAY="${QUIETWIRE_PUBLIC_DELAY:-5}"

WORK="$(mktemp -d)"
cleanup() {
  rm -rf "$WORK"
}
trap cleanup EXIT

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

command -v git >/dev/null || fail "git is required"
command -v make >/dev/null || fail "make is required"
command -v ssh >/dev/null || fail "ssh is required"
command -v scp >/dev/null || fail "scp is required"
command -v curl >/dev/null || fail "curl is required"
command -v sha256sum >/dev/null || fail "sha256sum is required"
command -v tar >/dev/null || fail "tar is required"

BRANCH="$(git branch --show-current)"
[ "$BRANCH" = "main" ] || fail "release only from main; current branch is $BRANCH"

[ -z "$(git status --porcelain)" ] || fail "working tree is not clean"

echo "== Updating main =="
git fetch origin main
git pull --ff-only origin main

echo
echo "== Building and validating =="
make check

[ -z "$(git status --porcelain)" ] || fail "build changed committed output; review and commit the generated diff before release"

COMMIT="$(git rev-parse HEAD)"
SHORT_COMMIT="$(git rev-parse --short=12 HEAD)"
RELEASE="$(date -u +%Y%m%dT%H%M%SZ)-${SHORT_COMMIT}"
RELEASE_DIR="$BASE/releases/$RELEASE"
ARCHIVE="$WORK/quietwire-site-${RELEASE}.tar.gz"
FILES_MANIFEST="$WORK/files.sha256"
RELEASE_RECORD="$WORK/release.txt"

PREVIOUS="$(
  ssh -o BatchMode=yes -o ConnectTimeout=10 "$T" \
    "test -L '$BASE/current' && test -d '$BASE/releases' && test -d '$BASE/provenance' && readlink '$BASE/current'"
)"

[ -n "$PREVIOUS" ] || fail "could not resolve the current Teddy release"

echo
echo "== Preparing immutable release =="
echo "Target:   $T"
echo "Previous: $PREVIOUS"
echo "New:      $RELEASE_DIR/public"

(
  cd dist
  while IFS= read -r -d '' file; do
    sha256sum "$file"
  done < <(find . -type f -print0 | sort -z)
) > "$FILES_MANIFEST"

tar -C dist -czf "$ARCHIVE" .
ARCHIVE_SHA="$(sha256sum "$ARCHIVE" | awk '{print $1}')"

{
  echo "release_id=$RELEASE"
  echo "git_commit=$COMMIT"
  echo "built_utc=$(date -u +%FT%TZ)"
  echo "built_on=$(hostname)"
  echo "target=$T"
  echo "previous_release=$PREVIOUS"
  echo "archive_sha256=$ARCHIVE_SHA"
} > "$RELEASE_RECORD"

REMOTE_ARCHIVE="/tmp/$(basename "$ARCHIVE")"
REMOTE_MANIFEST="/tmp/quietwire-site-${RELEASE}.files.sha256"
REMOTE_RECORD="/tmp/quietwire-site-${RELEASE}.release.txt"

scp "$ARCHIVE" "$T:$REMOTE_ARCHIVE"
scp "$FILES_MANIFEST" "$T:$REMOTE_MANIFEST"
scp "$RELEASE_RECORD" "$T:$REMOTE_RECORD"

echo
echo "== Staging, verifying, and activating on Teddy =="
ssh "$T" bash -s -- \
  "$BASE" \
  "$RELEASE" \
  "$PREVIOUS" \
  "$REMOTE_ARCHIVE" \
  "$REMOTE_MANIFEST" \
  "$REMOTE_RECORD" \
  "$ARCHIVE_SHA" \
  "$ORIGIN_HOST" <<'REMOTE'
set -euo pipefail

BASE="$1"
RELEASE="$2"
PREVIOUS="$3"
REMOTE_ARCHIVE="$4"
REMOTE_MANIFEST="$5"
REMOTE_RECORD="$6"
ARCHIVE_SHA="$7"
ORIGIN_HOST="$8"

if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
else
  SUDO="sudo"
fi

RELEASE_DIR="$BASE/releases/$RELEASE"
PUBLIC_DIR="$RELEASE_DIR/public"
PROVENANCE_DIR="$BASE/provenance/$RELEASE"

activate_release() {
  TARGET="$1"
  LINK="$BASE/.current-activation-$$"

  $SUDO rm -f "$LINK"
  $SUDO ln -s "$TARGET" "$LINK"
  $SUDO mv -Tf "$LINK" "$BASE/current"
}

cleanup_remote() {
  rm -f "$REMOTE_ARCHIVE" "$REMOTE_MANIFEST" "$REMOTE_RECORD"
}
trap cleanup_remote EXIT

[ ! -e "$RELEASE_DIR" ] || {
  echo "Release already exists: $RELEASE_DIR" >&2
  exit 20
}

REMOTE_ARCHIVE_SHA="$(sha256sum "$REMOTE_ARCHIVE" | awk '{print $1}')"
[ "$REMOTE_ARCHIVE_SHA" = "$ARCHIVE_SHA" ] || {
  echo "Uploaded archive hash mismatch" >&2
  exit 21
}

$SUDO install -d -m 0755 "$PUBLIC_DIR" "$PROVENANCE_DIR"
$SUDO tar -xzf "$REMOTE_ARCHIVE" -C "$PUBLIC_DIR"
$SUDO install -m 0644 "$REMOTE_MANIFEST" "$RELEASE_DIR/files.sha256"
$SUDO install -m 0644 "$REMOTE_RECORD" "$RELEASE_DIR/release.txt"
$SUDO install -m 0644 "$REMOTE_MANIFEST" "$PROVENANCE_DIR/files.sha256"
$SUDO install -m 0644 "$REMOTE_RECORD" "$PROVENANCE_DIR/release.txt"

(
  cd "$PUBLIC_DIR"
  sha256sum -c "$RELEASE_DIR/files.sha256"
)

$SUDO chmod -R a=rX,u+w "$RELEASE_DIR" "$PROVENANCE_DIR"

activate_release "$PUBLIC_DIR"
echo "Activated -> $(readlink "$BASE/current")"

echo "Verifying all generated HTML routes against Teddy origin"
ORIGIN_OK=1
COUNT=0

while IFS= read -r -d '' FILE; do
  REL="${FILE#$PUBLIC_DIR}"
  ROUTE="${REL%index.html}"
  OUT="/tmp/qw-origin-route-$$-${COUNT}.html"

  if ! curl -kfsSL \
      --resolve "$ORIGIN_HOST:443:127.0.0.1" \
      "https://$ORIGIN_HOST$ROUTE" \
      -o "$OUT"; then
    echo "Origin request failed: $ROUTE" >&2
    ORIGIN_OK=0
  elif ! cmp -s "$FILE" "$OUT"; then
    echo "Origin output mismatch: $ROUTE" >&2
    ORIGIN_OK=0
  fi

  rm -f "$OUT"
  COUNT=$((COUNT + 1))
done < <(find "$PUBLIC_DIR" -type f -name index.html -print0 | sort -z)

if [ "$ORIGIN_OK" -ne 1 ]; then
  echo "Origin verification failed; restoring previous release" >&2
  activate_release "$PREVIOUS"
  echo "Restored -> $(readlink "$BASE/current")"
  exit 22
fi

echo "Teddy origin matches all $COUNT generated HTML routes"
REMOTE

echo
echo "== Verifying public output =="
PUBLIC_OK=0

for ATTEMPT in $(seq 1 "$PUBLIC_ATTEMPTS"); do
  ATTEMPT_OK=1
  COUNT=0

  while IFS= read -r -d '' FILE; do
    REL="${FILE#dist}"
    ROUTE="${REL%index.html}"
    OUT="$WORK/public-${ATTEMPT}-${COUNT}.html"

    if ! curl -fsSL \
        -H 'Cache-Control: no-cache' \
        "${PUBLIC_ORIGIN}${ROUTE}?release=${RELEASE}-${ATTEMPT}" \
        -o "$OUT"; then
      ATTEMPT_OK=0
    elif ! cmp -s "$FILE" "$OUT"; then
      ATTEMPT_OK=0
    fi

    COUNT=$((COUNT + 1))
  done < <(find dist -type f -name index.html -print0 | sort -z)

  echo "Attempt $ATTEMPT: matched=$ATTEMPT_OK routes=$COUNT"

  if [ "$ATTEMPT_OK" -eq 1 ]; then
    PUBLIC_OK=1
    break
  fi

  sleep "$PUBLIC_DELAY"
done

ACTIVE="$(ssh "$T" "readlink '$BASE/current'")"

echo
echo "Active release: $ACTIVE"
echo "Previous release retained: $PREVIOUS"

if [ "$PUBLIC_OK" -eq 1 ]; then
  echo
echo "LIVE: $PUBLIC_ORIGIN/"
  echo "Public output matches the approved build exactly."
  exit 0
fi

echo
echo "Teddy origin is correct, but the public edge did not return identical files within the verification window."
echo "The new release remains active because origin verification passed."
exit 2
