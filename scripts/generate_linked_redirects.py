#!/usr/bin/env python3
"""
Generate redirect stub pages for linked projects.
Each page redirects to a GitHub Pages site and is nested under 'Projects > Linked Projects'.
"""

import json
from pathlib import Path

CONFIG = Path("sources.linked.json")
OUT_DIR = Path("docs/projects/linked")


def main():
    with CONFIG.open("r", encoding="utf-8") as f:
        data = json.load(f)

    projects = data.get("linked_projects", [])
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, proj in enumerate(projects, 1):
        name = proj["name"]
        title = proj.get("title", name)
        url = proj["url"]
        path = OUT_DIR / f"{name}.md"

        content = f"""---
layout: redirect
title: {title}
parent: Linked Projects
grand_parent: Projects
nav_order: {i}
redirect_to: {url}
---
"""

        path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"✔ Generated redirect: {path}")


if __name__ == "__main__":
    main()
