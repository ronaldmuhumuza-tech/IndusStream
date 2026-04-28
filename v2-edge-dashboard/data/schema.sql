CREATE TABLE raw_readings (
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
        );
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE hourly_summaries (
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
        );
