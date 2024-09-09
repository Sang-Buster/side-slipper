import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@st.cache_data
def prepare_plot_data(df, selected_columns):
    return {col: df[col] for col in selected_columns}


def create_initial_plot(df, selected_columns, plot_data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for column in selected_columns:
        fig.add_trace(
            go.Scatter(
                x=df["datetime"], y=plot_data[column], mode="lines", name=column
            ),
            secondary_y=False,
        )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Value",
        legend_title="Data",
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    fig.update_xaxes(
        tickformat="%H:%M:%S",
        dtick=60000,  # Show tick every 60 seconds
        tickangle=45,
    )

    return fig


def update_plot(fig, df, selected_columns, plot_data, current_time_index):
    current_time = df["datetime"].iloc[current_time_index]

    for i, column in enumerate(selected_columns):
        fig.data[i].x = df["datetime"][: current_time_index + 1]
        fig.data[i].y = plot_data[column][: current_time_index + 1]

    fig.layout.shapes = []  # Clear existing shapes
    fig.add_vline(
        x=current_time, line_dash="dash", line_color="red", name="Current Time"
    )

    # Update x-axis range to show a fixed time window (e.g., last 5 minutes)
    time_window = pd.Timedelta(minutes=5)
    x_min = max(df["datetime"].iloc[0], current_time - time_window)
    x_max = current_time + pd.Timedelta(seconds=10)  # Add a small buffer
    fig.update_xaxes(range=[x_min, x_max])

    return fig


def display_multi_select_and_line_plot(df, current_time_index):
    plottable_columns = [
        "CoG_base",
        "Lat_base",
        "Lon_base",
        "VX_base",
        "VY_base",
        "VZ_base",
        "CoG_rover",
        "Lat_rover",
        "Lon_rover",
        "VX_rover",
        "VY_rover",
        "VZ_rover",
        "relPosHeading",
        "beta",
    ]

    selected_columns = st.multiselect(
        "Select data to visualize:",
        plottable_columns,
        default=["CoG_base", "CoG_rover"],
    )

    if selected_columns:
        df["datetime"] = pd.to_datetime(df["GPS time"], format="%Y%m%d%H%M%S")
        plot_data = prepare_plot_data(df, selected_columns)

        # Use session state to store the figure
        if (
            "line_plot_fig" not in st.session_state
            or st.session_state.line_plot_selected_columns != selected_columns
        ):
            st.session_state.line_plot_fig = create_initial_plot(
                df, selected_columns, plot_data
            )
            st.session_state.line_plot_selected_columns = selected_columns

        # Update the plot with current data
        fig = update_plot(
            st.session_state.line_plot_fig,
            df,
            selected_columns,
            plot_data,
            current_time_index,
        )

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Please select at least one column to visualize.")
