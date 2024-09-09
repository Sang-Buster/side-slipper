import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


@st.cache_data
def prepare_seg_plot_data(df):
    # Convert GPS time to datetime
    df["datetime"] = pd.to_datetime(df["GPS time"], format="%Y%m%d%H%M%S")

    # Calculate necessary data for vectors
    df["rover_spd"] = np.sqrt(
        df["VX_rover"] ** 2 + df["VY_rover"] ** 2 + df["VZ_rover"] ** 2
    )
    df["base_spd"] = np.sqrt(
        df["VX_base"] ** 2 + df["VY_base"] ** 2 + df["VZ_base"] ** 2
    )

    # Calculate vector components
    df["vel_cg_X"] = df["rover_spd"] * np.sin(np.radians(df["CoG_rover"]))
    df["vel_cg_Y"] = df["rover_spd"] * np.cos(np.radians(df["CoG_rover"]))

    df["chassis_psi_X"] = df["rover_spd"] * np.sin(np.radians(df["relPosHeading"]))
    df["chassis_psi_Y"] = df["rover_spd"] * np.cos(np.radians(df["relPosHeading"]))

    df["vel_rear_X"] = df["base_spd"] * np.sin(np.radians(df["CoG_base"]))
    df["vel_rear_Y"] = df["base_spd"] * np.cos(np.radians(df["CoG_base"]))

    return df


def create_arrow(x, y, u, v, color, name, opacity=1):
    return go.Scatter(
        x=[x, x + u],
        y=[y, y + v],
        mode="lines+markers",
        line=dict(color=color, width=2),
        marker=dict(size=[0, 8], symbol=["circle", "arrow-wide"], color=color),
        name=name,
        showlegend=True,
        opacity=opacity,
    )


def create_seg_plot(df, current_time_index):
    # Get current data point and the data for the last 30 seconds
    current_data = df.iloc[current_time_index]
    current_time = current_data["datetime"]
    start_time = current_time - timedelta(seconds=30)
    last_30_seconds = df[
        (df["datetime"] >= start_time) & (df["datetime"] <= current_time)
    ]

    # Create the base figure
    fig = go.Figure()

    # Plot the traveled path for the last 30 seconds
    fig.add_trace(
        go.Scatter(
            x=last_30_seconds["Lon_base"],
            y=last_30_seconds["Lat_base"],
            mode="lines",
            name="Traveled Path",
            line=dict(color="blue", width=2),
        )
    )

    # Plot the three vectors as arrows for each data point
    vector_scale = 0.0001  # Adjust this value to scale the vectors appropriately

    for index, row in last_30_seconds.iterrows():
        opacity = 0.3 if index != current_time_index else 1

        # Rover Velocity Vector at CG (vel_cg_XY)
        fig.add_trace(
            create_arrow(
                row["Lon_base"],
                row["Lat_base"],
                row["vel_cg_X"] * vector_scale,
                row["vel_cg_Y"] * vector_scale,
                "red",
                "Rover Velocity at CG",
                opacity,
            )
        )

        # Chassis Orientation Vector (chassis_psi_XY)
        fig.add_trace(
            create_arrow(
                row["Lon_base"],
                row["Lat_base"],
                row["chassis_psi_X"] * vector_scale,
                row["chassis_psi_Y"] * vector_scale,
                "green",
                "Chassis Orientation",
                opacity,
            )
        )

        # Base Velocity Vector at Rear Axle (vel_rear_XY)
        fig.add_trace(
            create_arrow(
                row["Lon_base"],
                row["Lat_base"],
                row["vel_rear_X"] * vector_scale,
                row["vel_rear_Y"] * vector_scale,
                "orange",
                "Base Velocity at Rear Axle",
                opacity,
            )
        )

    # Update layout
    fig.update_layout(
        title="Vehicle Segmentation Plot (Last 30 Seconds)",
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        legend_title="Vectors",
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
    )

    # Set axis ranges to focus on the last 30 seconds of data
    x_range = [last_30_seconds["Lon_base"].min(), last_30_seconds["Lon_base"].max()]
    y_range = [last_30_seconds["Lat_base"].min(), last_30_seconds["Lat_base"].max()]

    # Add some padding to the ranges
    x_padding = (x_range[1] - x_range[0]) * 0.1
    y_padding = (y_range[1] - y_range[0]) * 0.1

    fig.update_xaxes(range=[x_range[0] - x_padding, x_range[1] + x_padding])
    fig.update_yaxes(range=[y_range[0] - y_padding, y_range[1] + y_padding])

    return fig


def display_seg_plot(df, current_time_index):
    df = prepare_seg_plot_data(df)
    fig = create_seg_plot(df, current_time_index)
    st.plotly_chart(fig, use_container_width=True)
