---
layout: page
title: Site Architecture
permalink: /site-architecture/
nav_order: 13
---

## Overview

The FEASTorg documentation is organized using a hybrid approach that balances searchability, maintainability, and CI/CD complexity.

## Technical Foundation

This site is built using [Jekyll](https://jekyllrb.com/), a static site generator that transforms plain text into static websites. Key technical components include:

- **Theme**: Using [Just the Docs](https://just-the-docs.github.io/just-the-docs/) theme for enhanced documentation features
- **Source Control**: All source code is maintained on [GitHub](https://github.com/FEASTorg)
- **Hosting**: Deployed via GitHub Pages at [feastorg.github.io](https://feastorg.github.io)

### Developer Resources

For contributors working on site improvements:

- Jekyll Documentation: [jekyllrb.com](https://jekyllrb.com/)
- GitHub Pages Guide: [pages.github.com](https://pages.github.com/)
- Just the Docs Theme: [just-the-docs.github.io](https://just-the-docs.github.io/just-the-docs/)

## Site Structure

### Main Documentation Repository

- This repository (`FEASTorg.github.io`) serves as the primary documentation hub
- Built as a monolithic site using Jekyll
- Features integrated search functionality
- Contains core documentation, guides, and project overviews

### Site Filtering

- `source.json` exclude: Hub-level filtering to enforce policy and catch missing, .indexignore in each repo does per-repo filtering

### Externally Generated Sites

Some documentation is intentionally maintained in separate repositories for the following reasons:

- To prevent search result pollution from repetitive content
- To maintain specialized CI/CD workflows
- To handle complex development documentation separately

These include:

- **Slice_XXXX pages**: Documentation for individual SLICE implementations
- **freeboard**: Development documentation with its own monorepo structure

### Documentation Integration Strategy

- Core documentation is pulled into this repository for unified access
- External documentation maintains independent build processes
- This approach ensures:
  - Efficient search functionality
  - Streamlined maintenance
  - Optimal performance
  - Separation of concerns where beneficial
