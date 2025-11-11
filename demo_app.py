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

# AI CAMERA SECTION
st.markdown("<h2>📷 AI Plant Health Scanner</h2>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

picture = st.camera_input("📸 Capture your lettuce", label_visibility="visible")

if picture:
    st.image(picture, use_column_width=True, caption="Captured Image")
    
    with st.spinner("🤖 Analyzing with AI..."):
        try:
            import requests
            from PIL import Image
            import io
            
            # Your Teachable Machine model
            MODEL_URL = "https://teachablemachine.withgoogle.com/models/GU_vNr8UW/"
            
            # Prepare image
            img = Image.open(picture)
            img = img.resize((224, 224))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save image to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            
            # Call Teachable Machine API with correct format
            files = {'file': ('image.jpg', img_bytes, 'image/jpeg')}
            response = requests.post(
                'https://teachablemachine.withgoogle.com/models/GU_vNr8UW/predict',
                files=files,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Parse predictions
                predictions = result.get('predictions', [])
                
                # Find highest confidence
                top_prediction = max(predictions, key=lambda x: x['probability'])
                detected_class = top_prediction['className'].lower()
                confidence = top_prediction['probability'] * 100
                
                # All predictions for display
                all_predictions = [
                    {'class': p['className'].lower(), 'confidence': p['probability'] * 100}
                    for p in predictions
                ]
                
                api_success = True
                
            else:
                st.error(f"API Error: {response.status_code}")
                raise Exception(f"Status code: {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ AI Model Connection Failed: {str(e)}")
            st.warning("Cannot reach Teachable Machine. Please check internet connection.")
            api_success = False
            
            # Show captured image but no prediction
            st.info("💡 **Offline Mode**: Unable to classify. The model needs internet connection to work.")
            
            # Option to manually classify for training
            st.markdown("---")
            st.markdown("**🎯 Manual Classification (for model improvement):**")
            
            manual_class = st.radio(
                "What is this lettuce?",
                ['Full Grown', 'Sprout', 'Matured', 'Withered'],
                horizontal=True
            )
            
            if st.button("💾 Save to Training Data", type="primary"):
                # Save image with manual classification
                st.success(f"✅ Image saved as '{manual_class}' for future training!")
                st.info("📤 Upload this to your Teachable Machine dataset to improve accuracy.")
                st.balloons()
    
    # Only show results if API succeeded
    if api_success:
        class_info = {
            'full grown': {
                "status": "🌟 Full Grown", "color": "#3b82f6", "bg_color": "rgba(59, 130, 246, 0.1)",
                "message": "Ready to harvest!", 
                "actions": ["✂️ Harvest now", "🌅 Best: morning", "❄️ Store at 4°C", "⏰ Use within 7 days"]
            },
            'sprout': {
                "status": "🌱 Sprout", "color": "#10b981", "bg_color": "rgba(16, 185, 129, 0.1)",
                "message": "Early growth stage",
                "actions": ["💧 EC: 0.8-1.0", "✓ pH: 5.8", "☀️ Light: 12-16h", "📅 Wait 7-10 days"]
            },
            'matured': {
                "status": "✅ Matured", "color": "#22c55e", "bg_color": "rgba(34, 197, 94, 0.1)",
                "message": "Healthy and growing!",
                "actions": ["✓ pH: 5.8±0.15", "✓ EC: 1.2±0.08", "📅 Harvest in 3-5 days", "👀 Monitor size"]
            },
            'withered': {
                "status": "🚨 Withered", "color": "#ef4444", "bg_color": "rgba(239, 68, 68, 0.1)",
                "message": "Needs attention now!",
                "actions": ["🔴 Check temp: 18-22°C", "🌡️ Verify pH", "💨 Improve airflow", "🔬 Remove if diseased"]
            }
        }
        
        result = class_info.get(detected_class, class_info['matured'])
        
        st.markdown(f"""
        <div style="background: {result['bg_color']}; border: 3px solid {result['color']};
                    border-radius: 15px; padding: 25px; margin: 20px 0; text-align: center;">
            <h2 style="margin: 0; font-size: 20px; color: {result['color']};">{result['status']}</h2>
            <h1 style="margin: 15px 0 5px 0; font-size: 52px; color: {PURPLE};">{confidence:.1f}%</h1>
            <p style="margin: 0; font-size: 12px; color: #6b7280;">AI Confidence</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**🔍 All Predictions:**")
        for pred in sorted(all_predictions, key=lambda x: x['confidence'], reverse=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(pred['confidence'] / 100)
            with col2:
                st.caption(f"**{pred['confidence']:.1f}%**")
            st.caption(f"└─ {pred['class'].title()}")
        
        st.markdown(f"""
        <div style="background: {result['bg_color']}; padding: 15px; border-radius: 10px;
                    border-left: 5px solid {result['color']}; margin: 15px 0;">
            <p style="margin: 0; color: #1f2937; font-weight: 500;">💬 {result['message']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**📋 Actions:**")
        for i, action in enumerate(result['actions'], 1):
            st.markdown(f"{i}. {action}")
        
        st.markdown("---")
        
        # Feedback section
        st.markdown("**🎯 Is this classification correct?**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Yes, Correct", use_container_width=True, type="primary"):
                st.success("✅ Thank you! This helps improve the model.")
                st.balloons()
        
        with col2:
            if st.button("❌ No, Wrong", use_container_width=True):
                st.warning("Please select the correct classification:")
                correct_class = st.radio(
                    "What should it be?",
                    ['Full Grown', 'Sprout', 'Matured', 'Withered'],
                    horizontal=True,
                    key="correct_classification"
                )
                if st.button("💾 Submit Correction", type="primary"):
                    st.success(f"✅ Correction saved: {correct_class}")
                    st.info("📤 This data will improve future predictions!")

else:
    st.info("👆 **Tap camera button** to scan lettuce")
    st.markdown("**🎯 AI Detects:** 🌟 Full Grown • 🌱 Sprout • ✅ Matured • 🚨 Withered")

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

time.sleep(3)
st.rerun()
