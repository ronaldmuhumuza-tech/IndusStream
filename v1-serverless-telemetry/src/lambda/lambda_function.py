import json
from datetime import datetime, timezone
import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "indusstream-telemetry-raw-eu-west-2-dev"

REQUIRED_FIELDS = ["timestamp", "device_id", "temperature_c", "pressure_bar", "status"]

def build_s3_key(payload):
    device_id = payload["device_id"]
    ts = payload["timestamp"]

    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    safe_timestamp = dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")

    return f"{device_id}/{dt:%Y}/{dt:%m}/{dt:%d}/{safe_timestamp}.json"

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        # Validate fields
        for field in REQUIRED_FIELDS:
            if field not in body:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Missing field: {field}"})
                }

        key = build_s3_key(body)

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(body),
            ContentType="application/json"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Telemetry stored", "key": key})
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }