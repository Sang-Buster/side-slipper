import streamlit as st
import pandas as pd
from components.veh_fig import display_vehicle_figure
from components.veh_map import display_map
from components.veh_data import display_vehicle_data
from components.veh_metrics import display_vehicle_metrics
from components.line_plot import display_multi_select_and_line_plot
from components.time_control import display_time_control

# Page configuration
st.set_page_config(
    page_title="Vehicle Side Slip Dashboard",
    page_icon="🚗",
    layout="wide",
)

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def main():
    df = load_data("./data/merged_cleaned.csv")

    # Initialize session state for current time index and playing state
    if 'current_time_index' not in st.session_state:
        st.session_state.current_time_index = 0
    if 'playing' not in st.session_state:
        st.session_state.playing = False

    row1_cols = st.columns((1, 3, 1))
    row2_cols = st.columns((1, 3, 1))

    with row1_cols[0]:
        display_vehicle_figure()

    with row1_cols[1]:
        st.markdown(
            """
        <style>
        iframe {
            width: 100% !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # Create an empty container for the map
        map_container = st.empty()

    with row1_cols[2]:
        display_vehicle_data()

    with row2_cols[0]:
        display_vehicle_metrics()

    with row2_cols[1]:
        display_multi_select_and_line_plot()

    with row2_cols[2]:
        display_time_control(df, map_container)

        # Update the map based on the current time index
        if 'current_time_index' in st.session_state:
            with map_container:
                display_map(df, st.session_state.current_time_index)

        with st.expander("About", expanded=True, icon=":material/info:"):
            st.write("""
            This dashboard displays vehicle side slip data.
            **Author:** 
            - Andrew Hannah
            - Levi Blumer 
            - Marc Compere
            
            **Contributors:** 
            - Sang Xing
            """)

if __name__ == "__main__":
    main()