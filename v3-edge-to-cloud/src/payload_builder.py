from datetime import datetime, timezone


def build_payload(reading: dict) -> dict:
    if not reading:
        raise ValueError("No reading provided")

    return {
        "device_id": "raspberry-pi-edge-gateway",
        "source": "sqlite-local-buffer",
        "published_at": datetime.now(timezone.utc).isoformat(),
        "reading": reading,
    }