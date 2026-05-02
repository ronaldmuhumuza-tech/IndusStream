import ssl
import paho.mqtt.client as mqtt

from config.settings import (
    MQTT_CLIENT_ID,
    ROOT_CA_PATH,
    DEVICE_CERT_PATH,
    PRIVATE_KEY_PATH,
)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to AWS IoT Core")
    else:
        print(f"Connection failed with code: {rc}")


def create_mqtt_client():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)

    client.tls_set(
        ca_certs=str(ROOT_CA_PATH),
        certfile=str(DEVICE_CERT_PATH),
        keyfile=str(PRIVATE_KEY_PATH),
        tls_version=ssl.PROTOCOL_TLSv1_2,
    )

    client.on_connect = on_connect

    return client