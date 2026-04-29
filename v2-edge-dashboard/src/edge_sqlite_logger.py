import sqlite3
import time
from datetime import UTC, datetime
from pathlib import Path

import serial


SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

DEVICE_ID = "indusstream-edge-gateway-01"
SOURCE_ID = "arduino-uno-wifi-rev2-01"

SAMPLE_INTERVAL_SECONDS = 60

SOUND_EVENT_THRESHOLD = 50
LIGHT_DARK_THRESHOLD = 200
LIGHT_BRIGHT_THRESHOLD = 700

DATA_DIR = Path("/home/pi/indusstream_v2/data")
DB_PATH = DATA_DIR / "indusstream.db"


def utc_now():
    return datetime.now(UTC)


def iso_z(dt):
    return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


def classify_light(light_raw):
    if light_raw < LIGHT_DARK_THRESHOLD:
        return "dark"
    if light_raw > LIGHT_BRIGHT_THRESHOLD:
        return "bright"
    return "normal"


def connect_db():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            device_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            temperature_c REAL,
            co_raw INTEGER,
            co_voltage REAL,
            co_rs_ohms REAL,
            sound_raw INTEGER,
            sound_event INTEGER,
            light_raw INTEGER,
            light_state TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS hourly_summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            window_start TEXT NOT NULL,
            window_end TEXT NOT NULL,
            device_id TEXT NOT NULL,
            source_id TEXT NOT NULL,

            temperature_avg REAL,
            temperature_min REAL,
            temperature_max REAL,

            co_raw_avg REAL,
            co_raw_min INTEGER,
            co_raw_max INTEGER,
            co_voltage_avg REAL,
            co_rs_avg REAL,

            sound_avg REAL,
            sound_min INTEGER,
            sound_max INTEGER,
            sound_event_count INTEGER,

            light_avg REAL,
            light_min INTEGER,
            light_max INTEGER,
            dark_count INTEGER,
            normal_light_count INTEGER,
            bright_count INTEGER,

            samples INTEGER
        )
    """)

    conn.commit()
    return conn


def parse_line(line):
    """
    Expected Arduino format:
    temperature_c,co_raw,co_voltage,co_rs,sound_raw,light_raw

    Example:
    24.50,429,2.097,13846,10,70
    """
    parts = line.strip().split(",")

    if len(parts) != 6:
        raise ValueError(f"Expected 6 fields, got {len(parts)}: {line}")

    temperature_c = float(parts[0])
    co_raw = int(parts[1])
    co_voltage = float(parts[2])
    co_rs_ohms = float(parts[3])
    sound_raw = int(parts[4])
    light_raw = int(parts[5])

    sound_event = 1 if sound_raw >= SOUND_EVENT_THRESHOLD else 0
    light_state = classify_light(light_raw)

    return {
        "temperature_c": temperature_c,
        "co_raw": co_raw,
        "co_voltage": co_voltage,
        "co_rs_ohms": co_rs_ohms,
        "sound_raw": sound_raw,
        "sound_event": sound_event,
        "light_raw": light_raw,
        "light_state": light_state,
    }


def insert_raw_reading(conn, timestamp, reading):
    conn.execute("""
        INSERT INTO raw_readings (
            timestamp, device_id, source_id,
            temperature_c, co_raw, co_voltage, co_rs_ohms,
            sound_raw, sound_event, light_raw, light_state
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        DEVICE_ID,
        SOURCE_ID,
        reading["temperature_c"],
        reading["co_raw"],
        reading["co_voltage"],
        reading["co_rs_ohms"],
        reading["sound_raw"],
        reading["sound_event"],
        reading["light_raw"],
        reading["light_state"],
    ))

    conn.commit()


def avg(values):
    return round(sum(values) / len(values), 2) if values else None


def write_hourly_summary(conn, window_start, window_end):
    start = iso_z(window_start)
    end = iso_z(window_end)

    rows = conn.execute("""
        SELECT
            temperature_c,
            co_raw,
            co_voltage,
            co_rs_ohms,
            sound_raw,
            sound_event,
            light_raw,
            light_state
        FROM raw_readings
        WHERE timestamp >= ? AND timestamp < ?
    """, (start, end)).fetchall()

    if not rows:
        return

    temperatures = [r[0] for r in rows if r[0] is not None]
    co_raw_values = [r[1] for r in rows if r[1] is not None]
    co_voltage_values = [r[2] for r in rows if r[2] is not None]
    co_rs_values = [r[3] for r in rows if r[3] is not None]
    sound_values = [r[4] for r in rows if r[4] is not None]
    sound_events = [r[5] for r in rows if r[5] is not None]
    light_values = [r[6] for r in rows if r[6] is not None]
    light_states = [r[7] for r in rows if r[7] is not None]

    conn.execute("""
        INSERT INTO hourly_summaries (
            window_start, window_end, device_id, source_id,

            temperature_avg, temperature_min, temperature_max,

            co_raw_avg, co_raw_min, co_raw_max,
            co_voltage_avg, co_rs_avg,

            sound_avg, sound_min, sound_max, sound_event_count,

            light_avg, light_min, light_max,
            dark_count, normal_light_count, bright_count,

            samples
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        start,
        end,
        DEVICE_ID,
        SOURCE_ID,

        avg(temperatures),
        round(min(temperatures), 2) if temperatures else None,
        round(max(temperatures), 2) if temperatures else None,

        avg(co_raw_values),
        min(co_raw_values) if co_raw_values else None,
        max(co_raw_values) if co_raw_values else None,
        avg(co_voltage_values),
        avg(co_rs_values),

        avg(sound_values),
        min(sound_values) if sound_values else None,
        max(sound_values) if sound_values else None,
        sum(sound_events),

        avg(light_values),
        min(light_values) if light_values else None,
        max(light_values) if light_values else None,
        light_states.count("dark"),
        light_states.count("normal"),
        light_states.count("bright"),

        len(rows)
    ))

    conn.commit()
    print(f"Hourly summary stored: {start} → {end} ({len(rows)} samples)")


def main():
    conn = connect_db()
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)

    print("IndusStream SQLite edge logger started")
    print(f"Database: {DB_PATH}")
    print(f"Reading from: {SERIAL_PORT}")
    print(f"Sampling every {SAMPLE_INTERVAL_SECONDS} seconds")
    print("Press CTRL+C to stop")

    current_window_start = utc_now().replace(minute=0, second=0, microsecond=0)
    last_sample_time = 0

    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        now = utc_now()

        if time.time() - last_sample_time < SAMPLE_INTERVAL_SECONDS:
            continue

        try:
            reading = parse_line(line)
        except ValueError as exc:
            print(f"Skipped line: {exc}")
            continue

        timestamp = iso_z(now)
        insert_raw_reading(conn, timestamp, reading)

        print(
            f"{timestamp} | "
            f"temp={reading['temperature_c']}C | "
            f"co_raw={reading['co_raw']} | "
            f"co_v={reading['co_voltage']}V | "
            f"co_rs={reading['co_rs_ohms']}Ω | "
            f"sound={reading['sound_raw']} | "
            f"sound_event={reading['sound_event']} | "
            f"light={reading['light_raw']} | "
            f"light_state={reading['light_state']}"
        )

        last_sample_time = time.time()

        current_hour_start = now.replace(minute=0, second=0, microsecond=0)

        if current_hour_start > current_window_start:
            write_hourly_summary(conn, current_window_start, current_hour_start)
            current_window_start = current_hour_start


if __name__ == "__main__":
    main()
