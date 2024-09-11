import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@st.cache_data
def prepare_line_plot_data(df, selected_columns):
    return {col: df[col] for col in selected_columns}


def create_initial_plot(df, selected_columns, time_range_seconds):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    current_time = df["datetime"].iloc[-1]
    start_time = (
        current_time - pd.Timedelta(seconds=time_range_seconds)
        if time_range_seconds
        else df["datetime"].iloc[0]
    )
    selected_data = df[
        (df["datetime"] >= start_time) & (df["datetime"] <= current_time)
    ]

    # Group data by second and calculate mean values
    grouped_data = selected_data.groupby(selected_data["datetime"].dt.floor("s")).mean()

    for column in selected_columns:
        fig.add_trace(
            go.Scatter(
                x=grouped_data.index,
                y=grouped_data[column],
                mode="lines",
                name=column
            ),
            secondary_y=False,
        )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Value",
        margin=dict(l=0, r=0, t=0, b=100),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
    )

    return fig


def update_plot(
    fig, df, selected_columns, current_time_index, time_range_seconds
):
    current_time = df["datetime"].iloc[current_time_index]
    start_time = (
        current_time - pd.Timedelta(seconds=time_range_seconds)
        if time_range_seconds
        else df["datetime"].iloc[0]
    )
    selected_data = df[
        (df["datetime"] >= start_time) & (df["datetime"] <= current_time)
    ]

    # Group data by second and calculate mean values
    grouped_data = selected_data.groupby(selected_data["datetime"].dt.floor("s")).mean()

    for i, column in enumerate(selected_columns):
        fig.data[i].x = grouped_data.index
        fig.data[i].y = grouped_data[column]

    fig.layout.shapes = []  # Clear existing shapes
    fig.add_vline(
        x=current_time, line_dash="dash", line_color="red", name="Current Time"
    )

    # Update x-axis range
    x_min = grouped_data.index[0]
    x_max = current_time + pd.Timedelta(seconds=10)  # Add a small buffer

    # Adjust x-axis format and tick frequency based on the time range
    if time_range_seconds is None or time_range_seconds > 300:
        dtick = 3600000  # 1 hour in milliseconds
        tickformat = "%H:%M"
    elif time_range_seconds > 60:
        dtick = 60000  # 1 minute in milliseconds
        tickformat = "%H:%M:%S"
    else:
        dtick = 10000  # 10 seconds in milliseconds
        tickformat = "%H:%M:%S"

    fig.update_xaxes(
        range=[x_min, x_max],
        tickformat=tickformat,
        dtick=dtick,
        tickangle=45,
    )

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

    # Add time range selector
    time_range_options = {
        "Last 30 seconds": 30,
        "Last 1 minute": 60,
        "Last 3 minutes": 180,
        "Last 5 minutes": 300,
        "All": None,
    }

    def update_time_range():
        st.session_state.selected_time_range_seconds = time_range_options[
            st.session_state.selected_time_range
        ]
        if "line_plot_fig" in st.session_state:
            del st.session_state.line_plot_fig

    selected_time_range = st.selectbox(
        "Select time range to display:",
        options=list(time_range_options.keys()),
        index=0,  # Default to "30 seconds"
        key="selected_time_range",
        on_change=update_time_range,
    )

    # Store the selected time range in session state
    st.session_state.selected_time_range_seconds = time_range_options[
        selected_time_range
    ]

    if selected_columns:
        df["datetime"] = pd.to_datetime(df["GPS time"], format="%Y%m%d%H%M%S")

        # Use session state to store the figure
        if (
            "line_plot_fig" not in st.session_state
            or st.session_state.line_plot_selected_columns != selected_columns
            or st.session_state.line_plot_time_range != selected_time_range
        ):
            st.session_state.line_plot_fig = create_initial_plot(
                df, selected_columns, time_range_options[selected_time_range]
            )
            st.session_state.line_plot_selected_columns = selected_columns
            st.session_state.line_plot_time_range = selected_time_range

        # Update the plot with current data
        fig = update_plot(
            st.session_state.line_plot_fig,
            df,
            selected_columns,
            current_time_index,
            time_range_options[selected_time_range],
        )

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Please select at least one column to visualize.")
