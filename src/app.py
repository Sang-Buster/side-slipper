import streamlit as st
import pandas as pd
from components.veh_data import display_vehicle_data
from components.veh_metrics import display_vehicle_metrics
from components.line_plot import display_multi_select_and_line_plot
from components.time_control import display_time_control
from components.seg_plot import display_seg_plot

# App information
about_info = """
This dashboard provides an interactive visualization of vehicle side slip data.

**Author:** 
- Andrew Hannah
- Levi Blumer 
- Marc Compere

**Contributors:** 
- Sang Xing
"""


# Page configuration
st.set_page_config(
    page_title="Vehicle Side Slip Dashboard",
    page_icon="🚗",
    layout="wide",
    menu_items={
        "Report a bug": "https://github.com/Sang-Buster/side-slipper/issues/new",
        "About": about_info,
    },
)


# Load and cache vehicle driving dataset
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


def main():
    # Load the dataset
    df = load_data("./data/merged_cleaned.csv")

    # Initialize session state variables if they don't exist
    if "current_time_index" not in st.session_state:
        st.session_state.current_time_index = 0
    if "playing" not in st.session_state:
        st.session_state.playing = False
    if "map_style" not in st.session_state:
        st.session_state.map_style = "Default"

    # Display the dashboard title
    st.markdown(
        "<h1 style='text-align: center;'>🚗 Side Slipper Dashboard 🚗</h1>",
        unsafe_allow_html=True,
    )

    # Create a 2x2 grid layout
    row1_cols = st.columns([1, 3])
    row2_cols = st.columns([1, 3])

    # Top-left section: Vehicle Data
    with row1_cols[0]:
        st.markdown(
            "<h3 style='text-align: center;'>Vehicle Data</h3>", unsafe_allow_html=True
        )
        display_vehicle_data(df, st.session_state.current_time_index)

    # Top-right section: Map and Map Style Selector
    with row1_cols[1]:
        # Set CSS to ensure proper iframe sizing for the map
        st.markdown(
            """
        <style>
        iframe {
            width: 100% !important;
            height: 420px !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # Function to update map style
        def update_map_style():
            st.session_state.map_style = st.session_state.map_style_selector

        # Add the selectbox for map style
        st.selectbox(
            "Select Map Style",
            options=["Default", "Streets", "Satellite", "Terrain", "Dark"],
            index=["Default", "Streets", "Satellite", "Terrain", "Dark"].index(
                st.session_state.map_style
            ),
            key="map_style_selector",
            on_change=update_map_style,
        )

        # Create an empty container for the map
        map_container = st.empty()

        # Update the map based on the current time index and selected style
        if "current_time_index" in st.session_state:
            display_time_control(df, map_container, st.session_state.map_style)

    # Bottom-left section: Vehicle Metrics and Segment Plot
    with row2_cols[0]:
        display_vehicle_metrics(df, st.session_state.current_time_index)
        display_seg_plot(df, st.session_state.current_time_index)

    # Bottom-right section: Multi-select and Line Plot
    with row2_cols[1]:
        display_multi_select_and_line_plot(df, st.session_state.current_time_index)


if __name__ == "__main__":
    main()
