import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# --- PWA CONFIGURATION ---
st.set_page_config(
    page_title="AVCS DNA Mobile",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject PWA meta tags
pwa_meta = """
<link rel="manifest" href="./manifest.json">
<meta name="theme-color" content="#0A5FBC">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
"""

st.markdown(pwa_meta, unsafe_allow_html=True)

# --- MOBILE-OPTIMIZED CSS ---
mobile_css = """
<style>
    .main > div {max-width: 100% !important; padding: 5px;}
    .stButton > button {width: 100%; height: 50px; font-size: 18px !important; margin: 8px 0;}
    [data-testid="metric-container"] {padding: 15px !important; margin: 10px 0 !important;}
    .mobile-alert {background-color: #ff4444; color: white; padding: 15px; border-radius: 10px; margin: 10px 0;}
    .mobile-warning {background-color: #ffaa00; color: white; padding: 15px; border-radius: 10px; margin: 10px 0;}
    @media (max-width: 768px) {
        .element-container {padding: 0px !important;}
        .stAlert {margin: 5px 0 !important;}
    }
</style>
"""

st.markdown(mobile_css, unsafe_allow_html=True)

# --- MOBILE DASHBOARD ---
def mobile_dashboard():
    st.title("🏭 AVCS DNA Mobile")
    st.markdown("**Field Operator Edition**")
    
    # Real-time Status Panel
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 System Status", "ACTIVE", "85%", delta_color="normal")
        st.metric("🚨 Active Alerts", "2")
    with col2:
        st.metric("⏳ RUL", "45 days")
        st.metric("🔧 Equipment", "12 units")
    
    # Alert Section
    st.markdown("### 🔔 Recent Alerts")
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        st.markdown('<div class="mobile-alert">HIGH VIBRATION<br>Pump A-205<br>6.8 mm/s</div>', unsafe_allow_html=True)
    
    with alert_col2:
        st.markdown('<div class="mobile-warning">TEMPERATURE RISE<br>Compressor C-102<br>89°C</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### 🎛 Quick Actions")
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("🔄 Refresh Data", use_container_width=True, key="refresh"):
            st.rerun()
        if st.button("📊 Generate Report", use_container_width=True, key="report"):
            st.toast("📋 Report generation started...", icon="✅")
    
    with action_col2:
        if st.button("🔔 Test Notification", use_container_width=True, key="test_alert"):
            st.toast("🔔 Test notification sent!", icon="📱")
        if st.button("🛑 Emergency Stop", use_container_width=True, key="emergency"):
            st.error("🚨 EMERGENCY STOP ACTIVATED!")
    
    # Equipment Health Overview
    st.markdown("### 📈 Equipment Health")
    
    # Simple health bars for mobile
    equipment_data = {
        'Equipment': ['Turbine T-101', 'Compressor C-102', 'Pump A-205', 'Generator G-304'],
        'Health': [85, 45, 92, 78],
        'Status': ['Normal', 'Warning', 'Normal', 'Normal']
    }
    
    df = pd.DataFrame(equipment_data)
    
    for _, row in df.iterrows():
        status_color = "#EF553B" if row['Status'] == 'Warning' else "#00CC96"
        st.progress(row['Health']/100, text=f"{row['Equipment']}: {row['Health']}%")
    
    # Simple vibration chart
    st.markdown("### 📊 Vibration Trend")
    
    # Generate sample vibration data
    time_points = pd.date_range(start='2024-01-01', periods=24, freq='H')
    vibration_data = np.random.normal(2.5, 0.8, 24)
    vibration_data[20:] = np.random.normal(5.5, 1.2, 4)  # Simulate fault
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_points, y=vibration_data, mode='lines', name='Vibration', line=dict(color='#0A5FBC')))
    fig.add_hline(y=4.0, line_dash="dash", line_color="red", annotation_text="Warning Level")
    fig.add_hline(y=6.0, line_dash="dash", line_color="red", annotation_text="Critical Level")
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="Time",
        yaxis_title="Vibration (mm/s)",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("📱 **AVCS DNA Mobile v1.0** | Add to Home Screen for best experience")

# Run the mobile dashboard
if __name__ == "__main__":
    mobile_dashboard()
