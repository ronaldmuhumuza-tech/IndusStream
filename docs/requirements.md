## Requirements

### Scope Summary

This requirements set is primarily derived from the main v1 use case:

**A simulated industrial edge device sends telemetry data securely to AWS for validation, storage, and operational visibility.**

The requirements also support two related secondary needs:

* central storage of raw telemetry data for later analysis
* operational visibility for troubleshooting ingestion failures

---

### Functional Requirements

1. The system must accept telemetry data from a local edge simulator over HTTPS.
2. The system must validate the incoming telemetry payload.
3. The system must store valid telemetry data in Amazon S3.
4. The system must log processing activity for troubleshooting.
5. The system must return a success or failure response to the sender.

---

### Non-Functional Requirements

1. The first version should be low-cost to build and run.
2. The design should remain simple and easy to explain.
3. The architecture should be scalable enough to support additional devices later.
4. The solution should rely on managed services where practical to reduce operational overhead.

---

### Security Requirements

1. Only the ingestion endpoint should be publicly reachable.
2. The S3 bucket must remain private.
3. Lambda should operate using a least-privilege IAM role.
4. No AWS credentials should be hardcoded into source code.

---

### Data Requirements

1. Telemetry data must include a timestamp.
2. Telemetry data must include a device identifier.
3. Telemetry payloads should support industrial-style metrics such as temperature, pressure, and status.
4. Stored objects should follow a consistent structure to support future analytics use.

---

### Cost Constraints

1. The architecture should avoid always-on compute for v1.
2. The solution should minimise unnecessary networking complexity and associated charges.
3. Storage should use a low-cost service suitable for raw telemetry retention.
