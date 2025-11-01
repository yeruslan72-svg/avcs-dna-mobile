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
    @media (max-width: 768px) {
        .element-container {padding: 0px !important;}
        .stAlert {margin: 5px 0 !important;}
        .main .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    }
</style>
"""

st.markdown(mobile_css, unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ СЕССИИ ---
if 'animation_data' not in st.session_state:
    st.session_state.animation_data = {
        'time_points': [],
        'vibration_data': [],
        'temperature_data': [],
        'is_running': False,
        'current_step': 0
    }

# --- МОБИЛЬНАЯ АНИМАЦИЯ ---
def smooth_animation():
    st.markdown("### 🎥 Live Equipment Monitoring")
    
    # Управление анимацией
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Start", use_container_width=True, type="primary"):
            st.session_state.animation_data['is_running'] = True
            st.rerun()
    
    with col2:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.animation_data['is_running'] = False
            st.rerun()
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.animation_data = {
                'time_points': [],
                'vibration_data': [], 
                'temperature_data': [],
                'is_running': False,
                'current_step': 0
            }
            st.rerun()
    
    # Слайдер скорости
    speed = st.select_slider("Animation Speed", 
                           options=["Very Slow", "Slow", "Normal", "Fast", "Very Fast"],
                           value="Normal")
    
    speed_map = {"Very Slow": 2.0, "Slow": 1.5, "Normal": 1.0, "Fast": 0.5, "Very Fast": 0.2}
    
    # Контейнер для анимации
    animation_placeholder = st.empty()
    
    # Запуск анимации
    if st.session_state.animation_data['is_running']:
        max_steps = 50
        
        for step in range(st.session_state.animation_data['current_step'], max_steps):
            if not st.session_state.animation_data['is_running']:
                break
                
            # Обновляем данные
            current_time = step
            vibration = 2.0 + (step * 0.15) + np.random.normal(0, 0.1)
            temperature = 65 + (step * 0.8) + np.random.normal(0, 1)
            
            # Сохраняем историю (последние 20 точек)
            st.session_state.animation_data['time_points'].append(current_time)
            st.session_state.animation_data['vibration_data'].append(vibration)
            st.session_state.animation_data['temperature_data'].append(temperature)
            
            # Ограничиваем историю для производительности
            if len(st.session_state.animation_data['time_points']) > 20:
                st.session_state.animation_data['time_points'] = st.session_state.animation_data['time_points'][-20:]
                st.session_state.animation_data['vibration_data'] = st.session_state.animation_data['vibration_data'][-20:]
                st.session_state.animation_data['temperature_data'] = st.session_state.animation_data['temperature_data'][-20:]
            
            st.session_state.animation_data['current_step'] = step
            
            # Отрисовываем кадр анимации
            with animation_placeholder.container():
                st.markdown('<div class="animation-container">', unsafe_allow_html=True)
                
                # Текущие показатели
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📊 Vibration", f"{vibration:.2f} mm/s", 
                             delta="↑ Critical" if vibration > 4.0 else "↑ Warning" if vibration > 3.0 else "✓ Normal")
                with col2:
                    st.metric("🌡️ Temperature", f"{temperature:.1f}°C",
                             delta="↑ High" if temperature > 80 else "✓ Normal")
                
                # График вибрации
                fig_vib = go.Figure()
                fig_vib.add_trace(go.Scatter(
                    x=st.session_state.animation_data['time_points'],
                    y=st.session_state.animation_data['vibration_data'],
                    mode='lines+markers',
                    name='Vibration',
                    line=dict(color='#0A5FBC', width=4),
                    marker=dict(size=8)
                ))
                
                fig_vib.add_hline(y=3.0, line_dash="dash", line_color="orange", annotation_text="Warning")
                fig_vib.add_hline(y=4.0, line_dash="dash", line_color="red", annotation_text="Critical")
                
                fig_vib.update_layout(
                    height=250,
                    margin=dict(l=0, r=0, t=30, b=0),
                    title="Real-time Vibration Monitoring",
                    showlegend=False
                )
                
                st.plotly_chart(fig_vib, use_container_width=True, config={'displayModeBar': False})
                
                # Прогресс симуляции
                progress = step / max_steps
                st.progress(progress, text=f"Simulation Progress: {step}/{max_steps}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Пауза между кадрами
            time.sleep(speed_map[speed])
        
        # Автоматическая остановка в конце
        if step >= max_steps - 1:
            st.session_state.animation_data['is_running'] = False
            st.success("✅ Simulation completed!")
    else:
        # Статичное отображение когда анимация остановлена
        with animation_placeholder.container():
            if st.session_state.animation_data['time_points']:
                st.markdown('<div class="animation-container">', unsafe_allow_html=True)
                st.info("⏸️ Animation paused. Press Start to continue.")
                
                # Показываем последние данные
                if st.session_state.animation_data['vibration_data']:
                    last_vib = st.session_state.animation_data['vibration_data'][-1]
                    last_temp = st.session_state.animation_data['temperature_data'][-1]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Last Vibration", f"{last_vib:.2f} mm/s")
                    with col2:
                        st.metric("Last Temperature", f"{last_temp:.1f}°C")
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("🎬 Press Start to begin live monitoring simulation")

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
def mobile_dashboard():
    st.title("🏭 AVCS DNA Mobile")
    st.markdown("**Live Equipment Monitoring**")
    
    # Статус система
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 System Status", "ACTIVE", "92%")
        st.metric("🚨 Active Alerts", "1")
    with col2:
        st.metric("⏳ RUL", "45 days")
        st.metric("🔧 Equipment", "8 units")
    
    # Запускаем анимацию
    smooth_animation()
    
    # Быстрые действия
    st.markdown("### 🎛 Quick Actions")
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("📋 Equipment health report generated!")
        if st.button("🔔 Test Alert", use_container_width=True):
            st.toast("Test notification sent to all devices!", icon="📱")
    
    with action_col2:
        if st.button("🔄 Refresh All", use_container_width=True):
            st.rerun()
        if st.button("🛑 Emergency Stop", use_container_width=True):
            st.error("🚨 EMERGENCY STOP - All systems halting!")
    
    # Footer
    st.markdown("---")
    st.markdown("📱 **AVCS DNA Mobile v2.0** | Real-time animation demo")

# Запуск приложения
if __name__ == "__main__":
    mobile_dashboard()
