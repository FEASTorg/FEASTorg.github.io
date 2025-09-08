#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
manifest="${ROOT:?}/sources.json"

# Require tools
command -v jq >/dev/null    || { echo "jq not found" >&2; exit 1; }
command -v rsync >/dev/null || { echo "rsync not found" >&2; exit 1; }

mkdir -p "${ROOT:?}/_ext"

jq -c '.sources[]' "$manifest" | while IFS= read -r row; do
  name="$(jq -r .name              <<<"$row")"
  title="$(jq -r '.title // .name' <<<"$row")"
  repo="$(jq -r .repo              <<<"$row")"
  ref="$(jq -r .ref                <<<"$row")"
  sub="$(jq -r .subdir             <<<"$row")"
  mount="$(jq -r .mount            <<<"$row")"

  # Basic path sanitization
  case "$sub"   in ""|/*|*"..*" )   echo "invalid subdir: $sub"   >&2; exit 1;; esac
  case "$mount" in ""|/*|*"..*" )   echo "invalid mount: $mount"  >&2; exit 1;; esac

  tmp="_ext/$name"
  case "$tmp"   in ""|/*|*"..*" )   echo "invalid tmp: $tmp"      >&2; exit 1;; esac

  TMP_ABS="${ROOT:?}/${tmp}"
  MOUNT_ABS="${ROOT:?}/${mount}"
  SRC_ABS="${TMP_ABS}/${sub}"

  url="https://github.com/$repo.git"

  echo "::group::Clone $repo@$ref → $tmp (sparse: $sub)"
  rm -rf -- "${TMP_ABS:?}"
  git clone --quiet --filter=blob:none --no-checkout --depth 1 --branch "$ref" "$url" "$TMP_ABS"
  git -C "$TMP_ABS" sparse-checkout init --cone
  git -C "$TMP_ABS" sparse-checkout set "$sub"
  git -C "$TMP_ABS" checkout --quiet
  echo "::endgroup::"

  echo "::group::Sync $sub → $mount"
  rm -rf -- "${MOUNT_ABS:?}"
  mkdir -p "${MOUNT_ABS:?}"

  # Build rsync filter list from manifest excludes
  RSYNC_FILTERS=()
  while IFS= read -r pat; do
    [[ -n "$pat" ]] && RSYNC_FILTERS+=(--filter="- ${pat}")
  done < <(jq -r '.exclude[]? // empty' <<<"$row")

  rsync -a --delete \
    --filter='dir-merge,- .indexignore' \
    "${RSYNC_FILTERS[@]}" \
    "${SRC_ABS%/}/" "${MOUNT_ABS%/}/"
  echo "::endgroup::"

  # Debug: list imported markdown
  echo "Imported files in ${mount}:"
  find "${MOUNT_ABS}" -maxdepth 1 -type f -name '*.md' -printf '  %P\n' | sort || true

  echo "::group::Normalize front matter for $mount"
  PROJECT_TITLE="$title" python3 "$ROOT/scripts/ensure_front_matter.py" "$MOUNT_ABS"
  echo "::endgroup::"
done
