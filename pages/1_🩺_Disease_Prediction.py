import streamlit as st
import pandas as pd
import time
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

from utils.predictor import predict_disease
from utils.disease_info import DISEASE_INFO
from utils.history_manager import save_prediction
from utils.risk_assessment import calculate_risk
from styles.theme import get_theme_css

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Diagnosis Wizard | MediSense AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# -----------------------------
# UI Component Helpers
# -----------------------------
def render_hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero-banner animate-fade-in" style="text-align: center; margin-bottom: 40px;">
            <h1 class="hero-title">{title}</h1>
            <p class="hero-subtitle" style="margin: 0 auto;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Data Loading
# -----------------------------
@st.cache_data
def load_symptoms():
    csv_path = BASE_DIR / "data" / "raw" / "Training.csv"
    try:
        train_df = pd.read_csv(csv_path)
        train_df = train_df.loc[:, ~train_df.columns.str.contains("^Unnamed")]
        return list(train_df.columns[:-1])
    except Exception:
        raise FileNotFoundError(f"Training database not found at matches expected path: {csv_path}")

try:
    all_symptoms = load_symptoms()
except Exception as e:
    st.error(f"Initialization Error: {str(e)}")
    st.stop()

# Initialize state
if "result" not in st.session_state:
    st.session_state.result = None

# Render Header Title Page
render_hero(
    "AI Diagnosis Wizard",
    "Select your symptoms below, and our advanced machine learning core will analyze them to predict potential health conditions instantly."
)

# -----------------------------
# Step 1 & 2: Search and Select symptoms
# -----------------------------
st.markdown("<h3 style='margin-bottom: 20px; font-weight: 700;'>Step 1: Symptom Input</h3>", unsafe_allow_html=True)

col_input, col_info = st.columns([2, 1])

with col_input:
    selected_symptoms = st.multiselect(
        "Select all symptoms you are experiencing:",
        options=all_symptoms,
        format_func=lambda x: x.replace("_", " ").title(),
        placeholder="Search symptoms (e.g. fever, headache, nausea...)"
    )
    
