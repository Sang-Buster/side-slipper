import streamlit as st
import pandas as pd
import time
from datetime import datetime
from components.veh_map import display_map

@st.cache_data
def load_data():
    df = pd.read_csv("./data/merged_cleaned.csv")
    return df

def format_time(time_int):
    time_str = str(time_int)
    dt = datetime.strptime(time_str, "%Y%m%d%H%M%S")
    return dt.strftime("%H:%M:%S")

@st.cache_data
def get_formatted_times(time_range):
    return [format_time(t) for t in time_range]

def update_slider_label():
    current_index = st.session_state.time_slider
    st.session_state.slider_label = f"Time: {formatted_times[current_index]} / {end_time}"

@st.fragment
def display_time_control(df, map_container):
    global formatted_times, end_time

    time_range = df["GPS time"].tolist()
    formatted_times = get_formatted_times(time_range)
    end_time = formatted_times[-1]

    if 'slider_label' not in st.session_state:
        st.session_state.slider_label = f"Time: {formatted_times[0]} / {end_time}"

    st.write(st.session_state.slider_label)
    current_time_index = st.slider(
        "Time",
        0, len(time_range) - 1, 0,
        key="time_slider",
        on_change=update_slider_label,
        format="",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Play", use_container_width=True):
            st.session_state.playing = True

    with col2:
        if st.button("Pause", use_container_width=True):
            st.session_state.playing = False

    with col3:
        if st.button("Restart", use_container_width=True):
            st.session_state.time_slider = 0
            update_slider_label()

    if st.session_state.get("playing", False):
        if current_time_index < len(time_range) - 1:
            st.session_state.time_slider += 1
            time.sleep(0.1)  # Adjust for playback speed
            st.experimental_rerun()
        else:
            st.session_state.playing = False

    with map_container:
        display_map(df, current_time_index)