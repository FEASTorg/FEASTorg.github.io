#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
manifest="$ROOT/sources.json"

# Hard fail if required tools are missing (no apt on CI)
command -v jq >/dev/null    || { echo "jq not found" >&2; exit 1; }
command -v rsync >/dev/null || { echo "rsync not found" >&2; exit 1; }

mkdir -p "$ROOT/_ext" "$ROOT/projects"

jq -c '.sources[]' "$manifest" | while IFS= read -r row; do
  name=$(jq -r .name                <<<"$row")
  title=$(jq -r '.title // .name'   <<<"$row")
  repo=$(jq -r .repo                <<<"$row")
  ref=$(jq -r .ref                  <<<"$row")
  sub=$(jq -r .subdir               <<<"$row")
  mount=$(jq -r .mount              <<<"$row")

  tmp="_ext/$name"
  url="https://github.com/$repo.git"

  echo "::group::Clone $repo@$ref → $tmp (sparse: $sub)"
  rm -rf "$ROOT/$tmp"
  git clone --quiet --filter=blob:none --no-checkout --depth 1 --branch "$ref" "$url" "$ROOT/$tmp"
  git -C "$ROOT/$tmp" sparse-checkout init --cone
  git -C "$ROOT/$tmp" sparse-checkout set "$sub"
  git -C "$ROOT/$tmp" checkout --quiet
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
