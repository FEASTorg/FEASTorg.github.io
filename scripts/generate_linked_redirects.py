#!/usr/bin/env python3
"""
Generate redirect stub pages for linked projects.

Behavior:
- Create or update canonical redirects under `projects/linked`.
- Create or update legacy redirects under `docs/projects/linked`.
- Remove stale `.md` files in those directories that are no longer configured.
"""

from __future__ import annotations

import json
from pathlib import Path

CONFIG = Path("_data/linked_projects.json")
CANONICAL_OUT_DIR = Path("projects/linked")
LEGACY_OUT_DIR = Path("docs/projects/linked")


def yaml_string(value: str) -> str:
    """Return a YAML-safe scalar using JSON quoting (valid YAML)."""
    return json.dumps(value, ensure_ascii=False)


def render_front_matter(lines: list[str]) -> str:
    return "---\n" + "\n".join(lines) + "\n---\n"


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return False
    path.write_text(content, encoding="utf-8")
    return True


def remove_stale_files(out_dir: Path, keep_filenames: set[str]) -> list[Path]:
    removed: list[Path] = []
    for path in out_dir.glob("*.md"):
        if path.name not in keep_filenames:
            path.unlink()
            removed.append(path)
    return removed


def main() -> None:
    with CONFIG.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    projects = data.get("linked_projects", [])

    CANONICAL_OUT_DIR.mkdir(parents=True, exist_ok=True)
    LEGACY_OUT_DIR.mkdir(parents=True, exist_ok=True)

    seen_names: set[str] = set()
    canonical_keep: set[str] = set()
    legacy_keep: set[str] = set()

    for index, project in enumerate(projects, 1):
        if not isinstance(project, dict):
            raise TypeError(f"linked_projects[{index - 1}] must be an object")

        raw_name = project.get("name")
        name = str(raw_name).strip() if raw_name is not None else ""
        if not name:
            raise ValueError("Each linked project must define a non-empty 'name'.")
        if Path(name).name != name or name in {".", ".."}:
            raise ValueError(
                f"Linked project '{name}' has an invalid name; use a simple file-safe slug."
            )
        if name in seen_names:
            raise ValueError(f"Duplicate linked project name: {name}")
        seen_names.add(name)

        raw_title = project.get("title")
        title = str(raw_title).strip() if raw_title is not None else name
        if not title:
            title = name

        raw_url = project.get("url")
        url = str(raw_url).strip() if raw_url is not None else ""
        if not url:
            raise ValueError(f"Linked project '{name}' is missing required 'url'.")

        filename = f"{name}.md"
        canonical_keep.add(filename)
        legacy_keep.add(filename)

        canonical_path = CANONICAL_OUT_DIR / filename
        legacy_path = LEGACY_OUT_DIR / filename

        canonical_content = render_front_matter(
            [
                "layout: redirect",
                f"title: {yaml_string(title)}",
                f'parent: {yaml_string("Linked Projects 🔗")}',
                "grand_parent: Projects",
                f"nav_order: {index}",
                f"redirect_to: {yaml_string(url)}",
            ]
        )
        legacy_content = render_front_matter(
            [
                "layout: redirect",
                f"title: {yaml_string(title)}",
                "nav_exclude: true",
                f"redirect_to: {yaml_string(url)}",
            ]
        )

        if write_if_changed(canonical_path, canonical_content):
            print(f"Generated redirect: {canonical_path}")
        if write_if_changed(legacy_path, legacy_content):
            print(f"Generated legacy redirect: {legacy_path}")

    for removed_path in remove_stale_files(CANONICAL_OUT_DIR, canonical_keep):
        print(f"Removed stale redirect: {removed_path}")
    for removed_path in remove_stale_files(LEGACY_OUT_DIR, legacy_keep):
        print(f"Removed stale legacy redirect: {removed_path}")


if __name__ == "__main__":
    main()
