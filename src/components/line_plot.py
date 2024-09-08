import streamlit as st
import pandas as pd
import altair as alt


def display_multi_select_and_line_plot():
    st.multiselect(
        "Select metrics to display",
        ["Speed", "Side Slip Angle", "Yaw Rate", "Lateral Acceleration"],
    )

    chart_data = pd.DataFrame({"time": range(100), "value": range(100)})
    st.altair_chart(
        alt.Chart(chart_data).mark_line().encode(x="time", y="value"),
        use_container_width=True,
    )
