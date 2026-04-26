## Data Structure Design

Telemetry data is stored in an S3 bucket designed to reflect how industrial systems generate time-series data.

### Bucket Naming

indusstream-telemetry-raw-eu-west-2-dev

The naming includes:

* project identifier
* data type (raw telemetry)
* region
* environment

### Object Structure

Data is organised by device and time:

device_id/year/month/day/timestamp.json

Example:

electrolyser-edge-01/2026/04/18/2026-04-18T19-30-00Z.json

### Rationale

This structure is designed to:

* support scalable storage as data grows
* allow future querying (e.g. Athena or analytics tools)
* keep data logically grouped by device and time

#### Sample Payload
{
  "timestamp": "2026-04-18T19:30:00Z",
  "device_id": "electrolyser-edge-01",
  "temperature_c": 72.4,
  "pressure_bar": 18.6,
  "status": "normal"
}