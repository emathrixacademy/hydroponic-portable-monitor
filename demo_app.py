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

python# AI CAMERA SECTION - FIXED WEBCAM DISPLAY
st.markdown("<h2>📷 AI Plant Health Scanner</h2>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

st.components.v1.html("""
<div style="text-align: center; padding: 20px;">
    <div id="status" style="margin: 10px 0; color: #6B21A8; font-weight: bold;"></div>
    <div id="webcam-container" style="margin: 20px auto; max-width: 350px;"></div>
    <button id="capture-btn" style="
        background: linear-gradient(135deg, #6B21A8 0%, #9333EA 100%);
        color: white;
        border: none;
        padding: 15px 40px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        cursor: pointer;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(107,33,168,0.3);
        display: none;
    ">📸 Capture & Analyze</button>
    <div id="result-container" style="margin-top: 20px;"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest/dist/teachablemachine-image.min.js"></script>

<script type="text/javascript">
    const URL = "https://teachablemachine.withgoogle.com/models/GU_vNr8UW/";
    let model, webcam, isAnalyzing = false;

    const recommendations = {
        'full grown': {
            emoji: '🌟',
            color: '#3b82f6',
            title: 'Full Grown - Ready for Harvest!',
            actions: [
                '✂️ Harvest immediately for best quality',
                '🌅 Best time: Early morning (6-8 AM)',
                '❄️ Store at 4°C with 95% humidity',
                '⏰ Consume within 7 days'
            ]
        },
        'matured': {
            emoji: '✅',
            color: '#22c55e',
            title: 'Matured - Healthy & Growing',
            actions: [
                '✓ Maintain pH at 5.8 ± 0.15',
                '✓ Keep EC at 1.2 ± 0.08 mS/cm',
                '📅 Ready to harvest in 3-5 days',
                '👀 Monitor size daily'
            ]
        },
        'sprout': {
            emoji: '🌱',
            color: '#10b981',
            title: 'Sprout - Early Growth',
            actions: [
                '💧 Keep EC low: 0.8-1.0 mS/cm',
                '✓ Maintain pH at 5.8',
                '☀️ Ensure 12-16 hours light daily',
                '📅 Expect harvest in 21-28 days'
            ]
        },
        'withered': {
            emoji: '🚨',
            color: '#ef4444',
            title: 'Withered - Needs Attention!',
            actions: [
                '🔴 Check water temp: 18-22°C',
                '🌡️ Verify pH level immediately',
                '💨 Improve air circulation',
                '🔬 Remove if disease spreads'
            ]
        }
    };

    async function init() {
        try {
            document.getElementById("status").innerHTML = "🔄 Loading AI model...";
            
            // Load model
            const modelURL = URL + "model.json";
            const metadataURL = URL + "metadata.json";
            model = await tmImage.load(modelURL, metadataURL);
            
            document.getElementById("status").innerHTML = "📷 Starting camera...";
            
            // Setup webcam - try mobile back camera first
            const flip = false;
            webcam = new tmImage.Webcam(320, 320, flip);
            
            await webcam.setup({ 
                facingMode: "environment"  // Use back camera on mobile
            });
            
            await webcam.play();
            
            // Show webcam
            const webcamContainer = document.getElementById("webcam-container");
            webcamContainer.innerHTML = "";
            webcamContainer.appendChild(webcam.canvas);
            
            // Show capture button
            document.getElementById("capture-btn").style.display = "inline-block";
            document.getElementById("capture-btn").addEventListener("click", captureAndAnalyze);
            
            document.getElementById("status").innerHTML = "✅ Camera ready! Point at your lettuce and click capture.";
            
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("status").innerHTML = "❌ Camera Error";
            document.getElementById("webcam-container").innerHTML = `
                <div style="padding: 20px; background: #fee; border: 2px solid #f00; border-radius: 10px; color: #c00;">
                    <h3>Camera Access Issue</h3>
                    <p><strong>On Phone:</strong> Allow camera permission in browser settings</p>
                    <p><strong>On Laptop:</strong> 
                        <br>• Check if another app is using camera
                        <br>• Allow camera in browser (check address bar)
                        <br>• Try Chrome browser for best results
                    </p>
                    <button onclick="location.reload()" style="
                        background: #6B21A8; color: white; padding: 10px 20px; 
                        border: none; border-radius: 5px; cursor: pointer; margin-top: 10px;">
                        🔄 Try Again
                    </button>
                </div>
            `;
        }
    }

    async function captureAndAnalyze() {
        if (isAnalyzing || !webcam) return;
        isAnalyzing = true;
        
        const btn = document.getElementById("capture-btn");
        btn.innerHTML = "🔄 Analyzing...";
        btn.disabled = true;
        
        try {
            // Get prediction
            const prediction = await model.predict(webcam.canvas);
            prediction.sort((a, b) => b.probability - a.probability);
            
            const topResult = prediction[0];
            const className = topResult.className.toLowerCase();
            const confidence = (topResult.probability * 100).toFixed(1);
            
            // Get recommendations
            const rec = recommendations[className] || recommendations['matured'];
            
            // Display result
            let resultHTML = `
                <div style="background: ${rec.color}20; border: 3px solid ${rec.color}; 
                            border-radius: 15px; padding: 25px; margin: 20px 0; text-align: center;">
                    <h2 style="margin: 0; color: ${rec.color}; font-size: 20px;">
                        ${rec.emoji} ${rec.title}
                    </h2>
                    <h1 style="margin: 10px 0; color: #6B21A8; font-size: 48px;">${confidence}%</h1>
                    <p style="margin: 0; color: #6b7280;">AI Confidence</p>
                </div>
                
                <div style="text-align: left; margin: 20px 0; padding: 20px; 
                            background: #f9fafb; border-radius: 10px;">
                    <h3 style="color: #6B21A8; margin-top: 0;">📋 What to Do Next:</h3>
                    ${rec.actions.map((action, i) => 
                        `<p style="margin: 10px 0; color: #1f2937;"><strong>${i+1}.</strong> ${action}</p>`
                    ).join('')}
                </div>
                
                <div style="text-align: left; margin: 20px 0;">
                    <h3 style="color: #6B21A8;">🔍 All Predictions:</h3>
            `;
            
            for (let i = 0; i < prediction.length; i++) {
                const name = prediction[i].className;
                const prob = (prediction[i].probability * 100).toFixed(1);
                const barColor = i === 0 ? rec.color : '#d1d5db';
                
                resultHTML += `
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span style="font-weight: 600; color: #1f2937;">${name}</span>
                            <span style="font-weight: bold; color: ${rec.color};">${prob}%</span>
                        </div>
                        <div style="background: #e5e7eb; border-radius: 10px; height: 25px; overflow: hidden;">
                            <div style="background: ${barColor}; width: ${prob}%; height: 100%; 
                                        transition: width 0.5s ease;"></div>
                        </div>
                    </div>
                `;
            }
            resultHTML += '</div>';
            
            document.getElementById("result-container").innerHTML = resultHTML;
            
        } catch (error) {
            document.getElementById("result-container").innerHTML = 
                '<p style="color: red;">❌ Analysis failed. Please try again.</p>';
        }
        
        // Reset button
        setTimeout(() => {
            btn.innerHTML = "📸 Capture Again";
            btn.disabled = false;
            isAnalyzing = false;
        }, 1000);
    }

    // Start on load
    init();
</script>
""", height=1100)

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
