import sqlite3
import math
import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output

DB_PATH = "/home/pi/indusstream_v2/data/indusstream.db"
TEMP_OFFSET_C = 6.29

# Replace this with your measured clean-air baseline
R0 = 23500

# CO alert threshold
CO_ALERT_PPM = 50

app = Dash(__name__)
app.title = "IndusStream Dashboard"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        """
        SELECT *
        FROM raw_readings
        ORDER BY timestamp DESC
        LIMIT 1000
        """,
        conn
    )
    conn.close()
    return df

def clean_data(df):
    df = df.copy()
    
    #convert to numeric safely
    numeric_cols = ["temperature_c", "co_voltage", "co_rs_ohms", "sound_raw", "light_raw"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
    #Remove impossible / unrealistic values
    df["temperature_c"] = df["temperature_c"] -  TEMP_OFFSET_C
    
    df = df[
        (df["temperature_c"].between(0, 35)) &
        (df["co_voltage"].between(0,5)) &
        (df["co_rs_ohms"].between(100, 1_000_000)) &
        (df["sound_raw"].between(0,1023)) &
        (df["light_raw"].between(0,1023))
    ]
    
    # ---- Remove spikes using rolling median--
    for col in ["temperature_c", "co_voltage", "co_rs_ohms"]:
        rolling_median = df[col].rolling(window=5, center=True).median()
        diff = abs(df[col] - rolling_median)
        
        # Threshold = allow smalll variation, kill big jumps
        df.loc[diff > (0.2 * rolling_median), col] = None
        
    #-----Smooth signals (moving average)---
    for col in ["temperature_c", "co_voltage"]:
        df[col] = df[col].rolling(window=5, min_periods=1).mean()
    
    return df

def estimate_co_ppm(rs_value):
    if rs_value is None or rs_value <= 0:
        return None

    ratio = rs_value / R0

    if ratio <= 0:
        return None

    # Approximate MQ-7 curve estimate
    return 10 ** ((-1.5 * math.log10(ratio)) + 1.7)

card_style = {
    "backgroundColor": "white",
    "padding": "4px",
    "borderRadius": "8px",
    "boxShadow": "0 1px 4px rgba(0,0,0,0.12)",
    "minWidth": "0"
}
app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "backgroundColor": "#eef2f7",
        "padding": "8px",
        "height": "100vh",
        "overflow": "hidden"
    },
    children=[

        html.H1(
            "IndusStream Industrial Sensor Monitoring Dashboard",
            style={"textAlign": "center", "marginBottom": "10px"}
        ),

        html.P(
            "Arduino sensor data logged to SQLite and visualised on Raspberry Pi",
            style={"textAlign": "center", "color": "#555"}
        ),

        #dcc.Interval(id="refresh", interval=10_000, n_intervals=0),
        dcc.Interval(
            id="interval-component",
            interval=30000, #30000 ms = 30 seconds
            n_intervals=0
        ),

        html.Div(
            id="latest-reading",
            style={
                "backgroundColor": "linear-gradient(135deg, #007BFF, #00C6FF)",
                "color": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 10px rgba(0,0,0,0.2)",
                "fontSize": "22px",
                "textAlign": "center",
                "marginBottom": "20px"
            }
        ),

        html.Div(
            dcc.Graph(id="temperature-chart"),
            style={
                "backgroundColor": "white",
                "padding": "10px",
                "borderRadius": "10px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)",
                "marginBottom": "20px",
                "height": 300
                }
            ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(3, minmax(0, 1fr))",
                "gap": "10px",
                "width": "100%",
                "maginTop": "10px"
            },
            children=[
            
                html.Div(dcc.Graph(id="co-chart", config={"displayModeBar": True}), style= card_style),
                html.Div(dcc.Graph(id="sound-chart", config={"displayModeBar": True}), style= card_style),
                html.Div(dcc.Graph(id="light-chart", config={"displayModeBar": True}), style= card_style)
            ]
        ),

        html.H3("Recent Readings"),

        dash_table.DataTable(
            id="readings-table",
            page_size=5,
            style_table={"overflowX": "auto"},
            style_cell={
                "textAlign": "center",
                "padding": "6px",
                "fontSize": "12px"
            },
            style_header={
                "backgroundColor": "#007BFF",
                "color": "white",
                "fontWeight": "bold"
            }
        ),
    ]

)


