import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go

# --- PAGE CONFIG FOR MOBILE ---
st.set_page_config(
    page_title="AVCS DNA Mobile",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PWA CONFIGURATION ---
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
    .stButton > button {width: 100%; height: 45px; font-size: 16px !important; margin: 5px 0;}
    [data-testid="metric-container"] {padding: 10px !important; margin: 5px 0 !important; min-height: 80px;}
    .mobile-card {border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin: 5px 0;}
    .status-normal {background-color: #d4edda; border-left: 4px solid #28a745;}
    .status-warning {background-color: #fff3cd; border-left: 4px solid #ffc107;}
    .status-critical {background-color: #f8d7da; border-left: 4px solid #dc3545;}
    .compact-chart {height: 200px !important;}
    @media (max-width: 768px) {
        .element-container {padding: 0px !important;}
        .main .block-container {padding-top: 0.5rem; padding-bottom: 0.5rem;}
    }
</style>
"""
st.markdown(mobile_css, unsafe_allow_html=True)

# --- SYSTEM CONFIG ---
class IndustrialConfig:
    VIBRATION_SENSORS = {
        'VIB_MOTOR_DRIVE': 'Motor Drive',
        'VIB_MOTOR_NONDRIVE': 'Motor Non-Drive', 
        'VIB_PUMP_INLET': 'Pump Inlet',
        'VIB_PUMP_OUTLET': 'Pump Outlet'
    }

    THERMAL_SENSORS = {
        'TEMP_MOTOR_WINDING': 'Motor Winding',
        'TEMP_MOTOR_BEARING': 'Motor Bearing',
        'TEMP_PUMP_BEARING': 'Pump Bearing',
        'TEMP_PUMP_CASING': 'Pump Casing'
    }

    MR_DAMPERS = {
        'DAMPER_FL': 'Front-Left',
        'DAMPER_FR': 'Front-Right', 
        'DAMPER_RL': 'Rear-Left',
        'DAMPER_RR': 'Rear-Right'
    }

    VIBRATION_LIMITS = {'normal': 2.0, 'warning': 4.0, 'critical': 6.0}
    TEMPERATURE_LIMITS = {'normal': 70, 'warning': 85, 'critical': 100}
    DAMPER_FORCES = {'standby': 500, 'normal': 1000, 'warning': 4000, 'critical': 8000}

# --- HEADER ---
st.title("🏭 AVCS DNA Mobile")
st.markdown("**AI-Powered Predictive Maintenance**")

# --- STATE INIT ---
if "system_running" not in st.session_state:
    st.session_state.system_running = False
if "vibration_data" not in st.session_state:
    st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
if "temperature_data" not in st.session_state:
    st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
if "damper_forces" not in st.session_state:
    st.session_state.damper_forces = {damper: 0 for damper in IndustrialConfig.MR_DAMPERS.keys()}
if "risk_history" not in st.session_state:
    st.session_state.risk_history = []
if "ai_model" not in st.session_state:
    normal_vibration = np.random.normal(1.0, 0.3, (100, 4))
    normal_temperature = np.random.normal(65, 5, (100, 4))
    normal_data = np.column_stack([normal_vibration, normal_temperature])
    st.session_state.ai_model = IsolationForest(contamination=0.1, random_state=42)
    st.session_state.ai_model.fit(normal_data)

# --- MOBILE CONTROL PANEL ---
col1, col2 = st.columns(2)
with col1:
    if st.button("⚡ Start System", type="primary", use_container_width=True):
        st.session_state.system_running = True
        st.session_state.vibration_data = pd.DataFrame(columns=list(IndustrialConfig.VIBRATION_SENSORS.keys()))
        st.session_state.temperature_data = pd.DataFrame(columns=list(IndustrialConfig.THERMAL_SENSORS.keys()))
        st.session_state.damper_forces = {damper: IndustrialConfig.DAMPER_FORCES['standby'] for damper in IndustrialConfig.MR_DAMPERS.keys()}
        st.session_state.risk_history = []
        st.rerun()
with col2:
    if st.button("🛑 Stop", use_container_width=True):
        st.session_state.system_running = False
        st.session_state.damper_forces = {damper: 0 for damper in IndustrialConfig.MR_DAMPERS.keys()}
        st.rerun()

# --- MAIN SIMULATION ---
if not st.session_state.system_running:
    st.info("🚀 System ready. Click 'Start System' to begin.")
else:
    # Progress and Status
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # Mobile-optimized layout
    tab1, tab2, tab3 = st.tabs(["📊 Monitoring", "🤖 AI Analysis", "🔧 Control"])
    
    max_cycles = 50
    current_cycle = 0
    
    with tab1:
        # Vibration Monitoring
        st.subheader("📈 Vibration")
        vib_col1, vib_col2 = st.columns([2, 1])
        
        with vib_col1:
            vib_chart = st.empty()
        with vib_col2:
            vib_status = st.empty()
        
        # Temperature Monitoring  
        st.subheader("🌡️ Temperature")
        temp_col1, temp_col2 = st.columns([2, 1])
        
        with temp_col1:
            temp_chart = st.empty()
        with temp_col2:
            temp_status = st.empty()
    
    with tab2:
        st.subheader("AI Risk Analysis")
        ai_col1, ai_col2 = st.columns(2)
        
        with ai_col1:
            gauge_placeholder = st.empty()
        with ai_col2:
            ai_metrics = st.empty()
    
    with tab3:
        st.subheader("🔄 MR Dampers")
        damper_status = st.empty()
        damper_chart = st.empty()
    
    # Simulation Loop
    while current_cycle < max_cycles and st.session_state.system_running:
        # Data Generation (same logic as desktop)
        if current_cycle < 15:
            # Normal operation
            vibration = {k: max(0.1, 1.0 + np.random.normal(0, 0.2)) for k in IndustrialConfig.VIBRATION_SENSORS.keys()}
            temperature = {k: max(20, 65 + np.random.normal(0, 3)) for k in IndustrialConfig.THERMAL_SENSORS.keys()}
        elif current_cycle < 30:
            # Gradual degradation
            degradation = (current_cycle - 15) * 0.1
            vibration = {k: max(0.1, 1.0 + degradation + np.random.normal(0, 0.3)) for k in IndustrialConfig.VIBRATION_SENSORS.keys()}
            temperature = {k: max(20, 65 + degradation * 2 + np.random.normal(0, 4)) for k in IndustrialConfig.THERMAL_SENSORS.keys()}
        else:
            # Critical condition
            vibration = {k: max(0.1, 5.0 + np.random.normal(0, 0.5)) for k in IndustrialConfig.VIBRATION_SENSORS.keys()}
            temperature = {k: max(20, 95 + np.random.normal(0, 5)) for k in IndustrialConfig.THERMAL_SENSORS.keys()}

        # Save data
        st.session_state.vibration_data.loc[current_cycle] = vibration
        st.session_state.temperature_data.loc[current_cycle] = temperature

        # AI Analysis
        features = list(vibration.values()) + list(temperature.values())
        ai_prediction = st.session_state.ai_model.predict([features])[0]
        ai_conf = st.session_state.ai_model.decision_function([features])[0]
        risk_index = min(100, max(0, int(abs(ai_conf) * 100)))

        # RUL Calculation
        rul_hours = max(0, int(100 - risk_index))

        st.session_state.risk_history.append(risk_index)

        # Damper Control Logic
        if ai_prediction == -1 or risk_index > 80:
            damper_force = IndustrialConfig.DAMPER_FORCES['critical']
            system_status = "🚨 CRITICAL"
            status_color = "red"
        elif risk_index > 50:
            damper_force = IndustrialConfig.DAMPER_FORCES['warning'] 
            system_status = "⚠️ WARNING"
            status_color = "orange"
        elif risk_index > 20:
            damper_force = IndustrialConfig.DAMPER_FORCES['normal']
            system_status = "✅ NORMAL"
            status_color = "green"
        else:
            damper_force = IndustrialConfig.DAMPER_FORCES['standby']
            system_status = "🟢 STANDBY"
            status_color = "blue"

        st.session_state.damper_forces = {d: damper_force for d in IndustrialConfig.MR_DAMPERS.keys()}

        # UPDATE DISPLAYS
        with status_placeholder.container():
            st.markdown(f"<h3 style='color: {status_color}; text-align: center;'>{system_status}</h3>", unsafe_allow_html=True)
        
        with progress_placeholder.container():
            st.progress((current_cycle + 1) / max_cycles, text=f"Cycle: {current_cycle+1}/{max_cycles}")

        # Tab 1: Monitoring
        with tab1:
            # Vibration
            with vib_chart.container():
                if len(st.session_state.vibration_data) > 0:
                    fig_vib = go.Figure()
                    for sensor in IndustrialConfig.VIBRATION_SENSORS.keys():
                        fig_vib.add_trace(go.Scatter(
                            y=st.session_state.vibration_data[sensor].tail(20),
                            mode='lines',
                            name=IndustrialConfig.VIBRATION_SENSORS[sensor]
                        ))
                    fig_vib.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
                    st.plotly_chart(fig_vib, use_container_width=True, config={'displayModeBar': False})
            
            with vib_status.container():
                for k, v in vibration.items():
                    status_class = "status-normal" if v < 2 else "status-warning" if v < 4 else "status-critical"
                    st.markdown(f'<div class="mobile-card {status_class}">{IndustrialConfig.VIBRATION_SENSORS[k]}: {v:.1f} mm/s</div>', unsafe_allow_html=True)

            # Temperature
            with temp_chart.container():
                if len(st.session_state.temperature_data) > 0:
                    fig_temp = go.Figure()
                    for sensor in IndustrialConfig.THERMAL_SENSORS.keys():
                        fig_temp.add_trace(go.Scatter(
                            y=st.session_state.temperature_data[sensor].tail(20),
                            mode='lines', 
                            name=IndustrialConfig.THERMAL_SENSORS[sensor]
                        ))
                    fig_temp.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
                    st.plotly_chart(fig_temp, use_container_width=True, config={'displayModeBar': False})
            
            with temp_status.container():
                for k, v in temperature.items():
                    status_class = "status-normal" if v < 70 else "status-warning" if v < 85 else "status-critical"
                    st.markdown(f'<div class="mobile-card {status_class}">{IndustrialConfig.THERMAL_SENSORS[k]}: {v:.0f}°C</div>', unsafe_allow_html=True)

        # Tab 2: AI Analysis
        with tab2:
            with gauge_placeholder.container():
                gauge_fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk_index,
                    title={'text': "Risk Index"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "green"},
                            {'range': [50, 80], 'color': "yellow"}, 
                            {'range': [80, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': risk_index
                        }
                    }
                ))
                gauge_fig.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(gauge_fig, use_container_width=True, config={'displayModeBar': False})
            
            with ai_metrics.container():
                st.metric("🤖 AI Confidence", f"{abs(ai_conf):.3f}")
                if rul_hours < 24:
                    st.error(f"⏳ RUL: {rul_hours}h")
                elif rul_hours < 72:
                    st.warning(f"⏳ RUL: {rul_hours}h") 
                else:
                    st.success(f"⏳ RUL: {rul_hours}h")

        # Tab 3: Dampers Control
        with tab3:
            with damper_status.container():
                cols = st.columns(2)
                damper_items = list(IndustrialConfig.MR_DAMPERS.items())
                for i, (d, loc) in enumerate(damper_items):
                    with cols[i % 2]:
                        force = st.session_state.damper_forces[d]
                        if force >= 4000:
                            st.error(f"🔴 {loc}\n{force} N")
                        elif force >= 1000:
                            st.warning(f"🟡 {loc}\n{force} N")
                        else:
                            st.success(f"🟢 {loc}\n{force} N")
            
            with damper_chart.container():
                if current_cycle > 0:
                    force_data = pd.DataFrame({
                        'Cycle': range(current_cycle + 1),
                        'Damper Force': [damper_force] * (current_cycle + 1)
                    })
                    st.line_chart(force_data, x='Cycle', y='Damper Force', height=200)

        current_cycle += 1
        time.sleep(1.0)  # Slower for mobile

    if current_cycle >= max_cycles:
        st.success("✅ Simulation completed!")
        st.session_state.system_running = False

st.markdown("---")
st.caption("AVCS DNA Mobile v5.2 | Predictive Maintenance System")
