# IndusStream – Industrial Telemetry Platform

This project began as a learning exercise to understand how edge telemetry devices can collect, process, and send data to the cloud using AWS services.

Over time, it evolved into a series of progressively more advanced implementations, each exploring different aspects of system design. These are organised as separate versioned subprojects within this repository.

The projects are developed using hardware deployed in a home environment, including Arduino-based sensors and a Raspberry Pi acting as an edge compute device. This setup allows for practical experimentation with real-world data acquisition, processing, and system integration.

## Projects

### [v1 – Serverless Telemetry](./v1-serverless-telemetry/)

Simulated telemetry data is sent to AWS via API Gateway, processed by Lambda, and stored in S3, with monitoring through CloudWatch. This version explores a serverless architecture, where compute resources are managed and scaled automatically without provisioning servers.

### [v2 – Edge Dashboard](./v2-edge-dashboard/)

Real sensor data from an Arduino is collected and processed on a Raspberry Pi, stored locally in SQLite, and visualised through a Python Dash dashboard. This version focuses on edge computing, enabling local data processing, storage, and real-time monitoring without relying on cloud connectivity.

### v3 – Edge to Cloud (in progress)

Extending the system to stream data from edge devices to AWS using MQTT and IoT services.
Focus: Scalable IoT architecture

## Stack

Python • Arduino • Raspberry Pi • SQLite • AWS • MQTT

## Goal

Simulation → Edge Systems → Cloud Integration

