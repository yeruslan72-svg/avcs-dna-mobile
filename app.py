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
    .compact-chart {height: 200px !important;}
    @media (max-width: 768px) {
        .element-container {padding: 0px !important;}
        .stAlert {margin: 5px 0 !important;}
        /* Уменьшаем отступы для мобильных */
        .main .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    }
</style>
"""

st.markdown(mobile_css, unsafe_allow_html=True)

# --- MOBILE DASHBOARD ---
def mobile_dashboard():
    st.title("🏭 AVCS DNA Mobile")
    st.markdown("**Field Operator Edition**")
    
    # Real-time Status Panel - БОЛЕЕ КОМПАКТНАЯ
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 Status", "ACTIVE", "85%")
        st.metric("🚨 Alerts", "2")
    with col2:
        st.metric("⏳ RUL", "45d")
        st.metric("🔧 Units", "12")
    
    # Alert Section - УПРОЩЕННАЯ
    st.markdown("### 🔔 Active Alerts")
    
    with st.expander("View Alerts", expanded=True):
        alert_col1, alert_col2 = st.columns(2)
        with alert_col1:
            st.markdown('<div class="mobile-alert">HIGH VIB<br>Pump A-205<br>6.8 mm/s</div>', unsafe_allow_html=True)
        with alert_col2:
            st.markdown('<div class="mobile-warning">TEMP RISE<br>Compressor<br>89°C</div>', unsafe_allow_html=True)
    
    # Quick Actions - ПЕРЕМЕЩЕНЫ ВВЕРХ
    st.markdown("### 🎛 Quick Actions")
    
    # Кнопки управления анимацией
    control_col1, control_col2, control_col3 = st.columns(3)
    with control_col1:
        if st.button("▶️ Start", use_container_width=True, key="start_anim"):
            st.session_state.animation_running = True
            st.toast("Animation started", icon="▶️")
    with control_col2:
        if st.button("⏸️ Pause", use_container_width=True, key="pause_anim"):
            st.session_state.animation_running = False
            st.toast("Animation paused", icon="⏸️")
    with control_col3:
        if st.button("🔄 Reset", use_container_width=True, key="reset_anim"):
            st.session_state.animation_running = False
            st.rerun()
    
    # Equipment Health - УПРОЩЕННЫЕ ПРОГРЕСС БАРЫ
    st.markdown("### 📈 Equipment Health")
    
    equipment_data = [
        {"name": "Turbine T-101", "health": 85, "status": "Normal"},
        {"name": "Compressor C-102", "health": 45, "status": "Warning"},
        {"name": "Pump A-205", "health": 92, "status": "Normal"},
        {"name": "Generator G-304", "health": 78, "status": "Normal"}
    ]
    
    for equipment in equipment_data:
        status_color = "🔴" if equipment["status"] == "Warning" else "🟢"
        st.write(f"{status_color} {equipment['name']}: {equipment['health']}%")
        st.progress(equipment['health']/100)
    
    # Vibration Chart - КОМПАКТНЫЙ ГРАФИК
    st.markdown("### 📊 Vibration Monitor")
    
    # Генерируем упрощенные данные
    time_points = list(range(24))
    vibration_data = np.random.normal(2.5, 0.8, 24)
    vibration_data[20:] = np.random.normal(5.5, 1.2, 4)  # Симуляция неисправности
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_points, 
        y=vibration_data, 
        mode='lines', 
        name='Vibration',
        line=dict(color='#0A5FBC', width=3)
    ))
    
    # Горизонтальные линии порогов
    fig.add_hline(y=4.0, line_dash="dash", line_color="orange", annotation_text="Warning")
    fig.add_hline(y=6.0, line_dash="dash", line_color="red", annotation_text="Critical")
    
    fig.update_layout(
        height=250,  # УМЕНЬШЕННАЯ ВЫСОТА
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="Time (hours)",
        yaxis_title="Vibration (mm/s)",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Live Animation Section - УПРОЩЕННАЯ
    if st.checkbox("🎥 Show Live Demo", key="show_demo"):
        st.markdown("#### Real-time Simulation")
        
        # Простая анимация с контролем скорости
        speed = st.select_slider("Animation Speed", options=["Slow", "Normal", "Fast"], value="Normal")
        speeds = {"Slow": 2.0, "Normal": 1.0, "Fast": 0.5}
        
        placeholder = st.empty()
        
        if st.button("Start Simulation", key="start_sim"):
            for i in range(20):
                with placeholder.container():
                    # Упрощенные данные для анимации
                    current_vib = 2.0 + (i * 0.3) + np.random.normal(0, 0.2)
                    current_temp = 65 + (i * 1.5) + np.random.normal(0, 2)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Current Vibration", f"{current_vib:.1f} mm/s")
                    with col2:
                        st.metric("Current Temperature", f"{current_temp:.0f}°C")
                    
                    # Мини-график
                    mini_fig = go.Figure()
                    mini_fig.add_trace(go.Scatter(
                        x=list(range(i+1)), 
                        y=[2.0 + (x * 0.3) for x in range(i+1)],
                        mode='lines+markers',
                        line=dict(color='#0A5FBC')
                    ))
                    mini_fig.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
                    st.plotly_chart(mini_fig, use_container_width=True, config={'displayModeBar': False})
                
                time.sleep(speeds[speed])
    
    # Footer
    st.markdown("---")
    st.markdown("📱 **AVCS DNA Mobile v1.1** | Optimized for mobile devices")

# Initialize session state
if 'animation_running' not in st.session_state:
    st.session_state.animation_running = False

# Run the mobile dashboard
if __name__ == "__main__":
    mobile_dashboard()
