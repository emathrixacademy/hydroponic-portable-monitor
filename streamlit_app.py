"""
========================================
HYDROPONIC MONITORING DASHBOARD
========================================

Real-time monitoring dashboard for IoT-based hydroponic system
Built with Streamlit for cloud deployment

Features:
- Real-time sensor monitoring
- Historical data trends
- AI plant health classification
- System control interface
- Data export functionality

========================================
"""

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import json
import time

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Hydroponic Monitor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CUSTOM CSS STYLING
# ========================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-good {
        color: #4CAF50;
        font-weight: bold;
    }
    .status-warning {
        color: #FF9800;
        font-weight: bold;
    }
    .status-critical {
        color: #F44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# FIREBASE INITIALIZATION
# ========================================
@st.cache_resource
def init_firebase():
    """Initialize Firebase connection"""
    try:
        # Check if Firebase is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Initialize Firebase with Streamlit secrets
        cred_dict = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

    return firestore.client()

# ========================================
# DATA RETRIEVAL FUNCTIONS
# ========================================
def get_current_sensor_data(db):
    """Retrieve latest sensor readings from Firestore"""
    try:
        doc = db.collection('sensors').document('current').get()
        if doc.exists:
            data = doc.to_dict()
            # Add timestamp formatting
            if 'timestamp' in data:
                data['datetime'] = datetime.fromtimestamp(data['timestamp'])
            return data
        return None
    except Exception as e:
        st.error(f"Error retrieving sensor data: {str(e)}")
        return None

def get_historical_data(db, hours=24):
    """Retrieve historical sensor data"""
    try:
        # Calculate timestamp for X hours ago
        cutoff_time = int((datetime.now() - timedelta(hours=hours)).timestamp())

        # Query Firestore
        docs = db.collection('sensors').document('history').collection('readings')\
            .where('timestamp', '>=', cutoff_time)\
            .order_by('timestamp', direction=firestore.Query.ASCENDING)\
            .stream()

        data_list = []
        for doc in docs:
            record = doc.to_dict()
            record['datetime'] = datetime.fromtimestamp(record['timestamp'])
            data_list.append(record)

        return pd.DataFrame(data_list) if data_list else pd.DataFrame()
    except Exception as e:
        st.error(f"Error retrieving historical data: {str(e)}")
        return pd.DataFrame()

def get_latest_image_data(db):
    """Retrieve latest plant image and AI classification"""
    try:
        doc = db.collection('images').document('latest').get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        st.error(f"Error retrieving image data: {str(e)}")
        return None

# ========================================
# VISUALIZATION FUNCTIONS
# ========================================
def create_gauge_chart(value, min_val, max_val, target, tolerance, title, unit):
    """Create a gauge chart for sensor display"""

    # Determine color based on target range
    if target - tolerance <= value <= target + tolerance:
        color = "#4CAF50"  # Green - Good
    elif target - 2*tolerance <= value <= target + 2*tolerance:
        color = "#FF9800"  # Orange - Warning
    else:
        color = "#F44336"  # Red - Critical

    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"{title}<br><span style='font-size:0.8em'>{unit}</span>"},
        delta = {'reference': target},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': [min_val, target - tolerance], 'color': "lightgray"},
                {'range': [target - tolerance, target + tolerance], 'color': "lightgreen"},
                {'range': [target + tolerance, max_val], 'color': "lightgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target
            }
        }
    ))

    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_time_series_chart(df, column, title, color):
    """Create time series chart for historical data"""
    if df.empty:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['datetime'],
        y=df[column],
        mode='lines+markers',
        name=title,
        line=dict(color=color, width=2),
        marker=dict(size=4)
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title=column,
        hovermode='x unified',
        height=300
    )

    return fig

