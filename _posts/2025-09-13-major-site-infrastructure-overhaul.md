---
layout: post
title: "Site Infrastructure Overhaul"
date: 2025-09-13 22:55:00 -0400
categories: [infrastructure, documentation]
author: Cameron K. Brooks
---

Major updates to the FEASTorg website structure and design completed today.

## Changes Made

### Site Organization

- Moved content to `_pages/` directory with proper categorization
- Added structured navigation hierarchy:
  - Implementation Domains (BREADS, FROOTS, PROTINS, SUGIRS)
  - System Levels (SLICE, LOAF, BATCH, OVEN)
  - Development (guides and documentation)
  - Developer Resources (KiCad libraries and examples)

### Custom Styling

- Implemented FEAST brand color scheme (`_sass/color_schemes/feast.scss`)
- Added color scales for primary blue, accent orange, and growth green
- Updated typography and visual hierarchy

### Jekyll Configuration

- Enhanced `_config.yml` with automated layout assignments
- Added proper parent-child navigation relationships
- Configured SEO optimization and callout system

### Content Automation

- Rewrote `ensure_front_matter.py` script for imported repository content
- Script automatically generates proper Jekyll front matter
- Ensures imported projects nest correctly in navigation

### New Documentation

- Added getting-started guides (`getting-started/`)
- Created usage documentation (`usage/`)
- Added development section (`development/`)
- Expanded contributor resources

## Technical Details

The site now uses a complete color system:

```scss
$feast-primary-200: #1e4d6b; // Main blue
$feast-accent-100: #e67e22; // Orange
$feast-growth-100: #27ae60; // Green
```

Navigation automatically organizes imported GitHub repositories under appropriate parent sections.

## Migration Notes

- Some URLs changed due to reorganization
- Navigation dropdowns now work properly
- Mobile responsiveness improved

This establishes the foundation for FEAST project documentation and community resources.
