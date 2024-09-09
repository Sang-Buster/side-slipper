import streamlit as st
import plotly.graph_objects as go


def display_vehicle_data(df, current_time_index):
    # Get current data
    current_data = df.iloc[current_time_index]

    # Calculate speed in mph
    speed = (
        (
            current_data["VX_base"] ** 2
            + current_data["VY_base"] ** 2
            + current_data["VZ_base"] ** 2
        )
        ** 0.5
    ) * 2.23694
    max_speed = 140

    # Speedometer
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
                "steps": [
                    {"range": [0, 40], "color": "#61afef"},
                    {"range": [40, 80], "color": "#98c379"},
                    {"range": [80, 120], "color": "#e5c07b"},
                    {"range": [120, max_speed], "color": "#e06c75"},
                ],
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
        st.metric("Latitude (°)", f"{current_data['Lat_base']:.6f}")
    with col2:
        st.metric("Longitude (°)", f"{current_data['Lon_base']:.6f}")

    # Velocity
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Velocity X (m/s)", f"{current_data['VX_base']:.2f}")
    with col2:
        st.metric("Velocity Y (m/s)", f"{current_data['VY_base']:.2f}")
    with col3:
        st.metric("Velocity Z (m/s)", f"{current_data['VZ_base']:.2f}")
