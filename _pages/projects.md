---
layout: page
title: Projects
permalink: /projects/
nav_order: 6
has_children: true
---

## FEAST Projects

The FEAST ecosystem consists of several project repositories that provide tools, resources, and implementations in support of our broader automation framework. Projects rendered directly on this site are accessible through the left-hand navigation menu.

Additional project pages, hosted standalone, can be accessed via their corresponding GitHub Pages sites:

{% for project in site.data.linked_projects.linked_projects %}
- [{{ project.title }}]({{ project.url }})
{% endfor %}
