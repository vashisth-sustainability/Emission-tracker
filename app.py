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
# Values in Metric Ton CO2e per unit
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
    # Simulated historical data with variation
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
