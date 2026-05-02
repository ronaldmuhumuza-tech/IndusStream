import json
import ssl
from time import sleep

import paho.mqtt.client as mqtt

from config.settings import (
    AWS_IOT_ENDPOINT,
    MQTT_PORT,
    MQTT_TOPIC,
    ROOT_CA_PATH,
    DEVICE_CERT_PATH,
    PRIVATE_KEY_PATH,
    MQTT_CLIENT_ID,
    PUBLISH_INTERVAL_SECONDS,
)

from src.read_latest_sqlite import read_latest_reading


def on_connect(client, userdata,flags,reason_code, properties):
    if reason_code == 0:
        print("Connected to AWS IoT Core ✅")
    else:
        print(f"Connection failed with code {reason_code}")


def create_mqtt_client():
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id=MQTT_CLIENT_ID
    )

    client.tls_set(
        ca_certs=str(ROOT_CA_PATH),
        certfile=str(DEVICE_CERT_PATH),
        keyfile=str(PRIVATE_KEY_PATH),
        tls_version=ssl.PROTOCOL_TLSv1_2,
    )

    client.on_connect = on_connect

    return client


def publish_loop():
    client = create_mqtt_client()

    print("Connecting to AWS IoT...")
    client.connect(AWS_IOT_ENDPOINT, MQTT_PORT)

    client.loop_start()

    while True:
        try:
            data = read_latest_reading()

            if data:
                payload = json.dumps(data)
                client.publish(MQTT_TOPIC, payload)
                print(f"Published: {payload}")
            else:
                print("No data available")

        except Exception as e:
            print(f"Error: {e}")

        sleep(PUBLISH_INTERVAL_SECONDS)


if __name__ == "__main__":
    publish_loop()
