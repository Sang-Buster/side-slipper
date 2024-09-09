import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import timedelta


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


def create_arrow(x, y, u, v, color, name, opacity=1, showlegend=True):
    return go.Scatter(
        x=[x, x + u],
        y=[y, y + v],
        mode="lines+markers",
        line=dict(color=color, width=2),
        marker=dict(size=[0, 8], symbol=["circle", "arrow-wide"], color=color),
        name=name,
        showlegend=showlegend,
        opacity=opacity,
    )


def create_seg_plot(df, current_time_index, time_range_seconds):
    # Get current data point and the data for the selected time range
    current_data = df.iloc[current_time_index]
    current_time = current_data["datetime"]
    start_time = (
        current_time - timedelta(seconds=time_range_seconds)
        if time_range_seconds
        else df["datetime"].iloc[0]
    )
    selected_data = df[
        (df["datetime"] >= start_time) & (df["datetime"] <= current_time)
    ]

    # Group data by second and calculate mean values
    grouped_data = selected_data.groupby(selected_data["datetime"].dt.floor("s")).mean()

    # Create the base figure
    fig = go.Figure()

    # Plot the traveled path for the selected time range
    fig.add_trace(
        go.Scatter(
            x=grouped_data["Lon_base"],
            y=grouped_data["Lat_base"],
            mode="lines",
            name="Traveled Path",
            line=dict(color="blue", width=2),
        )
    )

    # Plot the three vectors as arrows for each second
    vector_scale = 0.0001  # Adjust this value to scale the vectors appropriately

    for _, row in grouped_data.iterrows():
        # Rover Velocity Vector at CG (vel_cg_XY)
        fig.add_trace(
            create_arrow(
                row["Lon_base"],
                row["Lat_base"],
                row["vel_cg_X"] * vector_scale,
                row["vel_cg_Y"] * vector_scale,
                "red",
                "Rover Velocity at CG",
                opacity=0.7,
                showlegend=_
                == grouped_data.index[0],  # Only show legend for the first arrow
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
                opacity=0.7,
                showlegend=_
                == grouped_data.index[0],  # Only show legend for the first arrow
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
                opacity=0.7,
                showlegend=_
                == grouped_data.index[0],  # Only show legend for the first arrow
            )
        )

    # Update title
    time_range_text = (
        f"Last {time_range_seconds} Seconds" if time_range_seconds else "All Data"
    )
    fig.update_layout(
        title={
            "text": f"Vehicle Segmentation Plot ({time_range_text})",
            "y": 0.01,  # Set the y position to the bottom
            "x": 0.5,  # Center the title
            "xanchor": "center",
            "yanchor": "bottom",
        },
        xaxis_title="Longitude",
        yaxis=dict(
            title=dict(text="Latitude", standoff=10),
            side="right",
            title_standoff=5,
            automargin=True,
        ),
        height=520,
        margin=dict(l=0, r=0, t=20, b=140),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
    )

    # Set axis ranges to focus on the selected time range of data
    x_range = [grouped_data["Lon_base"].min(), grouped_data["Lon_base"].max()]
    y_range = [grouped_data["Lat_base"].min(), grouped_data["Lat_base"].max()]

    # Add some padding to the ranges
    x_padding = (x_range[1] - x_range[0]) * 0.1
    y_padding = (y_range[1] - y_range[0]) * 0.1

    fig.update_xaxes(range=[x_range[0] - x_padding, x_range[1] + x_padding])
    fig.update_yaxes(range=[y_range[0] - y_padding, y_range[1] + y_padding])

    return fig


def update_seg_plot(fig, df, current_time_index, time_range_seconds):
    current_data = df.iloc[current_time_index]
    current_time = current_data["datetime"]
    start_time = (
        current_time - timedelta(seconds=time_range_seconds)
        if time_range_seconds
        else df["datetime"].iloc[0]
    )
    selected_data = df[
        (df["datetime"] >= start_time) & (df["datetime"] <= current_time)
    ]

    grouped_data = selected_data.groupby(selected_data["datetime"].dt.floor("s")).mean()

    # Update the traveled path
    fig.data[0].x = grouped_data["Lon_base"]
    fig.data[0].y = grouped_data["Lat_base"]

    # Remove all existing vector traces
    fig.data = [fig.data[0]]

    # Update the vectors
    vector_scale = 0.0001
    for _, row in grouped_data.iterrows():
        # Add Rover Velocity Vector at CG
        fig.add_trace(
            create_arrow(
                row["Lon_base"],
                row["Lat_base"],
                row["vel_cg_X"] * vector_scale,
                row["vel_cg_Y"] * vector_scale,
                "red",
                "Rover Velocity at CG",
                opacity=0.7,
                showlegend=False,
            )
        )

        # Add Chassis Orientation Vector
        fig.add_trace(
            create_arrow(
                row["Lon_base"],
                row["Lat_base"],
                row["chassis_psi_X"] * vector_scale,
                row["chassis_psi_Y"] * vector_scale,
                "green",
                "Chassis Orientation",
                opacity=0.7,
                showlegend=False,
            )
        )

        # Add Base Velocity Vector at Rear Axle
        fig.add_trace(
            create_arrow(
                row["Lon_base"],
                row["Lat_base"],
                row["vel_rear_X"] * vector_scale,
                row["vel_rear_Y"] * vector_scale,
                "orange",
                "Base Velocity at Rear Axle",
                opacity=0.7,
                showlegend=False,
            )
        )

    # Update title
    time_range_text = (
        f"Last {time_range_seconds} Seconds" if time_range_seconds else "All Data"
    )
    fig.update_layout(
        title={
            "text": f"Vehicle Segmentation Plot ({time_range_text})",
            "y": 0.01,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "bottom",
        }
    )

    # Update axis ranges
    x_range = [grouped_data["Lon_base"].min(), grouped_data["Lon_base"].max()]
    y_range = [grouped_data["Lat_base"].min(), grouped_data["Lat_base"].max()]
    x_padding = (x_range[1] - x_range[0]) * 0.1
    y_padding = (y_range[1] - y_range[0]) * 0.1
    fig.update_xaxes(range=[x_range[0] - x_padding, x_range[1] + x_padding])
    fig.update_yaxes(range=[y_range[0] - y_padding, y_range[1] + y_padding])

    return fig


def display_seg_plot(df, current_time_index):
    df = prepare_seg_plot_data(df)

    # Get the selected time range from session state, with a default value
    time_range_seconds = st.session_state.get("selected_time_range_seconds", 30)

    # Always update the figure
    st.session_state.seg_plot_fig = create_seg_plot(
        df, current_time_index, time_range_seconds
    )

    st.plotly_chart(st.session_state.seg_plot_fig, use_container_width=True)
