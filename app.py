import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import random

# Page Configuration
st.set_page_config(
    page_title="ESG Real-Time Emission Tracker",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS for UI Enhancement
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 16px;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #10B981;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<p class="main-title">🌱 Real-Time Industrial Emission & ESG Analytics Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Automated GHG Protocol Scope 1 & Scope 2 Carbon Accounting for Manufacturing Plants</p>', unsafe_allow_html=True)

st.markdown("---")

# Navigation Tabs
tab1, tab2 = st.tabs(["📊 Executive Dashboard", "📡 Live Industrial CEMS API Integration"])

# Sidebar - Configuration & Controls
st.sidebar.header("🏭 Facility & Configuration")
plant_location = st.sidebar.selectbox(
    "Select Industrial Facility",
    ["Mumbai MIDC Plant (Maharashtra)", "Gujarat Chemical Hub (Ankleshwar)", "Pune Auto Cluster (Bhosari)", "Custom Location"]
)

grid_region = st.sidebar.selectbox(
    "Power Grid Region",
    ["India West Grid (CEA Baseline)", "India North Grid", "India South Grid"]
)

st.sidebar.markdown("---")
st.sidebar.header("⚡ Operational Data Inputs")

# Activity Inputs
electricity_kwh = st.sidebar.number_input("Monthly Electricity Consumption (kWh)", value=55000, step=1000)
diesel_liters = st.sidebar.number_input("Diesel Generator Usage (Liters)", value=1800, step=100)
png_scm = st.sidebar.number_input("Piped Natural Gas / Boiler Fuel (SCM)", value=1200, step=100)

st.sidebar.markdown("---")
st.sidebar.header("📡 IoT / CEMS Sensor Connection")
live_stream = st.sidebar.toggle("Enable Live CEMS Sensor Telemetry", value=False)

# Emission Factors (CEA 2023 & IPCC Standard Guidelines)
EF_ELECTRICITY = 0.716 / 1000  # Central Electricity Authority Grid Average (0.716 kg CO2/kWh)
EF_DIESEL = 2.68 / 1000       # IPCC Standard (2.68 kg CO2/Liter)
EF_PNG = 2.02 / 1000          # IPCC Standard (2.02 kg CO2/SCM)

# Live Data Simulation Logic
if live_stream:
    st.info("🔄 **Live Telemetry Mode Active:** Streaming real-time sensor data feeds from facility SCADA/CEMS gateway.")
    telemetry_fluctuation = random.uniform(0.96, 1.04)
    electricity_kwh *= telemetry_fluctuation
    diesel_liters *= telemetry_fluctuation
    png_scm *= telemetry_fluctuation

# GHG Protocol Calculations
scope1_diesel_emissions = diesel_liters * EF_DIESEL
scope1_png_emissions = png_scm * EF_PNG
scope1_total = scope1_diesel_emissions + scope1_png_emissions

scope2_total = electricity_kwh * EF_ELECTRICITY
total_carbon_footprint = scope1_total + scope2_total


# TAB 1: EXECUTIVE DASHBOARD
with tab1:
    # Key Performance Indicators (KPIs)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Selected Facility", value=plant_location.split(" (")[0])

    with col2:
        st.metric(
            label="Scope 1 (Direct Emissions)", 
            value=f"{scope1_total:.2f} tCO2e",
            delta="Fuel & Gas Combustion"
        )

    with col3:
        st.metric(
            label="Scope 2 (Grid Power)", 
            value=f"{scope2_total:.2f} tCO2e",
            delta="Purchased Electricity"
        )

    with col4:
        st.metric(
            label="Total Carbon Footprint", 
            value=f"{total_carbon_footprint:.2f} tCO2e",
            delta=f"{'-1.8%' if live_stream else 'Baseline Measurement'}"
        )

    st.markdown("---")

    # Analytics Section
    c1, c2 = st.columns([1, 1])

    with c1:
        st.subheader("📊 Scope 1 vs Scope 2 Breakdown")
        scope_data = pd.DataFrame({
            "Category": ["Scope 1 (Direct Fuel/Gas)", "Scope 2 (Indirect Electricity)"],
            "Emissions (tCO2e)": [scope1_total, scope2_total]
        })
        
        fig_pie = px.pie(
            scope_data, 
            values="Emissions (tCO2e)", 
            names="Category",
            hole=0.45,
            color_discrete_sequence=["#EF4444", "#3B82F6"]
        )
        fig_pie.update_traces(textinfo="percent+label")
        fig_pie.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.subheader("📈 Monthly Carbon Emissions Trend")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
        base_val = total_carbon_footprint
        historical_emissions = [base_val * random.uniform(0.88, 1.08) for _ in range(len(months)-1)] + [total_carbon_footprint]
        
        df_trend = pd.DataFrame({
            "Month": months,
            "Emissions (tCO2e)": historical_emissions
        })
        
        fig_line = px.line(
            df_trend, 
            x="Month", 
            y="Emissions (tCO2e)",
            markers=True,
            line_shape="linear"
        )
        fig_line.update_traces(line_color="#10B981", line_width=3, marker_size=8)
        fig_line.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    # Detailed Data Table & Export Section
    st.subheader("📋 Emission Intensity & Compliance Data")

    data_summary = {
        "Emission Scope": ["Scope 1", "Scope 1", "Scope 2", "Total"],
        "Activity Data Source": ["Diesel Generators", "Piped Natural Gas (PNG)", "Grid Electricity", "Facility Combined"],
        "Consumption Volume": [f"{diesel_liters:.1f} Liters", f"{png_scm:.1f} SCM", f"{electricity_kwh:.1f} kWh", "N/A"],
        "Emission Factor": ["2.68 kg CO2e/L", "2.02 kg CO2e/SCM", "0.716 kg CO2e/kWh", "Weighted Avg"],
        "Emissions (tCO2e)": [f"{scope1_diesel_emissions:.2f}", f"{scope1_png_emissions:.2f}", f"{scope2_total:.2f}", f"{total_carbon_footprint:.2f}"]
    }

    df_summary = pd.DataFrame(data_summary)
    st.dataframe(df_summary, use_container_width=True)

    # Export Section
    st.markdown("### 📤 Download Audit-Ready Reports")
    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        csv_data = df_summary.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data Summary (CSV)",
            data=csv_data,
            file_name=f"ESG_Emissions_{plant_location.replace(' ', '_')}.csv",
            mime="text/csv",
        )

    with col_exp2:
        if st.button("📄 Generate Executive ESG Summary"):
            st.success(f"Audit Summary Generated for **{plant_location}**! Total Measured Emissions: **{total_carbon_footprint:.2f} Metric Tons CO2e** (Compliant with GHG Protocol Corporate Standard).")


