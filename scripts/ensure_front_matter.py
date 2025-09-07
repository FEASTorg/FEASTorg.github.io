#!/usr/bin/env python3
import os, sys, re, pathlib, yaml

root = pathlib.Path(sys.argv[1]).resolve()
project = os.environ.get("PROJECT_TITLE", root.name).strip()
md = {".md", ".markdown"}
fm_re = re.compile(r"^---\s*\n.*?\n---\s*\n", re.S)


def split_fm(t):
    m = fm_re.match(t)
    return (yaml.safe_load(m.group(0)) or {}, t[m.end() :]) if m else ({}, t)


def dump_fm(d, body):
    return f"---\n{yaml.safe_dump(d, sort_keys=False)}---\n\n{body}"


def h1(body):
    for ln in body.splitlines():
        m = re.match(r"^\s{0,3}#\s+(.+?)\s*$", ln)
        if m:
            return m.group(1).strip()


# Parent landing page
hub = root / "index.md"
if not hub.exists():
    hub.write_text(
        f"---\nlayout: default\ntitle: {project}\nnav_order: 20\nhas_children: true\npermalink: /{root.relative_to(root.parents[list(root.parts).index('projects')]).as_posix()}/\n---\n",
        encoding="utf-8",
    )

for p in root.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in md:
        continue
    if p.samefile(hub):  # ensure hub stays a section
        fm, body = split_fm(p.read_text(encoding="utf-8", errors="ignore"))
        fm["has_children"] = True
        p.write_text(dump_fm(fm, body), encoding="utf-8")
        continue

    txt = p.read_text(encoding="utf-8", errors="ignore")
    fm, body = split_fm(txt)
    fm.setdefault("layout", "default")
    fm["title"] = (
        fm.get("title")
        or h1(body)
        or p.stem.replace("_", " ").replace("-", " ").title()
    )

    rel = p.relative_to(root)
    if rel.parent == pathlib.Path("."):
        fm.setdefault("parent", project)
    else:
        sec = rel.parts[0].replace("_", " ").replace("-", " ").title()
        sec_index = p.parents[0] / "index.md"
        if not sec_index.exists():
            sec_index.write_text(
                f"---\nlayout: default\ntitle: {sec}\nhas_children: true\nparent: {project}\n---\n",
                encoding="utf-8",
            )
        fm.setdefault("grand_parent", project)
        fm.setdefault("parent", sec)

    if p.name.lower() == "readme.md" and (p.parent / "index.md").exists():
        fm["nav_exclude"] = True

    p.write_text(dump_fm(fm, body), encoding="utf-8")
