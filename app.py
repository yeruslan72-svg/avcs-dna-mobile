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
    .mobile-good {background-color: #00C851; color: white; padding: 15px; border-radius: 10px; margin: 10px 0;}
    .animation-container {border: 2px solid #0A5FBC; border-radius: 10px; padding: 10px; margin: 10px 0;}
    .smooth-chart {transition: all 0.3s ease-in-out;}
    @media (max-width: 768px) {
        .element-container {padding: 0px !important;}
        .stAlert {margin: 5px 0 !important;}
        .main .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    }
</style>
"""

st.markdown(mobile_css, unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ СЕССИИ ---
if 'smooth_data' not in st.session_state:
    st.session_state.smooth_data = {
        'time_points': list(range(20)),  # Фиксированные 20 точек времени
        'vibration_data': [2.0] * 20,   # Начальные данные
        'temperature_data': [65.0] * 20,
        'is_running': False,
        'current_index': 0
    }

# --- ГЛАДКАЯ АНИМАЦИЯ С ПРЕДСКАЗУЕМЫМ ОБНОВЛЕНИЕМ ---
def create_smooth_chart():
    st.markdown("### 🎥 Live Equipment Monitoring")
    
    # Управление анимацией
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Start", use_container_width=True, type="primary"):
            st.session_state.smooth_data['is_running'] = True
            st.rerun()
    
    with col2:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.smooth_data['is_running'] = False
            st.rerun()
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.smooth_data = {
                'time_points': list(range(20)),
                'vibration_data': [2.0] * 20,
                'temperature_data': [65.0] * 20,
                'is_running': False,
                'current_index': 0
            }
            st.rerun()
    
    # Слайдер скорости
    speed = st.select_slider("Animation Speed", 
                           options=["Very Slow", "Slow", "Normal", "Fast", "Very Fast"],
                           value="Normal")
    
    speed_map = {"Very Slow": 1.0, "Slow": 0.7, "Normal": 0.4, "Fast": 0.2, "Very Fast": 0.1}
    
    # Основной контейнер для анимации
    chart_placeholder = st.empty()
    metrics_placeholder = st.empty()
    progress_placeholder = st.empty()
    
    # Запуск плавной анимации
    if st.session_state.smooth_data['is_running']:
        max_steps = 100
        
        for step in range(st.session_state.smooth_data['current_index'], max_steps):
            if not st.session_state.smooth_data['is_running']:
                st.session_state.smooth_data['current_index'] = step
                break
            
            # ПЛАВНОЕ ОБНОВЛЕНИЕ ДАННЫХ - сдвигаем массив
            current_vibration = 2.0 + (step * 0.1) + np.sin(step * 0.3) * 0.5 + np.random.normal(0, 0.05)
            current_temperature = 65 + (step * 0.5) + np.cos(step * 0.2) * 2 + np.random.normal(0, 0.3)
            
            # Сдвигаем массивы для плавного движения
            st.session_state.smooth_data['vibration_data'] = st.session_state.smooth_data['vibration_data'][1:] + [current_vibration]
            st.session_state.smooth_data['temperature_data'] = st.session_state.smooth_data['temperature_data'][1:] + [current_temperature]
            
            st.session_state.smooth_data['current_index'] = step
            
            # ОБНОВЛЯЕМ ТОЛЬКО ГРАФИКИ - без перерисовки всего интерфейса
            with chart_placeholder.container():
                # График вибрации с плавными линиями
                fig_vib = go.Figure()
                
                fig_vib.add_trace(go.Scatter(
                    x=st.session_state.smooth_data['time_points'],
                    y=st.session_state.smooth_data['vibration_data'],
                    mode='lines',
                    name='Vibration',
                    line=dict(color='#0A5FBC', width=4, shape='spline'),
                    fill='tozeroy',
                    fillcolor='rgba(10, 95, 188, 0.1)'
                ))
                
                # Добавляем плавные пороговые линии
                fig_vib.add_hline(y=3.0, line_dash="dash", line_color="orange", 
                                annotation_text="Warning", annotation_position="right")
                fig_vib.add_hline(y=4.0, line_dash="dash", line_color="red", 
                                annotation_text="Critical", annotation_position="right")
                
                fig_vib.update_layout(
                    height=280,
                    margin=dict(l=0, r=0, t=40, b=0),
                    title=dict(
                        text="Real-time Vibration Monitoring",
                        x=0.5,
                        font=dict(size=16)
                    ),
                    xaxis_title="Time (seconds)",
                    yaxis_title="Vibration (mm/s)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                
                st.plotly_chart(fig_vib, use_container_width=True, config={'displayModeBar': False})
            
            # ОБНОВЛЯЕМ МЕТРИКИ ОТДЕЛЬНО
            with metrics_placeholder.container():
                col1, col2 = st.columns(2)
                with col1:
                    vib_status = "🔴 CRITICAL" if current_vibration > 4.0 else "🟡 WARNING" if current_vibration > 3.0 else "🟢 NORMAL"
                    st.metric("📊 Vibration", f"{current_vibration:.2f} mm/s", vib_status)
                with col2:
                    temp_status = "🔴 HIGH" if current_temperature > 80 else "🟢 NORMAL"
                    st.metric("🌡️ Temperature", f"{current_temperature:.1f}°C", temp_status)
            
            # ОБНОВЛЯЕМ ПРОГРЕСС БАР
            with progress_placeholder.container():
                progress = step / max_steps
                st.progress(progress, text=f"Simulation: {step}/{max_steps} steps")
            
            # Плавная пауза между кадрами
            time.sleep(speed_map[speed])
        
        # Автостоп в конце
        if step >= max_steps - 1:
            st.session_state.smooth_data['is_running'] = False
            st.session_state.smooth_data['current_index'] = 0
            
    else:
        # Статичное отображение при паузе
        with chart_placeholder.container():
            if st.session_state.smooth_data['current_index'] > 0:
                # Показываем последний кадр анимации
                fig_static = go.Figure()
                fig_static.add_trace(go.Scatter(
                    x=st.session_state.smooth_data['time_points'],
                    y=st.session_state.smooth_data['vibration_data'],
                    mode='lines',
                    name='Vibration',
                    line=dict(color='#0A5FBC', width=4, shape='spline'),
                    fill='tozeroy',
                    fillcolor='rgba(10, 95, 188, 0.1)'
                ))
                
                fig_static.add_hline(y=3.0, line_dash="dash", line_color="orange")
                fig_static.add_hline(y=4.0, line_dash="dash", line_color="red")
                
                fig_static.update_layout(
                    height=280,
                    margin=dict(l=0, r=0, t=40, b=0),
                    title="Vibration Monitoring (Paused)",
                    showlegend=False
                )
                
                st.plotly_chart(fig_static, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("🎬 Press START to begin real-time monitoring")

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
def mobile_dashboard():
    st.title("🏭 AVCS DNA Mobile")
    st.markdown("**Real-time Equipment Monitoring**")
    
    # Статус система
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 System Status", "ACTIVE", "94%")
        st.metric("🚨 Active Alerts", "1")
    with col2:
        st.metric("⏳ RUL", "52 days")
        st.metric("🔧 Equipment", "6 units")
    
    # Запускаем гладкую анимацию
    create_smooth_chart()
    
    # Быстрые действия
    st.markdown("### 🎛 Quick Actions")
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("📊 Health Report", use_container_width=True):
            st.success("📋 Comprehensive report generated!")
        if st.button("🔔 Test Alert", use_container_width=True):
            st.toast("Test notification sent!", icon="📱")
    
    with action_col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        if st.button("🛑 Emergency", use_container_width=True, type="secondary"):
            st.error("🚨 EMERGENCY PROCEDURE ACTIVATED!")
    
    st.markdown("---")
    st.markdown("📱 **AVCS DNA Mobile v2.1** | Smooth real-time animation")

if __name__ == "__main__":
    mobile_dashboard()
