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
    
    /* Remove default Streamlit padding */
    .main {{
        padding: 0;
        max-width: 100%;
    }}
    
    /* Phone frame container */
    .phone-frame {{
        position: relative;
        max-width: 400px;
        margin: 50px auto;
        background-image: url('https://raw.githubusercontent.com/emathrixacademy/hydroponic-portable-monitor/main/assets/phone-frame.png');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        padding: 70px 25px 70px 25px;  /* Adjust based on your phone frame */
        min-height: 800px;
    }}
    
    /* Content inside phone */
    .block-container {{
        padding: 35px 20px 20px 20px;
        max-height: 740px;
        overflow-y: auto;
        overflow-x: hidden;
        background: {WHITE};
        border-radius: 35px;
    }}
    
    /* Custom scrollbar */
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
    
    /* Rest of your existing styles... */
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

Replace the camera section with this mobile-friendly version:
python# AI CAMERA SECTION - MOBILE OPTIMIZED
st.markdown("<h2>📷 AI Plant Health Scanner</h2>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

st.components.v1.html("""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 10px; margin: 0; }
        #webcam-container { margin: 15px auto; max-width: 100%; }
        canvas { border: 3px solid #6B21A8; border-radius: 15px; max-width: 100%; height: auto; }
        button { 
            background: linear-gradient(135deg, #6B21A8 0%, #9333EA 100%);
            color: white; border: none; padding: 12px 30px; font-size: 16px;
            font-weight: bold; border-radius: 10px; cursor: pointer; margin: 10px;
            width: 90%; max-width: 300px;
        }
        button:disabled { opacity: 0.5; }
        .status { color: #6B21A8; font-weight: bold; margin: 10px; font-size: 13px; }
        #live-container, #result-container { margin: 15px auto; max-width: 90%; }
        .live-bar { margin: 8px 0; }
        .bar-label { font-weight: 600; margin-bottom: 3px; color: #1f2937; font-size: 13px; text-align: left; }
        .bar-bg { background: #e5e7eb; border-radius: 8px; height: 25px; overflow: hidden; }
        .bar-fill { height: 100%; transition: width 0.3s; display: flex; align-items: center; 
                    justify-content: center; color: white; font-weight: bold; font-size: 12px; }
        .result-box { border-radius: 15px; padding: 20px; margin: 15px 0; }
        .actions { text-align: left; background: #f9fafb; padding: 15px; border-radius: 10px; margin: 15px 0; }
        .actions h3 { color: #6B21A8; margin-top: 0; font-size: 16px; }
        .actions p { margin: 8px 0; color: #1f2937; font-size: 13px; }
    </style>
</head>
<body>
    <div class="status" id="status">🔄 Initializing...</div>
    <div id="webcam-container"></div>
    <button id="start-btn" onclick="startCamera()" style="display:block;">📷 Start Camera</button>
    <button id="capture-btn" onclick="captureAndAnalyze()" style="display:none;">📸 Capture & Analyze</button>
    <div id="live-container"></div>
    <div id="result-container"></div>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest"></script>
    
    <script>
        const URL = "https://teachablemachine.withgoogle.com/models/GU_vNr8UW/";
        let model, webcam, maxPredictions, isRunning = false, isAnalyzing = false;

        const recommendations = {
            'full grown': { emoji: '🌟', color: '#3b82f6', title: 'Full Grown - Ready!', 
                actions: ['✂️ Harvest now', '🌅 Morning best', '❄️ Store 4°C', '⏰ 7 days'] },
            'matured': { emoji: '✅', color: '#22c55e', title: 'Matured - Healthy',
                actions: ['✓ pH: 5.8±0.15', '✓ EC: 1.2±0.08', '📅 3-5 days', '👀 Monitor'] },
            'sprout': { emoji: '🌱', color: '#10b981', title: 'Sprout - Early',
                actions: ['💧 EC: 0.8-1.0', '✓ pH: 5.8', '☀️ 12-16h', '📅 21-28 days'] },
            'withered': { emoji: '🚨', color: '#ef4444', title: 'Withered - Alert',
                actions: ['🔴 18-22°C', '🌡️ Check pH', '💨 Airflow', '🔬 Remove'] }
        };

        async function startCamera() {
            try {
                document.getElementById('status').innerHTML = '🔄 Loading AI model...';
                
                model = await tmImage.load(URL + "model.json", URL + "metadata.json");
                maxPredictions = model.getTotalClasses();
                
                document.getElementById('status').innerHTML = '📷 Starting camera...';
                
                // Mobile-optimized webcam setup
                const size = Math.min(300, window.innerWidth - 40);
                webcam = new tmImage.Webcam(size, size, false);
                
                await webcam.setup({ 
                    facingMode: "environment",
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                });
                
                await webcam.play();
                isRunning = true;
                window.requestAnimationFrame(loop);

                document.getElementById("webcam-container").appendChild(webcam.canvas);
                
                const liveContainer = document.getElementById("live-container");
                liveContainer.innerHTML = '';
                for (let i = 0; i < maxPredictions; i++) {
                    liveContainer.appendChild(document.createElement("div"));
                }
                
                document.getElementById('start-btn').style.display = 'none';
                document.getElementById('capture-btn').style.display = 'block';
                document.getElementById('status').innerHTML = '✅ Ready! Point at lettuce';
                
            } catch (error) {
                document.getElementById('status').innerHTML = '❌ Camera Error';
                document.getElementById("webcam-container").innerHTML = 
                    '<div style="color: red; padding: 15px; background: #fee; border-radius: 10px; margin: 10px;">' +
                    '<h3 style="margin-top:0;">Cannot Access Camera</h3>' +
                    '<p><strong>On Phone:</strong><br>• Use Chrome browser<br>• Allow camera permission<br>• Check if another app is using camera</p>' +
                    '<p><strong>Error:</strong> ' + error.message + '</p>' +
                    '<button onclick="location.reload()" style="margin-top:10px;">🔄 Try Again</button></div>';
            }
        }

        async function loop() {
            if (!isRunning) return;
            webcam.update();
            await showLivePredictions();
            window.requestAnimationFrame(loop);
        }

        async function showLivePredictions() {
            const prediction = await model.predict(webcam.canvas);
            prediction.sort((a, b) => b.probability - a.probability);
            
            const liveContainer = document.getElementById("live-container");
            
            for (let i = 0; i < maxPredictions; i++) {
                const className = prediction[i].className;
                const probability = (prediction[i].probability * 100).toFixed(1);
                
                let color = '#3b82f6';
                if (className.toLowerCase().includes('sprout')) color = '#10b981';
                if (className.toLowerCase().includes('matured')) color = '#22c55e';
                if (className.toLowerCase().includes('withered')) color = '#ef4444';
                
                liveContainer.childNodes[i].innerHTML = 
                    '<div class="live-bar">' +
                    '<div class="bar-label">' + (i === 0 ? '🎯 ' : '') + className + '</div>' +
                    '<div class="bar-bg">' +
                    '<div class="bar-fill" style="background: ' + color + '; width: ' + probability + '%;">' + 
                    probability + '%</div></div></div>';
            }
        }

        async function captureAndAnalyze() {
            if (isAnalyzing || !isRunning) return;
            isAnalyzing = true;
            
            const btn = document.getElementById("capture-btn");
            btn.innerHTML = "🔄 Analyzing...";
            btn.disabled = true;
            
            const prediction = await model.predict(webcam.canvas);
            prediction.sort((a, b) => b.probability - a.probability);
            
            const topResult = prediction[0];
            const className = topResult.className.toLowerCase();
            const confidence = (topResult.probability * 100).toFixed(1);
            const rec = recommendations[className] || recommendations['matured'];
            
            let html = '<div class="result-box" style="background: ' + rec.color + '20; border: 3px solid ' + rec.color + ';">' +
                '<h2 style="margin: 0; color: ' + rec.color + ';">' + rec.emoji + ' ' + rec.title + '</h2>' +
                '<h1 style="margin: 10px 0; color: #6B21A8; font-size: 42px;">' + confidence + '%</h1>' +
                '<p style="color: #6b7280; margin: 0;">AI Confidence</p></div>' +
                '<div class="actions"><h3>📋 What to Do Next:</h3>';
            
            rec.actions.forEach((action, i) => {
                html += '<p><strong>' + (i+1) + '.</strong> ' + action + '</p>';
            });
            
            html += '</div><div class="actions"><h3>🔍 All Predictions:</h3>';
            
            for (let i = 0; i < prediction.length; i++) {
                const name = prediction[i].className;
                const prob = (prediction[i].probability * 100).toFixed(1);
                const barColor = i === 0 ? rec.color : '#d1d5db';
                
                html += '<div style="margin: 8px 0;">' +
                    '<div style="display: flex; justify-content: space-between; margin-bottom: 3px; font-size: 13px;">' +
                    '<span style="font-weight: 600;">' + name + '</span>' +
                    '<span style="font-weight: bold; color: ' + rec.color + ';">' + prob + '%</span></div>' +
                    '<div class="bar-bg"><div style="background: ' + barColor + '; width: ' + prob + '%; height: 100%;"></div></div></div>';
            }
            html += '</div>';
            
            document.getElementById('result-container').innerHTML = html;
            
            setTimeout(() => {
                btn.innerHTML = "📸 Capture Again";
                btn.disabled = false;
                isAnalyzing = false;
            }, 1000);
        }
    </script>
</body>
</html>
""", height=1300)

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
