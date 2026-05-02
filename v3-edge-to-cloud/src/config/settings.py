from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
CERTS_DIR = BASE_DIR / "certs"
LOGS_DIR = BASE_DIR / "logs"

# Local SQLite database
DB_FILE_PREFIX = "indusstream"
V2_DB_PATH = BASE_DIR.parent / "v2-edge-dashboard" / "data" / "indusstream.db"

# AWS IoT Core MQTT settings
AWS_IOT_ENDPOINT = "a3gt3vmsguju2d-ats.iot.eu-west-2.amazonaws.com"
MQTT_PORT = 8883
MQTT_TOPIC = "indusstream/v3/telemetry"

# AWS IoT certificate paths
ROOT_CA_PATH = CERTS_DIR / "AmazonRootCA1.pem"
DEVICE_CERT_PATH = CERTS_DIR / "device-certificate.pem.crt"
PRIVATE_KEY_PATH = CERTS_DIR / "private.pem.key"

# Publish behaviour
PUBLISH_INTERVAL_SECONDS = 1800
MQTT_CLIENT_ID = "indusstream-edge-gateway-01"
