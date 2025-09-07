---
layout: home
title: Home
nav_order: 1
---

## Overview

_**FEAST:** Flexible and Expandable Automation System Technology_

### Supporting Resources & Tools

- [KiCad-Master-Lib](/KiCad-Master-Lib/)

  **KiCad-Master-Lib** is a centralized and curated library of schematic symbols, PCB footprints, and 3D models for use with KiCad.

- [KiCad-Hierarchical-Designs](/KiCad-Hierarchical-Designs/)

  **KiCad-Hierarchical-Designs** provides reference designs demonstrating best practices for hierarchical schematic structures and modular PCB design in KiCad.

- [KiCad-Simulation-Examples](/KiCad-Simulation-Examples/)

  **KiCad-Simulation-Examples** is a collection of simulation-ready examples and tutorials for circuit validation and analysis using KiCad’s integrated simulation features.

- [KNEEAD](/KNEEAD/)

  **Knowledge for Navigating Electrical & Electronic Architecture and Design** or _"knead"_ is a comprehensive knowledge base featuring hardware guidelines, best practices, review checklists, design conventions, hardware patterns, architectural principles, and supporting tools such as Python-powered calculators & JupyterLite demos.

### Functional Implementation Domains

- [BREADS](/BREADS/)

  **Broadly Expandable and Reconfigurable Data Acquisition and Automation Device Standard** or _"breads"_ encompasses the hardware domain. It defines the electromechanical specifications for compatible hardware. Implementations include: SLICE function cards CRUST interface bridges, and LOAF controllers & backplanes.

- [FROOTS](/FROOTS/)

  **Firmware for Resilient, (Function-)Oriented Operation of Things Specification** or _"fruits"_ encompasses the firmware domain. It defines standardized logic, interfaces and modules for hardware operation.

- [PROTINS](/PROTINS/)

  **Programmable Runtime Orchestration and Transport Interfaces for Node Supervision** or _"proteins"_ encompasses the middleware domain. It provides runtime orchestration, device management, and modular drivers to bridge the gap between device firmware and user-defined software.

- [SUGIRS](/SUGIRS/)

  **System User Graphical Interface and Remote Scheduling** or _"sugars"_ encompasses the software/interface domain. It's purpose is enabling user interaction, system monitoring, control interfaces, and remote scheduling.

### Hierarchical System Levels

- [SLICE](/SLICE/)

  **Single-function Logic Interface & Controller Element** or _"slice"_ implements the BREAD standard (BREADS). Single-function boards with onboard processing and communication capabilities. CRUST interfaces can be used to adapt non-SLICE devices into ones that SLICE compliant with BREAD.

- [LOAF](/LOAF/)

  **Locally Operated Automation Framework** or _"loaf"_ implements the BREAD standard (BREADS) for controllers and corresponding bus infrastructure. Controller and shared communication & power bus to connect multiple SLICEs and coordinate their functions to perform a localized process.

- [BATCH](/BATCH/)

  **Bridged Architecture for Task Control & Handling** or _"batch"_ represents the coordination of multiple LOAFs in a leader-follower configuration. In this clustered configuration one LOAF is designated the leader to manage the coordination of multiple (follower) LOAF systems to perform complex or distributed processes.

- [OVEN](/OVEN/)

  **Orchestrated Versatile Embedded Network** or _"oven"_ represents the aggregation and coordination of one or more BATCH clusters. Networks multiple BATCH-level systems to a central server for high-level management and monitoring of production scheduling, historical archiving, and facility alerts to achieve broader organizational or operational goals.

### Miscellaneous Concepts

- [VEGIES](/vegies-concept/)

  **Versatile External Gear, Interfaces, and Experimental Subsystems** or _"vegies"_ is a conceptual framework for user-fabricated hardware that can integrate with BREADS-compatible systems. This includes DIY sensors, actuators, and tools made through various fabrication methods like 3D printing, digital manufacturing, and component modification.
