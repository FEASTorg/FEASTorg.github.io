---
layout: default
title: Archives
permalink: /archives/
---

# Archives

Below are the site posts and announcements.

{% raw %}
{% for post in site.posts %}

- [{{ post.title }}]({{ post.url }}) — {{ post.date | date: "%Y-%m-%d" }}
  {% endfor %}
  {% endraw %}
