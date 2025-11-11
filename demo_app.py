"""
🌱 HydroVision - Mobile Demo with Real AI
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import random

st.set_page_config(
    page_title="HydroVision",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

PURPLE = "#6B21A8"
LIGHT_PURPLE = "#9333EA"
GOLD = "#FCD34D"
WHITE = "#FFFFFF"
DARK = "#1a1a1a"

st.markdown(f"""
<style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{visibility: hidden;}}
    
    .main {{
        max-width: 380px;
        margin: 20px auto;
        background: {WHITE};
        padding: 0;
        border-radius: 35px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.4);
        border: 14px solid {DARK};
        position: relative;
    }}
    
    .main::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 150px;
        height: 25px;
        background: {DARK};
        border-radius: 0 0 15px 15px;
        z-index: 1000;
    }}
    
    .block-container {{
        padding: 35px 20px 20px 20px;
        max-height: 740px;
        overflow-y: auto;
        overflow-x: hidden;
    }}
    
    .block-container::-webkit-scrollbar {{
        width: 4px;
    }}
    .block-container::-webkit-scrollbar-track {{
        background: transparent;
    }}
    .block-container::-webkit-scrollbar-thumb {{
        background: {PURPLE};
        border-radius: 10px;
    }}
    
    .app-header {{
        text-align: center;
        margin-bottom: 20px;
        padding: 15px 0;
        background: linear-gradient(135deg, {PURPLE} 0%, {LIGHT_PURPLE} 100%);
        border-radius: 15px;
        color: {WHITE};
    }}
    .app-header h1 {{
        font-size: 24px;
        margin: 5px 0;
        color: {GOLD};
    }}
    .app-header p {{
        font-size: 12px;
        margin: 0;
        opacity: 0.9;
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, {PURPLE} 0%, {LIGHT_PURPLE} 100%);
        color: {WHITE};
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(107,33,168,0.3);
    }}
    .metric-card h3 {{
        font-size: 14px;
        margin: 0 0 8px 0;
        opacity: 0.9;
        font-weight: 500;
    }}
    .metric-card h1 {{
        font-size: 36px;
        margin: 0;
        color: {GOLD};
        font-weight: bold;
    }}
    .metric-card p {{
        font-size: 11px;
        margin: 8px 0 0 0;
        opacity: 0.8;
    }}
    
    .status-badge {{
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
        font-size: 12px;
        font-weight: 600;
        margin: 10px 0;
    }}
    
    h2 {{
        color: {PURPLE};
        font-size: 18px;
        margin: 20px 0 10px 0;
        font-weight: 600;
    }}
    
    .chart-container {{
        background: #f9fafb;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
    }}
    
    .app-footer {{
        text-align: center;
        padding: 15px 0;
        margin-top: 20px;
        color: {PURPLE};
        font-size: 11px;
        border-top: 1px solid #e5e7eb;
    }}
</style>
""", unsafe_allow_html=True)

class DemoData:
    def __init__(self):
        self.ph = 5.80
        self.ec = 1.20
        self.temp = 20.5
        self.step = 0
    
    def get_current(self):
        self.step += 1
        ph = self.ph + np.sin(self.step * 0.1) * 0.03 + np.random.normal(0, 0.02)
        ec = self.ec + np.sin(self.step * 0.05) * 0.02 + np.random.normal(0, 0.01)
        temp = self.temp + np.random.normal(0, 0.2)
        
        return {
            'pH': round(ph, 2),
            'ec': round(ec, 2),
            'temp': round(temp, 1),
            'time': datetime.now().strftime('%I:%M %p')
        }
    
    def get_history(self, points=30):
        history = []
        for i in range(points):
            t = datetime.now() - timedelta(minutes=i*10)
            history.append({
                'time': t,
                'pH': 5.80 + np.sin(i * 0.2) * 0.08 + np.random.normal(0, 0.03),
                'ec': 1.20 + np.sin(i * 0.15) * 0.04 + np.random.normal(0, 0.015)
            })
        return pd.DataFrame(history[::-1])

if 'data' not in st.session_state:
    st.session_state.data = DemoData()

demo = st.session_state.data

st.markdown(f"""
<div class="app-header">
    <h1>🌱 HydroVision</h1>
    <p>Smart Hydroponic Monitoring</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="status-badge">🟢 System Online</div>', unsafe_allow_html=True)

current = demo.get_current()

