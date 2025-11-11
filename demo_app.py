"""
🌱 Hydroponic Monitor - Simple Demo
Purple, white, and gold theme
Straightforward design for easy understanding
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="Hydroponic Monitor",
    page_icon="🌱",
    layout="wide"
)

# ═══════════════════════════════════════════
# SIMPLE COLORS - Purple, White, Gold
# ═══════════════════════════════════════════
PURPLE = "#6B21A8"
LIGHT_PURPLE = "#9333EA"
GOLD = "#FCD34D"
WHITE = "#FFFFFF"

# ═══════════════════════════════════════════
# SIMPLE STYLING
# ═══════════════════════════════════════════
st.markdown(f"""
<style>
    .main {{background-color: {WHITE}; padding: 2rem;}}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    .big-metric {{
        background: {PURPLE};
        color: {WHITE};
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }}
    .big-metric h1 {{
        font-size: 48px;
        margin: 10px 0;
        color: {GOLD};
    }}
    .big-metric h3 {{
        font-size: 18px;
        margin: 0;
        opacity: 0.9;
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
# SIMPLE DATA GENERATOR
# ═══════════════════════════════════════════
class SimpleDemo:
    def __init__(self):
        self.ph = 5.80
        self.ec = 1.20
        self.temp = 20.5
        self.step = 0
    
    def get_data(self):
        self.step += 1
        return {
            'pH': round(self.ph + np.random.normal(0, 0.02), 2),
            'ec': round(self.ec + np.random.normal(0, 0.01), 2),
            'temp': round(self.temp + np.random.normal(0, 0.2), 1),
            'time': datetime.now()
        }
    
    def get_history(self):
        history = []
        for i in range(50):
            t = datetime.now() - timedelta(minutes=i*5)
            history.append({
                'time': t,
                'pH': 5.80 + np.random.normal(0, 0.05),
                'ec': 1.20 + np.random.normal(0, 0.03)
            })
        return pd.DataFrame(history[::-1])

if 'demo' not in st.session_state:
    st.session_state.demo = SimpleDemo()

demo = st.session_state.demo

# ═══════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════
st.markdown(f"<h1 style='color:{PURPLE}; text-align:center;'>🌱 Hydroponic Monitoring System</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{LIGHT_PURPLE};'>Real-time monitoring for optimal plant growth</p>", unsafe_allow_html=True)
st.markdown("---")

# ═══════════════════════════════════════════
# MAIN METRICS - BIG AND SIMPLE
# ═══════════════════════════════════════════
data = demo.get_data()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="big-metric">
            <h3>pH Level</h3>
            <h1>{data['pH']:.2f}</h1>
            <p>Target: 5.8</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="big-metric">
            <h3>EC Level</h3>
            <h1>{data['ec']:.2f}</h1>
            <p>Target: 1.2 mS/cm</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="big-metric">
            <h3>Water Temp</h3>
            <h1>{data['temp']:.1f}°C</h1>
            <p>Optimal: 18-22°C</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════
# SIMPLE GRAPHS - ONE LINE EACH
# ═══════════════════════════════════════════
history = demo.get_history()

col1, col2 = st.columns(2)

with col1:
    st.subheader("pH Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history['time'],
        y=history['pH'],
        mode='lines',
        line=dict(color=PURPLE, width=3),
        showlegend=False
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("EC Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history['time'],
        y=history['ec'],
        mode='lines',
        line=dict(color=LIGHT_PURPLE, width=3),
        showlegend=False
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE
    )
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════
st.markdown("---")
st.markdown(f"<p style='text-align:center; color:{PURPLE};'>🌱 Hydroponic Portable Monitor | Demo Version</p>", unsafe_allow_html=True)

# Auto-refresh every 3 seconds
time.sleep(3)
st.rerun()
