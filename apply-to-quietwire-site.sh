#!/usr/bin/env bash
set -Eeuo pipefail

BUNDLE_ROOT="$(cd "$(dirname "$0")" && pwd)"
SOURCE="$BUNDLE_ROOT/site"
TARGET="${TARGET:-$HOME/quietwire-site}"
REMOTE="${REMOTE:-git@github.com:QuietWire-Civic-AI/quietwire-site.git}"

[ -d "$SOURCE" ] || { echo "Missing bundle site directory: $SOURCE" >&2; exit 1; }
command -v git >/dev/null
command -v python3 >/dev/null

if [ -e "$TARGET" ]; then
  echo "Refusing to overwrite existing target: $TARGET" >&2
  exit 1
fi

git clone "$REMOTE" "$TARGET"

if [ -n "$(find "$TARGET" -mindepth 1 -maxdepth 1 ! -name .git -print -quit)" ]; then
  echo "Remote repository is not empty; review before applying this foundation." >&2
  exit 1
fi

cp -a "$SOURCE"/. "$TARGET"/
cd "$TARGET"

if ! git symbolic-ref --quiet --short HEAD >/dev/null 2>&1; then
  git switch -c main
fi

git config user.name >/dev/null 2>&1 || git config user.name "QuietWire Site Builder"
git config user.email >/dev/null 2>&1 || git config user.email "hello@quietwire.ai"

python3 scripts/build.py
python3 scripts/check.py
git add .
git commit -m "Launch QuietWire static site foundation"
git push -u origin main

echo
echo "QuietWire site pushed:"
git log -1 --oneline --decorate