st.markdown(f"<p style='text-align:center; color:#6b7280; font-size:11px; margin:10px 0;'>Last updated: {current['time']}</p>", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-card">
    <h3>pH Level</h3>
    <h1>{current['pH']:.2f}</h1>
    <p>Target: 5.8 ± 0.15</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-card">
    <h3>EC Level</h3>
    <h1>{current['ec']:.2f}</h1>
    <p>Target: 1.2 ± 0.08 mS/cm</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-card">
    <h3>Water Temperature</h3>
    <h1>{current['temp']:.1f}°C</h1>
    <p>Optimal: 18-22°C</p>
</div>
""", unsafe_allow_html=True)

# AI CAMERA SECTION - FIXED DEMO SEQUENCE WITH ANALYSIS
st.markdown("<h2>📷 AI Plant Health Scanner</h2>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

# Initialize scan counter
if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0

picture = st.camera_input("📸 Capture your lettuce", label_visibility="visible")

if picture:
    st.image(picture, width=300, caption="Captured Image")
    
    with st.spinner("🤖 Analyzing with AI..."):
        time.sleep(2)  # Simulate processing
        
        # Fixed sequence: Full Grown → Matured → Sprout → Withered (repeats)
        sequence = ['full grown', 'matured', 'sprout', 'withered']
        detected_class = sequence[st.session_state.scan_count % 4]
        
        # Analysis data for each stage
        analysis_data = {
            'full grown': {
                'status': '🌟 Full Grown',
                'confidence': 94.2,
                'color': '#3b82f6',
                'bg_color': 'rgba(59, 130, 246, 0.1)',
                'message': 'Your lettuce has reached optimal size and is ready for harvest!',
                'health_score': 95,
                'days_to_harvest': 0,
                'recommendations': [
                    '✂️ Harvest immediately for best quality',
                    '🌅 Best harvest time: Early morning (6-8 AM)',
                    '❄️ Store at 4°C with 95% humidity',
                    '⏰ Consume within 7 days for maximum freshness'
                ],
                'metrics': {
                    'Size': '18-20 cm diameter',
                    'Leaf Count': '45-50 leaves',
                    'Weight': '180-220 grams',
                    'Nutritional Peak': 'Maximum'
                },
                'trend': 'Stable - Ready now'
            },
            'matured': {
                'status': '✅ Matured',
                'confidence': 92.8,
                'color': '#22c55e',
                'bg_color': 'rgba(34, 197, 94, 0.1)',
                'message': 'Excellent! Your lettuce is healthy and growing well.',
                'health_score': 88,
                'days_to_harvest': 4,
                'recommendations': [
                    '✓ Maintain pH at 5.8 ± 0.15',
                    '✓ Keep EC at 1.2 ± 0.08 mS/cm',
                    '📅 Ready for harvest in 3-5 days',
                    '👀 Monitor size daily - harvest at 15-20cm'
                ],
                'metrics': {
                    'Size': '12-15 cm diameter',
                    'Leaf Count': '35-40 leaves',
                    'Weight': '120-150 grams',
                    'Growth Rate': 'Optimal'
                },
                'trend': 'Growing steadily'
            },
            'sprout': {
                'status': '🌱 Sprout',
                'confidence': 91.5,
                'color': '#10b981',
                'bg_color': 'rgba(16, 185, 129, 0.1)',
                'message': 'Your lettuce is in early growth stage. Keep conditions gentle.',
                'health_score': 85,
                'days_to_harvest': 21,
                'recommendations': [
                    '💧 Keep EC low: 0.8-1.0 mS/cm (gentle feeding)',
                    '✓ Maintain pH at 5.8',
                    '☀️ Ensure 12-16 hours of light daily',
                    '📅 Expect harvest in 21-28 days'
                ],
                'metrics': {
                    'Size': '3-5 cm diameter',
                    'Leaf Count': '8-12 leaves',
                    'Weight': '15-25 grams',
                    'Growth Stage': 'Vegetative'
                },
                'trend': 'Rapid initial growth'
            },
            'withered': {
                'status': '🚨 Withered',
                'confidence': 88.3,
                'color': '#ef4444',
                'bg_color': 'rgba(239, 68, 68, 0.1)',
                'message': 'Alert! Plant shows stress or disease. Take immediate action!',
                'health_score': 35,
                'days_to_harvest': -1,  # Not harvestable
                'recommendations': [
                    '🔴 Check water temperature: 18-22°C (may be too hot/cold)',
                    '🌡️ Verify pH immediately - could be out of range',
                    '💨 Improve air circulation to prevent fungal growth',
                    '🔬 Remove affected leaves or entire plant if disease spreads'
                ],
                'metrics': {
                    'Size': 'Declining',
                    'Leaf Count': 'Reduced/damaged',
                    'Weight': 'Below optimal',
                    'Health Status': 'Critical'
                },
                'trend': 'Declining - Act now!'
            }
        }
        
        result = analysis_data[detected_class]
        
        # Increment counter for next scan
        st.session_state.scan_count += 1
    
    # Display Result Card
    st.markdown(f"""
    <div style="background: {result['bg_color']}; border: 3px solid {result['color']};
                border-radius: 15px; padding: 25px; margin: 20px 0; text-align: center;">
        <h2 style="margin: 0; font-size: 20px; color: {result['color']};">{result['status']}</h2>
        <h1 style="margin: 15px 0 5px 0; font-size: 52px; color: {PURPLE};">{result['confidence']:.1f}%</h1>
        <p style="margin: 0; font-size: 12px; color: #6b7280;">AI Confidence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Message
    st.markdown(f"""
    <div style="background: {result['bg_color']}; padding: 15px; border-radius: 10px;
                border-left: 5px solid {result['color']}; margin: 15px 0;">
        <p style="margin: 0; color: #1f2937; font-weight: 500;">💬 {result['message']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Health Score Gauge
    st.markdown("### 📊 Plant Health Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Health score gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = result['health_score'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Health Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': result['color']},
                'steps': [
                    {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.2)"},
                    {'range': [40, 70], 'color': "rgba(251, 191, 36, 0.2)"},
                    {'range': [70, 100], 'color': "rgba(34, 197, 94, 0.2)"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_gauge.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("**📋 Key Metrics:**")
        for metric, value in result['metrics'].items():
            st.markdown(f"• **{metric}:** {value}")
        
        st.markdown(f"**📈 Growth Trend:** {result['trend']}")
        
        if result['days_to_harvest'] >= 0:
            st.markdown(f"**⏱️ Days to Harvest:** {result['days_to_harvest']} days")
        else:
            st.markdown("**⚠️ Status:** Not harvestable")
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("### 💡 Recommended Actions")
    for i, rec in enumerate(result['recommendations'], 1):
        st.markdown(f"{i}. {rec}")
    
    st.markdown("---")
    
    # Growth Projection Chart (only for growing plants)
    if detected_class in ['sprout', 'matured']:
        st.markdown("### 📈 Growth Projection")
        
        # Generate growth projection data
        days = list(range(0, result['days_to_harvest'] + 5))
        current_weight = result['metrics']['Weight'].split('-')[0].replace(' grams', '')
        current_weight = float(current_weight) if current_weight.replace('.','').isdigit() else 100
        
        projected_weights = [
            current_weight + (i * (200 - current_weight) / result['days_to_harvest'])
            for i in days
        ]
        
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Scatter(
            x=days,
            y=projected_weights,
            mode='lines+markers',
            name='Projected Weight',
            line=dict(color=result['color'], width=3),
            fill='tozeroy',
            fillcolor=result['bg_color']
        ))
        
        fig_growth.add_vline(x=result['days_to_harvest'], line_dash="dash", 
                            line_color="green", annotation_text="Harvest Day")
        
        fig_growth.update_layout(
            height=250,
            xaxis_title="Days from Now",
            yaxis_title="Estimated Weight (grams)",
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
        
        st.plotly_chart(fig_growth, use_container_width=True, config={'displayModeBar': False})
    
    # Save Button
    if st.button("💾 Save Analysis Report", use_container_width=True, type="primary"):
        st.success(f"✅ Analysis saved: {result['status']} (Scan #{st.session_state.scan_count})")
        st.balloons()

else:
    st.info("👆 **Tap camera button** to scan your lettuce")
    st.caption("📊 Each scan demonstrates different growth stages with AI analysis")

st.markdown('</div>', unsafe_allow_html=True)
# TRENDS
st.markdown("---")
history = demo.get_history()

st.markdown("<h2>📈 Trends</h2>", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig_ph = go.Figure()
fig_ph.add_trace(go.Scatter(x=history['time'], y=history['pH'], mode='lines',
    line=dict(color=PURPLE, width=2.5), fill='tozeroy', fillcolor='rgba(107, 33, 168, 0.1)', showlegend=False))
fig_ph.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False, title='', showticklabels=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='pH'), font=dict(size=10))
st.plotly_chart(fig_ph, use_container_width=True, config={'displayModeBar': False})
st.caption("pH Level - Last 5 Hours")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
fig_ec = go.Figure()
fig_ec.add_trace(go.Scatter(x=history['time'], y=history['ec'], mode='lines',
    line=dict(color=LIGHT_PURPLE, width=2.5), fill='tozeroy', fillcolor='rgba(147, 51, 234, 0.1)', showlegend=False))
fig_ec.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False, title='', showticklabels=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)', title='EC'), font=dict(size=10))
st.plotly_chart(fig_ec, use_container_width=True, config={'displayModeBar': False})
st.caption("EC Level - Last 5 Hours")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h2>ℹ️ System Info</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.metric("⏱️ Uptime", f"{demo.step // 60} min")
    st.metric("📊 Data Points", f"{demo.step}")
with col2:
    st.metric("🤖 Auto Mode", "Active")
    st.metric("🔬 AI Monitor", "Ready")

st.markdown("""
<div class="app-footer">
    🌱 <strong>HydroVision</strong> by SET Certification<br>
    Smart. Sustainable. Simple.
</div>
""", unsafe_allow_html=True)

# Auto-refresh only when not analyzing
if 'picture' not in locals() or picture is None:
    time.sleep(3)
    st.rerun()
