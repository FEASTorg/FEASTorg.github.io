---
layout: page
title: Naming Organization (Old)
permalink: /archive/naming-organization-old/
parent: Archive
nav_order: 3
---

## Layered Architecture

FEAST uses a layered approach where each layer provides services to the layer above it:

1. **Hardware Layer (BREADS)**: Physical devices, sensors, actuators, and mechanical interfaces
2. **Firmware Layer (FROOTS)**: Device control logic, real-time operations, and hardware abstraction
3. **Middleware Layer (PROTINS)**: Device orchestration, communication protocols, and runtime management
4. **Software Layer (SUGIRS)**: User interfaces, monitoring systems, and business logic

## Hierarchical Organization

Systems are organized hierarchically to manage complexity and enable scalability:

- **Module Level (SLICE)**: Single-function modules (e.g., temperature sensor, motor controller)
- **Device Level (LOAF)**: Local systems combining multiple SLICE modules to form a cohesive device (e.g., standalone machine, test bench)
- **System Level (BATCH)**: Coordinated groups of LOAF devices working together as an integrated system (e.g., production line, multi-station cell)
- **Facility Level (OVEN)**: Facility-wide networks of BATCH systems (e.g., entire factory, campus)