# ========================================
# STATUS EVALUATION FUNCTIONS
# ========================================
def evaluate_status(value, target, tolerance):
    """Determine if value is within acceptable range"""
    if target - tolerance <= value <= target + tolerance:
        return "✓ OPTIMAL", "status-good"
    elif target - 2*tolerance <= value <= target + 2*tolerance:
        return "⚠ WARNING", "status-warning"
    else:
        return "✗ CRITICAL", "status-critical"

# ========================================
# MAIN APPLICATION
# ========================================
def main():
    # Initialize Firebase
    db = init_firebase()

    # Header
    st.markdown('<div class="main-header">🌱 Hydroponic Monitoring System</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio("Go to", [
        "🏠 Dashboard",
        "📈 Historical Trends",
        "🤖 AI Plant Health",
        "⚙️ System Control",
        "📥 Data Export"
    ])

    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh (every 5s)", value=True)
    if auto_refresh:
        time.sleep(5)
        st.rerun()

    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.info("**System Status**\n\nConnected to Firebase ✓")

    # ========================================
    # PAGE: DASHBOARD
    # ========================================
    if page == "🏠 Dashboard":
        st.header("Real-Time Monitoring Dashboard")

        # Retrieve current data
        current_data = get_current_sensor_data(db)

        if current_data is None:
            st.warning("⚠ No sensor data available. Check ESP32 connection.")
            st.info("**Troubleshooting:**\n- Verify ESP32 is powered on\n- Check WiFi connection\n- Confirm Firebase credentials")
            return

        # Display last update time
        if 'datetime' in current_data:
            st.caption(f"Last updated: {current_data['datetime'].strftime('%Y-%m-%d %H:%M:%S')}")

        # Create gauge charts
        col1, col2, col3 = st.columns(3)

        with col1:
            st.plotly_chart(
                create_gauge_chart(
                    current_data.get('pH', 0),
                    min_val=4.0,
                    max_val=8.0,
                    target=5.8,
                    tolerance=0.15,
                    title="pH Level",
                    unit="pH"
                ),
                use_container_width=True
            )
            status, status_class = evaluate_status(current_data.get('pH', 0), 5.8, 0.15)
            st.markdown(f'<p class="{status_class}">{status}</p>', unsafe_allow_html=True)

        with col2:
            st.plotly_chart(
                create_gauge_chart(
                    current_data.get('ec', 0),
                    min_val=0.0,
                    max_val=3.0,
                    target=1.2,
                    tolerance=0.08,
                    title="EC Level",
                    unit="mS/cm"
                ),
                use_container_width=True
            )
            status, status_class = evaluate_status(current_data.get('ec', 0), 1.2, 0.08)
            st.markdown(f'<p class="{status_class}">{status}</p>', unsafe_allow_html=True)

        with col3:
            st.plotly_chart(
                create_gauge_chart(
                    current_data.get('waterTemp', 0),
                    min_val=10.0,
                    max_val=30.0,
                    target=20.0,
                    tolerance=2.0,
                    title="Water Temperature",
                    unit="°C"
                ),
                use_container_width=True
            )
            status, status_class = evaluate_status(current_data.get('waterTemp', 0), 20.0, 2.0)
            st.markdown(f'<p class="{status_class}">{status}</p>', unsafe_allow_html=True)

        st.markdown("---")

        # Additional metrics
        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric("Air Temperature", f"{current_data.get('airTemp', 0):.1f} °C")
            st.metric("Humidity", f"{current_data.get('humidity', 0):.1f} %")

        with col5:
            st.metric("TDS", f"{current_data.get('tds', 0):.0f} ppm")
            st.metric("Water Level", f"{current_data.get('waterLevel', 0):.1f} cm")

        with col6:
            # System health summary
            ph_ok = evaluate_status(current_data.get('pH', 0), 5.8, 0.15)[0] == "✓ OPTIMAL"
            ec_ok = evaluate_status(current_data.get('ec', 0), 1.2, 0.08)[0] == "✓ OPTIMAL"
            temp_ok = evaluate_status(current_data.get('waterTemp', 0), 20.0, 2.0)[0] == "✓ OPTIMAL"

            overall_status = "🟢 HEALTHY" if all([ph_ok, ec_ok, temp_ok]) else "🟡 ATTENTION NEEDED"
            st.metric("System Status", overall_status)

    # ========================================
    # PAGE: HISTORICAL TRENDS
    # ========================================
    elif page == "📈 Historical Trends":
        st.header("Historical Data Analysis")

        # Time range selector
        time_range = st.selectbox("Select time range", ["Last 24 hours", "Last 48 hours", "Last 7 days"])
        hours_map = {"Last 24 hours": 24, "Last 48 hours": 48, "Last 7 days": 168}
        selected_hours = hours_map[time_range]

        # Retrieve historical data
        df = get_historical_data(db, hours=selected_hours)

        if df.empty:
            st.warning("⚠ No historical data available yet.")
            st.info("Historical data will appear after the system has been running for some time.")
            return

        # Display charts
        st.subheader("pH Trend")
        st.plotly_chart(create_time_series_chart(df, 'pH', 'pH Level Over Time', '#2196F3'), use_container_width=True)

        st.subheader("EC Trend")
        st.plotly_chart(create_time_series_chart(df, 'ec', 'EC Level Over Time', '#4CAF50'), use_container_width=True)

        st.subheader("Temperature Trends")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_time_series_chart(df, 'waterTemp', 'Water Temperature', '#FF5722'), use_container_width=True)
        with col2:
            st.plotly_chart(create_time_series_chart(df, 'airTemp', 'Air Temperature', '#FF9800'), use_container_width=True)

        # Statistics summary
        st.subheader("Statistics Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg pH", f"{df['pH'].mean():.2f}")
            st.metric("Min pH", f"{df['pH'].min():.2f}")
            st.metric("Max pH", f"{df['pH'].max():.2f}")
        with col2:
            st.metric("Avg EC", f"{df['ec'].mean():.2f}")
            st.metric("Min EC", f"{df['ec'].min():.2f}")
            st.metric("Max EC", f"{df['ec'].max():.2f}")
        with col3:
            st.metric("Avg Water Temp", f"{df['waterTemp'].mean():.1f} °C")
            st.metric("Min Water Temp", f"{df['waterTemp'].min():.1f} °C")
            st.metric("Max Water Temp", f"{df['waterTemp'].max():.1f} °C")
        with col4:
            st.metric("Avg Humidity", f"{df['humidity'].mean():.1f} %")
            st.metric("Min Humidity", f"{df['humidity'].min():.1f} %")
            st.metric("Max Humidity", f"{df['humidity'].max():.1f} %")

    # ========================================
    # PAGE: AI PLANT HEALTH
    # ========================================
    elif page == "🤖 AI Plant Health":
        st.header("AI-Powered Plant Health Analysis")

        # Retrieve latest image data
        image_data = get_latest_image_data(db)

        if image_data is None:
            st.warning("⚠ No plant images available yet.")
            st.info("The ESP32-CAM will capture images hourly. Check back soon!")
            return

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Latest Plant Image")
            if 'imageURL' in image_data:
                st.image(image_data['imageURL'], caption="Current plant condition", use_container_width=True)
            else:
                st.warning("Image URL not available")

        with col2:
            st.subheader("AI Classification")

            if 'aiClass' in image_data:
                ai_class = image_data['aiClass']
                confidence = image_data.get('aiConfidence', 0) * 100

                # Display classification with styling
                class_colors = {
                    'healthy': '🟢',
                    'nutrient_deficiency': '🟡',
                    'disease': '🔴',
                    'optimal_growth': '🟢'
                }

                icon = class_colors.get(ai_class.lower(), '⚪')
                st.markdown(f"### {icon} {ai_class.upper()}")
                st.progress(confidence / 100)
                st.caption(f"Confidence: {confidence:.1f}%")

                # Recommendations
                st.markdown("---")
                st.subheader("Recommendations")

                if ai_class == 'healthy':
                    st.success("✓ Plants are healthy! Continue current care routine.")
                elif ai_class == 'nutrient_deficiency':
                    st.warning("⚠ Nutrient deficiency detected. Consider:\n- Increasing nutrient concentration\n- Checking pH balance\n- Verifying EC levels")
                elif ai_class == 'disease':
                    st.error("✗ Disease detected! Action required:\n- Inspect plants closely\n- Remove affected leaves\n- Check water quality\n- Consider fungicide treatment")
                elif ai_class == 'optimal_growth':
                    st.success("✓ Optimal growth conditions! Plants are thriving.")

            # Timestamp
            if 'timestamp' in image_data:
                capture_time = datetime.fromtimestamp(image_data['timestamp'])
                st.caption(f"Captured: {capture_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # ========================================
    # PAGE: SYSTEM CONTROL
    # ========================================
    elif page == "⚙️ System Control":
        st.header("System Control Panel")

        st.warning("⚠️ Manual control overrides automatic adjustments. Use with caution!")

        # Automatic control toggle
        st.subheader("Automatic Control")
        auto_enabled = st.checkbox("Enable automatic pH/EC adjustment", value=True)

        if auto_enabled:
            st.success("✓ Automatic control is ENABLED. System will adjust pH and EC automatically.")
        else:
            st.warning("⚠ Automatic control is DISABLED. Manual intervention required.")

        st.markdown("---")

        # Manual pump controls
        st.subheader("Manual Pump Control")
        st.caption("Activate pumps manually (use for testing or emergency adjustments)")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Activate pH-UP Pump", type="primary"):
                st.info("Signal sent to ESP32... (Implementation: Update Firestore control document)")
                # TODO: Update Firestore document to trigger pump

        with col2:
            if st.button("Activate pH-DOWN Pump", type="primary"):
                st.info("Signal sent to ESP32... (Implementation: Update Firestore control document)")

        with col3:
            if st.button("Activate Nutrient Pump", type="primary"):
                st.info("Signal sent to ESP32... (Implementation: Update Firestore control document)")

        st.markdown("---")

        # Target setpoints
        st.subheader("Target Setpoints")

        col1, col2 = st.columns(2)

        with col1:
            target_ph = st.number_input("Target pH", min_value=4.0, max_value=8.0, value=5.8, step=0.1)
            ph_tolerance = st.number_input("pH Tolerance (±)", min_value=0.05, max_value=0.5, value=0.15, step=0.05)

        with col2:
            target_ec = st.number_input("Target EC (mS/cm)", min_value=0.5, max_value=3.0, value=1.2, step=0.1)
            ec_tolerance = st.number_input("EC Tolerance (±)", min_value=0.02, max_value=0.2, value=0.08, step=0.02)

        if st.button("Save Setpoints"):
            st.success("✓ Setpoints saved! (Implementation: Update Firestore control document)")
            # TODO: Update Firestore with new setpoints

    # ========================================
    # PAGE: DATA EXPORT
    # ========================================
    elif page == "📥 Data Export":
        st.header("Data Export & Reports")

        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", datetime.now() - timedelta(days=7))
        with col2:
            end_date = st.date_input("End date", datetime.now())

        # Retrieve data
        hours_diff = int((end_date - start_date).total_seconds() / 3600)
        df = get_historical_data(db, hours=hours_diff)

        if df.empty:
            st.warning("No data available for selected date range")
            return

        # Display data preview
        st.subheader("Data Preview")
        st.dataframe(df.head(100))

        st.caption(f"Total records: {len(df)}")

        # Export button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"hydroponic_data_{start_date}_{end_date}.csv",
            mime="text/csv"
        )

        # Summary report
        st.markdown("---")
        st.subheader("Summary Report")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**pH Statistics**")
            st.write(df['pH'].describe())

        with col2:
            st.markdown("**EC Statistics**")
            st.write(df['ec'].describe())

# ========================================
# RUN APPLICATION
# ========================================
if __name__ == "__main__":
    main()
