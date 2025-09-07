#!/usr/bin/env python3
import sys, re, pathlib

root = pathlib.Path(sys.argv[1]).resolve()

md_exts = {".md", ".markdown"}
fm_re = re.compile(r"^---\s*\n", re.M)


def title_from_h(content: str) -> str:
    for line in content.splitlines():
        m = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    # fallback to filename
    return None


for p in root.rglob("*"):
    if p.is_file() and p.suffix.lower() in md_exts:
        text = p.read_text(encoding="utf-8", errors="ignore")
        if fm_re.match(text):
            continue
        title = title_from_h(text) or p.stem.replace("_", " ").replace("-", " ").title()
        fm = f"---\nlayout: default\ntitle: {title}\n---\n\n"
        p.write_text(fm + text, encoding="utf-8")
