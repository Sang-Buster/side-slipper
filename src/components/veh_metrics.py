import streamlit as st
import pandas as pd
import altair as alt


def make_donut(input_response, input_text, input_color):
    if input_color == "blue":
        chart_color = ["#29b5e8", "#155F7A"]
    elif input_color == "green":
        chart_color = ["#27AE60", "#12783D"]
    elif input_color == "orange":
        chart_color = ["#F39C12", "#875A12"]
    elif input_color == "red":
        chart_color = ["#E74C3C", "#781F16"]

    source = pd.DataFrame(
        {"Topic": ["", input_text], "% value": [100 - input_response, input_response]}
    )
    source_bg = pd.DataFrame({"Topic": ["", input_text], "% value": [100, 0]})

    plot = (
        alt.Chart(source)
        .mark_arc(innerRadius=45, cornerRadius=25)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic:N",
                scale=alt.Scale(domain=[input_text, ""], range=chart_color),
                legend=None,
            ),
        )
        .properties(width=130, height=130)
    )

    text = plot.mark_text(
        align="center",
        color="#29b5e8",
        font="Lato",
        fontSize=32,
        fontWeight=700,
        fontStyle="italic",
    ).encode(text=alt.value(f"{input_response}"))
    plot_bg = (
        alt.Chart(source_bg)
        .mark_arc(innerRadius=45, cornerRadius=20)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic:N",
                scale=alt.Scale(domain=[input_text, ""], range=chart_color),
                legend=None,
            ),
        )
        .properties(width=130, height=130)
    )
    return plot_bg + plot + text


def display_vehicle_metrics():
    metrics_col = st.columns(2)

    yaw_rate = 0.5
    cg = 180
    lateral_acceleration = 2.5
    beta = 5

    with metrics_col[0]:
        st.altair_chart(make_donut(yaw_rate, "Yaw Rate (rad/s)", "orange"))
        st.metric("Lateral Acc (m/s²)", f"{lateral_acceleration}", delta="-0.1")

    with metrics_col[1]:
        st.altair_chart(make_donut(cg, "Center of Gravity (°)", "red"))
        st.metric("Side Slip Angle (β°)", f"{beta}", delta="1.2")
