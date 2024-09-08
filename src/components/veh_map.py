import streamlit as st
import folium
from streamlit_folium import folium_static


def create_base_map(initial_lat, initial_lon, style="Default"):
    m = folium.Map(
        location=[initial_lat, initial_lon],
        tiles=None,
    )

    if style == "Default":
        folium.TileLayer(
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="© OpenStreetMap contributors",
            name="OpenStreetMap",
            max_zoom=19,
            overlay=False,
            control=True,
        ).add_to(m)
    elif style == "Streets":
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Maps",
            max_zoom=20,
            overlay=False,
            control=True,
        ).add_to(m)
    elif style == "Satellite":
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Satellite",
            max_zoom=20,
            overlay=False,
            control=True,
        ).add_to(m)
    elif style == "Terrain":
        folium.TileLayer(
            tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
            attr="Map data: © OpenStreetMap contributors, SRTM | Map style: © OpenTopoMap (CC-BY-SA)",
            name="OpenTopoMap",
            max_zoom=15,
            overlay=False,
            control=True,
        ).add_to(m)
    elif style == "Dark":
        folium.TileLayer(
            tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            attr="© OpenStreetMap contributors © CARTO",
            name="CARTO Dark",
            max_zoom=16,
            overlay=False,
            control=True,
        ).add_to(m)
    else:
        raise ValueError("Invalid map style")

    return m


def display_map(
    df,
    current_time_index,
    initial_lat=29.18853467,
    initial_lon=-81.04548,
    map_style="Default",
):
    if "Lat_base" not in df.columns or "Lon_base" not in df.columns:
        st.error(
            "Could not find latitude and longitude columns after cleaning. Please check your CSV file."
        )
        return

    if df.empty:
        st.error("No valid data available to display on the map.")
        return

    # Create a new map instance with the specified style
    m = create_base_map(initial_lat, initial_lon, style=map_style)

    # Add a marker for the base start point (first entry)
    folium.Marker(
        [df["Lat_base"].iloc[0], df["Lon_base"].iloc[0]],
        popup="Base Start",
        icon=folium.Icon(color="green", icon="play"),
    ).add_to(m)

    # Plot the traveled path up to the current time index
    traveled_path = (
        df[["Lat_base", "Lon_base"]].iloc[: current_time_index + 1].values.tolist()
    )
    if len(traveled_path) > 1:
        folium.PolyLine(
            traveled_path,
            weight=2,
            color="blue",
            opacity=0.8,
            tooltip="Traveled Path",
        ).add_to(m)

    # Add current position marker (now blue)
    current_position = [
        df["Lat_base"].iloc[current_time_index],
        df["Lon_base"].iloc[current_time_index],
    ]
    folium.Marker(
        current_position,
        popup="Current Position",
        icon=folium.Icon(color="blue", icon="car", prefix="fa"),
    ).add_to(m)

    # Add end marker only if we've reached the end of the data
    if current_time_index == len(df) - 1:
        folium.Marker(
            [df["Lat_base"].iloc[-1], df["Lon_base"].iloc[-1]],
            popup="Base End",
            icon=folium.Icon(color="red", icon="stop"),
        ).add_to(m)

    # Fit the map to the traveled path
    if len(traveled_path) > 1:
        m.fit_bounds(traveled_path)
    else:
        m.fit_bounds([current_position, current_position])

    # Update the map
    folium_static(m)