with col_info:
    count_color = "#2563EB" if selected_symptoms else "var(--text-muted)"
    st.markdown(
        f"""
        <div class="glass-card" style="padding: 20px; text-align: center;">
            <p style="margin: 0; font-size: 0.85rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">Tracker</p>
            <div style="font-size: 2.2rem; font-weight: 800; color: {count_color}; margin: 5px 0;">{len(selected_symptoms)}</div>
            <p style="margin: 0; font-size: 0.9rem; color: var(--text-muted);">Symptoms selected</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

# Analysis Action Trigger
do_analyze = st.button("🚀 Run AI Diagnostic Analysis", type="primary", use_container_width=True)

if do_analyze:
    if not selected_symptoms:
        st.error("⚠️ Please select at least one symptom to run the analysis.")
    else:
        # Step 3: Animation State Setup
        st.session_state.result = None
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        stages = [
            (20, "Initializing Machine Learning Core..."),
            (40, "Mapping symptom features to latent space..."),
            (60, "Evaluating deep confidence matrices..."),
            (80, "Aligning differential predictions..."),
            (100, "Diagnostic prediction ready!")
        ]
        
        current_val = 0
        for target_val, text in stages:
            status_text.markdown(f"**🔄 {text}**")
            for i in range(current_val, target_val + 1):
                progress_bar.progress(i)
                time.sleep(0.01)
            current_val = target_val
            time.sleep(0.15)
            
        time.sleep(0.2)
        status_text.empty()
        progress_bar.empty()
        
        # ML Inference Process
        with st.spinner("Compiling results..."):
            try:
                pred_result = predict_disease(selected_symptoms, all_symptoms)
                disease = pred_result["disease"]
                confidence = pred_result["confidence"]
                top_predictions = pred_result["top_predictions"]
                
                risk = calculate_risk(confidence, len(selected_symptoms))
                info = DISEASE_INFO.get(disease, {})
                
                # Wrapped save trigger
                try:
                    save_prediction(
                        disease=disease,
                        symptoms=selected_symptoms,
                        confidence=confidence,
                        risk=risk["level"],
                        top_predictions=top_predictions
                    )
                except Exception:
                    st.warning("⚠️ Prediction completed, but directory logs could not be stored in prediction history CSV.")
                
                # Update Session State dict
                st.session_state.result = {
                    "disease": disease,
                    "confidence": confidence,
                    "risk": risk,
                    "top_predictions": top_predictions,
                    "info": info
                }
                
            except Exception as e:
                st.error(f"Inference pipeline execution failed: {str(e)}")

# -----------------------------
# Results Section Rendering
# -----------------------------
if st.session_state.result is not None:
    res = st.session_state.result
    disease = res["disease"]
    confidence = res["confidence"]
    risk = res["risk"]
    top_predictions = res["top_predictions"]
    info = res["info"]
    
    st.markdown("<hr style='border-color: var(--border-color); margin: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 40px; font-weight: 800;'>Diagnostic Analysis Results</h2>", unsafe_allow_html=True)
    
    # Theme configuration colors for charts
    theme_mode = st.session_state.theme
    text_color = "#F8FAFC" if theme_mode == "dark" else "#0F172A"
    
    res_col1, res_col2, res_col3 = st.columns([1.5, 1, 1])
    
    # Step 4: Diagnosis Card
    with res_col1:
        st.markdown(
            f"""
            <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center; padding: 35px;">
                <p style="text-transform: uppercase; font-size: 0.85rem; font-weight: 700; color: var(--text-muted); letter-spacing: 0.1em; margin-bottom: 8px;">Primary AI Prediction</p>
                <h2 style="font-size: 2.2rem; font-weight: 800; color: #2563EB; margin: 0 0 15px 0;">🩺 {disease}</h2>
                <div style="background: rgba(37,99,235,0.08); padding: 12px 18px; border-radius: 12px; display: inline-block; border: 1px solid rgba(37,99,235,0.15);">
                    <span style="font-weight: 700; color: #2563EB;">Diagnostic Confidence: {confidence}%</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Step 5: Confidence Gauge
    with res_col2:
        fig_conf = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = confidence,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence Level", 'font': {'size': 18, 'color': text_color, 'family': 'Outfit'}},
            number = {'suffix': "%", 'font': {'color': text_color, 'family': 'Outfit', 'size': 32}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': text_color},
                'bar': {'color': "#2563EB", 'thickness': 0.25},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 1,
                'bordercolor': text_color,
                'steps': [
                    {'range': [0, 50], 'color': "rgba(220, 38, 38, 0.1)"},
                    {'range': [50, 80], 'color': "rgba(245, 158, 11, 0.1)"},
                    {'range': [80, 100], 'color': "rgba(16, 185, 129, 0.1)"}
                ],
            }
        ))
        fig_conf.update_layout(height=250, margin=dict(l=30, r=30, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': text_color})
        st.plotly_chart(fig_conf, use_container_width=True, config={'displayModeBar': False})
        
    # Step 6: Risk Meter
    with res_col3:
        risk_map = {"Low": 20, "Medium": 45, "High": 75, "Severe": 95}
        r_val = risk_map.get(risk['level'], 50)
        color = "#10B981" if r_val < 40 else "#F59E0B" if r_val < 70 else "#EF4444"
        
        fig_risk = go.Figure(go.Indicator(
            mode = "gauge",
            value = r_val,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Risk Severity: {risk['level']}", 'font': {'size': 18, 'color': color, 'family': 'Outfit'}},
            gauge = {
                'axis': {'range': [None, 100], 'visible': False},
                'bar': {'color': color, 'thickness': 0.3},
                'bgcolor': "rgba(0,0,0,0.05)",
                'borderwidth': 0,
            }
        ))
        fig_risk.update_layout(height=250, margin=dict(l=30, r=30, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': text_color})
        st.plotly_chart(fig_risk, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    # Step 7: Top 3 Diseases & Step 8/9 Details
    det_col1, det_col2 = st.columns([1, 1.5])
    
    with det_col1:
        st.markdown("<h4 style='font-weight: 700; margin-bottom: 20px;'>Differential Diagnosis</h4>", unsafe_allow_html=True)
        chart_data = pd.DataFrame(top_predictions).rename(columns={"disease": "Condition", "probability": "Probability (%)"})
        
        fig_bar = px.bar(chart_data, x="Probability (%)", y="Condition", orientation='h', text="Probability (%)", color="Probability (%)", color_continuous_scale="Blues")
        fig_bar.update_layout(height=300, yaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        
    with det_col2:
        st.markdown(f"<h4 style='font-weight: 700; margin-bottom: 20px;'>About Predicted Condition</h4>", unsafe_allow_html=True)
        if info:
            tab1, tab2, tab3, tab4 = st.tabs(["📖 Description", "🛡 Precautions", "🥗 Diet", "👨‍⚕️ Doctor Advice"])
            
            with tab1:
                st.markdown(f"<div class='glass-card' style='padding: 20px;'><p>{info.get('description', 'Information not available.')}</p></div>", unsafe_allow_html=True)
            with tab2:
                items = "".join([f"<li>{x}</li>" for x in info.get("precautions", [])])
                st.markdown(f"<div class='glass-card' style='padding: 20px;'><ul>{items}</ul></div>", unsafe_allow_html=True)
            with tab3:
                items = "".join([f"<li>{x}</li>" for x in info.get("diet", [])])
                st.markdown(f"<div class='glass-card' style='padding: 20px;'><ul>{items}</ul></div>", unsafe_allow_html=True)
            with tab4:
                st.markdown(f"""
                <div class='glass-card' style='padding: 20px; border-left: 4px solid #F59E0B;'>
                    <p style='font-weight: 600; color: #F59E0B; margin-bottom: 10px;'>Professional Recommendation</p>
                    <p>{info.get("doctor", "Consult a registered doctor for clinical diagnosis.")}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No detailed clinical information available in the database for this specific condition.")
            
    # Step 10: Next Steps Shortcut
    st.markdown("<hr style='border-color: var(--border-color); margin: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-weight: 700; margin-bottom: 20px;'>Next Available Workflow Actions</h4>", unsafe_allow_html=True)
    c_pdf, c_spacer = st.columns([1.5, 1])
    with c_pdf:
        if st.button("📄 Generate formal Hospital-Grade PDF Report for this case", type="primary", use_container_width=True):
            st.switch_page("pages/5_📄_Generate_Report.py")
else:
    # Empty/Initial Page State Encouraging input
    st.markdown(
        """
        <div style='text-align: center; padding: 60px 40px; border: 2px dashed var(--border-color); border-radius: 24px; background: rgba(0,0,0,0.01);' class='animate-fade-in'>
            <div style='font-size: 3.5rem; margin-bottom: 15px;'>🩺</div>
            <h4 style='font-weight: 700; color: var(--text-color); margin-bottom: 10px;'>No Diagnostic Data Rendered</h4>
            <p style='color: var(--text-muted); max-width: 450px; margin: 0 auto 20px auto; font-size: 0.95rem;'>Please search for and select your clinical symptoms in the input interface above, then click 'Run AI Diagnostic Analysis' to see AI findings.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Legal Disclaimer Section
# -----------------------------
with st.expander("⚠️ Medical Disclaimer and Clinical Terms", expanded=False):
    st.warning(
        "This automated AI diagnostic analysis prediction is intended for educational, portfolio demonstration, and research purposes only. "
        "It DOES NOT constitute formal medical advice, medical diagnosis, or patient care guidelines. "
        "Always consult a registered clinical healthcare provider or medical specialist to discuss symptoms, prescriptions, or treatments."
    )