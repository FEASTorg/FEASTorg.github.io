#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Ensure tools
if ! command -v jq >/dev/null 2>&1; then
  sudo apt-get update && sudo apt-get install -y jq
fi
if ! command -v rsync >/dev/null 2>&1; then
  sudo apt-get update && sudo apt-get install -y rsync
fi

manifest="$ROOT/sources.json"
mkdir -p "$ROOT/_ext" "$ROOT/projects"

jq -c '.sources[]' "$manifest" | while read -r row; do
  name=$(echo "$row" | jq -r .name)
  title=$(echo "$row" | jq -r '.title // .name')
  repo=$(echo "$row" | jq -r .repo)
  ref=$(echo "$row" | jq -r .ref)
  sub=$(echo "$row" | jq -r .subdir)
  mount=$(echo "$row" | jq -r .mount)

  tmp="_ext/$name"
  url="https://github.com/$repo.git"
  if [[ -n "${DOCS_READ_TOKEN:-}" ]]; then
    url="https://x-access-token:${DOCS_READ_TOKEN}@github.com/${repo}.git"
  fi

  echo "::group::Clone $repo@$ref → $tmp (sparse: $sub)"
  rm -rf "$ROOT/$tmp"
  git clone --no-checkout --depth 1 --branch "$ref" "$url" "$ROOT/$tmp"
  git -C "$ROOT/$tmp" sparse-checkout init --cone
  git -C "$ROOT/$tmp" sparse-checkout set "$sub"
  git -C "$ROOT/$tmp" checkout
  echo "::endgroup::"

  echo "::group::Sync $sub → $mount"
  rm -rf "$ROOT/$mount"
  mkdir -p "$ROOT/$mount"

  # Build rsync filter list from manifest excludes
  RSYNC_FILTERS=()
  while IFS= read -r pat; do
    [[ -n "$pat" ]] && RSYNC_FILTERS+=(--filter="- ${pat}")
  done < <(jq -r '.exclude[]? // empty' <<<"$row")

  rsync -a --delete \
    --filter='dir-merge,- .indexignore' \
    "${RSYNC_FILTERS[@]}" \
    "$ROOT/$tmp/$sub/" "$ROOT/$mount/"
  echo "::endgroup::"

  echo "::group::Normalize front matter for $mount"
  PROJECT_TITLE="$title" python3 "$ROOT/scripts/ensure_front_matter.py" "$ROOT/$mount"
  echo "::endgroup::"
done
