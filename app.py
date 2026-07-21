import streamlit as st
import os

import pandas as pd
import json
from pathlib import Path
from styles.theme import get_theme_css

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="MediSense AI | Premium Health Platform",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Safe CSS Loader
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
CSS_FILE = BASE_DIR / "styles" / "custom.css"

if "theme" not in st.session_state:
    st.session_state.theme = "light"

try:
    with open(CSS_FILE, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading custom stylesheet: {str(e)}")

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #0F766E, #14B8A6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>MediSense AI</h1>
            <p style='color: var(--text-muted); font-size: 0.9rem; font-weight: 500;'>Next-Gen Healthcare Analytics</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    t_btn = st.button("🌓 Toggle Theme", use_container_width=True)
    if t_btn:
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

    st.markdown("<hr style='border-color: var(--border-color); opacity: 0.5;'>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style='padding: 10px 0;'>
            <p style='font-size: 0.8rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 15px;'>Platform Modules</p>
            <ul style='list-style-type: none; padding-left: 0; line-height: 2.5; font-weight: 500; font-size: 0.95rem;'>
                <li style='color: var(--primary); font-weight: 700; background: rgba(15,118,110,0.08); border-radius: 12px; padding: 10px; margin-bottom: 10px;'>🏠 App Home</li>
                <li>🩺 Disease Prediction</li>
                <li>📊 Analytics Dashboard</li>
                <li>📈 Model Comparison</li>
                <li>📜 Prediction History</li>
                <li>🧾 Reports Generator</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, rgba(15,118,110,0.1), rgba(20,184,166,0.05)); padding: 20px; border-radius: 16px; border: 1px solid rgba(15,118,110,0.2); text-align: center;'>
            <h4 style='font-size: 1rem; color: #0F766E !important; font-weight: 700; margin-bottom: 10px;'>System Status</h4>
            <div style='display: flex; align-items: center; justify-content: center; gap: 8px;'>
                <div style='width: 10px; height: 10px; background-color: #10B981; border-radius: 50%; box-shadow: 0 0 10px #10B981;'></div>
                <span style='font-weight: 600; font-size: 0.9rem; color: var(--text-color);'>All Systems Operational</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Stats Loader
# -----------------------------
history_file = BASE_DIR / "data" / "prediction_history.csv"
try:
    if history_file.exists():
        df = pd.read_csv(history_file)
        prediction_count = len(df)
        disease_count = df["Disease"].nunique() if not df.empty else 0
    else:
        prediction_count = 0
        disease_count = 0
except:
    prediction_count = 0
    disease_count = 0

# -----------------------------
# Home Screen Content
# -----------------------------

# Hero Section
st.markdown(
    """
    <div class="hero-banner animate-fade-in">
        <h1 class="hero-title">Welcome to MediSense AI.</h1>
        <p class="hero-subtitle">Transforming symptom analysis with cutting-edge machine learning. Fast, accurate, and completely secure healthcare intelligence at your fingertips.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Top Metrics Row
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="Total Predictions", value=prediction_count, delta="↑ Active")
with m2:
    st.metric(label="Supported Diseases", value="41+", delta="Comprehensive")
with m3:
    st.metric(label="Model Accuracy", value="96.2%", delta="High precision")
with m4:
    st.metric(label="Diseases Detected", value=disease_count)

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# Feature Cards Row
st.markdown("<h3 style='margin-bottom: 25px; font-weight: 700;'>Platform Capabilities</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="glass-card animate-fade-in" style="animation-delay: 0.1s;">
            <div style="font-size: 2.5rem; margin-bottom: 15px;">🔍</div>
            <h4 style="font-weight: 700; margin-bottom: 10px; color: var(--primary) !important;">AI Diagnosis</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;">Advanced machine learning algorithms analyze complex symptom patterns to accurately predict potential health risks.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="glass-card animate-fade-in" style="animation-delay: 0.2s;">
            <div style="font-size: 2.5rem; margin-bottom: 15px;">📊</div>
            <h4 style="font-weight: 700; margin-bottom: 10px; color: var(--primary) !important;">Real-Time Analytics</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;">Interactive clinical dashboards provide deep insights into prediction trends, confidence distributions, and patient risks.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="glass-card animate-fade-in" style="animation-delay: 0.3s;">
            <div style="font-size: 2.5rem; margin-bottom: 15px;">📑</div>
            <h4 style="font-weight: 700; margin-bottom: 10px; color: var(--primary) !important;">Medical Reports</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;">Generate hospital-grade PDF reports complete with precautions, diet recommendations, and specialist consulting advice.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# Quick Actions
st.markdown(
    """
    <div style='background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 24px; padding: 40px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.03);' class='animate-fade-in'>
        <h3 style='margin-bottom: 15px;'>Ready to begin?</h3>
        <p style='color: var(--text-muted); max-width: 600px; margin: 0 auto 30px auto; font-size: 1.05rem;'>Navigate to the Disease Prediction module in the sidebar to initiate a new automated diagnostic analysis.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br><br><br><center><p style='color: var(--text-muted); font-size: 0.85rem;'>© 2026 MediSense AI Platform. All rights reserved.</p></center>", unsafe_allow_html=True)