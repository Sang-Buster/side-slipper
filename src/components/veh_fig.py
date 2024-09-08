import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def create_vehicle_plot(heading_angle, velocity_angle):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Vehicle body
    vehicle_length = 2
    vehicle_width = 1
    vehicle = Rectangle(
        (-vehicle_width / 2, -vehicle_length / 2),
        vehicle_width,
        vehicle_length,
        fill=False,
        color="black",
    )
    ax.add_patch(vehicle)

    # Wheels aligned with heading angle
    wheel_width = 0.2
    wheel_length = 0.4
    wheel_positions = [
        (-vehicle_width / 2, -vehicle_length / 2.5 + wheel_length / 2),
        (-vehicle_width / 2, vehicle_length / 2.5 - wheel_length / 2),
        (vehicle_width / 2, -vehicle_length / 2.5 + wheel_length / 2),
        (vehicle_width / 2, vehicle_length / 2.5 - wheel_length / 2),
    ]

    for x, y in wheel_positions:
        # Wheels aligned with the heading angle
        wheel = Rectangle(
            (x - wheel_width / 2, y - wheel_length / 2),
            wheel_width,
            wheel_length,
            angle=heading_angle,
            fill=True,
            color="gray",
        )
        ax.add_patch(wheel)

    # Heading vector
    heading_x = np.sin(np.radians(heading_angle))
    heading_y = np.cos(np.radians(heading_angle))
    ax.arrow(
        0,
        0,
        heading_x,
        heading_y,
        color="blue",
        width=0.02,
        head_width=0.1,
        head_length=0.1,
        label="Heading",
    )

    # Velocity vector
    velocity_x = np.sin(np.radians(velocity_angle))
    velocity_y = np.cos(np.radians(velocity_angle))
    ax.arrow(
        0,
        0,
        velocity_x,
        velocity_y,
        color="red",
        width=0.02,
        head_width=0.1,
        head_length=0.1,
        label="Velocity",
    )

    # Beta (slip angle) calculation
    beta = velocity_angle - heading_angle

    # Adding the beta slip angle as a dashed green line
    slip_x = velocity_x - heading_x
    slip_y = velocity_y - heading_y
    ax.arrow(
        heading_x,
        heading_y,
        slip_x,
        slip_y,
        color="green",
        linestyle="dashed",
        width=0.01,
        head_width=0.05,
        head_length=0.05,
        label="Slip Angle (β)",
    )

    # Plot limits and appearance
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal", adjustable="box")

    # Beta angle text with green color
    ax.text(
        -0.03,
        0.88,
        f"β:   {beta:.2f}°",
        fontsize=20,
        color="green",
        horizontalalignment="left",
        verticalalignment="top",
        transform=ax.transAxes,
    )

    # Adding a legend for heading, velocity, and slip angle
    ax.legend(loc="upper left", bbox_to_anchor=(-0.1, 1.1), fontsize=18)

    # Removing axis lines for clarity
    ax.axis("off")

    # Adjust the layout to make room for the legend and text
    plt.tight_layout()

    return fig


def display_vehicle_figure():
    st.markdown(
        "<h3 style='text-align: center; margin-bottom: 50px;'>Vehicle Metrics</h3>",
        unsafe_allow_html=True,
    )

    # Example heading and velocity angles
    heading_angle = 55  # You can make this dynamic later
    velocity_angle = 35  # You can make this dynamic later

    # Create and display the figure
    fig = create_vehicle_plot(heading_angle, velocity_angle)
    st.pyplot(fig, clear_figure=True, use_container_width=True)
