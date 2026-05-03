# DynamoDB design + future S3

## Covers:
* Table design:

```Bash
PK: device_id
SK: timestamp
```
* Final item structure:

```Bash
{
  "device_id": "...",
  "timestamp": "...",
  "metrics": {...},
  "status": {...},
  "ttl": ...
}
```

* Why this is scalable
* Trade-offs vs:
    - S3
    - Timestream
* Preview next step:

DynamoDB → S3 → QuickSight