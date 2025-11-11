"""
🌱 HYDROPONIC PORTABLE MONITORING SYSTEM - DEMO VERSION
═══════════════════════════════════════════════════════

Perfect for Streamlit Cloud deployment & GitHub sharing

✅ Zero configuration needed
✅ Works on Streamlit Cloud instantly
✅ Professional presentation-ready interface
✅ All data self-contained and simulated

GitHub: https://github.com/YOUR_USERNAME/hydroponic-monitor-demo
Live Demo: https://hydroponic-monitor.streamlit.app
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time

# ═══════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Hydroponic Monitor - Demo",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/YOUR_USERNAME/hydroponic-monitor-demo',
        'Report a bug': 'https://github.com/YOUR_USERNAME/hydroponic-monitor-demo/issues',
        'About': """
        # Hydroponic Portable Monitoring System
        
        A portable, AI-powered IoT solution for urban hydroponic cultivation.
        
        **Research Project Demo Version**
        
        This demo showcases the full system capabilities with simulated data,
        perfect for presentations and research defense.
        """
    }
)

# ═══════════════════════════════════════════════════════
# DEMO DATA ENGINE
# ═══════════════════════════════════════════════════════
class DemoEngine:
    """Generates realistic sensor data for demonstration"""
    
    def __init__(self):
        self.ph = 5.80
        self.ec = 1.20
        self.water_temp = 20.5
        self.air_temp = 24.0
        self.humidity = 65.0
        self.water_level = 18.5
        self.battery = 12.4
        self.time_step = 0
        self.action_count = 0
        self.last_action = "System initialized"
        
        # Pre-scripted events for smooth demo flow
        self.events = [
            (40, "ph_drift", "pH drifting upward..."),
            (80, "auto_ph", "AUTO: pH corrected with pH DOWN (0.5ml)"),
            (120, "ec_drop", "EC decreasing (nutrient uptake)"),
            (160, "auto_ec", "AUTO: Nutrients added (1.0ml)"),
            (200, "stable", "All parameters stabilized ✓")
        ]
    
    def get_current_data(self):
        """Generate current readings with realistic variance"""
        self.time_step += 1
        
        # Check for scripted events
        for event_time, event_type, event_msg in self.events:
            if self.time_step == event_time:
                self.last_action = event_msg
                if event_type == "ph_drift":
                    self.ph = 6.15
                elif event_type == "auto_ph":
                    self.ph = 5.82
                    self.action_count += 1
                elif event_type == "ec_drop":
                    self.ec = 1.08
                elif event_type == "auto_ec":
                    self.ec = 1.18
                    self.action_count += 1
                elif event_type == "stable":
                    self.ph = 5.80
                    self.ec = 1.20
        
        # Natural variance
        ph_noise = np.random.normal(0, 0.015)
        ec_noise = np.random.normal(0, 0.008)
        
        return {
            'pH': round(self.ph + ph_noise, 2),
            'ec': round(self.ec + ec_noise, 2),
            'waterTemp': round(self.water_temp + np.random.normal(0, 0.2), 1),
            'airTemp': round(self.air_temp + np.random.normal(0, 0.5), 1),
            'humidity': round(self.humidity + np.random.normal(0, 1.5), 1),
            'waterLevel': round(max(5, self.water_level - self.time_step * 0.001), 1),
            'battery': round(max(11.5, self.battery - self.time_step * 0.00008), 2),
            'timestamp': datetime.now(),
            'lastAction': self.last_action,
            'actionCount': self.action_count
        }
    
    def get_history(self, hours=24):
        """Generate historical data"""
        points = hours * 12
        history = []
        
        for i in range(points):
            time_ago = datetime.now() - timedelta(minutes=5*i)
            ph = 5.80 + np.sin(i * 0.08) * 0.12 + np.random.normal(0, 0.02)
            ec = 1.20 + np.sin(i * 0.04) * 0.06 + np.random.normal(0, 0.01)
            
            history.append({
                'timestamp': time_ago,
                'pH': round(ph, 2),
                'ec': round(ec, 2),
                'waterTemp': round(20.5 + np.random.normal(0, 0.3), 1)
            })
        
        history.reverse()
        return pd.DataFrame(history)

# Initialize demo engine
if 'demo' not in st.session_state:
    st.session_state.demo = DemoEngine()
    st.session_state.page = "Dashboard"
    st.session_state.selected_plant = None

demo = st.session_state.demo

# ═══════════════════════════════════════════════════════
# PLANT HEALTH AI DATA
# ═══════════════════════════════════════════════════════
PLANTS = {
    "healthy": {
        "name": "Healthy Lettuce",
        "emoji": "🟢",
        "class": "Healthy",
        "confidence": 94.2,
        "predictions": [
            ("Healthy", 94.2),
            ("Optimal Growth", 4.1),
            ("Nutrient Deficiency", 1.2),
            ("Disease", 0.5)
        ],
        "status": "success",
        "message": "✅ Plant is healthy! Maintain current conditions.",
        "actions": [
            "Continue pH: 5.8 ± 0.15",
            "Maintain EC: 1.2 ± 0.08 mS/cm",
            "Keep water temp: 18-22°C",
            "Daily monitoring recommended"
        ]
    },
    "deficiency": {
        "name": "Nutrient Deficiency",
        "emoji": "🟡",
        "class": "Nutrient Deficiency",
        "confidence": 89.7,
        "predictions": [
            ("Nutrient Deficiency", 89.7),
            ("Healthy", 7.3),
            ("Disease", 2.5),
            ("Optimal Growth", 0.5)
        ],
        "status": "warning",
        "message": "⚠️ Nutrient deficiency detected! Adjust feeding.",
        "actions": [
            "Increase EC to 1.3-1.4 mS/cm",
            "Verify pH at 5.8",
            "Add balanced nutrient solution",
            "Re-evaluate in 48 hours"
        ]
    },
    "disease": {
        "name": "Disease/Stress",
        "emoji": "🔴",
        "class": "Disease",
        "confidence": 86.3,
        "predictions": [
            ("Disease", 86.3),
            ("Nutrient Deficiency", 9.2),
            ("Healthy", 3.8),
            ("Optimal Growth", 0.7)
        ],
        "status": "error",
        "message": "🚨 Disease or stress detected! Take immediate action.",
        "actions": [
            "Isolate affected plants",
            "Check water temp (18-22°C)",
            "Improve air circulation",
            "Consider H₂O₂ treatment",
            "Consult specialist if persists"
        ]
    },
    "optimal": {
        "name": "Ready for Harvest",
        "emoji": "🔵",
        "class": "Optimal Growth",
        "confidence": 92.8,
        "predictions": [
            ("Optimal Growth", 92.8),
            ("Healthy", 6.1),
            ("Nutrient Deficiency", 0.8),
            ("Disease", 0.3)
        ],
        "status": "info",
        "message": "🌟 Plant is ready for harvest!",
        "actions": [
            "Harvest when crisp (15-20cm)",
            "Best time: morning hours",
            "Store at 4°C with humidity",
            "Use within 7 days for quality"
        ]
    }
}

# ═══════════════════════════════════════════════════════
# CUSTOM STYLING
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
    .main {padding: 0rem 1rem;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .metric-card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        margin: 10px 0;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-card h3 {
        margin: 0;
        font-size: 16px;
        opacity: 0.9;
    }
    .metric-card h1 {
        margin: 10px 0;
        font-size: 42px;
        font-weight: bold;
    }
    .metric-card p {
        margin: 0;
        font-size: 13px;
        opacity: 0.85;
    }
    
    .metric-good {background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);}
    .metric-warning {background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);}
    .metric-critical {background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);}
    .metric-info {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .demo-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {opacity: 1;}
        50% {opacity: 0.8;}
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════
def get_status(value, target, tolerance):
    diff = abs(value - target)
    return "good" if diff <= tolerance else "warning" if diff <= tolerance * 2 else "critical"

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.title("🌱 Hydroponic Monitor")
    st.markdown('<div class="demo-badge">🎭 DEMO MODE</div>', unsafe_allow_html=True)
    st.caption("Self-running demonstration with simulated data")
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "🌱 Plant Health AI", "📖 About"],
        key="nav_radio",
        label_visibility="collapsed"
    )
    st.session_state.page = page
    
    st.markdown("---")
    
    # Quick stats
    current = demo.get_current_data()
    st.subheader("Quick Stats")
    st.metric("pH", f"{current['pH']:.2f}")
    st.metric("EC", f"{current['ec']:.2f} mS/cm")
    st.metric("Battery", f"{current['battery']:.1f}V")
    st.caption(f"System uptime: {demo.time_step // 60} min")
    
    st.markdown("---")
    
    # Controls
    st.subheader("🎬 Demo Controls")
    
    auto_refresh = st.checkbox("Auto-refresh", value=True)
    if auto_refresh:
        refresh_rate = st.slider("Refresh (sec)", 2, 10, 3)
    
    if st.button("🔄 Reset Demo", use_container_width=True):
        st.session_state.demo = DemoEngine()
        st.rerun()
    
    st.markdown("---")
    
    # Links
    st.subheader("🔗 Links")
    st.markdown("""
    - [GitHub Repository](https://github.com/YOUR_USERNAME/hydroponic-monitor-demo)
    - [Research Paper](https://github.com/YOUR_USERNAME/hydroponic-monitor-demo/blob/main/docs/paper.pdf)
    - [Full Documentation](https://github.com/YOUR_USERNAME/hydroponic-monitor-demo#readme)
    """)
    
    st.markdown("---")
    st.caption("🎓 Research Project Demo\nv1.0 - 2025")

# ═══════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════
if st.session_state.page == "📊 Dashboard":
    st.title("📊 Real-Time Monitoring Dashboard")
    st.caption("Live sensor data with automated control system")
    st.markdown("---")
    
    placeholder = st.empty()
    
    with placeholder.container():
        data = demo.get_current_data()
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status = get_status(data['pH'], 5.8, 0.15)
            st.markdown(f"""
                <div class="metric-card metric-{status}">
                    <h3>pH Level</h3>
                    <h1>{data['pH']:.2f}</h1>
                    <p>Target: 5.8 ± 0.15</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            status = get_status(data['ec'], 1.2, 0.08)
            st.markdown(f"""
                <div class="metric-card metric-{status}">
                    <h3>EC Level</h3>
                    <h1>{data['ec']:.2f}</h1>
                    <p>Target: 1.2 ± 0.08 mS/cm</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            status = get_status(data['waterTemp'], 20.0, 2.0)
            st.markdown(f"""
                <div class="metric-card metric-{status}">
                    <h3>Water Temp</h3>
                    <h1>{data['waterTemp']:.1f}°C</h1>
                    <p>Optimal: 18-22°C</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            status = "good" if data['battery'] > 12.0 else "warning"
            st.markdown(f"""
                <div class="metric-card metric-{status}">
                    <h3>Battery</h3>
                    <h1>{data['battery']:.1f}V</h1>
                    <p>{'🔋 Good' if data['battery'] > 12.0 else '⚠️ Low'}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # System status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("🟢 **System Online**")
        with col2:
            st.info(f"🤖 **Auto Mode Active** ({data['actionCount']} actions)")
        with col3:
            st.success("📊 **Data Quality: Excellent**")
        
        if data['lastAction']:
            st.info(f"🔧 **Status:** {data['lastAction']}")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 pH History (24h)")
            history = demo.get_history(24)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=history['timestamp'],
                y=history['pH'],
                mode='lines',
                line=dict(color='#667eea', width=3),
                fill='tozeroy',
                fillcolor='rgba(102,126,234,0.1)'
            ))
            fig.add_hrect(y0=5.65, y1=5.95, fillcolor="green", opacity=0.1, line_width=0)
            fig.update_layout(
                height=300,
                margin=dict(l=0,r=0,t=0,b=0),
                xaxis_title="Time",
                yaxis_title="pH",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 EC History (24h)")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=history['timestamp'],
                y=history['ec'],
                mode='lines',
                line=dict(color='#38ef7d', width=3),
                fill='tozeroy',
                fillcolor='rgba(56,239,125,0.1)'
            ))
            fig.add_hrect(y0=1.12, y1=1.28, fillcolor="green", opacity=0.1, line_width=0)
            fig.update_layout(
                height=300,
                margin=dict(l=0,r=0,t=0,b=0),
                xaxis_title="Time",
                yaxis_title="EC (mS/cm)",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Additional metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💧 Water Level", f"{data['waterLevel']:.1f} cm")
            st.progress(data['waterLevel'] / 20)
        
        with col2:
            st.metric("🌡️ Air Temp", f"{data['airTemp']:.1f}°C")
            st.caption(f"Humidity: {data['humidity']:.1f}%")
        
        with col3:
            st.metric("⚡ System Power", f"{data['battery']:.2f}V")
            st.progress((data['battery'] - 11) / 1.6)
        
        with col4:
            st.metric("📊 Data Points", f"{demo.time_step:,}")
            st.caption("Total readings")
        
        st.caption(f"🕐 Updated: {datetime.now().strftime('%H:%M:%S')} | "
                  f"Auto-refresh: {'ON' if auto_refresh else 'OFF'}")
    
    if auto_refresh:
        time.sleep(refresh_rate)
        st.rerun()

# ═══════════════════════════════════════════════════════
# PAGE: PLANT HEALTH AI
# ═══════════════════════════════════════════════════════
elif st.session_state.page == "🌱 Plant Health AI":
    st.title("🌱 AI-Powered Plant Health Detection")
    st.caption("Teachable Machine integration for automated monitoring")
    st.markdown("---")
    
    st.info("💡 Click any plant sample below to see AI analysis")
    
    # Sample selection
    col1, col2, col3, col4 = st.columns(4)
    
    for idx, (key, plant) in enumerate(PLANTS.items()):
        with [col1, col2, col3, col4][idx]:
            if st.button(
                f"{plant['emoji']}\n\n**{plant['name']}**",
                key=f"btn_{key}",
                use_container_width=True
            ):
                st.session_state.selected_plant = key
    
    # Analysis results
    if st.session_state.selected_plant:
        st.markdown("---")
        plant = PLANTS[st.session_state.selected_plant]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(f"{plant['emoji']} {plant['name']}")
            st.info(f"📷 **Sample Plant Image**\n\n"
                   f"*High-resolution photo (1600x1200px)*\n\n"
                   f"In production, actual ESP32-CAM capture appears here")
        
        with col2:
            st.subheader("🤖 AI Analysis")
            
            with st.spinner("Analyzing with Teachable Machine..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)
            
            st.success("✅ Analysis complete!")
            
            st.markdown(f"""
                <div class="metric-card metric-info">
                    <h3>Classification</h3>
                    <h1>{plant['class']}</h1>
                    <p>{plant['confidence']:.1f}% Confidence</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📊 Confidence Breakdown")
            for class_name, conf in plant['predictions']:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.progress(conf / 100)
                with col_b:
                    st.caption(f"{conf:.1f}%")
                st.caption(f"**{class_name}**")
        
        st.markdown("---")
        
        # Recommendations
        st.subheader("💡 Recommended Actions")
        
        if plant['status'] == 'success':
            st.success(plant['message'])
        elif plant['status'] == 'warning':
            st.warning(plant['message'])
        elif plant['status'] == 'error':
            st.error(plant['message'])
        else:
            st.info(plant['message'])
        
        st.markdown("**Action Plan:**")
        for i, action in enumerate(plant['actions'], 1):
            st.markdown(f"{i}. {action}")
        
        if st.button("💾 Save Analysis", use_container_width=True):
            st.success(f"✅ Saved: **{plant['class']}** ({plant['confidence']:.1f}%)")
            st.balloons()
    
    else:
        st.info("👆 Select a plant sample above to begin analysis")
    
    st.markdown("---")
    
    # History
    st.subheader("📜 Recent Analysis History")
    samples = [
        ("2 min", "Healthy", 94.2, "🟢"),
        ("15 min", "Optimal Growth", 92.8, "🔵"),
        ("1 hour", "Healthy", 91.5, "🟢"),
        ("3 hours", "Nutrient Deficiency", 89.7, "🟡"),
    ]
    
    for time_ago, cls, conf, emoji in samples:
        with st.expander(f"{emoji} {time_ago} ago - **{cls}** ({conf:.1f}%)"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Class", cls)
            col2.metric("Confidence", f"{conf:.1f}%")
            col3.metric("Source", "Demo")

# ═══════════════════════════════════════════════════════
# PAGE: ABOUT
# ═══════════════════════════════════════════════════════
elif st.session_state.page == "📖 About":
    st.title("📖 About This System")
    st.markdown("---")
    
    st.subheader("🌱 Hydroponic Portable Monitoring System")
    st.markdown("""
    A **portable, AI-powered IoT solution** for urban hydroponic lettuce cultivation.
    
    **Key Features:**
    - ✅ Real-time pH/EC monitoring (±0.15 pH, ±0.08 mS/cm)
    - ✅ Automated nutrient dosing and pH adjustment
    - ✅ AI-powered plant health detection (Teachable Machine)
    - ✅ Battery-powered (48-72 hour runtime)
    - ✅ Cloud dashboard with Firebase backend
    - ✅ ESP32-CAM for automated image capture
    
    **Cost:** ₱22,000 vs ₱65,000+ commercial systems (**66% savings**)
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Technical Specs")
        st.markdown("""
        **Sensors:**
        - pH: Gravity Analog (±0.1)
        - EC: 0-5 mS/cm (±0.05)
        - Temp: DS18B20 (±0.5°C)
        - Air: DHT22 (±2% RH)
        
        **Control:**
        - 3× Peristaltic pumps
        - Automated dosing
        - PID + Fuzzy logic
        
        **Power:**
        - 18650 Li-ion (14.8V, 6Ah)
        - Solar charging capable
        - 48-72h runtime
        """)
    
    with col2:
        st.subheader("🎯 Performance")
        st.markdown("""
        **Optimal Conditions:**
        - pH: 5.5-6.0 (target: 5.8)
        - EC: 1.0-1.4 mS/cm (target: 1.2)
        - Water: 18-22°C (target: 20°C)
        - Growth: 28-35 days
        
        **Expected Results:**
        - Yield: +37% vs manual
        - Quality: 95%+ Grade A
        - Water: -27% consumption
        - Labor: -60% reduction
        """)
    
    st.markdown("---")
    
    st.subheader("🏗️ System Architecture")
    st.code("""
    ESP32 + Sensors → Firebase Cloud → Streamlit Dashboard
                   ↓                  ↓
              ESP32-CAM         Teachable Machine AI
    """, language="text")
    
    st.markdown("---")
    
    st.subheader("🎓 Research Information")
    st.markdown("""
    **Title:** Development of a Portable IoT-Based Hydroponic Monitoring System  
    with AI-Powered Plant Health Detection
    
    **Researcher:** [Your Name]  
    **Institution:** Polytechnic University of the Philippines  
    **Program:** MS Computer Engineering (Data Science & Engineering)  
    **Year:** 2025
    """)
    
    st.markdown("---")
    
    st.info("""
    ### 🎭 About This Demo
    
    This is a **self-contained demonstration** perfect for presentations.
    All data is pre-programmed and simulated to show realistic behavior
    without requiring hardware, Firebase, or internet connection.
    
    **Live Demo:** https://YOUR-APP.streamlit.app  
    **GitHub:** https://github.com/YOUR_USERNAME/hydroponic-monitor-demo
    """)

st.markdown("---")
st.caption("🌱 Hydroponic Portable Monitor | 🎭 Demo v1.0 | © 2025")
