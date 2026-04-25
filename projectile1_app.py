import math
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import streamlit as st


# ============================
# Cached Physics Engine
# ============================
@st.cache_data
def calculate_projectile(u, theta_deg, g):
    theta = math.radians(theta_deg)
    T = (2 * u * math.sin(theta)) / g
    R = (u ** 2 * math.sin(2 * theta)) / g
    H = (u ** 2 * (math.sin(theta)) ** 2) / (2 * g)
    return T, R, H


@st.cache_data
def get_trajectory(u, theta_deg, g, T_total, num_points=300):
    theta = math.radians(theta_deg)
    t = np.linspace(0, T_total, num_points)
    x = u * math.cos(theta) * t
    y = u * math.sin(theta) * t - 0.5 * g * t ** 2
    return t, x, y


# ============================
# Page Configuration
# ============================
st.set_page_config(
    page_title="PRI Motion Lab",
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
        font-size: 46px;
        font-weight: 850;
        color: #111827;
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
    .insight-card {
        background-color: #EEF6FF;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #BFDBFE;
        margin-top: 16px;
    }
    .footer {
        font-size: 20px;
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
    "<div class='main-title'>🏛️ PRI Motion Lab</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Interactive Projectile System — PRI Framework</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='caption-text'>Explore motion, symmetry, and system response through simplified geometric projectile relationships.</div>",
    unsafe_allow_html=True
)

st.markdown("---")


# ============================
# Sidebar Inputs
# ============================
st.sidebar.title("🧭 System Control Panel")
st.sidebar.caption("Adjust the motion system parameters below.")

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Environment Presets")

preset = st.sidebar.selectbox(
    "Select Environment",
    ["Earth", "Moon", "Mars", "Custom"]
)

if preset == "Earth":
    default_g = 9.81
elif preset == "Moon":
    default_g = 1.62
elif preset == "Mars":
    default_g = 3.71
else:
    default_g = 9.81

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
    value=default_g,
    step=0.1
)

if st.sidebar.button("🔄 Reset System"):
    st.rerun()


# ============================
# Core Projectile Values
# ============================
T_total, R_total, H_max = calculate_projectile(u, theta_deg, g)
t_points, x_points, y_points = get_trajectory(u, theta_deg, g, T_total)


# ============================
# Metrics
# ============================
m1, m2, m3, m4 = st.columns(4)
m1.metric("Maximum Height H", f"{H_max:.2f} m")
m2.metric("Total Range R", f"{R_total:.2f} m")
m3.metric("Flight Time T", f"{T_total:.2f} s")
m4.metric("Environment g", f"{g:.2f} m/s²")

st.markdown("---")


# ============================
# Main Layout
# ============================
col_calc, col_plot = st.columns([1, 2], gap="large")


# ============================
# System Solver
# ============================
with col_calc:
    st.subheader("🔢 System Solver")

    st.markdown("<div class='formula-card'>", unsafe_allow_html=True)
    st.markdown("**Paudelian Research Institute's Derivations**")

    st.latex(r"H = \frac{R}{4}\tan\theta")
    st.latex(r"H = \frac{1}{4}Tu\sin\theta")
    st.latex(r"R = \frac{4H}{\tan\theta}")
    st.latex(r"R = Tu\cos\theta")
    st.latex(r"T = \frac{R}{u\cos\theta}")
    st.latex(r"T = \frac{4H}{u\sin\theta}")

    st.markdown("</div>", unsafe_allow_html=True)

    choice = st.selectbox(
        "Select Solver Mode",
        [
            "1. Find H from R and θ",
            "2. Find H from T, u, θ",
            "3. Find R from H and θ",
            "4. Find R from T, u, θ",
            "5. Find T from R, u, θ",
            "6. Find T from H, u, θ",
        ]
    )

    theta = math.radians(theta_deg)

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
# Motion Dynamics
# ============================
with col_plot:
    st.subheader("📊 Motion Dynamics")

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

    ax.axvline(
        x=peak_x,
        linestyle="--",
        alpha=0.45,
        label="Symmetry Axis (R/2)"
    )

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
        f"Projectile Path: u={u:.1f} m/s, θ={theta_deg:.1f}°, g={g:.2f} m/s²"
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
# Multi-Trajectory Comparison
# ============================
st.markdown("---")
st.subheader("🧭 Multi-Trajectory Comparison")

st.write(
    "Compare multiple launch angles under the same initial speed and gravity. "
    "This reveals how angle controls range, height, and flight time."
)

comparison_angles = st.multiselect(
    "Select launch angles to compare",
    options=[15, 30, 45, 60, 75],
    default=[30, 45, 60]
)

