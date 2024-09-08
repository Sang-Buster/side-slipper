import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
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


def display_time_control(df, map_container, map_style):
    time_range = df["GPS time"].tolist()
    formatted_times = get_formatted_times(time_range)
    end_time = formatted_times[-1]

    if "current_time_index" not in st.session_state:
        st.session_state.current_time_index = 0

    current_time = formatted_times[st.session_state.current_time_index]
    st.write(f"Time: {current_time} / {end_time}")

    st.slider(
        "Time",
        0,
        len(time_range) - 1,
        st.session_state.current_time_index,
        key="time_slider",
        on_change=lambda: st.session_state.update(
            {"current_time_index": st.session_state.time_slider}
        ),
        format="",
        label_visibility="collapsed",
    )

    def adjust_time(seconds):
        current_time_int = time_range[st.session_state.current_time_index]
        current_time_str = str(current_time_int).zfill(14)  # Ensure 14 digits
        current_time = datetime.strptime(current_time_str, "%Y%m%d%H%M%S")
        target_time = current_time + timedelta(seconds=seconds)
        target_time_int = int(target_time.strftime("%Y%m%d%H%M%S"))
        new_index = min(
            max(0, df[df["GPS time"] >= target_time_int].index.min()),
            len(time_range) - 1,
        )
        if pd.isna(new_index):
            new_index = len(time_range) - 1 if seconds > 0 else 0
        return int(new_index)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        if st.button("-10s", use_container_width=True):
            st.session_state.current_time_index = adjust_time(-10)
    with col2:
        if st.button("-5s", use_container_width=True):
            st.session_state.current_time_index = adjust_time(-5)
    with col3:
        if st.button("-1s", use_container_width=True):
            st.session_state.current_time_index = adjust_time(-1)
    with col4:
        if st.button("+1s", use_container_width=True):
            st.session_state.current_time_index = adjust_time(1)
    with col5:
        if st.button("+5s", use_container_width=True):
            st.session_state.current_time_index = adjust_time(5)
    with col6:
        if st.button("+10s", use_container_width=True):
            st.session_state.current_time_index = adjust_time(10)

    with map_container:
        display_map(df, st.session_state.current_time_index, map_style=map_style)

    # Force a rerun if the current_time_index has changed
    if st.session_state.current_time_index != st.session_state.time_slider:
        st.rerun()
