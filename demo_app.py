"""
🌱 HYDROPONIC PORTABLE MONITORING SYSTEM - DEMO VERSION
═══════════════════════════════════════════════════════

PERFECT FOR PRESENTATIONS & RESEARCH DEFENSE

✅ No hardware needed
✅ No Firebase setup required  
✅ No internet connection needed
✅ Looks 100% real-time
✅ All data pre-programmed
✅ Smooth animations
✅ Professional appearance

USAGE:
    streamlit run demo_app.py

Then open browser and present! That's it!
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
from PIL import Image
import io
import base64

# ═══════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Hydroponic Portable Monitor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════
# DEMO DATA ENGINE
# ═══════════════════════════════════════════════════════
class DemoEngine:
    """Self-contained demo data generator - looks real-time but fully scripted"""
    
    def __init__(self):
        # Starting values (perfect conditions)
        self.ph = 5.80
        self.ec = 1.20
        self.water_temp = 20.5
        self.air_temp = 24.0
        self.humidity = 65.0
        self.water_level = 18.5
        self.battery = 12.4
        self.time_step = 0
        
        # Control state
        self.auto_mode = True
        self.last_action = "System initialized"
        self.action_count = 0
        
        # Pre-scripted "events" for demonstration
        self.events = [
            (50, "ph_drift_high", "pH slowly increasing..."),
            (100, "auto_correct_ph", "AUTO: pH adjusted with pH DOWN"),
            (150, "ec_drift_low", "EC decreasing (plant uptake)"),
            (200, "auto_correct_ec", "AUTO: Nutrients added"),
            (250, "water_low", "Water level dropping"),
            (300, "all_stable", "All parameters stabilized")
        ]
        
    def get_current_data(self):
        """Generate realistic 'live' data with scripted events"""
        self.time_step += 1
        
        # Check for scripted events
        for event_time, event_type, event_msg in self.events:
            if self.time_step == event_time:
                self.last_action = event_msg
                self._trigger_event(event_type)
        
        # Add natural variance (very small, realistic)
        ph_noise = np.random.normal(0, 0.01)
        ec_noise = np.random.normal(0, 0.005)
        temp_noise = np.random.normal(0, 0.1)
        
        # Natural slow drifts
        ph_drift = np.sin(self.time_step * 0.02) * 0.03
        ec_drift = -0.0001 * self.time_step  # Slow EC drop (plant uptake)
        water_drift = -0.002 * self.time_step  # Evaporation
        battery_drift = -0.00005 * self.time_step  # Discharge
        
        # Current readings
        current = {
            'pH': round(self.ph + ph_drift + ph_noise, 2),
            'ec': round(max(0.8, self.ec + ec_drift + ec_noise), 2),
            'waterTemp': round(self.water_temp + temp_noise, 1),
            'airTemp': round(self.air_temp + np.random.normal(0, 0.5), 1),
            'humidity': round(self.humidity + np.random.normal(0, 1), 1),
            'waterLevel': round(max(5, self.water_level + water_drift), 1),
            'battery': round(max(11.5, self.battery + battery_drift), 2),
            'timestamp': datetime.now(),
            'lastAction': self.last_action
        }
        
        return current
    
    def _trigger_event(self, event_type):
        """Trigger scripted events for demo"""
        if event_type == "ph_drift_high":
            self.ph = 6.1
        elif event_type == "auto_correct_ph":
            self.ph = 5.85
            self.action_count += 1
        elif event_type == "ec_drift_low":
            self.ec = 1.08
        elif event_type == "auto_correct_ec":
            self.ec = 1.18
            self.action_count += 1
        elif event_type == "water_low":
            self.water_level = 12.0
        elif event_type == "all_stable":
            self.ph = 5.80
            self.ec = 1.20
            self.water_level = 18.0
    
    def get_history_data(self, hours=24):
        """Generate historical data for charts"""
        points = hours * 12  # 5-minute intervals
        history = []
        
        for i in range(points):
            time_ago = datetime.now() - timedelta(minutes=5*i)
            
            # Create realistic historical pattern
            ph_value = 5.80 + np.sin(i * 0.1) * 0.08 + np.random.normal(0, 0.02)
            ec_value = 1.20 + np.sin(i * 0.05) * 0.04 + np.random.normal(0, 0.01)
            temp_value = 20.5 + np.random.normal(0, 0.3)
            
            history.append({
                'timestamp': time_ago,
                'pH': round(ph_value, 2),
                'ec': round(ec_value, 2),
                'waterTemp': round(temp_value, 1)
            })
        
        history.reverse()
        return pd.DataFrame(history)
    
    def manual_action(self, action_type):
        """Simulate manual control actions"""
        self.action_count += 1
        
        if action_type == "ph_up":
            self.ph += 0.15
            return "✅ pH UP dosed (0.5ml) - pH increased by +0.15"
        elif action_type == "ph_down":
            self.ph -= 0.15
            return "✅ pH DOWN dosed (0.5ml) - pH decreased by -0.15"
        elif action_type == "nutrient":
            self.ec += 0.08
            return "✅ Nutrients added (1ml) - EC increased by +0.08"
        elif action_type == "refill":
            self.water_level = 20.0
            return "✅ Water reservoir refilled to 20cm"
        elif action_type == "reset":
            self.__init__()
            return "✅ System reset to initial conditions"

# Initialize demo engine
if 'demo' not in st.session_state:
    st.session_state.demo = DemoEngine()
    st.session_state.target_ph = 5.8
    st.session_state.target_ec = 1.2

demo = st.session_state.demo

# ═══════════════════════════════════════════════════════
# PLANT HEALTH AI (PRE-PROGRAMMED PREDICTIONS)
# ═══════════════════════════════════════════════════════
PLANT_SAMPLES = {
    "healthy": {
        "name": "Healthy Lettuce",
        "emoji": "🟢",
        "prediction": {
            "class": "Healthy",
            "confidence": 94.2,
            "details": [
                {"class": "Healthy", "conf": 94.2},
                {"class": "Optimal Growth", "conf": 4.1},
                {"class": "Nutrient Deficiency", "conf": 1.2},
                {"class": "Disease", "conf": 0.5}
            ]
        },
        "recommendation": {
            "status": "success",
            "message": "✅ Plant is healthy! Maintain current conditions.",
            "actions": [
                "Continue pH: 5.8 ± 0.15",
                "Maintain EC: 1.2 ± 0.08 mS/cm", 
                "Keep water temp: 18-22°C",
                "Monitor daily for changes"
            ]
        }
    },
    "deficiency": {
        "name": "Nutrient Deficiency",
        "emoji": "🟡",
        "prediction": {
            "class": "Nutrient Deficiency",
            "confidence": 89.7,
            "details": [
                {"class": "Nutrient Deficiency", "conf": 89.7},
                {"class": "Healthy", "conf": 7.3},
                {"class": "Disease", "conf": 2.5},
                {"class": "Optimal Growth", "conf": 0.5}
            ]
        },
        "recommendation": {
            "status": "warning",
            "message": "⚠️ Nutrient deficiency detected! Adjust feeding.",
            "actions": [
                "Increase EC to 1.3-1.4 mS/cm",
                "Verify pH is at 5.8",
                "Add balanced nutrient solution",
                "Check again in 48 hours"
            ]
        }
    },
    "disease": {
        "name": "Disease Detected",
        "emoji": "🔴",
        "prediction": {
            "class": "Disease",
            "confidence": 86.3,
            "details": [
                {"class": "Disease", "conf": 86.3},
                {"class": "Nutrient Deficiency", "conf": 9.2},
                {"class": "Healthy", "conf": 3.8},
                {"class": "Optimal Growth", "conf": 0.7}
            ]
        },
        "recommendation": {
            "status": "error",
            "message": "🚨 Disease or pest issue detected! Take action now.",
            "actions": [
                "Isolate affected plants",
                "Check water temp (18-22°C)",
                "Improve air circulation",
                "Consider H₂O₂ treatment",
                "Consult specialist if persists"
            ]
        }
    },
    "optimal": {
        "name": "Ready for Harvest",
        "emoji": "🔵",
        "prediction": {
            "class": "Optimal Growth",
            "confidence": 92.8,
            "details": [
                {"class": "Optimal Growth", "conf": 92.8},
                {"class": "Healthy", "conf": 6.1},
                {"class": "Nutrient Deficiency", "conf": 0.8},
                {"class": "Disease", "conf": 0.3}
            ]
        },
        "recommendation": {
            "status": "info",
            "message": "🌟 Plant is ready for harvest!",
            "actions": [
                "Harvest when crisp (15-20cm)",
                "Best time: morning hours",
                "Store at 4°C with humidity",
                "Use within 7 days for best quality"
            ]
        }
    }
}

# ═══════════════════════════════════════════════════════
# CUSTOM STYLING
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Main layout */
    .main {padding: 0rem 1rem;}
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Metric cards */
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
        font-weight: 500;
        opacity: 0.95;
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
    
    .metric-good {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .metric-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .metric-critical {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    .metric-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Alert boxes */
    .alert-box {
        padding: 15px 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
        font-weight: 500;
    }
    .alert-success {
        background: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
    .alert-warning {
        background: #fff3cd;
        border-color: #ffc107;
        color: #856404;
    }
    .alert-danger {
        background: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }
    .alert-info {
        background: #d1ecf1;
        border-color: #17a2b8;
        color: #0c5460;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
    }
    .status-online {
        background: #28a745;
        color: white;
    }
    .status-demo {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Plant sample cards */
    .plant-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        background: white;
        border: 3px solid #e0e0e0;
    }
    .plant-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        border-color: #667eea;
    }
    .plant-card h2 {
        font-size: 48px;
        margin: 10px 0;
    }
    .plant-card h3 {
        font-size: 18px;
        margin: 10px 0;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════
def get_status_color(value, target, tolerance):
    """Determine metric status color"""
    diff = abs(value - target)
    if diff <= tolerance:
        return "good"
    elif diff <= tolerance * 2:
        return "warning"
    else:
        return "critical"

# ═══════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════
with st.sidebar:
    st.title("🌱 Hydroponic Monitor")
    
    # Demo mode badge
    st.markdown('<div class="status-badge status-demo">🎭 DEMO MODE</div>', 
                unsafe_allow_html=True)
    st.caption("Self-running demonstration - perfect for presentations!")
    
    st.markdown("---")
    
    # Page selection
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "🌱 Plant Health AI", "📖 About System"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("Quick Stats")
    current = demo.get_current_data()
    st.metric("Current pH", f"{current['pH']:.2f}")
    st.metric("Current EC", f"{current['ec']:.2f} mS/cm")
    st.metric("Battery", f"{current['battery']:.1f}V")
    
    st.markdown("---")
    
    # Demo controls
    st.subheader("🎬 Demo Controls")
    
    if st.button("🔄 Reset Demo", use_container_width=True):
        st.session_state.demo = DemoEngine()
        st.success("Demo reset!")
        st.rerun()
    
    auto_refresh = st.checkbox("Auto-refresh", value=True)
    if auto_refresh:
        refresh_rate = st.slider("Refresh (sec)", 2, 10, 3)
    
    st.markdown("---")
    st.caption("🎓 Research Project Demo\nHydroponic Portable Monitor\nv1.0 - 2025")

# ═══════════════════════════════════════════════════════
# PAGE 1: DASHBOARD
# ═══════════════════════════════════════════════════════
if page == "📊 Dashboard":
    st.title("📊 Real-Time Monitoring Dashboard")
    st.caption("Live sensor data with automated control system")
    st.markdown("---")
    
    # Auto-refresh container
    dashboard_placeholder = st.empty()
    
    with dashboard_placeholder.container():
        # Get current data
        data = demo.get_current_data()
        
        # ═══ METRIC CARDS ═══
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ph_status = get_status_color(data['pH'], st.session_state.target_ph, 0.15)
            st.markdown(f"""
                <div class="metric-card metric-{ph_status}">
                    <h3>pH Level</h3>
                    <h1>{data['pH']:.2f}</h1>
                    <p>Target: {st.session_state.target_ph} ± 0.15</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            ec_status = get_status_color(data['ec'], st.session_state.target_ec, 0.08)
            st.markdown(f"""
                <div class="metric-card metric-{ec_status}">
                    <h3>EC Level</h3>
                    <h1>{data['ec']:.2f}</h1>
                    <p>Target: {st.session_state.target_ec} ± 0.08 mS/cm</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            temp_status = get_status_color(data['waterTemp'], 20.0, 2.0)
            st.markdown(f"""
                <div class="metric-card metric-{temp_status}">
                    <h3>Water Temp</h3>
                    <h1>{data['waterTemp']:.1f}°C</h1>
                    <p>Optimal: 18-22°C</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            battery_status = "good" if data['battery'] > 12.0 else "warning"
            st.markdown(f"""
                <div class="metric-card metric-{battery_status}">
                    <h3>Battery</h3>
                    <h1>{data['battery']:.1f}V</h1>
                    <p>{'🔋 Good' if data['battery'] > 12.0 else '⚠️ Low'}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ═══ SYSTEM STATUS ═══
        st.subheader("📡 System Status")
        
        status_col1, status_col2, status_col3 = st.columns(3)
        with status_col1:
            st.success("🟢 **System Online**")
            st.caption(f"Uptime: {demo.time_step // 60} min")
        with status_col2:
            st.info(f"🤖 **Auto Mode: Active**")
            st.caption(f"Actions taken: {demo.action_count}")
        with status_col3:
            st.success(f"📊 **Data Quality: Excellent**")
            st.caption("99.7% accuracy")
        
        # Last action
        if data['lastAction']:
            st.info(f"🔧 **Last Action:** {data['lastAction']}")
        
        st.markdown("---")
        
        # ═══ CHARTS ═══
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📈 pH History (24 Hours)")
            history = demo.get_history_data(hours=24)
            
            fig_ph = go.Figure()
            fig_ph.add_trace(go.Scatter(
                x=history['timestamp'],
                y=history['pH'],
                mode='lines',
                name='pH',
                line=dict(color='#667eea', width=3),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.1)'
            ))
            
            # Target range
            fig_ph.add_hrect(
                y0=st.session_state.target_ph - 0.15,
                y1=st.session_state.target_ph + 0.15,
                fillcolor="green",
                opacity=0.1,
                line_width=0
            )
            
            fig_ph.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Time",
                yaxis_title="pH",
                hovermode='x unified',
                showlegend=False
            )
            st.plotly_chart(fig_ph, use_container_width=True)
        
        with col_right:
            st.subheader("📈 EC History (24 Hours)")
            
            fig_ec = go.Figure()
            fig_ec.add_trace(go.Scatter(
                x=history['timestamp'],
                y=history['ec'],
                mode='lines',
                name='EC',
                line=dict(color='#38ef7d', width=3),
                fill='tozeroy',
                fillcolor='rgba(56, 239, 125, 0.1)'
            ))
            
            # Target range
            fig_ec.add_hrect(
                y0=st.session_state.target_ec - 0.08,
                y1=st.session_state.target_ec + 0.08,
                fillcolor="green",
                opacity=0.1,
                line_width=0
            )
            
            fig_ec.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Time",
                yaxis_title="EC (mS/cm)",
                hovermode='x unified',
                showlegend=False
            )
            st.plotly_chart(fig_ec, use_container_width=True)
        
        st.markdown("---")
        
        # ═══ ADDITIONAL METRICS ═══
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💧 Water Level", f"{data['waterLevel']:.1f} cm")
            level_pct = data['waterLevel'] / 20.0
            st.progress(min(level_pct, 1.0))
        
        with col2:
            st.metric("🌡️ Air Temp", f"{data['airTemp']:.1f}°C")
            st.caption(f"Humidity: {data['humidity']:.1f}%")
        
        with col3:
            st.metric("⚡ System Power", f"{data['battery']:.2f}V")
            battery_pct = (data['battery'] - 11.0) / 1.6
            st.progress(max(0, min(battery_pct, 1.0)))
        
        with col4:
            st.metric("📊 Data Points", f"{demo.time_step:,}")
            st.caption("Total readings collected")
        
        st.markdown("---")
        
        # ═══ MANUAL CONTROLS (DEMO) ═══
        with st.expander("🎛️ Manual Controls (Demo)", expanded=False):
            st.info("💡 Click buttons to see simulated control actions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("➕ pH UP", use_container_width=True):
                    msg = demo.manual_action("ph_up")
                    st.success(msg)
                    time.sleep(0.5)
                    st.rerun()
                
                if st.button("➖ pH DOWN", use_container_width=True):
                    msg = demo.manual_action("ph_down")
                    st.success(msg)
                    time.sleep(0.5)
                    st.rerun()
            
            with col2:
                if st.button("💧 Add Nutrients", use_container_width=True):
                    msg = demo.manual_action("nutrient")
                    st.success(msg)
                    time.sleep(0.5)
                    st.rerun()
                
                if st.button("🚰 Refill Water", use_container_width=True):
                    msg = demo.manual_action("refill")
                    st.success(msg)
                    time.sleep(0.5)
                    st.rerun()
            
            with col3:
                if st.button("🔄 Reset System", use_container_width=True):
                    msg = demo.manual_action("reset")
                    st.success(msg)
                    time.sleep(0.5)
                    st.rerun()
        
        # Update timestamp
        st.caption(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')} | "
                  f"Auto-refresh: {'ON' if auto_refresh else 'OFF'}")
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_rate)
        st.rerun()

# ═══════════════════════════════════════════════════════
# PAGE 2: PLANT HEALTH AI
# ═══════════════════════════════════════════════════════
elif page == "🌱 Plant Health AI":
    st.title("🌱 AI-Powered Plant Health Detection")
    st.caption("Teachable Machine integration for automated plant health monitoring")
    st.markdown("---")
    
    st.info("💡 **Demo Mode:** Click any plant sample below to see AI analysis")
    
    # ═══ SAMPLE SELECTION ═══
    st.subheader("📸 Select Plant Sample")
    
    col1, col2, col3, col4 = st.columns(4)
    
    selected = None
    
    with col1:
        if st.button(f"{PLANT_SAMPLES['healthy']['emoji']}\n\n**{PLANT_SAMPLES['healthy']['name']}**", 
                     key="btn_healthy", use_container_width=True, height=120):
            selected = "healthy"
    
    with col2:
        if st.button(f"{PLANT_SAMPLES['deficiency']['emoji']}\n\n**{PLANT_SAMPLES['deficiency']['name']}**", 
                     key="btn_deficiency", use_container_width=True, height=120):
            selected = "deficiency"
    
    with col3:
        if st.button(f"{PLANT_SAMPLES['disease']['emoji']}\n\n**{PLANT_SAMPLES['disease']['name']}**", 
                     key="btn_disease", use_container_width=True, height=120):
            selected = "disease"
    
    with col4:
        if st.button(f"{PLANT_SAMPLES['optimal']['emoji']}\n\n**{PLANT_SAMPLES['optimal']['name']}**", 
                     key="btn_optimal", use_container_width=True, height=120):
            selected = "optimal"
    
    # ═══ ANALYSIS RESULTS ═══
    if selected:
        st.markdown("---")
        sample = PLANT_SAMPLES[selected]
        pred = sample['prediction']
        rec = sample['recommendation']
        
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.subheader(f"{sample['emoji']} {sample['name']}")
            
            # Simulate image placeholder
            st.info(f"📷 **Sample Image: {sample['name']}**\n\n"
                   f"*High-resolution plant photo would display here*\n\n"
                   f"Image resolution: 1600x1200px\nCapture time: {datetime.now().strftime('%H:%M:%S')}")
        
        with col_right:
            st.subheader("🤖 AI Analysis Results")
            
            # Simulate processing
            with st.spinner("🔄 Analyzing plant health with Teachable Machine..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
            
            st.success("✅ Analysis complete!")
            
            # Main prediction
            st.markdown(f"""
                <div class="metric-card metric-info">
                    <h3>Classification</h3>
                    <h1>{pred['class']}</h1>
                    <p>{pred['confidence']:.1f}% Confidence</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Detailed predictions
            st.markdown("#### 📊 Confidence Breakdown")
            for detail in pred['details']:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.progress(detail['conf'] / 100)
                with col_b:
                    st.caption(f"{detail['conf']:.1f}%")
                st.caption(f"**{detail['class']}**")
        
        st.markdown("---")
        
        # ═══ RECOMMENDATIONS ═══
        st.subheader("💡 Recommended Actions")
        
        if rec['status'] == 'success':
            st.success(rec['message'])
        elif rec['status'] == 'warning':
            st.warning(rec['message'])
        elif rec['status'] == 'error':
            st.error(rec['message'])
        else:
            st.info(rec['message'])
        
        st.markdown("**Action Plan:**")
        for i, action in enumerate(rec['actions'], 1):
            st.markdown(f"{i}. {action}")
        
        st.markdown("---")
        
        # Save button
        if st.button("💾 Save Analysis Report", use_container_width=True):
            st.success(f"✅ Analysis saved: **{pred['class']}** ({pred['confidence']:.1f}% confidence)")
            st.balloons()
    
    else:
        st.info("👆 **Select a plant sample above to begin AI analysis**")
    
    st.markdown("---")
    
    # ═══ ANALYSIS HISTORY ═══
    st.subheader("📜 Recent Analysis History")
    
    # Sample history data
    history_samples = [
        ("2 min ago", "Healthy", 94.2, "🟢"),
        ("15 min ago", "Optimal Growth", 92.8, "🔵"),
        ("1 hour ago", "Healthy", 91.5, "🟢"),
        ("3 hours ago", "Nutrient Deficiency", 89.7, "🟡"),
        ("Yesterday", "Healthy", 93.1, "🟢"),
    ]
    
    for time_ago, classification, confidence, emoji in history_samples:
        with st.expander(f"{emoji} {time_ago} - **{classification}** ({confidence:.1f}%)"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Classification", classification)
            col2.metric("Confidence", f"{confidence:.1f}%")
            col3.metric("Source", "Demo Data")

# ═══════════════════════════════════════════════════════
# PAGE 3: ABOUT SYSTEM
# ═══════════════════════════════════════════════════════
elif page == "📖 About System":
    st.title("📖 About This System")
    st.markdown("---")
    
    # System overview
    st.subheader("🌱 Hydroponic Portable Monitoring System")
    st.markdown("""
    A **portable, AI-powered IoT solution** for urban hydroponic lettuce cultivation with:
    
    - ✅ Real-time pH and EC monitoring (±0.15 pH, ±0.08 mS/cm accuracy)
    - ✅ Automated nutrient dosing and pH adjustment
    - ✅ AI-powered plant health detection (Teachable Machine)
    - ✅ Battery-powered with 48-72 hour runtime
    - ✅ Cloud dashboard with Streamlit
    - ✅ Firebase backend for data storage
    - ✅ ESP32-CAM for automated image capture
    
    **Cost:** ₱22,000 vs ₱65,000+ commercial systems (**66% savings**)
    """)
    
    st.markdown("---")
    
    # Technical specifications
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Technical Specs")
        st.markdown("""
        **Sensors:**
        - pH: Gravity Analog (±0.1 accuracy)
        - EC: 0-5 mS/cm (±0.05 accuracy)
        - Water Temp: DS18B20 (±0.5°C)
        - Air: DHT22 (±0.5°C, ±2% RH)
        
        **Control:**
        - 3x Peristaltic pumps (pH/nutrients)
        - Automated dosing system
        - PID + Fuzzy logic control
        
        **Power:**
        - 18650 Li-ion battery (14.8V, 6Ah)
        - Solar charging capable
        - 48-72 hour runtime
        """)
    
    with col2:
        st.subheader("🎯 Target Performance")
        st.markdown("""
        **Lettuce Optimal Conditions:**
        - pH: 5.5 - 6.0 (target: 5.8)
        - EC: 1.0 - 1.4 mS/cm (target: 1.2)
        - Water Temp: 18-22°C (target: 20°C)
        - Growth Time: 28-35 days
        
        **Expected Results:**
        - Yield: +37% vs manual
        - Quality: 95%+ Grade A
        - Water Savings: 27%
        - Labor Reduction: 60%
        """)
    
    st.markdown("---")
    
    # System architecture
    st.subheader("🏗️ System Architecture")
    st.code("""
    ┌─────────────────────┐
    │   ESP32 Device      │ ← Sensors (pH, EC, Temp)
    │   + ESP32-CAM       │ ← Camera (Plant Images)
    └──────────┬──────────┘
               │ WiFi/MQTT
               ↓
    ┌─────────────────────┐
    │   Firebase Cloud    │ ← Real-time Database
    │   + Storage         │ ← Image Storage
    └──────────┬──────────┘
               │ REST API
               ↓
    ┌─────────────────────┐
    │ Streamlit Dashboard │ ← Web Interface
    │ + Teachable Machine │ ← AI Analysis
    └─────────────────────┘
    """, language="text")
    
    st.markdown("---")
    
    # Research info
    st.subheader("🎓 Research Information")
    st.markdown("""
    **Title:** Development of a Portable IoT-Based Hydroponic Monitoring and Control System  
    for Urban Lettuce Cultivation with AI-Powered Plant Health Detection
    
    **Researcher:** [Your Name]  
    **Institution:** [Your University]  
    **Program:** Master of Science in Computer Engineering  
    **Year:** 2025
    
    **Research Objectives:**
    1. Develop affordable portable hydroponic monitoring system
    2. Implement automated pH/EC control
    3. Integrate AI plant health detection
    4. Validate system performance vs. manual methods
    5. Evaluate user acceptance and economic viability
    """)
    
    st.markdown("---")
    
    # Demo mode info
    st.info("""
    ### 🎭 About This Demo
    
    This is a **self-contained demonstration version** perfect for:
    - Research presentations and thesis defense
    - System capability showcase
    - User interface testing
    - Feature demonstrations
    
    **All data is pre-programmed and simulated** to show realistic system behavior  
    without requiring actual hardware, Firebase connection, or internet access.
    
    For the production version with real hardware, see the full documentation.
    """)

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════
st.markdown("---")
st.caption("🌱 Hydroponic Portable Monitoring System | 🎭 Demo Version v1.0 | "
          "© 2025 Research Project")
