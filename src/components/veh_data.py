import streamlit as st
import plotly.graph_objects as go


def display_vehicle_data():
    st.markdown(
        "<h3 style='text-align: center;'>Vehicle Data</h3>", unsafe_allow_html=True
    )

    # Speedometer
    speed = 60
    max_speed = 140

    # Create color gradient
    colors = ["lightblue", "cyan", "lime", "yellow", "orange", "red"]
    n_colors = len(colors)
    color_steps = []
    for i in range(n_colors - 1):
        start = i * max_speed / (n_colors - 1)
        end = (i + 1) * max_speed / (n_colors - 1)
        color_steps.extend(
            [
                {"range": [start, (start + end) / 2], "color": colors[i]},
                {"range": [(start + end) / 2, end], "color": colors[i + 1]},
            ]
        )

    fig_speed = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=speed,
            title={"text": "Speed (mph)"},
            gauge={
                "axis": {
                    "range": [None, max_speed],
                    "tickmode": "linear",
                    "tick0": 0,
                    "dtick": 10,
                    "tickwidth": 1,
                    "tickcolor": "darkblue",
                },
                "bar": {"color": "rgba(0,0,0,0)"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": color_steps,
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": speed,
                },
            },
        )
    )

    fig_speed.update_layout(
        height=290,
        margin=dict(l=25, r=25, t=50, b=5),
    )
    st.plotly_chart(fig_speed, use_container_width=True)

    # Lat, Lon
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Latitude (°)", "37.7749")
    with col2:
        st.metric("Longitude (°)", "-122.4194")

    # Velocity
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Velocity X (m/s)", "10.5")
    with col2:
        st.metric("Velocity Y (m/s)", "5.2")
    with col3:
        st.metric("Velocity Z (m/s)", "0.1")
