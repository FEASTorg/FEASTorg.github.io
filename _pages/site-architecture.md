---
layout: page
title: Site Architecture
permalink: /site-architecture/
nav_order: 12
---

## Overview

FEASTorg uses a hybrid Jekyll architecture that combines automated content import from across multiple repositories with centralized presentation and search. This is designed to balance site quality, maintainability, performance, and workflow efficiency.

## Technical Stack

**Core**: Jekyll 4.4+ with Just the Docs v0.10.1, Ruby 3.3, GitHub Pages  
**Plugins**: SEO-tag, feed, relative-links, redirect-from, include-cache

## Content Architecture

### Hub Repository Structure

- **`_pages/`**: Hand-maintained core documentation
- **`getting-started/`, `usage/`**: Organized guide collections
- **`_posts/`**: Project updates and announcements
- **Auto-imported content**: collection of repositories via `_data/sources.json`

### Automated Import System

**Process**: Daily automated import via `scripts/import_sources.sh`

1. Sparse Git cloning (docs subdirectories only)
2. Intelligent filtering (global + per-repo `.indexignore`)
3. Front matter normalization for navigation hierarchy
4. URL redirect management

### Linked Projects Architecture

Some projects maintain standalone GitHub Pages sites but are linked through the hub due to complex CI/CD requirements. For example, hardware projects have their own build pipeline using [bread-infra](https://github.com/FEASTorg/bread-infra), or the Freeboard Project, which has its own CI/CD setup using auto-generated developer API reference and component documentation from monorepo packages, published via VuePress and GitHub Actions.

These are managed via `_data/linked_projects.json` and automatically generate redirect stub pages.

## Navigation & Styling

**Structure**: Just the Docs hierarchical parent-child system with automated layout assignment via `_config.yml` defaults

**Branding**: Custom FEAST color system (`_sass/custom/tokens.scss`) with:

- Primary blues (engineering theme)
- Accent oranges (harvest/warmth)
- Growth greens (automation/nature)
- Neutral grays (surfaces)

## Build Pipeline

**Triggers**: Push to main, daily at 23:11 EST, manual dispatch  
**Process**: Environment setup → Content import → Stub generation → Jekyll build → Deploy

**Features**:

- Daily sync keeps external content current
- Full-text search across all imported content
- Smart tokenization for hyphenated terms
- Pretty URLs with redirect management
- Performance optimizations (sparse cloning, asset optimization, CDN)

## Using Jekyll Features

Callout examples:

{: .note }
This project is under heavy development

{: .new }

> A paragraph
>
> Another paragraph
>
> The last paragraph
