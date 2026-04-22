## Architecture

### Architecture Summary

IndusStream v1 is a lightweight industrial telemetry ingestion platform built on AWS. A local Python-based edge simulator sends telemetry data over HTTPS to Amazon API Gateway. API Gateway invokes an AWS Lambda function, which validates the payload and stores the telemetry in a private Amazon S3 bucket. Amazon CloudWatch Logs provide operational visibility for troubleshooting and validation.

---

### How the Architecture Was Derived

The architecture was derived from the primary v1 use case:

**A simulated industrial edge device sends telemetry data securely to AWS for validation, storage, and operational visibility.**

From that use case, the platform needs to:

* accept telemetry over HTTPS
* validate incoming payloads
* store valid telemetry data
* provide operational logging
* return a response to the sender

Those needs were then translated into architecture responsibilities and component choices.

---

### Requirements-to-Architecture Traceability

The table below shows how the v1 architecture was derived from the primary use case and requirements, and why each component was selected.

| Requirement / Need                                    | Selected Component                            | Why Selected                                                                                                                          | Alternatives Considered / Deferred                                                                            |
| ----------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Accept telemetry over HTTPS                           | Amazon API Gateway                            | API Gateway provides a managed HTTPS endpoint with low operational overhead and cleanly separates the sender from backend processing. | Direct S3 upload was rejected because validation and controlled ingestion are required.                       |
| Validate incoming payloads                            | AWS Lambda                                    | Lambda is event-driven and low-cost for low-volume telemetry processing. It avoids the need for always-on compute.                    | Amazon EC2 was deferred because it would introduce more operational overhead and continuous cost.             |
| Store raw telemetry data                              | Amazon S3                                     | S3 is durable, scalable, and low-cost. It fits the need to store raw JSON telemetry for later analysis.                               | DynamoDB was deferred because the immediate need is raw object storage, not query-optimised application data. |
| Provide operational visibility                        | Amazon CloudWatch Logs                        | CloudWatch integrates naturally with Lambda and provides simple execution logging and troubleshooting.                                | External logging tools were unnecessary for the first version.                                                |
| Avoid hardcoded credentials and apply least privilege | IAM execution role for Lambda                 | IAM roles allow Lambda to access only the resources it needs without embedding credentials in code.                                   | Static access keys were rejected as a poor security practice.                                                 |
| Keep v1 simple and low-cost                           | Serverless design (API Gateway + Lambda + S3) | Managed services minimise operational complexity and idle cost while satisfying the main use case.                                    | VPC integration was deferred because it adds complexity not yet justified by the v1 requirements.             |

---

### Version 1 Components

The first version of the platform includes:

* Local Python edge simulator
* Amazon API Gateway
* AWS Lambda
* Amazon S3
* Amazon CloudWatch Logs
* IAM execution role for Lambda

This set of components is sufficient to implement the core telemetry path without introducing unnecessary complexity.

---

### Data Flow

1. A local Python script generates a telemetry payload.
2. The payload is sent over HTTPS to Amazon API Gateway.
3. API Gateway invokes the Lambda function.
4. Lambda validates the payload.
5. If valid, Lambda writes the telemetry object to Amazon S3.
6. Lambda logs execution details to Amazon CloudWatch Logs.
7. Lambda returns a success or failure response to the sender.

---

### Security Boundaries

The v1 design keeps the trust boundaries simple and explicit:

* **API Gateway** is the only public-facing component.
* **Lambda** processes incoming requests using a least-privilege IAM execution role.
* **S3** remains private and is not publicly accessible.
* **CloudWatch Logs** are used for operational visibility and troubleshooting.

This limits the public attack surface while keeping compute and storage access-controlled.

---

### Cost Rationale

The v1 architecture uses managed, serverless services to minimise both idle cost and operational overhead.

* **AWS Lambda** was chosen instead of EC2 because the workload is event-driven and low volume.
* **Amazon S3** was chosen because it is a low-cost and scalable storage service for raw telemetry data.
* **API Gateway** provides a simple managed ingestion point without requiring a self-managed web server.

The first version intentionally avoids VPC integration and always-on infrastructure so that the platform remains simple and inexpensive while the core data flow is being established.

---

### Out of Scope for v1

The following items are intentionally excluded from version 1 to keep the design simple, low-cost, and aligned with the current requirements:

* **VPC integration**: not required for the initial ingestion workflow and would introduce additional networking complexity.
* **Private subnets**: unnecessary at this stage as no resources require isolated network placement.
* **NAT gateway**: avoided due to added cost and because outbound private networking is not yet needed.
* **API authentication and authorisation**: deferred to focus on core ingestion functionality before adding access control mechanisms.
* **DynamoDB**: not required as the current need is raw telemetry storage rather than structured query-optimised data.
* **SNS alerts**: monitoring is handled via CloudWatch logs in v1; alerting can be introduced later.
* **Analytics dashboards**: analysis is out of scope until sufficient data is collected.
* **Multi-region architecture**: not required for the initial prototype and would add unnecessary complexity.

This scope ensures that version 1 remains focused on establishing a reliable telemetry ingestion pipeline before introducing additional architectural layers.

---

### Summary

The v1 architecture is intentionally small, explainable, and cost-aware. It demonstrates a realistic industrial edge-to-cloud telemetry pattern using managed AWS services and provides a strong foundation for future enhancements such as private networking, alerting, analytics, or hybrid connectivity.
