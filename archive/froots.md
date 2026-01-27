---
layout: page
title: FROOTS Concept
permalink: /archive/froots/
parent: Archive
nav_order: 4
---

## FROOTS Concept

FROOTS is a modular firmware base/template designed for single-function embedded devices that:

- 🔧 **Perform a dedicated control task** (e.g., temperature regulation, motor control).
- 🧠 **Execute all logic locally**, maintaining autonomy and robustness.
- 🔄 **Accept optional supervisor commands** for configuration or coordination.
- 🛡️ **Continue safe, deterministic operation** even if the supervisor becomes unavailable.
- ⏱️ **Support scheduled or profiled behavior**, such as ramping temperature or timed sequences.
- 🤝 **Enable distributed deployment**, where each device operates independently or as part of a networked system.
- 🔌 **Respond appropriately to supervision loss**, using fallback behaviors or hold-states rather than failing unsafely.

- **FROOTS**: Firmware for Resilient, (Function-)Oriented Operation of Things Specification
  - Pronounced like "fruits"
  - Defines **firmware** standard for BREADS to create FEAST-compliant devices
  - Standardized communication over I²C, SPI, UART, etc.
  - Modular driver model for sensors and actuators
  - Lightweight, MCU-agnostic state-based control framework

  - Planned implementations:
    - SPREAD firmware for SLICEs
      - Standardized PRogram for Expandable Automation Devices
    - JUICE firmware for CRUST
      - Joint Utility Interface for Control & Expansion
