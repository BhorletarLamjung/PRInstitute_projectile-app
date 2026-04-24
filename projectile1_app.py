import math
import numpy as np
import pandas as pd
import streamlit as st

# Force wide mode so everything fits on one screen
st.set_page_config(page_title="PRI Projectile Motion", layout="wide")

st.title("🚀 Projectile Motion Dashboard")

# 1. Setup the layout (Left for inputs, Right for the Graph)
col_input, col_graph = st.columns([1, 2])

with col_input:
    st.subheader("Settings")
    u = st.number_input("Initial speed (m/s)", value=50.0)
    theta_deg = st.number_input("Launch angle (°)", value=45.0)
    g = st.number_input("Gravity (m/s²)", value=9.81)

    st.divider()

    st.subheader("Manual Calculator")
    mode = st.selectbox("I want to find:", ["Height (H)", "Range (R)", "Time (T)"])
    st.info("Input known values below to solve.")

with col_graph:
    # --- MATH SECTION ---
    theta_rad = math.radians(theta_deg)
    t_total = (2 * u * math.sin(theta_rad)) / g

    # Generate points for the graph
    t_points = np.linspace(0, t_total, 100)
    x = u * math.cos(theta_rad) * t_points
    y = u * math.sin(theta_rad) * t_points - 0.5 * g * t_points ** 2

    # Put data in a format Streamlit loves (a DataFrame)
    chart_data = pd.DataFrame({"Distance (m)": x, "Height (m)": y})
    chart_data = chart_data.set_index("Distance (m)")

    # --- PLOT SECTION ---
    st.subheader("Trajectory Path")
    # Using st.line_chart is MUCH more reliable than st.pyplot
    st.line_chart(chart_data)

    # Big Metrics at the bottom of the graph
    m1, m2 = st.columns(2)
    m1.metric("Max Range", f"{max(x):.2f} m")
    m2.metric("Flight Time", f"{t_total:.2f} s")