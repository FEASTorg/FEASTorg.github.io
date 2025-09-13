---
layout: post
title: "Reusable KiBot → Pages slice pipeline MVP rolls out!"
date: 2025-09-07 17:18:45 -0400
categories: development
author: Cameron K. Brooks
---

We now have a **reusable CI/CD pipeline** for KiCad boards that builds with **KiBot**, generates a Markdown index, and deploys to **GitHub Pages**—all centralized in **[`FEASTorg/slice-infra`](https://github.com/FEASTorg/slice-infra)**. First trials complete and working at: **[`FEASTorg/Slice_DCMT`](https://feastorg.github.io/Slice_DCMT)** and **[`FEASTorg/Slice_TEMP`](https://feastorg.github.io/Slice_TEMP)**.

### What has shipped?

- Reusable workflows in `slice-infra`:
  - `kibot-ci.yml` – runs ERC/DRC and fabricates artifacts.
  - `publish-kibot.yml` – resolves artifacts (incl. iBOM variants), writes `docs/kibot/index.md`, commits.
  - `deploy-pages.yml` – stages selected outputs and deploys Jekyll site.
- Example Pages:
  - Slice_DCMT: `https://feastorg.github.io/Slice_DCMT/kibot/`
  - Slice_TEMP: `https://feastorg.github.io/Slice_TEMP/kibot/`

### How to consume (in a slice repo)

Create `.github/workflows/docs-pipeline.yml`:

```yml
name: Docs Pipeline

on:
  push:
    branches: [main]
    paths:
      - "hardware/**"
      - "docs/**"
      - ".github/workflows/**"
  workflow_dispatch:

jobs:
  kibot:
    uses: FEASTorg/slice-infra/.github/workflows/kibot-ci.yml@main

  gen-kibot-index:
    uses: FEASTorg/slice-infra/.github/workflows/publish-kibot.yml@main
    needs: [kibot]
    with:
      kibot_run_id: ${{ needs.kibot.outputs.kibot_run_id }}

  deploy-pages:
    uses: FEASTorg/slice-infra/.github/workflows/deploy-pages.yml@main
    needs: [gen-kibot-index]
    with:
      kibot_run_id: ${{ needs.kibot.outputs.kibot_run_id }}
      commit_sha: ${{ needs.gen-kibot-index.outputs.kibot_index_sha }}
```

### Required files in the slice repo

- `hardware/config.kibot.yaml` (your KiBot recipe).

- `hardware/Makefile` (KiBot Make commands)

- `docs/_config.yml` (Jekyll).

- `docs/kibot/config.kibot.site.yml` (e.g.):

```yml
project_name: "Slice Foo"
artifacts:
  - Schematic.pdf
  - PCB.pdf
  - kibot.log
  - BoM/*.html # picks up bom + ibom
images:
  - board_top.png
  - board_bottom.png
```

- `docs/kibot/index_template.md` to customize the index.

- The standard documentation files in `docs/` including:
  - `architecture.md`
  - `changelog.md`
  - `testing.md`
  - `index.md`

### Notes

- iBOM filenames vary; the publisher handles `*_iBoM.html` / `*ibom.html` and case differences.
- We generate **Markdown only** and let Jekyll render—no `.nojekyll` needed.
- Pages deploy stages only the configured artifact patterns into `docs/kibot/`.

### Next

Rolling this out to the rest of the slices is now a copy-paste of the workflow and a small `config.kibot.site.yml`...stay tuned!
