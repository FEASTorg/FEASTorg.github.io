#!/usr/bin/env python3
"""
Generate redirect stub pages for linked projects.
Canonical pages are generated under projects/linked, with legacy redirects
preserved under docs/projects/linked for backward compatibility.
"""

import json
from pathlib import Path

CONFIG = Path("_data/linked_projects.json")
CANONICAL_OUT_DIR = Path("projects/linked")
LEGACY_OUT_DIR = Path("docs/projects/linked")


def main():
    with CONFIG.open("r", encoding="utf-8") as f:
        data = json.load(f)

    projects = data.get("linked_projects", [])
    CANONICAL_OUT_DIR.mkdir(parents=True, exist_ok=True)
    LEGACY_OUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, proj in enumerate(projects, 1):
        name = proj["name"]
        title = proj.get("title", name)
        url = proj["url"]
        canonical_path = CANONICAL_OUT_DIR / f"{name}.md"
        legacy_path = LEGACY_OUT_DIR / f"{name}.md"

        canonical_content = f"""---
layout: redirect
title: {title}
parent: "Linked Projects 🔗"
grand_parent: Projects
nav_order: {i}
redirect_to: {url}
---
"""
        legacy_content = f"""---
layout: redirect
title: {title}
nav_exclude: true
redirect_to: {url}
---
"""

        canonical_path.write_text(canonical_content.strip() + "\n", encoding="utf-8")
        legacy_path.write_text(legacy_content.strip() + "\n", encoding="utf-8")
        print(f"Generated redirect: {canonical_path}")
        print(f"Generated legacy redirect: {legacy_path}")


if __name__ == "__main__":
    main()
