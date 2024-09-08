import streamlit as st
import folium
from streamlit_folium import folium_static


def create_base_map(initial_lat, initial_lon):
    m = folium.Map(location=[initial_lat, initial_lon], zoom_start=14)
    return m


@st.fragment
def display_map(df, current_time_index, initial_lat=29.18853467, initial_lon=-81.04548):
    # Check for the correct latitude and longitude columns
    if "Lat_base" not in df.columns or "Lon_base" not in df.columns:
        st.error(
            "Could not find latitude and longitude columns after cleaning. Please check your CSV file."
        )
        return

    # Check if the DataFrame is empty after cleaning
    if df.empty:
        st.error("No valid data available to display on the map.")
        return

    # Create or get the cached map
    m = create_base_map(initial_lat, initial_lon)

    # Clear existing markers and paths
    for key in list(m._children.keys()):
        if key.startswith("marker_") or key == "path":
            del m._children[key]

    # Add a marker for the base start point (first entry)
    folium.Marker(
        [df["Lat_base"].iloc[0], df["Lon_base"].iloc[0]],
        popup="Base Start",
        icon=folium.Icon(color="green", icon="play"),
    ).add_to(m)

    # Plot the traveled path up to the current time index
    if current_time_index > 0:
        traveled_path = df.iloc[: current_time_index + 1]
        base_coordinates = traveled_path[["Lat_base", "Lon_base"]].values.tolist()
        folium.PolyLine(
            base_coordinates,
            weight=2,
            color="blue",
            opacity=0.8,
            tooltip="Traveled Path",
            name="path",
        ).add_to(m)

    # Add or update the current position marker
    current_pos = [
        df["Lat_base"].iloc[current_time_index],
        df["Lon_base"].iloc[current_time_index],
    ]
    folium.Marker(
        current_pos,
        popup="Current Position",
        icon=folium.Icon(color="blue", prefix="fa", icon="car"),
        name="marker_current",
    ).add_to(m)

    # Add the end marker only if we're at the last index
    if current_time_index == len(df) - 1:
        folium.Marker(
            [df["Lat_base"].iloc[-1], df["Lon_base"].iloc[-1]],
            popup="Base End",
            icon=folium.Icon(color="red", icon="stop"),
            name="marker_end",
        ).add_to(m)

    # Display the map
    folium_static(m)
