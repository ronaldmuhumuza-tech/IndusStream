import json
import requests

API_URL = "https://p6pg5m8627.execute-api.eu-west-2.amazonaws.com/telemetry"

with open("sample_payload.json") as f:
    payload = json.load(f)

response = requests.post(API_URL, json=payload, timeout=10)

print("Status code:", response.status_code)
print("Response body:", response.text)