## Deployment Guide

### Phase 1 – S3 and Lambda

Created S3 bucket:
- `indusstream-telemetry-raw-eu-west-2-dev`

Bucket settings:
- Block public access enabled
- Default encryption enabled

Created Lambda function:
- `indusstream-telemetry-processor-dev`

Permissions:
- AWSLambdaBasicExecutionRole
- Inline policy allowing `s3:PutObject` to the telemetry bucket

Validation:
- Lambda test executed successfully
- Telemetry JSON object was written to S3 using the expected path structure

### Phase 2 – API Gateway and end-to-end test

Created HTTP API in Amazon API Gateway.

Route:
- `POST /telemetry`

Integration:
- Lambda function `indusstream-telemetry-processor-dev`

Validation:
- Local Python simulator successfully sent telemetry to the API endpoint
- API Gateway invoked Lambda
- Lambda stored the JSON payload in S3
- A 200 response was returned to the client

Example response:
```json
{
  "message": "Telemetry stored",
  "key": "electrolyser-edge-01/2026/04/23/2026-04-23T21-00-00Z.json"
}