if comparison_angles:
    fig_multi, ax_multi = plt.subplots(figsize=(10, 5.8))

    comparison_rows = []

    for angle in comparison_angles:
        T_c, R_c, H_c = calculate_projectile(u, angle, g)
        _, x_c, y_c = get_trajectory(u, angle, g, T_c)

        ax_multi.plot(
            x_c,
            y_c,
            linewidth=2.3,
            label=f"θ = {angle}°"
        )

        ax_multi.scatter(R_c / 2, H_c, s=45)
        ax_multi.scatter(R_c, 0, s=45)

        comparison_rows.append({
            "Angle θ (deg)": angle,
            "Max Height H (m)": round(H_c, 2),
            "Range R (m)": round(R_c, 2),
            "Flight Time T (s)": round(T_c, 2),
        })

    ax_multi.set_xlabel("Range x (m)")
    ax_multi.set_ylabel("Height y (m)")
    ax_multi.set_title(
        f"Multi-Trajectory Comparison: u={u:.1f} m/s, g={g:.2f} m/s²"
    )
    ax_multi.grid(True, linestyle="--", alpha=0.6)
    ax_multi.set_ylim(bottom=0)
    ax_multi.legend()

    st.pyplot(fig_multi)
    plt.close(fig_multi)

    st.dataframe(comparison_rows, use_container_width=True)

    st.info(
        "The 45° trajectory generally maximizes range under ideal equal-height conditions. "
        "Higher angles increase height and flight time, while lower angles flatten the path."
    )
else:
    st.warning("Select at least one angle to compare.")


# ============================
# System Interpretation
# ============================
st.markdown("---")
st.subheader("🧠 System Interpretation")

if theta_deg < 30:
    interpretation = (
        "Low-angle launch favors horizontal motion. The system produces a flatter arc, "
        "lower peak height, and comparatively longer horizontal reach."
    )
elif theta_deg < 60:
    interpretation = (
        "Mid-angle launch produces a balanced motion state. Around 45°, ideal projectile "
        "motion approaches maximum range because horizontal and vertical components are well-balanced."
    )
else:
    interpretation = (
        "High-angle launch favors vertical motion. The projectile reaches greater height "
        "and remains in flight longer, but horizontal range decreases."
    )

st.markdown(
    f"""
    <div class='insight-card'>
    <b>Current Motion Interpretation</b><br><br>
    {interpretation}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### 🎯 Key Insight")
st.write(
    "Under ideal equal-height conditions, maximum range occurs near **45°**. "
    "This reflects the symmetry between vertical lift and horizontal motion."
)


# ============================
# System Response / Sensitivity Analysis
# ============================
st.markdown("---")
st.subheader("📈 System Response: Sensitivity to Launch Angle θ")

theta_values_deg = np.linspace(5, 85, 200)
theta_values_rad = np.radians(theta_values_deg)

R_values = (u ** 2 * np.sin(2 * theta_values_rad)) / g
H_values = (u ** 2 * (np.sin(theta_values_rad)) ** 2) / (2 * g)
T_values = (2 * u * np.sin(theta_values_rad)) / g

sensitivity_choice = st.selectbox(
    "Choose system response view",
    [
        "Range R vs Angle θ",
        "Height H vs Angle θ",
        "Flight Time T vs Angle θ",
    ]
)

fig2, ax2 = plt.subplots(figsize=(9.5, 4.8))

if sensitivity_choice == "Range R vs Angle θ":
    ax2.plot(theta_values_deg, R_values, linewidth=2.4)
    ax2.axvline(theta_deg, linestyle="--", alpha=0.6)
    ax2.scatter(theta_deg, R_total, s=80)
    ax2.set_ylabel("Range R (m)")
    ax2.set_title("System Response: Range Sensitivity to Launch Angle")

elif sensitivity_choice == "Height H vs Angle θ":
    ax2.plot(theta_values_deg, H_values, linewidth=2.4)
    ax2.axvline(theta_deg, linestyle="--", alpha=0.6)
    ax2.scatter(theta_deg, H_max, s=80)
    ax2.set_ylabel("Maximum Height H (m)")
    ax2.set_title("System Response: Height Sensitivity to Launch Angle")

else:
    ax2.plot(theta_values_deg, T_values, linewidth=2.4)
    ax2.axvline(theta_deg, linestyle="--", alpha=0.6)
    ax2.scatter(theta_deg, T_total, s=80)
    ax2.set_ylabel("Flight Time T (s)")
    ax2.set_title("System Response: Flight Time Sensitivity to Launch Angle")

ax2.set_xlabel("Launch Angle θ (degrees)")
ax2.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig2)
plt.close(fig2)

st.info(
    "Sensitivity analysis reveals how changes in launch angle affect the system response. "
    "This converts formulas into visible behavior."
)


# ============================
# Footer
# ============================
st.markdown("---")
st.markdown(
    "<div class='footer'>© Paudelian Research Institute — PRI Motion Lab</div>",
    unsafe_allow_html=True
)
