# Definitions

FEAST: Flexible and Expandable Automation System Technology

## Hierarchical Abstraction Levels

- **SLICE**

  - Each PCB performs a single function
  - This is referred to as a **SLICE** which stands for _Single-function Logic Interface & Controller Element_
  - It has at minimum some onboard controller (processing) and logic (communication) interface along with supporting circuitry (function)
  - **Example:** A temperature sensor PCB with an I2C capable MCU that reads temperature data and applies a control signal to a power switch.

- **LOAF**

  - Multiple SLICEs can be connected to create a system via a shared communication and power bus with a designated leader to create a system from number of function cards to perform some discrete process
  - This is referred to as a **LOAF** which stands for _Locally Operated Automation Framework_
  - **Example:** A small system that made up of XXXXXXXXXXXXXXXXXXXXXXX to coordinate their functions for a localized process—e.g., a temperature controller, motor controller, and pH sensor working together to run a bioreactor.

- **BATCH**

  - Multiple LOAF subsystems can be connected to a (micro)computer via interfacing with the leader SLICE of each LOAF to aggregate and coordinate multiple processes to perform some abstract process and connect to a wider network
  - This is referred to as **BATCH** which stands for _Bridged Architecture for Task Control & Handling_
  - **Example:** A microcomputer managing multiple LOAFs (e.g., one for a mechanical shredder, one for a chemical reactor, and one for a bioreactor,) to create a plastic upcycling system that converts PET waste into edible microbial protein.

- **OVEN**

  - Multiple (micro)computers can be networked in a leader-worker configuration to achieve some business / organizational goal
  - This is referred to as **OVEN** which stands for _Orchestrated Versatile Embedded Network_
  - **Example:** A distributed recycling and manufacturing system where multiple microcomputers, each managing different BATCH nodes (e.g., plastic upcycling, intermediate conveyor systems, and quality control sensors), coordinate through a central server to optimize production.

## Functional Implementation Domains

- **BREADS**: Broadly Expandable and Reconfigurable Data Acquisition and Automation Device Standard

  - Pronounced like "breads"
  - Defines **hardware** standard for FEAST-compatible devices
  - Specifies mechanical form factor and connector pinout
  - Defines power distribution and signal bus conventions
  - Supports scalable, stackable, and distributed systems

  - Planned implementations:
    - SLICE function cards
      - Single-function Logic Interface Controller Element
    - CRUST interface bridges
      - Configurable Routing & Universal Signal Translator
    - LOAF backplanes
      - Local Operations Attachment Frame

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

- **PROTNS**: Programmable Runtime Orchestration & Transport Node Supervisor

  - Pronounced like "proteins"
  - Provides **middleware** to provide drivers and runtime environment for orchestrating interfacing with FROOTS devices
  - Manages configuration, data logging, and control loops
  - Compatible with embedded Linux, PLCs, or microcontrollers

  - Planned implementations:
    - PEA-LC python software for makers and scientists
      - Python Environment for Automation and Logic Control
    - OpenPLC drivers for industrial support

- **SUGIRS**: System User Graphical Interface & Remote Scheduling

  - Pronounced like "sugars"
  - Provides the **software** (front-end) user interface layer for monitoring, control, and scheduling
  - Supports dashboards, web UIs, SCADA, and scripting
  - Enables remote scheduling and manual overrides
  - Abstracts system internals for end-user interaction

  - Planned implementations:
    - FreeBoard configs for makers and scientists
    - ScadaBR for industrial support

**_Future..._**

- **VEGIES**: Versatile External Gear, Interfaces, and Experimental Subsystems

  - Pronounced like "veggies"
  - Refers to **off-board, user-fabricated hardware** that can be used in BREADS-compatible systems
  - Includes sensors, actuators, and tools made or modified by users (e.g., DIY sensors and actuators, additive or other digitally manufactured parts, hacked devices and components)

  - Ideas for implementations:
    - Handmade thermocouples
    - DIY pH/ORP/EC probes
    - DIY optical turbidity sensors using LED + photodiode in 3D printed holder
    - Capacitive soil moisture sensors with etched foil or PCB traces
    - Printed or milled strain gauge structures
    - Homemade load cells using strain gauges on flexures
    - Thermistor or RTD sensor assemblies in waterproof housings
    - 3D-printed linear actuators with screw drives or sliders
    - DIY stepper or brushed motors from recycled components
    - Custom solenoid valves with 3D printed bodies
    - Servo/solenoid-driven micro-dispensers for fluids or reagents
    - Magnetic stirrers or vibratory actuators with scrap coils
    - Modular sensor mounts and probe holders (3D printed)
    - Custom wire harnesses, pogo-pin adapters, breakout jigs
    - Printable mechanical positioning systems for probe insertion
    - Environmental test enclosures with integrated sensing (e.g. temp/humidity)
    - Electrochemical cells with swappable electrodes using common components
    - Low-cost microfluidic chips cut from acrylic or molded in PDMS
    - DIY cuvettes or optical measurement paths for colorimetry
    - Textile-based biosensors or conductive gel patches for touch/contact sensing
