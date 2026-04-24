import math
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import streamlit as st


# ============================
# Page Configuration
# ============================
st.set_page_config(
    page_title="PRI Projectile Motion",
    page_icon="🚀",
    layout="wide"
)


# ============================
# Custom Styling
# ============================
st.markdown(
    """
    <style>
    .main-title {
        font-size: 44px;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 24px;
        font-weight: 600;
        color: #374151;
        margin-top: 0px;
    }
    .caption-text {
        font-size: 16px;
        color: #6B7280;
    }
    .formula-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #CBD5E1;
        margin-bottom: 20px;
    }
    .footer {
        font-size: 14px;
        color: #6B7280;
        text-align: center;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================
# Header
# ============================
st.markdown(
    "<div class='main-title'>🏛️ Paudelian Research Institute</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>🚀 Projectile Motion System — PRI Framework</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='caption-text'>Interactive scientific tool for exploring simplified geometric relationships among height H, range R, and flight time T.</div>",
    unsafe_allow_html=True
)

st.markdown("---")


# ============================
# Sidebar Inputs
# ============================
st.sidebar.title("🧭 PRI Control Panel")
st.sidebar.caption("Adjust the system parameters below.")

u = st.sidebar.number_input(
    "Initial speed u (m/s)",
    min_value=0.1,
    value=50.0,
    step=1.0
)

theta_deg = st.sidebar.number_input(
    "Launch angle θ (degrees)",
    min_value=0.1,
    max_value=89.9,
    value=45.0,
    step=1.0
)

g = st.sidebar.number_input(
    "Gravity g (m/s²)",
    min_value=0.1,
    value=9.81,
    step=0.1
)

theta = math.radians(theta_deg)


# ============================
# Standard Projectile Values
# ============================
T_total = (2 * u * math.sin(theta)) / g
R_total = (u ** 2 * math.sin(2 * theta)) / g
H_max = (u ** 2 * (math.sin(theta)) ** 2) / (2 * g)


# ============================
# Metrics
# ============================
m1, m2, m3 = st.columns(3)
m1.metric("Maximum Height H", f"{H_max:.2f} m")
m2.metric("Total Range R", f"{R_total:.2f} m")
m3.metric("Flight Time T", f"{T_total:.2f} s")

st.markdown("---")


# ============================
# Main Layout
# ============================
col_calc, col_plot = st.columns([1, 2], gap="large")


# ============================
# Formula Calculator
# ============================
with col_calc:
    st.subheader("🔢 Formula Calculator")

    st.markdown("<div class='formula-card'>", unsafe_allow_html=True)
    st.markdown("**PRI Simplified Relations**")

    st.latex(r"H = \frac{R}{4}\tan\theta")
    st.latex(r"H = \frac{1}{4}Tu\sin\theta")
    st.latex(r"R = \frac{4H}{\tan\theta}")
    st.latex(r"R = Tu\cos\theta")
    st.latex(r"T = \frac{R}{u\cos\theta}")
    st.latex(r"T = \frac{4H}{u\sin\theta}")

    st.markdown("</div>", unsafe_allow_html=True)

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

    if choice == "1. Find H from R and θ":
        R_val = st.number_input("Known Range R (m)", min_value=0.0, value=100.0)
        result = (R_val / 4) * math.tan(theta)
        st.success(f"Calculated Height H = {result:.4f} m")

    elif choice == "2. Find H from T, u, θ":
        T_val = st.number_input("Known Time T (s)", min_value=0.0, value=5.0)
        result = 0.25 * T_val * u * math.sin(theta)
        st.success(f"Calculated Height H = {result:.4f} m")

    elif choice == "3. Find R from H and θ":
        H_val = st.number_input("Known Height H (m)", min_value=0.0, value=25.0)
        result = (4 * H_val) / math.tan(theta)
        st.success(f"Calculated Range R = {result:.4f} m")

    elif choice == "4. Find R from T, u, θ":
        T_val = st.number_input("Known Time T (s)", min_value=0.0, value=5.0)
        result = T_val * u * math.cos(theta)
        st.success(f"Calculated Range R = {result:.4f} m")

    elif choice == "5. Find T from R, u, θ":
        R_val = st.number_input("Known Range R (m)", min_value=0.0, value=100.0)
        result = R_val / (u * math.cos(theta))
        st.success(f"Calculated Time T = {result:.4f} s")

    elif choice == "6. Find T from H, u, θ":
        H_val = st.number_input("Known Height H (m)", min_value=0.0, value=25.0)
        result = (4 * H_val) / (u * math.sin(theta))
        st.success(f"Calculated Time T = {result:.4f} s")

    st.info(
        "Assumptions: equal launch/landing height, ideal motion, no air resistance."
    )


# ============================
# Trajectory Visualization
# ============================
with col_plot:
    st.subheader("📊 Trajectory Visualization")

    t_points = np.linspace(0, T_total, 300)

    x_points = u * math.cos(theta) * t_points
    y_points = u * math.sin(theta) * t_points - 0.5 * g * t_points ** 2

    peak_x = R_total / 2
    peak_y = H_max

    fig, ax = plt.subplots(figsize=(9.5, 5.8))

    ax.plot(
        x_points,
        y_points,
        linewidth=2.7,
        label="Projectile Path"
    )

    ax.fill_between(
        x_points,
        y_points,
        alpha=0.15
    )

    # Midpoint symmetry line
    ax.axvline(
        x=peak_x,
        linestyle="--",
        alpha=0.45,
        label="Symmetry Axis (R/2)"
    )

    # Peak and landing markers
    ax.scatter(
        peak_x,
        peak_y,
        s=90,
        label="Peak Height"
    )

    ax.scatter(
        R_total,
        0,
        s=90,
        label="Landing Point"
    )

    ax.annotate(
        f"Peak\nH = {H_max:.2f} m\nx = R/2",
        xy=(peak_x, peak_y),
        xytext=(peak_x * 0.82, peak_y + H_max * 0.20),
        arrowprops=dict(arrowstyle="->"),
        fontsize=10
    )

    ax.annotate(
        f"Landing\nR = {R_total:.2f} m",
        xy=(R_total, 0),
        xytext=(R_total * 0.68, H_max * 0.20),
        arrowprops=dict(arrowstyle="->"),
        fontsize=10
    )

    ax.set_xlabel("Range x (m)")
    ax.set_ylabel("Height y (m)")
    ax.set_title(
        f"Projectile Path: u={u:.1f} m/s, θ={theta_deg:.1f}°"
    )

    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_ylim(bottom=0)
    ax.legend()

    st.pyplot(fig)
    plt.close(fig)

    st.info(
        "The peak occurs at half the total range, revealing the symmetry of ideal projectile motion. "
        "PRI simplified relations express this structure through compact geometric formulas."
    )


# ============================
# Footer
# ============================
st.markdown("---")
st.markdown(
    "<div class='footer'>© Paudelian Research Institute — Interactive Scientific Tool</div>",
    unsafe_allow_html=True
)
