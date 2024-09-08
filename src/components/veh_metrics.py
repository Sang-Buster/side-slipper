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
    ).encode(text=alt.value(f"{input_response:.1f}"))
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

def display_vehicle_metrics(df, current_time_index):
    metrics_col = st.columns(2)

    current_data = df.iloc[current_time_index]
    previous_data = df.iloc[max(0, current_time_index - 1)]  # Ensure we don't go below 0

    cog_base = current_data['CoG_base']
    cog_rover = current_data['CoG_rover']
    beta = current_data['beta']
    rel_pos_heading = current_data['relPosHeading']

    # Calculate deltas
    delta_rel_pos_heading = rel_pos_heading - previous_data['relPosHeading']
    delta_beta = beta - previous_data['beta']

    with metrics_col[0]:
        st.metric("Relative Position Heading (°)", f"{rel_pos_heading:.2f}", f"{delta_rel_pos_heading:.2f}")
        st.altair_chart(make_donut(cog_rover, "Rover CoG (°)", "red"))

    with metrics_col[1]:
        st.metric("Side Slip Angle (β°)", f"{beta:.2f}", f"{delta_beta:.2f}")
        st.altair_chart(make_donut(cog_base, "Base CoG (°)", "orange"))
