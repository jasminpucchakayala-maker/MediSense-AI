import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
from styles.theme import get_theme_css

st.set_page_config(
    page_title="Analytics Dashboard | MediSense AI",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Path Resolution & Theme Loading
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
CSS_FILE = BASE_DIR / "styles" / "custom.css"

if "theme" not in st.session_state:
    st.session_state.theme = "light"

try:
    with open(CSS_FILE, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading custom stylesheet: {str(e)}")

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# Main Title & Hero Header
st.markdown(
    """
    <div style='margin-bottom: 40px;' class='animate-fade-in'>
        <h1 style='font-size: 2.8rem; font-weight: 800;'>Healthcare Analytics Dashboard</h1>
        <p style='color: var(--text-muted); font-size: 1.1rem;'>Macro-level insights into patient diagnostics and platform utilization.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

history_file = BASE_DIR / "data" / "prediction_history.csv"

# -----------------------------
# Data Loading & Caching
# -----------------------------
@st.cache_data(show_spinner=False)
def load_data():
    if os.path.exists(history_file):
        df = pd.read_csv(history_file)
        
        # Parse Dates safely
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
            df = df.dropna(subset=["Date"])
            
        # Guarantee fallback columns exist
        if "Confidence" not in df.columns:
            df["Confidence"] = 85.0
        else:
            df["Confidence"] = df["Confidence"].fillna(85.0).astype(float)

        if "Risk Level" not in df.columns:
            df["Risk Level"] = "Medium"
        else:
            df["Risk Level"] = df["Risk Level"].fillna("Medium")
            
        return df
    else:
        return pd.DataFrame()

df = load_data()

# Clean empty state transition if no history exists
if df.empty:
    st.info("ℹ️ No prediction history found in this database yet. Run an analysis on the disease prediction page first to generate analytics.")
    st.stop()

df = df.sort_values(by="Date")

# -----------------------------
# Advanced Filters Sidebar/Top Layer
# -----------------------------
st.markdown("<h4 style='font-weight: 700; margin-bottom: 15px;'>Clinical Filters</h4>", unsafe_allow_html=True)
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    disease_filter = st.multiselect("Select Disease Profile(s)", options=sorted(df["Disease"].unique()), default=[])
with f_col2:
    risk_filter = st.multiselect("Select Severity Range", options=["Low", "Medium", "High", "Severe"], default=[])
with f_col3:
    min_date = df["Date"].min().date() if not df.empty else pd.Timestamp.now().date()
    max_date = df["Date"].max().date() if not df.empty else pd.Timestamp.now().date()
    date_range = st.date_input("Select Date Range", value=(min_date, max_date))

# Filter evaluation logic
filtered_df = df.copy()
if disease_filter: 
    filtered_df = filtered_df[filtered_df["Disease"].isin(disease_filter)]
if risk_filter: 
    filtered_df = filtered_df[filtered_df["Risk Level"].isin(risk_filter)]
if len(date_range) == 2:
    s_date, e_date = date_range
    filtered_df = filtered_df[(filtered_df["Date"].dt.date >= s_date) & (filtered_df["Date"].dt.date <= e_date)]

# Transition if filters exclude everything
if filtered_df.empty:
    st.warning("⚠️ No records match the selected metrics range combinations.")
    st.stop()

# -----------------------------
# KPI Calculations
# -----------------------------
total_pred = len(filtered_df)
avg_conf = filtered_df["Confidence"].mean()
high_risk = len(filtered_df[filtered_df["Risk Level"].isin(["High", "Severe"])])
most_common = filtered_df["Disease"].mode()[0] if not filtered_df.empty else "N/A"

# Time analysis elements
today = pd.Timestamp.now().normalize()
week_ago = today - pd.Timedelta(days=7)
predictions_today = len(filtered_df[filtered_df["Date"] >= today])
predictions_week = len(filtered_df[filtered_df["Date"] >= week_ago])

# Theme configurations
theme_mode = st.session_state.theme
text_color = "#F8FAFC" if theme_mode == "dark" else "#0F172A"

# Layout: Metric Cards Layer
c1, c2, c3, c4 = st.columns(4)
with c1: 
    st.metric("Total Case Studies", total_pred, f"+{predictions_week} this wk")
with c2: 
    st.metric("Average Confidence", f"{avg_conf:.1f}%", f"+{(avg_conf - 80.0):.1f}% over baseline")
with c3: 
    st.metric("Critical Risk Cases", high_risk, delta_color="inverse")
with c4: 
    st.metric("Dominant Symptom Profile", most_common)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Charts Section
# -----------------------------
row1_1, row1_2 = st.columns([2, 1])

with row1_1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Health Scan Trends over Timeline</h4>", unsafe_allow_html=True)
    trend = filtered_df.groupby("Date").size().reset_index(name="Count")
    fig_line = px.area(trend, x="Date", y="Count", color_discrete_sequence=["#3B82F6"])
    fig_line.update_layout(
        height=350, 
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Inter", size=12, color=text_color),
        xaxis_title="",
        yaxis_title=""
    )
    st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with row1_2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Severity Matrix (Risk Level)</h4>", unsafe_allow_html=True)
    risk_cnt = filtered_df["Risk Level"].value_counts().reset_index()
    risk_cnt.columns = ["Risk", "Count"]
    color_map = {"Low": "#10B981", "Medium": "#F59E0B", "High": "#EF4444", "Severe": "#991B1B"}
    fig_pie = px.pie(risk_cnt, names="Risk", values="Count", hole=0.7, color="Risk", color_discrete_map=color_map)
    fig_pie.update_layout(
        height=350, 
        paper_bgcolor="rgba(0,0,0,0)", 
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Inter", size=12, color=text_color)
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

row2_1, row2_2 = st.columns([1, 1])

with row2_1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Top Diagnosed medical Profiles</h4>", unsafe_allow_html=True)
    top_d = filtered_df["Disease"].value_counts().head(8).reset_index()
    top_d.columns = ["Disease", "Count"]
    fig_bar = px.bar(top_d, x="Count", y="Disease", orientation='h', color="Count", color_continuous_scale="Blues")
    fig_bar.update_layout(
        height=350, 
        yaxis={'categoryorder':'total ascending'}, 
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Inter", size=12, color=text_color),
        xaxis_title="",
        yaxis_title=""
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with row2_2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Average Confidence Gauge</h4>", unsafe_allow_html=True)
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_conf,
        number={'suffix': '%'},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': text_color},
            'bar': {'color': '#3B82F6', 'thickness': 0.3},
            'bgcolor': 'rgba(0,0,0,0.05)',
            'steps': [
                {'range': [0, 60], 'color': 'rgba(239, 68, 68, 0.1)'},
                {'range': [60, 80], 'color': 'rgba(245, 158, 11, 0.1)'},
                {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.1)'}
            ]
        }
    ))
    fig_gauge.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=50, b=10),
        font=dict(family="Inter", size=12, color=text_color)
    )
    st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Export Staged Data
# -----------------------------
st.markdown("<h4 style='font-weight: 700; margin-bottom: 15px;'>Dataset Export</h4>", unsafe_allow_html=True)
c_csv, c_spacer = st.columns([1.5, 3])
with c_csv:
    st.download_button(
        label="📥 Download Filtered Analytics History (CSV)",
        data=filtered_df.to_csv(index=False),
        file_name="medisense_filtered_analytics.csv",
        mime="text/csv",
        use_container_width=True
    )
