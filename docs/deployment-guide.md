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