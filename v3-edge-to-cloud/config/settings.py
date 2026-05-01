from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CERTS_DIR = BASE_DIR / "certs"
LOGS_DIR = BASE_DIR / "logs"

# Local SQLite database
DB_FILE_PREFIX = "indusstream"

# AWS IoT Core MQTT settings
AWS_IOT_ENDPOINT = "REPLACE_WITH_YOUR_AWS_IOT_ENDPOINT"
MQTT_PORT = 8883
MQTT_TOPIC = "indusstream/v3/telemetry"

# AWS IoT certificate paths
ROOT_CA_PATH = CERTS_DIR / "AmazonRootCA1.pem"
DEVICE_CERT_PATH = CERTS_DIR / "device-certificate.pem.crt"
PRIVATE_KEY_PATH = CERTS_DIR / "private.pem.key"

# Publish behaviour
PUBLISH_INTERVAL_SECONDS = 30
MQTT_CLIENT_ID = "indusstream-edge-gateway-01"