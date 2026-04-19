## Use Cases

### Primary Use Case: Telemetry ingestion from an industrial edge device

A simulated industrial edge device generates telemetry data such as temperature, pressure, and operating status. The device sends this telemetry securely to AWS for central collection.

**Goal:**
Provide a simple and scalable way to ingest machine telemetry into the cloud.

**Actors:**

* Edge device (Python simulator)
* AWS ingestion platform

**Outcome:**
Telemetry is received, validated, and stored in a structured format for later use.

---

### Secondary Use Case: Central storage of raw telemetry data

An engineer or operations team needs raw telemetry data stored centrally so that it can later be analysed for performance trends, fault investigation, or predictive maintenance.

**Goal:**
Store telemetry in a structured, durable, and low-cost format.

**Actors:**

* AWS telemetry platform## Use Cases

### Primary Use Case: Telemetry ingestion from an industrial edge device

A simulated industrial edge device generates telemetry data such as temperature, pressure, and operating status. The device sends this telemetry securely to AWS for central collection.

**Goal:**
Provide a simple and scalable way to ingest machine telemetry into the cloud.

**Actors:**

* Edge device (Python simulator)
* AWS ingestion platform

**Outcome:**
Telemetry is received, validated, and stored in a structured format for later use.

---

### Secondary Use Case: Central storage of raw telemetry data

An engineer or operations team needs raw telemetry data stored centrally so that it can later be analysed for performance trends, fault investigation, or predictive maintenance.

**Goal:**
Store telemetry in a structured, durable, and low-cost format.

**Actors:**

* AWS telemetry platform
* Engineering / operations user

**Outcome:**
Telemetry is stored in a private S3 bucket using a consistent and scalable structure.

---

### Secondary Use Case: Operational visibility for troubleshooting

If telemetry ingestion fails or behaves unexpectedly, an engineer needs enough visibility to identify what went wrong.

**Goal:**
Provide basic observability for ingestion events.

**Actors:**

* AWS Lambda
* CloudWatch
* Engineer / operator

**Outcome:**
Execution logs and error information are available for troubleshooting and validation.

* Engineering / operations user

**Outcome:**
Telemetry is stored in a private S3 bucket using a consistent and scalable structure.

---

### Secondary Use Case: Operational visibility for troubleshooting

If telemetry ingestion fails or behaves unexpectedly, an engineer needs enough visibility to identify what went wrong.

**Goal:**
Provide basic observability for ingestion events.

**Actors:**

* AWS Lambda
* CloudWatch
* Engineer / operator

**Outcome:**
Execution logs and error information are available for troubleshooting and validation.
