import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ============================
# 1. Branding & Page Config
# ============================
st.set_page_config(
    page_title="PRI Projectile Motion",
    page_icon="🚀",
    layout="wide"
)

# Header with PRI Branding
st.title("🏛️ Paudelian Research Institute")
st.subheader("Simplified Projectile Motion Calculator")
st.markdown("---")

# ============================
# 2. Input Parameters (Sidebar)
# ============================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2038/2038171.png", width=100)  # Optional icon
st.sidebar.title("PRI Control Panel")
u = st.sidebar.number_input("Initial speed u (m/s)", min_value=0.1, value=50.0, step=1.0)
theta_deg = st.sidebar.number_input("Launch angle θ (deg)", min_value=0.1, max_value=89.9, value=45.0, step=1.0)
g = st.sidebar.number_input("Gravity g (m/s²)", min_value=0.1, value=9.81, step=0.1)

theta = math.radians(theta_deg)

# ============================
# 3. Main Layout: Two Columns
# ============================
col_calc, col_plot = st.columns([1, 1.5], gap="large")

with col_calc:
    st.markdown("### 🔢 Formula Calculator")
    choice = st.selectbox(
        "Select Formula Mode",
        [
            "1. Find H from R and θ",
            "2. Find H from T, u, θ",
            "3. Find R from H and θ",
            "4. Find R from T, u, θ",
            "5. Find T from R, u, θ",
            "6. Find T from H, u, θ",
        ]
    )

    # Logic for the 6 PRI Formulas
    if "1." in choice:
        R_val = st.number_input("Known Range R (m)", value=100.0)
        res = (R_val / 4) * math.tan(theta)
        st.success(f"**Calculated Height H = {res:.4f} m**")

    elif "2." in choice:
        T_val = st.number_input("Known Time T (s)", value=5.0)
        res = 0.25 * T_val * u * math.sin(theta)
        st.success(f"**Calculated Height H = {res:.4f} m**")

    elif "3." in choice:
        H_val = st.number_input("Known Height H (m)", value=25.0)
        res = (4 * H_val) / math.tan(theta)
        st.success(f"**Calculated Range R = {res:.4f} m**")

    elif "4." in choice:
        T_val = st.number_input("Known Time T (s)", value=5.0)
        res = T_val * u * math.cos(theta)
        st.success(f"**Calculated Range R = {res:.4f} m**")

    elif "5." in choice:
        R_val = st.number_input("Known Range R (m)", value=100.0)
        res = R_val / (u * math.cos(theta))
        st.success(f"**Calculated Time T = {res:.4f} s**")

    elif "6." in choice:
        H_val = st.number_input("Known Height H (m)", value=25.0)
        res = (4 * H_val) / (u * math.sin(theta))
        st.success(f"**Calculated Time T = {res:.4f} s**")

    st.caption("PRI Simplified Relationships: No air resistance assumed.")

with col_plot:
    st.markdown("### 📊 Trajectory Visualization")

    # Calculate trajectory points
    T_total = (2 * u * math.sin(theta)) / g
    t_points = np.linspace(0, T_total, 200)
    x_points = u * math.cos(theta) * t_points
    y_points = u * math.sin(theta) * t_points - 0.5 * g * t_points ** 2

    # Create the figure
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x_points, y_points, color='#1E88E5', linewidth=2.5)
    ax.fill_between(x_points, y_points, alpha=0.1, color='#1E88E5')
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Visualized Projectile Path")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_ylim(bottom=0)

    st.pyplot(fig)

# ============================
# 4. Footer
# ============================
st.markdown("---")
st.info("© 2025 Paudelian Research Institute (PRI) | Science & Research Tools")
