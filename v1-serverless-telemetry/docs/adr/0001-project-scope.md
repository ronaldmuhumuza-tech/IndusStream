# 0001 – Project Scope

## Context

The goal of v1 is to build a simple telemetry ingestion pipeline using AWS managed services.

The system should simulate how industrial devices send data to the cloud.

---

## Decision

Focus on a minimal, fully serverless architecture using:

- API Gateway
- AWS Lambda
- Amazon S3
- CloudWatch Logs

Avoid adding unnecessary complexity (e.g. databases, VPC, authentication) at this stage.

---

## Rationale

- Keeps the system simple and easy to understand  
- Minimises cost and operational overhead  
- Provides a clear foundation for future versions  

---

## Consequences

### Positive
- Fast to build and deploy  
- Easy to explain and demonstrate  
- Fully managed (no infrastructure)

### Negative
- No security or authentication  
- Limited control over networking  
- Not production-ready