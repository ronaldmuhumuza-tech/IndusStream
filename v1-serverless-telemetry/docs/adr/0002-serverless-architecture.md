# 0002 – Serverless Architecture

## Context

Telemetry data needs to be ingested, validated, and stored in a scalable way.

---

## Decision

Use a serverless ingestion pattern:

- API Gateway for ingestion
- Lambda for processing
- S3 for storage
- CloudWatch for logging

---

## Rationale

- Serverless scales automatically with incoming data  
- No infrastructure management required  
- Well-aligned with event-driven telemetry systems  

---

## Consequences

### Positive
- Highly scalable  
- Cost-efficient for low-to-medium workloads  
- Easy integration between services  

### Negative
- Cold starts in Lambda  
- Limited execution time  
- Harder to debug compared to local systems  