# IndusStream – Industrial Telemetry Platform

A hands-on project exploring how telemetry systems collect, process, and visualise data across edge and cloud environments.

The project evolves through progressively more advanced implementations, moving from simulation to real hardware and toward scalable cloud architectures.

## Projects

### [v1 – Serverless Telemetry](./v1-serverless-telemetry/)

Simulated telemetry data is sent to AWS via API Gateway, processed by Lambda, and stored in S3.

Focus:
- Serverless architecture
- Event-driven processing
- Cloud-native monitoring

### [v2 – Edge Dashboard](./v2-edge-dashboard/)

Real sensor data from an Arduino is collected and processed on a Raspberry Pi, stored locally in SQLite, and visualised via a Python Dash dashboard.

Focus:
- Edge computing
- Local data processing and storage
- Real-time visualisation over LAN

### v3 – Edge to Cloud (in progress)

Extending the system to stream data from edge devices to AWS using MQTT and IoT services.

Focus:
- IoT architecture
- Scalable data ingestion
- Cloud integration

## Stack

Python • Arduino • Raspberry Pi • SQLite • AWS • MQTT

## Goal

Simulation → Edge Systems → Cloud Integration

