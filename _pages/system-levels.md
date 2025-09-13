---
layout: page
title: System Levels
permalink: /system-levels/
nav_order: 8
has_children: true
---

## Hierarchical System Levels

Currently, FEAST defines several **hierarchical system levels** to organize its architecture and functionality. These levels include:

- [SLICE](/slice/)

  **Single-function Logic Interface & Controller Element** or _"slice"_ implements the BREAD standard (BREADS). Single-function boards with onboard processing and communication capabilities. CRUST interfaces can be used to adapt non-SLICE devices into ones that SLICE compliant with BREAD.

- [LOAF](/loaf/)

  **Locally Operated Automation Framework** or _"loaf"_ implements the BREAD standard (BREADS) for controllers and corresponding bus infrastructure. Controller and shared communication & power bus to connect multiple SLICEs and coordinate their functions to perform a localized process.

- [BATCH](/batch/)

  **Bridged Architecture for Task Control & Handling** or _"batch"_ represents the coordination of multiple LOAFs in a leader-follower configuration. In this clustered configuration one LOAF is designated the leader to manage the coordination of multiple (follower) LOAF systems to perform complex or distributed processes.

- [OVEN](/oven/)

  **Orchestrated Versatile Embedded Network** or _"oven"_ represents the aggregation and coordination of one or more BATCH clusters. Networks multiple BATCH-level systems to a central server for high-level management and monitoring of production scheduling, historical archiving, and facility alerts to achieve broader organizational or operational goals.
