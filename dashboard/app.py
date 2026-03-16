# dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os
import sys
import time

# Ensure Plotly uses Kaleido for image export
import plotly.io as pio

# Optional: Check if kaleido is installed
try:
    import kaleido
    print("Kaleido is installed.")
except ImportError:
    print("Kaleido is not installed. Run: pip install kaleido")

# ----------------------------
# Fix project path
# ----------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ----------------------------
# Import project modules
# ----------------------------
from src.ingest_live_data import fetch_live_flights
from src.preprocess import FlightPreprocessor
from src.anomaly_detection import FlightAnomalyDetector
from src.pattern_discovery import FlightPatternDiscovery
from src.graph_analysis import FlightGraphAnalyzer
from src.delay_prediction import FlightDelayPredictor

# ----------------------------
# Create image folder if not exists
# ----------------------------
image_folder = "dashboard/images"
os.makedirs(image_folder, exist_ok=True)

# ----------------------------
# Page settings
# ----------------------------
st.set_page_config(page_title="Global Flight Analytics", layout="wide")
st.title("Global Flight Analytics Dashboard")
st.write(
    "Explore real-time flights worldwide. "
    "Understand flight movements, busiest airports, and potential delays."
)

# ----------------------------
# Fetch and preprocess data
# ----------------------------
preprocessor = FlightPreprocessor()
flights = fetch_live_flights()

if flights.empty:
    st.warning("No live flight data available.")
    st.stop()

data = preprocessor.preprocess(flights)
data = data.dropna(subset=["latitude", "longitude"])
data["callsign"] = data["callsign"].fillna("Unknown")
data["AirlineCode"] = data["callsign"].astype(str).str[:3]

# ----------------------------
# ML Pipeline
# ----------------------------
detector = FlightAnomalyDetector()
data = detector.detect(data)

pattern_model = FlightPatternDiscovery()
data = pattern_model.discover(data)

graph_model = FlightGraphAnalyzer()
graph_model.build_graph(data)

predictor = FlightDelayPredictor()
predictor.train(data)
data = predictor.predict(data)

# ----------------------------
# Helper: Save Preprocessed Data Table
# ----------------------------
def save_dataframe_image(df, filename="preprocessed_data.png", num_rows=10):
    columns_to_show = ["callsign", "AirlineCode", "velocity", "baro_altitude", 
                       "vertical_rate", "delay_risk", "anomaly"]
    df_to_save = df[columns_to_show].head(num_rows)
    
    fig_width = max(12, len(df_to_save.columns) * 2)
    fig_height = 2 + 0.5*num_rows
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')
    table = ax.table(
        cellText=df_to_save.values,
        colLabels=df_to_save.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df_to_save.columns))))
    plt.tight_layout()
    plt.savefig(os.path.join(image_folder, filename), dpi=300, bbox_inches='tight')
    plt.close()

save_dataframe_image(data, filename="preprocessed_data.png")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")
airlines = ["All"] + sorted(data["AirlineCode"].unique().tolist())
selected_airline = st.sidebar.selectbox("Select Airline", airlines)

min_altitude = st.sidebar.slider("Minimum Altitude", 0, int(data["baro_altitude"].max()), 0)

filtered_data = data.copy()
if selected_airline != "All":
    filtered_data = filtered_data[filtered_data["AirlineCode"] == selected_airline]
filtered_data = filtered_data[filtered_data["baro_altitude"] >= min_altitude]

# ----------------------------
# Tabs for Story-like Dashboard
# ----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "Live Map", "Traffic Heatmap", "Animated Movement", "Insights"
])

