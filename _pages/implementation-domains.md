---
layout: page
title: Functional Implementation Domains
permalink: /implementation-domains/
nav_order: 7
has_children: true
---

Currently, FEAST defines several **functional implementation domains** to organize its architecture and development. These domains include:

### Functional Implementation Domains

- [BREADS](/breads/)

  **Broadly Expandable and Reconfigurable Data Acquisition and Automation Device Standard** or _"breads"_ encompasses the hardware domain. It defines the electromechanical specifications for compatible hardware. Implementations include: SLICE function cards CRUST interface bridges, and LOAF controllers & backplanes.

- [FROOTS](/froots/)

  **Firmware for Resilient, (Function-)Oriented Operation of Things Specification** or _"fruits"_ encompasses the firmware domain. It defines standardized logic, interfaces and modules for hardware operation.

- [PROTINS](/protins/)

  **Programmable Runtime Orchestration and Transport Interfaces for Node Supervision** or _"proteins"_ encompasses the middleware domain. It provides runtime orchestration, device management, and modular drivers to bridge the gap between device firmware and user-defined software.

- [SUGIRS](/sugirs/)

  **System User Graphical Interface and Remote Scheduling** or _"sugars"_ encompasses the software/interface domain. It's purpose is enabling user interaction, system monitoring, control interfaces, and remote scheduling.

### Future Domains

- [VEGIES](/vegies-concept/)

  **Versatile External Gear, Interfaces, and Experimental Subsystems** or _"vegies"_ is a conceptual framework for user-fabricated hardware that can integrate with BREADS-compatible systems. This includes DIY sensors, actuators, and tools made through various fabrication methods like 3D printing, digital manufacturing, and component modification. Conceptually, these are used by the BREADS hardware domain and would be considered as "below" BREADS in the hierarchy (VEGIES -> BREADS -> FROOTS -> PROTINS -> SUGIRS).
