# 06 – Data Lake and Query Layer (S3 + Athena)

This stage introduces a scalable analytics layer using Amazon S3 and Amazon Athena.

While DynamoDB serves as the operational data store for real-time ingestion, Amazon S3 is used as a data lake for long-term storage and analytical workloads.

---

## 6.1 Amazon S3 (Data Lake)

DynamoDB data was initially exported to Amazon S3 to validate archival and data lake integration capabilities.

This confirmed that operational telemetry data can be offloaded for long-term storage.

However, the native export format (Amazon Ion) is not optimised for analytics workloads and can lead to parsing issues when queried using Athena.

---

### Limitation of DynamoDB Export

The exported dataset uses Amazon Ion format, which introduces:

* Nested structures
* Type annotations (e.g. `N`, `S`)
* Compatibility challenges with Athena queries

As a result, this format is suitable for archival purposes but not ideal for analytics or dashboarding.

---

### Analytics Dataset (Lambda → S3)

To address this limitation, the Lambda function was extended to write a separate, flattened JSON dataset directly to S3.

Each telemetry event is transformed into an analytics-friendly structure before being stored.

Example structure:

```json
{
  "device_id": "raspberry-pi-edge-gateway",
  "timestamp": "2026-05-04T12:44:44Z",
  "temperature_c": 28.84,
  "co_raw": 279,
  "light_raw": 36,
  "sound_raw": 12,
  "light_state": "dark",
  "sound_event": false
}
```
### Partitioning Strategy

Data is stored using a date-based partitioning scheme:

```text
analytics/year=YYYY/month=MM/day=DD/
```

This improves query performance and reduces cost when using Athena.

## 6.2 Data Flow
Lambda → S3 → Athena → QuickSight

This pipeline enables:

* Serverless querying using Athena
* Efficient access to large datasets
* Integration with visualisation tools

## 6.3 Analytics Data Strategy

Two data paths are maintained:

* DynamoDB – Operational store for real-time ingestion and recent telemetry access
* S3 (JSON) – Analytics store for Athena and QuickSight

This separation ensures:

* Low-latency access for operational workloads
* Scalable and cost-efficient storage for analytics
* Clean data structures optimised for querying

## 6.4 Athena Query Layer

Amazon Athena is used to query telemetry data stored in S3 using standard SQL.

Key capabilities include:

* Serverless querying (no infrastructure required)
* Direct integration with S3
* Seamless connection to QuickSight

Athena enables efficient analysis of telemetry data without impacting the operational DynamoDB workload.

Notes

Due to the architecture (S3 → Athena), this layer supports near-real-time analytics rather than real-time processing. Data availability depends on S3 write timing and Athena query execution.