# ----------------------------
# Tab 1: Overview
# ----------------------------
with tab1:
    st.subheader("Live Flight Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Flights", len(filtered_data))
    col2.metric("Active Airlines", filtered_data["AirlineCode"].nunique())
    col3.metric("Possible Delays", len(filtered_data[filtered_data["delay_risk"] == 1]))

    st.write("Top Airlines in the sky right now:")
    airline_counts = filtered_data["AirlineCode"].value_counts().head(10).reset_index()
    airline_counts.columns = ["Airline", "Flights"]
    
    fig_airline = px.bar(
        airline_counts,
        x="Airline",
        y="Flights",
        text="Flights",
        color="Flights",
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    fig_airline.update_layout(xaxis_title="Airline", yaxis_title="Number of Flights")
    st.plotly_chart(fig_airline, use_container_width=True)
    fig_airline.write_image(os.path.join(image_folder, "top_airlines.png"), engine="kaleido", scale=2)

# ----------------------------
# Tab 2: Live Map
# ----------------------------
with tab2:
    st.subheader("Aircraft Live Positions")
    st.write("Color shows altitude; size shows speed.")

    fig_map = px.scatter_mapbox(
        filtered_data,
        lat="latitude",
        lon="longitude",
        hover_name="callsign",
        hover_data={"AirlineCode": True, "velocity": True, "baro_altitude": True},
        color="baro_altitude",
        size="velocity",
        size_max=15,
        color_continuous_scale=px.colors.sequential.Plasma,
        zoom=1,
        height=600,
    )
    fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
    fig_map.write_image(os.path.join(image_folder, "live_map.png"), engine="kaleido", scale=2)

# ----------------------------
# Tab 3: Traffic Heatmap
# ----------------------------
with tab3:
    st.subheader("Flight Traffic Heatmap")
    fig_heat = px.density_mapbox(
        filtered_data,
        lat="latitude",
        lon="longitude",
        z="velocity",
        radius=15,
        zoom=1,
        mapbox_style="carto-positron",
        color_continuous_scale=px.colors.sequential.Rainbow,
        title="Flight Traffic Intensity"
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    fig_heat.write_image(os.path.join(image_folder, "traffic_heatmap.png"), engine="kaleido", scale=2)

# ----------------------------
# Tab 4: Animated Movement
# ----------------------------
with tab4:
    st.subheader("Animated Aircraft Movement")
    anim_data = filtered_data.copy()
    anim_data["frame"] = anim_data.index % 20

    fig_anim = px.scatter_geo(
        anim_data,
        lat="latitude",
        lon="longitude",
        hover_name="callsign",
        size="velocity",
        color="baro_altitude",
        animation_frame="frame",
        color_continuous_scale=px.colors.sequential.Rainbow,
        size_max=15,
        projection="natural earth",
        title="Aircraft Movement Animation"
    )
    fig_anim.update_layout(geo=dict(showland=True, landcolor="rgb(240,240,240)", oceancolor="lightblue"))
    st.plotly_chart(fig_anim, use_container_width=True)
    fig_anim.write_image(os.path.join(image_folder, "animated_movement.png"), engine="kaleido", scale=2)

# ----------------------------
# Tab 5: Insights
# ----------------------------
with tab5:
    st.subheader("Insights and Observations")
    st.write("• Most aircraft cruise between 9000–12000 meters altitude.")
    st.write("• Faster aircraft usually operate at higher altitudes.")
    st.write("• Abnormal flights may indicate unusual behaviour.")

    st.write("Busiest Airports right now:")
    airport_df = graph_model.busiest_airports()
    fig_airports = px.bar(
        airport_df,
        x="Airport",
        y="Flights",
        text="Flights",
        color="Flights",
        color_continuous_scale=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig_airports, use_container_width=True)
    fig_airports.write_image(os.path.join(image_folder, "busiest_airports.png"), engine="kaleido", scale=2)

    st.write("Flight Delay Risk Distribution:")
    delay_counts = filtered_data["delay_risk"].value_counts().reset_index()
    delay_counts.columns = ["Status", "Flights"]
    delay_counts["Status"] = delay_counts["Status"].map({0: "On Time", 1: "Possible Delay"})
    fig_delay = px.pie(
        delay_counts,
        names="Status",
        values="Flights",
        color_discrete_sequence=px.colors.sequential.Rainbow
    )
    st.plotly_chart(fig_delay)
    fig_delay.write_image(os.path.join(image_folder, "delay_distribution.png"), engine="kaleido", scale=2)

    st.write("Detected Abnormal Flights:")
    anomalies = filtered_data[filtered_data["anomaly"] == -1]
    st.dataframe(anomalies[["callsign", "velocity", "baro_altitude", "vertical_rate"]])

# ----------------------------
# Auto-refresh every 60 seconds
# ----------------------------
st.sidebar.write("Auto refresh every 60 seconds")
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=60*1000, key="flight_autorefresh")