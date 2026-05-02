# v3 – Edge to Cloud

This version extends the system from local edge processing to a cloud-based telemetry pipeline using AWS IoT services.

Telemetry data is collected from Arduino-based sensors, processed at a Raspberry Pi edge gateway, and streamed to AWS using Message Queuing Telemetry Transport (MQTT).

---

## Architecture

![Architecture Diagram](docs/architecture.png)

---

## System Flow
Arduino Sensors --> Raspberry Pi (Edge Gateway) --> AWS IoT Core (MQTT) --> AWS Lambda --> Data Storage

---

## Overview

* Edge devices (Arduino sensors) generate telemetry data
* Raspberry Pi performs data collection, validation, and publishing
* AWS IoT Core handles secure Message Queuing Relemetry Transport (MQTT)
* AWS Lambda processes and routes incoming telemetry
* Data is stored for analysis and downstream use.

---
## Objectives

* Implement reliable edge-to-cloud telemetry streaming
* Use MQTT for lightweight, event-driven communication
* Build a scalable and cost-effective ingestion pipeline

---
## Implementation

Detailed implementation steps and configuration can be found here:

[Implementation](docs/implementation.md)
