#!/usr/bin/env bash
# scripts/import_sources.sh
# -----------------------------------------------------------------------------
# Import remote repository docs into the hub repo.
#
# Behavior (idempotent):
# - For each entry in sources.json:
#     * Shallow clone the repo with sparse-checkout limited to .subdir
#     * Rsync the selected subtree into the local .mount path
#       - Respects per-source "exclude" globs and per-repo ".indexignore"
#     * Normalize front matter for Just the Docs via ensure_front_matter.py
#       - Passes PROJECT_TITLE, REDIRECT_FROM (JSON), and NAV_ORDER env vars
#
# Inputs:
#   sources.json entries:
#     - name            : short id
#     - title           : display name (defaults to name)
#     - repo            : org/repo
#     - ref             : branch or tag
#     - subdir          : subtree to import
#     - mount           : destination mount path in this repo
#     - exclude[]       : optional rsync exclude patterns
#     - redirect_from[] : optional legacy slugs (or "redirects[]" for bw-compat)
#     - nav_order       : optional integer for navigation ordering
#
# Requirements: bash, git, jq, rsync
# Safe defaults: set -euo pipefail, strict quoting, basic path sanitization.
# -----------------------------------------------------------------------------

set -euo pipefail
IFS=$'\n\t'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly ROOT
readonly MANIFEST="${ROOT}/_data/sources.json"

# --- Utilities ----------------------------------------------------------------

die() { echo "error: $*" >&2; exit 1; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "$1 not found"
}

# Retry helper with exponential backoff.
retry_cmd() {
  local label="$1"
  shift

  local max_retries="${IMPORT_MAX_RETRIES:-3}"
  local base_delay="${IMPORT_RETRY_BASE_SECONDS:-2}"
  local attempt=1
  local delay="$base_delay"

  while true; do
    if "$@"; then
      return 0
    fi
    if (( attempt >= max_retries )); then
      echo "error: ${label} failed after ${attempt} attempts" >&2
      return 1
    fi
    echo "warning: ${label} failed on attempt ${attempt}/${max_retries}; retrying in ${delay}s..." >&2
    sleep "$delay"
    attempt=$((attempt + 1))
    delay=$((delay * 2))
  done
}

clone_sparse_repo() {
  local url="$1"
  local ref="$2"
  local tmp_abs="$3"
  local sub="$4"

  rm -rf -- "${tmp_abs:?}"
  git clone --quiet --filter=blob:none --no-checkout --depth 1 --branch "$ref" "$url" "$tmp_abs"
  git -C "$tmp_abs" sparse-checkout init --cone
  git -C "$tmp_abs" sparse-checkout set "$sub"
  git -C "$tmp_abs" checkout --quiet
}

sanitize_relpath() {
  # Reject empty, absolute, or parent-traversal paths.
  local p="${1:-}"
  [[ -n "$p" && "$p" != /* && "$p" != *"..*" ]] || return 1
}

# --- Preflight -----------------------------------------------------------------

require_cmd jq
require_cmd rsync
require_cmd git

[[ -f "$MANIFEST" ]] || die "missing ${MANIFEST}"
mkdir -p "${ROOT}/_ext"

# --- Main ----------------------------------------------------------------------

jq -c '.sources[]' "$MANIFEST" | while IFS= read -r row; do
  name="$(jq -r .name                <<<"$row")"
  title="$(jq -r '.title // .name'   <<<"$row")"
  repo="$(jq -r .repo                <<<"$row")"
  ref="$(jq -r .ref                  <<<"$row")"
  sub="$(jq -r .subdir               <<<"$row")"
  mount="$(jq -r .mount              <<<"$row")"

  sanitize_relpath "$sub"   || die "invalid subdir: $sub"
  sanitize_relpath "$mount" || die "invalid mount: $mount"

  tmp="_ext/$name"
  sanitize_relpath "$tmp" || die "invalid tmp: $tmp"

  TMP_ABS="${ROOT}/${tmp}"
  MOUNT_ABS="${ROOT}/${mount}"
  SRC_ABS="${TMP_ABS}/${sub}"

  url="https://github.com/${repo}.git"

  echo "::group::Clone ${repo}@${ref} -> ${tmp} (sparse: ${sub})"
  retry_cmd "clone ${repo}@${ref}" clone_sparse_repo "$url" "$ref" "$TMP_ABS" "$sub" \
    || die "unable to import ${repo}@${ref}"
  echo "::endgroup::"

  echo "::group::Sync ${sub} -> ${mount}"
  rm -rf -- "${MOUNT_ABS:?}"
  mkdir -p "${MOUNT_ABS}"

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

  # Debug: list top-level imported Markdown files
  echo "Imported files in ${mount}:"
  find "${MOUNT_ABS}" -maxdepth 1 -type f -name '*.md' -printf '  %P\n' | sort || true

  echo "::group::Normalize front matter for ${mount}"
  # Accept either "redirect_from" or legacy "redirects"
  redirect_from_json="$(jq -c '.redirect_from? // .redirects? // []' <<<"$row")"
  nav_order="$(jq -r '.nav_order? // ""' <<<"$row")"
  PROJECT_TITLE="$title" REDIRECT_FROM="$redirect_from_json" NAV_ORDER="$nav_order" \
    python3 "${ROOT}/scripts/ensure_front_matter.py" "$MOUNT_ABS"
  echo "::endgroup::"
done
# --- EOF -----------------------------------------------------------------------
