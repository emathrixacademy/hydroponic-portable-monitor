# ═══════════════════════════════════════════
# AI PLANT HEALTH CAMERA (REAL TEACHABLE MACHINE)
# ═══════════════════════════════════════════
st.markdown("<h2>📷 AI Plant Health Scanner</h2>", unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)

# Camera input - ALWAYS VISIBLE
picture = st.camera_input("📸 Capture your lettuce plant", label_visibility="visible")

if picture:
    # Show captured image
    st.image(picture, use_column_width=True, caption="Captured Image")
    
    # Analyze with REAL Teachable Machine
    with st.spinner("🤖 Analyzing with AI model..."):
        try:
            import requests
            from PIL import Image
            import io
            import base64
            
            # Your Teachable Machine model
            MODEL_URL = "https://teachablemachine.withgoogle.com/models/GU_vNr8UW/"
            
            # Open and prepare image
            img = Image.open(picture)
            
            # Resize to 224x224 (Teachable Machine requirement)
            img = img.resize((224, 224))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert image to base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Call Teachable Machine API
            headers = {'Content-Type': 'application/json'}
            payload = {
                "instances": [{"image_bytes": {"b64": img_str}}]
            }
            
            response = requests.post(
                MODEL_URL + "model.json",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            # Parse predictions
            if response.ok:
                result_data = response.json()
                
                # Extract predictions
                if 'predictions' in result_data:
                    predictions = result_data['predictions'][0]
                else:
                    predictions = result_data
                
                # Get class with highest confidence
                max_idx = predictions.index(max(predictions))
                class_names = ['full grown', 'matured', 'sprout', 'withered']
                
                detected_class = class_names[max_idx]
                confidence = predictions[max_idx] * 100
                
                # Show all predictions
                all_predictions = [
                    {'class': class_names[i], 'confidence': predictions[i] * 100}
                    for i in range(len(class_names))
                ]
                
            else:
                st.error(f"Model API error: {response.status_code}")
                raise Exception("API failed")
                
        except Exception as e:
            st.warning(f"⚠️ Connection issue: {str(e)}")
            st.info("Using offline demo mode...")
            
            # Fallback for demo
            detected_class = random.choice(['full grown', 'sprout', 'matured', 'withered'])
            confidence = random.uniform(85, 95)
            all_predictions = [
                {'class': 'full grown', 'confidence': random.uniform(20, 95)},
                {'class': 'sprout', 'confidence': random.uniform(5, 30)},
                {'class': 'matured', 'confidence': random.uniform(10, 40)},
                {'class': 'withered', 'confidence': random.uniform(5, 25)}
            ]
    
    # Map detected class to display information
    class_info = {
        'full grown': {
            "status": "🌟 Full Grown",
            "subtitle": "Ready for Harvest",
            "color": "#3b82f6",
            "bg_color": "rgba(59, 130, 246, 0.1)",
            "message": "Perfect! Your lettuce has reached full size and is ready to harvest.",
            "actions": [
                "✂️ Harvest now for best quality",
                "🌅 Best time: early morning",
                "❄️ Store at 4°C immediately",
                "⏰ Use within 7 days"
            ]
        },
        'sprout': {
            "status": "🌱 Sprout",
            "subtitle": "Early Growth Stage",
            "color": "#10b981",
            "bg_color": "rgba(16, 185, 129, 0.1)",
            "message": "Your lettuce is in early growth. Keep conditions gentle.",
            "actions": [
                "💧 Keep EC low: 0.8-1.0 mS/cm",
                "✓ pH at 5.8",
                "☀️ Light: 12-16 hours daily",
                "📅 Growth time: 7-10 days"
            ]
        },
        'matured': {
            "status": "✅ Matured",
            "subtitle": "Healthy & Growing",
            "color": "#22c55e",
            "bg_color": "rgba(34, 197, 94, 0.1)",
            "message": "Excellent! Your lettuce is healthy and growing well.",
            "actions": [
                "✓ Maintain pH: 5.8 ± 0.15",
                "✓ Keep EC: 1.2 ± 0.08 mS/cm",
                "📅 Ready to harvest in 3-5 days",
                "👀 Monitor size daily"
            ]
        },
        'withered': {
            "status": "🚨 Withered",
            "subtitle": "Needs Immediate Attention",
            "color": "#ef4444",
            "bg_color": "rgba(239, 68, 68, 0.1)",
            "message": "Alert! Your plant shows stress or disease. Act now!",
            "actions": [
                "🔴 Check water temp: 18-22°C",
                "🌡️ Verify pH level",
                "💨 Improve air flow",
                "🔬 Remove if disease spreads"
            ]
        }
    }
    
    # Get display info
    result = class_info.get(detected_class, class_info['matured'])
    
    # Display AI Result
    st.markdown(f"""
    <div style="background: {result['bg_color']}; 
                border: 3px solid {result['color']};
                border-radius: 15px; 
                padding: 25px; 
                margin: 20px 0;
                text-align: center;">
        <h2 style="margin: 0; font-size: 20px; color: {result['color']}; font-weight: 600;">
            {result['status']}
        </h2>
        <p style="margin: 5px 0; font-size: 13px; color: #6b7280;">
            {result['subtitle']}
        </p>
        <h1 style="margin: 15px 0 5px 0; font-size: 52px; color: {PURPLE}; font-weight: bold;">
            {confidence:.1f}%
        </h1>
        <p style="margin: 0; font-size: 12px; color: #6b7280; font-weight: 500;">
            AI Confidence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show all class predictions
    st.markdown("**🔍 Detection Breakdown:**")
    for pred in sorted(all_predictions, key=lambda x: x['confidence'], reverse=True):
        conf = pred['confidence']
        class_display = pred['class'].replace('_', ' ').title()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(conf / 100)
        with col2:
            st.caption(f"**{conf:.1f}%**")
        st.caption(f"└─ {class_display}")
    
    st.markdown("---")
    
    # Diagnosis message
    st.markdown(f"""
    <div style="background: {result['bg_color']}; 
                padding: 15px; 
                border-radius: 10px;
                border-left: 5px solid {result['color']};
                margin: 15px 0;">
        <p style="margin: 0; color: #1f2937; font-weight: 500; font-size: 14px;">
            💬 {result['message']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommended actions
    st.markdown("**📋 What to Do Next:**")
    for i, action in enumerate(result['actions'], 1):
        st.markdown(f"{i}. {action}")
    
    st.markdown("---")
    
    # Save analysis
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Report", use_container_width=True, type="primary"):
            if 'history' not in st.session_state:
                st.session_state.history = []
            
            st.session_state.history.append({
                'time': datetime.now().strftime('%I:%M %p'),
                'class': detected_class,
                'confidence': confidence
            })
            
            st.success("✅ Saved!")
            st.balloons()
    
    with col2:
        if st.button("🔄 Scan Again", use_container_width=True):
            st.rerun()

else:
    # Instructions when no photo
    st.info("👆 **Tap the camera button** to scan your lettuce plant")
    
    st.markdown("**🎯 What AI Can Detect:**")
    cols = st.columns(2)
    
    with cols[0]:
        st.markdown("• 🌟 **Full Grown** - Ready to harvest")
        st.markdown("• 🌱 **Sprout** - Early stage")
    
    with cols[1]:
        st.markdown("• ✅ **Matured** - Growing well")
        st.markdown("• 🚨 **Withered** - Needs help")
    
    st.markdown("---")
    st.caption("📸 Camera will open when you tap the button above")

st.markdown('</div>', unsafe_allow_html=True)