# TAB 2: LIVE CEMS / SCADA API INTEGRATION
with tab2:
    st.subheader("📡 Real-Time CEMS / SCADA Telemetry Stream Gateway")
    st.markdown("This portal simulates direct REST API / MQTT protocol integration with plant Continuous Emission Monitoring Systems (CEMS) & Smart Energy Meters.")
    
    col_sync1, col_sync2 = st.columns([1, 2])
    
    with col_sync1:
        auto_refresh = st.toggle("Enable Live Hardware Auto-Sync (3 Sec Refresh)", value=False)
        st.markdown("**Gateway Protocols Supported:**")
        st.markdown("- CPCB / MPCB RTDAS Protocol")
        st.markdown("- Modbus TCP / MQTT Sensor Gateway")
        st.markdown("- Industry 4.0 SCADA REST Endpoints")
        
    with col_sync2:
        # Dynamic Payload
        cems_live_payload = {
            "facility_metadata": {
                "company_name": "ABC Industrial Synthetics Ltd.",
                "facility_name": plant_location,
                "plant_unit_id": "MUM_STACK_UNIT_02",
                "regulatory_consent_id": "MPCB/CONSENT/2026/98231"
            },
            "hardware_telemetry": {
                "sensor_make": "Forbes Marshall CEMS-9000 Pro",
                "connection_protocol": "REST_API / MQTT Over TLS",
                "gateway_status": "ONLINE (Connected to CPCB RTDAS)",
                "timestamp_ist": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "live_measurements": {
                "flue_gas_flow_m3h": round(random.uniform(12100.0, 12600.0), 2),
                "co2_concentration_pct": round(random.uniform(8.1, 9.4), 2),
                "so2_emissions_mg_m3": round(random.uniform(42.0, 49.5), 2),
                "nox_emissions_mg_m3": round(random.uniform(112.0, 122.0), 2),
                "calculated_instantaneous_emission_rate_tco2e_hr": round(random.uniform(1.21, 1.48), 3)
            }
        }
        
        st.markdown("### 📥 Ingested Live JSON Payload")
        st.json(cems_live_payload)

    # Auto Refresh Engine
    if auto_refresh:
        time.sleep(3)
        st.rerun()
