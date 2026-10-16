import math
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Sensory Glove Live Demo", layout="centered"
)

st.title("Gant sensoriel: Visualisation de la flexion")
st.markdown(
    "Démo en direct de la flexion et de la tension au pont selon la résistance du capteur"
)

# 1. Slider for Flex Sensor Resistance
r_flex = st.slider(
    "Résistance du capteur de flexion ($R_{flex}$ en k$\\Omega$)",
    min_value=25.0,
    max_value=62.5,
    value=30.0,
    step=1.0,
)

# 2. Calculations based on circuit equations
# Bridge voltage with R2 = 40 kΩ and flex sensor on top
v_bridge = 5.0 * (40.0 / (r_flex + 40.0))

# Angle calculation
theta = 90 - 18.0 * (4.425 * (v_bridge - 1.95))
theta_display = max(0.0, min(theta, 110.0))

# Display Metrics side by side
col1, col2, col3 = st.columns(3)
col1.metric("Résistance du capteur", f"{r_flex:.1f} kΩ")
col2.metric("Tension au pont", f"{v_bridge:.3f} V")
col3.metric("Angle calculé (θ)", f"{theta_display:.1f}°")

# 3. Draw the Finger (Bending DOWNWARDS)
fig, ax = plt.subplots(figsize=(6, 4))

# Finger dimensions (segment lengths)
L1 = 3.0  # Proximal phalanx (Knuckle to Middle Joint)
L2 = 2.5  # Distal phalanx (Middle Joint to Fingertip)

# Joint coordinates starting at origin (0,0)
x0, y0 = 0.0, 0.0
x1, y1 = L1, 0.0  # Middle joint extends horizontally right

# Fingertip coordinates (bending DOWNWARDS by using negative sine)
theta_rad = math.radians(theta_display)
x2 = x1 + L2 * math.cos(theta_rad)
y2 = y1 - L2 * math.sin(theta_rad)  


# Conditional color logic: Red if > 45°, otherwise Blue
if theta_display > 45.0:
    finger_color = "#d62728"  # Professional Red
else:
    finger_color = "#1f77b4"  # Professional Blue


ax.plot(
    [x0, x1, x2],
    [y0, y1, y2],
    color=finger_color,
    linewidth=12,
    marker="o",
    markersize=14,
    solid_capstyle="round",
)

# Styling the plot for a clean presentation look
ax.set_xlim(-0.5, 6.0)
ax.set_ylim(-3.5, 1.5)  # Adjusted limits for downward bending
ax.axhline(0, color="black", linestyle="--", alpha=0.2)
ax.set_title(
    f"Simulation de la flexion de la première jointure (Angle: {theta_display:.1f}°)",
    fontsize=12,
    fontweight="bold",
)
ax.axis("off")  # Hide axes

# Render plot in Streamlit
st.pyplot(fig)