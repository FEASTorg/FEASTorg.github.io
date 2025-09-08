#!/usr/bin/env python3
import os
import pathlib
import re
import sys
import yaml

root = pathlib.Path(sys.argv[1]).resolve()
project = os.environ.get("PROJECT_TITLE", root.name).strip()
md_exts = {".md", ".markdown"}

# Capture ONLY the YAML between the delimiters
fm_re = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def split_fm(text: str):
    m = fm_re.match(text)
    if not m:
        return {}, text
    yaml_str = m.group(1)
    try:
        data = yaml.safe_load(yaml_str) or {}
    except Exception:
        data = {}
    return data, text[m.end() :]


def dump_fm(data: dict, body: str) -> str:
    return f"---\n{yaml.safe_dump(data, sort_keys=False)}---\n\n{body}"


def first_h1(body: str):
    for ln in body.splitlines():
        m = re.match(r"^\s{0,3}#\s+(.+?)\s*$", ln)
        if m:
            return m.group(1).strip()


# 1) Ensure hub index exists and is a section page with canonical title
hub = root / "index.md"
if hub.exists():
    txt = hub.read_text(encoding="utf-8", errors="ignore")
    fm, body = split_fm(txt)
else:
    fm, body = {}, f"# {project}\n\n"

fm["layout"] = fm.get("layout") or "default"
fm["title"] = project  # force exact title for parent matching
fm["has_children"] = True
fm.pop("parent", None)  # hub must not be a child
fm.pop("grand_parent", None)
hub.write_text(dump_fm(fm, body), encoding="utf-8")

# 2) Walk pages and assign grouping
for p in root.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in md_exts:
        continue
    if p.samefile(hub):
        continue

    txt = p.read_text(encoding="utf-8", errors="ignore")
    fm, body = split_fm(txt)
    fm.setdefault("layout", "default")
    fm["title"] = (
        fm.get("title")
        or first_h1(body)
        or p.stem.replace("_", " ").replace("-", " ").title()
    )

    rel = p.relative_to(root)
    if rel.parent == pathlib.Path("."):
        # direct child of hub
        fm.setdefault("parent", project)
    else:
        # section handling
        section = rel.parts[0].replace("_", " ").replace("-", " ").title()
        sec_index = root / rel.parts[0] / "index.md"

        if sec_index.exists():
            s_txt = sec_index.read_text(encoding="utf-8", errors="ignore")
            s_fm, s_body = split_fm(s_txt)
        else:
            s_fm, s_body = {}, f"# {section}\n\n"

        s_fm["layout"] = s_fm.get("layout") or "default"
        s_fm["title"] = section  # force exact section title
        s_fm["has_children"] = True
        s_fm["parent"] = project  # ensure linked to hub
        sec_index.write_text(dump_fm(s_fm, s_body), encoding="utf-8")

        if p.name != "index.md":
            fm.setdefault("grand_parent", project)
            fm.setdefault("parent", section)

    # Hide README when an index exists in same dir
    if p.name.lower() == "readme.md" and (p.parent / "index.md").exists():
        fm["nav_exclude"] = True

    p.write_text(dump_fm(fm, body), encoding="utf-8")
