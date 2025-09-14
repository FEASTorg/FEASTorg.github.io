#!/usr/bin/env python3
"""
Ensure and normalize Jekyll front matter for imported Markdown trees.

This script is idempotent. It:
  1) Creates or normalizes the hub page at <root>/index.md with:
     - layout: "default"
     - title: PROJECT_TITLE (forced)
     - has_children: true
     - no parent/grand_parent (hub must not be a child)
     - optional redirect_from entries merged from the REDIRECT_FROM env var
       (JSON array or string), for use with jekyll-redirect-from.
  2) Walks all Markdown files under <root> and ensures minimal front matter:
     - layout: "default" (if absent)
     - title: from existing FM, first H1, or filename
     - Top-level pages: parent: PROJECT_TITLE
     - Subdirectory pages:
         * Ensure a section index.md with has_children: true, layout: default,
           title = section name (forced), parent = PROJECT_TITLE
         * Non-index pages: parent: <Section Title>, grand_parent: PROJECT_TITLE
     - README.md is excluded from nav when an index.md exists beside it.

Inputs
------
argv[1]            : Path to the imported project root (mount directory)
Env.PROJECT_TITLE  : Optional project display name (defaults to directory name)
Env.REDIRECT_FROM  : Optional JSON array or string for redirect_from on hub

Outputs
-------
Rewrites Markdown files in-place to include normalized front matter.

Notes
-----
- Designed for Just the Docs’ exact-title parent/child matching.
- Safe on repeated runs (no behavioral drift, stable formatting).
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

import yaml

# Supported Markdown extensions
MARKDOWN_EXTS = {".md", ".markdown"}

# Regex: capture ONLY YAML between the leading '---' delimiters
_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

# Regex: first Markdown H1
_H1_RE = re.compile(r"^\s{0,3}#\s+(.+?)\s*$")


def split_front_matter(text: str) -> Tuple[Dict, str]:
    """
    Split a Markdown document into (front_matter_dict, body).

    Parses only the YAML between the top '---' fences. Returns ({}, text) if
    no front matter exists or parsing fails.
    """
    m = _FRONT_MATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        # Be forgiving; treat malformed YAML as missing
        data = {}
    return data, text[m.end() :]


def dump_front_matter(data: Dict, body: str) -> str:
    """
    Render a Markdown document from a front matter dict and body.

    Keys are emitted in insertion order (sort_keys=False) for stable diffs.
    """
    return f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n\n{body}"


def first_h1(body: str) -> Optional[str]:
    """Return the first H1 text from body, if present; otherwise None."""
    for line in body.splitlines():
        m = _H1_RE.match(line)
        if m:
            return m.group(1).strip()
    return None


def titleize(filename: str) -> str:
    """Derive a human-friendly title from a filename."""
    return Path(filename).stem.replace("_", " ").replace("-", " ").title()


def _normalize_redirect_from(
    redirect_from_env: str, existing: list | str | None
) -> list[str]:
    """
    Merge redirects from environment JSON/string with existing front matter.

    Returns a sorted list including both '/path' and '/path/' variants for robustness.
    """
    # Parse env as JSON array or scalar
    try:
        extra = yaml.safe_load(redirect_from_env) if redirect_from_env else []
    except yaml.YAMLError:
        extra = []
    if isinstance(extra, str):
        extra = [extra]

    # Normalize existing to a list
    if existing is None:
        existing_list: list[str] = []
    elif isinstance(existing, str):
        existing_list = [existing]
    else:
        existing_list = list(existing)

    merged = [
        p.rstrip("/")
        for p in (existing_list + extra)
        if isinstance(p, str) and p.strip()
    ]
    if not merged:
        return []

    # Keep both slashless and slash-trailing forms
    out = {f"/{q.lstrip('/')}" for q in merged}
    out |= {f"/{q.lstrip('/')}/" for q in merged}
    return sorted(out)


def ensure_hub_index(root: Path, project_title: str, redirect_from_env: str) -> Path:
    """
    Create or normalize the hub page at <root>/index.md.

    Forces canonical title and section semantics. Merges redirect_from entries
    from REDIRECT_FROM env to support legacy slugs via jekyll-redirect-from.
    """
    hub = root / "index.md"
    if hub.exists():
        txt = hub.read_text(encoding="utf-8", errors="ignore")
        fm, body = split_front_matter(txt)
    else:
        fm, body = {}, f"# {project_title}\n\n"

    fm["layout"] = fm.get("layout") or "default"
    fm["title"] = project_title
    fm["has_children"] = True
    fm.pop("parent", None)
    fm.pop("grand_parent", None)

    redirects = _normalize_redirect_from(redirect_from_env, fm.get("redirect_from"))
    if redirects:
        fm["redirect_from"] = redirects
    elif "redirect_from" in fm:
        # Keep existing if non-empty, otherwise drop the key for cleanliness
        existing = fm.get("redirect_from")
        if not existing:
            fm.pop("redirect_from", None)

    hub.write_text(dump_front_matter(fm, body), encoding="utf-8")
    return hub


def ensure_section_index(
    section_dir: Path, project_title: str, section_title: str
) -> None:
    """
    Create or normalize a section index.md for a subdirectory.

    Ensures the section acts as a parent page under the hub.
    """
    sec_index = section_dir / "index.md"
    if sec_index.exists():
        txt = sec_index.read_text(encoding="utf-8", errors="ignore")
        s_fm, s_body = split_front_matter(txt)
    else:
        s_fm, s_body = {}, f"# {section_title}\n\n"

    s_fm["layout"] = s_fm.get("layout") or "default"
    s_fm["title"] = section_title
    s_fm["has_children"] = True
    s_fm["parent"] = project_title

    sec_index.write_text(dump_front_matter(s_fm, s_body), encoding="utf-8")


def process_page(root: Path, hub: Path, project_title: str, page_path: Path) -> None:
    """
    Normalize a single Markdown page under <root>.

    - Adds layout/title if missing.
    - Assigns parent/grand_parent based on directory depth.
    - Hides README.md when an index.md exists in the same directory.
    """
    if not page_path.is_file() or page_path.suffix.lower() not in MARKDOWN_EXTS:
        return
    if page_path.samefile(hub):
        return

    txt = page_path.read_text(encoding="utf-8", errors="ignore")
    fm, body = split_front_matter(txt)

    fm.setdefault("layout", "default")
    fm["title"] = fm.get("title") or first_h1(body) or titleize(page_path.name)

    rel = page_path.relative_to(root)
    if rel.parent == Path("."):
        # Top-level child of hub
        fm.setdefault("parent", project_title)
    else:
        # Section child
        section_slug = rel.parts[0]
        section_title = section_slug.replace("_", " ").replace("-", " ").title()
        ensure_section_index(root / section_slug, project_title, section_title)

        if page_path.name != "index.md":
            fm.setdefault("grand_parent", project_title)
            fm.setdefault("parent", section_title)

    # Hide README when a sibling index exists
    if (
        page_path.name.lower() == "readme.md"
        and (page_path.parent / "index.md").exists()
    ):
        fm["nav_exclude"] = True

    page_path.write_text(dump_front_matter(fm, body), encoding="utf-8")


def main(argv: list[str]) -> int:
    """CLI entrypoint."""
    if len(argv) < 2:
        sys.stderr.write("usage: ensure_front_matter.py <root-dir>\n")
        return 2

    root = Path(argv[1]).resolve()
    project_title = os.environ.get("PROJECT_TITLE", root.name).strip() or root.name
    redirect_from_env = os.environ.get("REDIRECT_FROM", "")

    hub = ensure_hub_index(root, project_title, redirect_from_env)

    for path in root.rglob("*"):
        process_page(root, hub, project_title, path)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