@app.callback(
    [
    Output("latest-reading", "children"),
    Output("latest-reading", "style"),
    Output("temperature-chart", "figure"),
    Output("co-chart", "figure"),
    Output("sound-chart", "figure"),
    Output("light-chart", "figure"),
    Output("readings-table", "data"),
    Output("readings-table", "columns"),
    ],
    [
    Input("interval-component", "n_intervals"),
    ],
)
def update_dashboard(_):
    df = load_data()
    df = clean_data(df)

    if df.empty:
        empty_fig = {"data": [], "layout": {"title": "No data"}}
        empty_style = {
            "backgroundColor": "5c757d",
            "color": "white",
            "padding": "16px",
            "borderRadius": "10px",
            "fontSize": "22px",
            "fontWeight": "bold",
            "textAlign": "center",
            "marginBottom": "20px"
        }
        
        return (
            "No readings found.",
            empty_style,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            [],
            []
        )

    selected_device = df["device_id"].iloc[0]
    df_filtered = df[df["device_id"] == selected_device].copy()
    df_chart = df_filtered.sort_values("timestamp").copy()

    df_chart["co_ppm_est"] = df_chart["co_rs_ohms"].apply(estimate_co_ppm)
    df_filtered["co_ppm_est"] =  df_chart["co_ppm_est"]

    latest = df_chart.iloc[-1]

    latest_co = latest["co_ppm_est"]

    if latest_co is not None and latest_co >= CO_ALERT_PPM:
        alert_color = "#dc3545" # red
        alert_text = f"⚠️ CO HIGH: {latest_co:.1f} ppm"
    else:
        alert_color = "#28a745" # green
        alert_text = f"✅ CO Normal: {latest_co:.1f} ppm" if latest_co is not None else "CO unavailable"
    
    status_style = {
        "backgroundColor": alert_color,
        "color": "white",
        "padding": "16px",
        "borderRadius": "10px",
        "boxShadow": "0 3px 8px rgba(0,0,0,0.25)",
        "fontSize": "22px",
        "fontWeight": "bold",
        "textAlign": "center",
        "marginBottom": "20px"
    }
    
    latest_text = (
        f"{selected_device} | "
        f"Temperature: {latest['temperature_c']} °C | "
        f"{alert_text}"
    )

    temp_fig = {
        "data": [
            {
                "x": df_chart["timestamp"],
                "y": df_chart["temperature_c"],
                "type": "line",
                "name": "Temperature",
                "line": {"color": "#FF5733", "width": 3}
            }
        ],
        "layout": {
            "title": {
                "text": "Temperature Trend (°C) - Last 24 hours",
                "x": 0.5
            },
            "plot_bgcolor": "#ffffff",
            "paper_bgcolor": "#ffffff",
            "font":{"color": "#333"},
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Temperature (°C)"},
            "plot_bgcolor": "white",
            "paper_bgcolor": "white",
            "height": 280,
            "margin": {"l": 40, "r": 15, "t": 40, "b": 55}
        }
    }

    co_fig = {
        "data": [
            {
                "x": df_chart["timestamp"],
                "y": df_chart["co_ppm_est"],
                "type": "line",
                "name": "CO Estimate",
                "line": {"color": "#C70039", "width": 3}
            }
        ],
        "layout": {
            "title": {
                "text": "Estimated Carbon Monoxide (ppm)",
                "x": 0.5
            },
            "plot_bgcolor": "#ffffff",
            "paper_bgcolor": "#ffffff",
            "font":{"color": "#333"},
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "CO ppm"},
            "plot_bgcolor": "white",
            "paper_bgcolor": "white",
            "height": 210,
            "margin": {"l": 40, "r": 15, "t": 40, "b": 55}
        }
    }

    sound_fig = {
        "data": [
            {
                "x": df_chart["timestamp"],
                "y": df_chart["sound_raw"],
                "type": "line",
                "name": "Sound",
                "line": {"color": "#6A5ACD", "width": 3}
            }
        ],
        "layout": {
            "title": {
                "text": "Sound Level (Raw)",
                "x": 0.5
            },
            "plot_bgcolor": "#ffffff",
            "paper_bgcolor": "#ffffff",
            "font":{"color": "#333"},
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Raw value"},
            "plot_bgcolor": "white",
            "paper_bgcolor": "white",
            "height": 210,
            "margin": {"l": 40, "r": 15, "t": 40, "b": 55}
        }
    }

    light_fig = {
        "data": [
            {
                "x": df_chart["timestamp"],
                "y": df_chart["light_raw"],
                "type": "line",
                "name": "Light",
                "line": {"color": "#FFC300", "width": 3}
            }
        ],
        "layout": {
            "title": {
                "text": "Light Level (Raw)",
                "x": 0.5
            },
            "plot_bgcolor": "#ffffff",
            "paper_bgcolor": "#ffffff",
            "font":{"color": "#333"},
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Raw value"},
            "plot_bgcolor": "white",
            "paper_bgcolor": "white",
            "height": 210,
            "margin": {"l": 40, "r": 15, "t": 40, "b": 55}
        }
    }

    display_df = df_chart.sort_values("timestamp", ascending=False)[
        [
            "timestamp",
            "temperature_c",
            "co_voltage",
            "co_rs_ohms",
            "co_ppm_est",
            "sound_raw",
            "sound_event",
            "light_raw",
            "light_state",
        ]
    ].copy()
    
    display_df = display_df.head(3)
    display_df["co_ppm_est"] = display_df["co_ppm_est"].round(1)

    columns = [{"name": col, "id": col} for col in display_df.columns]

    return (
        latest_text,
        status_style,
        temp_fig,
        co_fig,
        sound_fig,
        light_fig,
        display_df.to_dict("records"),
        columns,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
