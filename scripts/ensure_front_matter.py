#!/usr/bin/env python3
"""
Ensure Jekyll front matter for imported Markdown content.

Behavior (intentionally minimal and idempotent):
- Creates/updates a hub index.md in the given root with:
  layout: default, title: PROJECT_TITLE (forced), has_children: true
  Removes any parent/grand_parent on the hub page.
- For each Markdown file under root:
  * Adds minimal front matter if missing.
  * Derives title from existing front matter, first H1, or filename.
  * Top-level pages get parent: PROJECT_TITLE.
  * Subdirectory pages:
      - Ensure a section index.md exists with has_children: true,
        layout: default, title = section name (forced), parent = PROJECT_TITLE.
      - Child pages get grand_parent: PROJECT_TITLE and parent: <Section>.
  * README.md is excluded from nav when an index.md exists in the same directory.

Input:
- argv[1]: path to the project mount directory (e.g., "breads")
- Env: PROJECT_TITLE (optional). Defaults to the directory name.

Outputs:
- Rewrites Markdown files in-place with normalized front matter.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional

import yaml

# Markdown extensions we normalize
MARKDOWN_EXTS = {".md", ".markdown"}

# Front matter regex: capture ONLY the YAML content between delimiters.
_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

# Heading regex: first Markdown H1
_H1_RE = re.compile(r"^\s{0,3}#\s+(.+?)\s*$")


def split_front_matter(text: str) -> Tuple[Dict, str]:
    """Return (front_matter_dict, body) for a Markdown document."""
    m = _FRONT_MATTER_RE.match(text)
    if not m:
        return {}, text
    yaml_str = m.group(1)
    try:
        data = yaml.safe_load(yaml_str) or {}
    except (yaml.YAMLError, ValueError):
        data = {}
    return data, text[m.end() :]


def dump_front_matter(data: Dict, body: str) -> str:
    """Render a Markdown document from front matter dict and body."""
    return f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n\n{body}"


def first_h1(body: str) -> Optional[str]:
    """Return the first H1 text from body, if any."""
    for line in body.splitlines():
        m = _H1_RE.match(line)
        if m:
            return m.group(1).strip()
    return None


def titleize(filename: str) -> str:
    """Derive a human title from a filename."""
    stem = Path(filename).stem
    return stem.replace("_", " ").replace("-", " ").title()


def ensure_hub_index(root: Path, project_title: str) -> Path:
    """Create or normalize the hub index.md under root."""
    hub = root / "index.md"
    if hub.exists():
        txt = hub.read_text(encoding="utf-8", errors="ignore")
        fm, body = split_front_matter(txt)
    else:
        fm, body = {}, f"# {project_title}\n\n"

    # Canonicalize hub metadata
    fm["layout"] = fm.get("layout") or "default"
    fm["title"] = (
        project_title  # exact match required by Just the Docs for parent linking
    )
    fm["has_children"] = True
    fm.pop("parent", None)
    fm.pop("grand_parent", None)

    hub.write_text(dump_front_matter(fm, body), encoding="utf-8")
    return hub


def ensure_section_index(
    section_dir: Path, project_title: str, section_title: str
) -> None:
    """Create or normalize a section index.md for a subdirectory."""
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
    """Normalize one Markdown page's front matter and grouping."""
    if not page_path.is_file() or page_path.suffix.lower() not in MARKDOWN_EXTS:
        return
    if page_path.samefile(hub):
        return

    txt = page_path.read_text(encoding="utf-8", errors="ignore")
    fm, body = split_front_matter(txt)

    # Required basics
    fm.setdefault("layout", "default")
    fm["title"] = fm.get("title") or first_h1(body) or titleize(page_path.name)

    # Grouping
    rel = page_path.relative_to(root)
    if rel.parent == Path("."):
        # Top-level child of hub
        fm.setdefault("parent", project_title)
    else:
        # Section children
        section_slug = rel.parts[0]
        section_title = section_slug.replace("_", " ").replace("-", " ").title()
        ensure_section_index(root / section_slug, project_title, section_title)

        if page_path.name != "index.md":
            fm.setdefault("grand_parent", project_title)
            fm.setdefault("parent", section_title)

    # Hide README when an index exists alongside it
    if (
        page_path.name.lower() == "readme.md"
        and (page_path.parent / "index.md").exists()
    ):
        fm["nav_exclude"] = True

    page_path.write_text(dump_front_matter(fm, body), encoding="utf-8")


def create_redirect_stubs(
    redirects: list[str], target_path: str, site_root: Path
) -> None:
    """Create redirect stub files for short URLs that redirect to the full path."""
    for redirect_url in redirects:
        # Clean path: /batch/ -> batch, /batch -> batch
        clean_path = redirect_url.strip("/")
        stub_path = site_root / f"{clean_path}.md"

        # Create redirect content using Jekyll's redirect_from plugin
        content = f"""---
layout: default
redirect_to: /{target_path}/
permalink: {redirect_url}
title: "{clean_path.upper()} (Redirecting...)"
nav_exclude: true
---

Redirecting to [/{target_path}/](/{target_path}/)...
"""

        # Ensure parent directory exists
        stub_path.parent.mkdir(parents=True, exist_ok=True)
        stub_path.write_text(content, encoding="utf-8")
        print(f"Created redirect stub: {stub_path} -> /{target_path}/")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        sys.stderr.write("usage: ensure_front_matter.py <root-dir>\n")
        return 2

    root = Path(argv[1]).resolve()
    project_title = os.environ.get("PROJECT_TITLE", root.name).strip() or root.name

    # Get redirects from environment (comma-separated list from shell script)
    redirects_env = os.environ.get("REDIRECTS", "").strip()
    redirects = (
        [r.strip() for r in redirects_env.split(",") if r.strip()]
        if redirects_env
        else []
    )

    hub = ensure_hub_index(root, project_title)

    for path in root.rglob("*"):
        process_page(root, hub, project_title, path)

    # Create redirect stubs if any redirects are specified
    if redirects:
        # Determine the target path relative to site root
        site_root = root.parent  # Go up from mounted directory to site root
        relative_mount = root.relative_to(site_root)
        create_redirect_stubs(redirects, str(relative_mount), site_root)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
