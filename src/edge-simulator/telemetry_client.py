import json
import requests

API_URL = "https://p6pg5m8627.execute-api.eu-west-2.amazonaws.com/telemetry"

payload = {
    "timestamp": "2026-04-23T21:00:00Z",
    "device_id": "electrolyser-edge-01",
    "temperature_c": 73.1,
    "pressure_bar": 18.9,
    "status": "normal"
}

response = requests.post(API_URL, json=payload, timeout=10)

print("Status code:", response.status_code)
print("Response body:", response.text)