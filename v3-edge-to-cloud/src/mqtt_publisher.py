import json
from time import sleep

from src.config.settings import (
    AWS_IOT_ENDPOINT,
    MQTT_PORT,
    MQTT_TOPIC,
    PUBLISH_INTERVAL_SECONDS,
)

from src.mqtt_client import create_mqtt_client
from src.read_latest_sqlite import read_latest_reading
from src.payload_builder import build_payload


def publish_loop():
    client = create_mqtt_client()

    print("Connecting to AWS IoT Core...")
    client.connect(AWS_IOT_ENDPOINT, MQTT_PORT)
    client.loop_start()

    while True:
        try:
            reading = read_latest_reading()

            if reading:
                payload = build_payload(reading)
                payload_json = json.dumps(payload)

                client.publish(MQTT_TOPIC, payload_json)
                print(f"Published: {payload_json}")
            else:
                print("No data available")

        except Exception as e:
            print(f"Publisher error: {e}")

        sleep(PUBLISH_INTERVAL_SECONDS)


if __name__ == "__main__":
    publish_loop()