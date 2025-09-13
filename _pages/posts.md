---
layout: default
title: Posts
permalink: /posts/
nav_order: 3
---

Below are our posts and announcements.

{% for post in site.posts %}

- [{{ post.title }}]({{ post.url }}) — {{ post.date | date: "%Y-%m-%d" }}

{% endfor %}
