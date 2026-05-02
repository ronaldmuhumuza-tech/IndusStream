import json
from time import sleep

from read_latest_sqlite import read_latest_reading
from mqtt_client import create_mqtt_client
from payload_builder import build_payload

from config.settings import (
    AWS_IOT_ENDPOINT,
    MQTT_PORT,
    MQTT_TOPIC,
    PUBLISH_INTERVAL_SECONDS,
)


def run_gateway():
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
            print(f"Gateway error: {e}")

        sleep(PUBLISH_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_gateway()