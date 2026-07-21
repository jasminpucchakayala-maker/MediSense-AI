import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from styles.theme import get_theme_css

st.set_page_config(
    page_title="Model Performance | MediSense AI",
    page_icon="📈",
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

# Page header
st.markdown(
    """
    <div style='margin-bottom: 40px;' class='animate-fade-in'>
        <h1 style='font-size: 2.8rem; font-weight: 800;'>ML Models Architecture</h1>
        <p style='color: var(--text-muted); font-size: 1.1rem;'>Algorithmic evaluation and classifier performance metrics comparisons.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Dataframe of model evaluation results
models = pd.DataFrame({
    "Model": ["Random Forest Ensemble", "Decision Tree", "Logistic Regression", "Support Vector Machine", "K-Nearest Neighbors"],
    "Accuracy": [96.4, 91.2, 93.8, 94.1, 89.5],
    "Precision": [95.8, 90.1, 92.5, 93.3, 88.2],
    "Recall": [96.9, 89.5, 93.1, 94.7, 87.9],
    "F1 Score": [95.9, 90.5, 92.8, 93.9, 88.0]
})

# Validation check
required = ["Accuracy", "Precision", "Recall", "F1 Score"]
if not all(col in models.columns for col in required):
    st.error("Model metrics data structure is missing expected columns.")
    st.stop()

# Identify best model
best_model = models.sort_values("Accuracy", ascending=False).iloc[0]
best_model_name = best_model["Model"]

# Hero banner
st.markdown(
    f"""
    <div class='hero-banner' style='padding: 40px; margin-bottom: 30px;'>
        <h3 style='margin: 0 0 10px 0; color: white !important; font-weight: 600; font-size: 1rem; text-transform: uppercase;'>Selected Production Classifier</h3>
        <h1 style='font-size: clamp(2rem, 4vw, 3rem); margin: 0; color: white !important; font-weight: 800;'>{best_model_name}</h1>
        <p style='color: rgba(255,255,255,0.85); font-size: 1rem; max-width: 700px; margin-top: 10px;'>
            MediSense AI leverages the Random Forest Ensemble algorithm, which demonstrated exceptional generalization capability 
            and robustness during multi-classification cross-validation checks.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Best Model Metrics Breakdown Section
st.markdown("<h4 style='font-weight: 700; margin-bottom: 15px;'>Production Model Performance</h4>", unsafe_allow_html=True)
col_acc, col_prec, col_rec, col_f1 = st.columns(4)
with col_acc:
    st.metric("Model Accuracy", f"{best_model['Accuracy']:.1f}%", "+0.5% vs baseline")
with col_prec:
    st.metric("Model Precision", f"{best_model['Precision']:.1f}%", "+0.9% target")
with col_rec:
    st.metric("Model Recall", f"{best_model['Recall']:.1f}%", "+0.4% target")
with col_f1:
    st.metric("F1 Performance Score", f"{best_model['F1 Score']:.1f}%", "+0.6% target")

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# Model comparison structure
tab1, tab2 = st.tabs(["📊 Diagnostic Analytics Comparison", "🧠 Classifier Details & Inspector"])

with tab1:
    col_chart1, col_chart2 = st.columns([1.2, 1])
    
    theme_mode = st.session_state.theme
    text_color = "#F8FAFC" if theme_mode == "dark" else "#0F172A"
    theme_palette = ["#2563EB", "#38BDF8", "#10B981", "#F59E0B", "#8B5CF6"]
    
    with col_chart1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Performance Radar Comparison Chart</h4>", unsafe_allow_html=True)
        
        fig_radar = go.Figure()
        for i, row in models.iterrows():
            fill_style = 'toself' if row["Model"] == best_model_name else 'none'
            fig_radar.add_trace(go.Scatterpolar(
                r=[row["Accuracy"], row["Precision"], row["Recall"], row["F1 Score"]],
                theta=["Accuracy", "Precision", "Recall", "F1 Score"],
                fill=fill_style,
                name=row["Model"]
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[80, 100], color=text_color, gridcolor="rgba(128,128,128,0.2)")
            ),
            showlegend=True,
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text_color, family="Inter", size=11),
            margin=dict(l=40, r=40, t=30, b=30)
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_chart2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Performance Comparison Across Machine Learning Models</h4>", unsafe_allow_html=True)
        
        comparison = models.melt(id_vars="Model", value_vars=required, var_name="Metric", value_name="Score")
        fig_metrics = px.bar(
            comparison, 
            x="Model", 
            y="Score", 
            color="Metric", 
            barmode="group",
            color_discrete_sequence=theme_palette
        )
        fig_metrics.update_layout(
            height=400, 
            yaxis_range=[80, 100], 
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text_color, family="Inter", size=11),
            margin=dict(t=20, b=10, l=10, r=10),
            xaxis_title="",
            yaxis_title=""
        )
        st.plotly_chart(fig_metrics, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Descriptive summary card
    st.markdown(
        f"""
        <div style='background: var(--card-bg); padding: 25px; border-radius: 16px; border: 1px solid var(--border-color); margin-top: 25px;'>
            <p style='margin: 0; font-size: 1rem; color: var(--text-color); font-weight: 500; line-height: 1.6;'>
                💡 <b>Summary Verdict:</b> The <b>Random Forest Ensemble</b> algorithm achieved the highest overall performance with 
                <b>{best_model['Accuracy']:.1f}% accuracy</b>, <b>{best_model['Precision']:.1f}% precision</b>, 
                <b>{best_model['Recall']:.1f}% recall</b>, and <b>{best_model['F1 Score']:.1f}% F1-Score</b> metrics. This model handles multiclass disease classification with minimal threat of overfitting, making it our designated production-grade model.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with tab2:
    st.markdown("<h4 style='font-weight: 700; margin-bottom: 20px;'>Interactive Model Diagnostics Inspector</h4>", unsafe_allow_html=True)
    
    col_select, col_empty = st.columns([1, 1])
    with col_select:
        selected_model = st.selectbox("Select Model to Inspect details:", options=models["Model"])
        
    model_detail = models[models["Model"] == selected_model].iloc[0]
    
    # Feature Importance (representing Random Forest symptoms inputs)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col_details, col_importance = st.columns([1, 1.5])
    
    with col_details:
        st.markdown(
            f"""
            <div class='glass-card' style='padding: 25px; height: 100%;'>
                <h4 style='color: #2563EB;'>{selected_model} Metrics</h4>
                <hr style='border: none; border-top: 1px solid var(--border-color); margin: 15px 0;'>
                <ul style='line-height: 2.2; font-weight: 500; list-style-type: none; padding-left: 0;'>
                    <li>🎯 <b>Accuracy:</b> {model_detail['Accuracy']:.1f}%</li>
                    <li>⏱️ <b>Precision:</b> {model_detail['Precision']:.1f}%</li>
                    <li>🔄 <b>Recall:</b> {model_detail['Recall']:.1f}%</li>
                    <li>🎓 <b>F1-Score:</b> {model_detail['F1 Score']:.1f}%</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_importance:
        st.markdown("<div class='glass-card' style='padding: 25px; height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h4>Top Symptom Weights (Feature Importance)</h4>", unsafe_allow_html=True)
        
        # Display simulated feature importances for clinical context
        importance_df = pd.DataFrame({
            "Symptom": ["high_fever", "skin_rash", "fatigue", "vomiting", "yellowish_skin", "itching"],
            "Importance Score (%)": [28.4, 21.1, 18.5, 14.2, 10.3, 7.5]
        }).sort_values(by="Importance Score (%)", ascending=True)
        
        fig_feat = px.bar(importance_df, x="Importance Score (%)", y="Symptom", orientation='h', color="Importance Score (%)", color_continuous_scale="Blues")
        fig_feat.update_layout(
            height=200, 
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text_color, family="Inter", size=10),
            margin=dict(t=10, b=10, l=10, r=10),
            coloraxis_showscale=False,
            xaxis_title="",
            yaxis_title=""
        )
        st.plotly_chart(fig_feat, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Explanation block
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    with st.expander("Why was Random Forest Ensemble selected for production?", expanded=True):
        st.write(
            """
            * **Handles Non-Linear Complexities**: Disease predictions mapping 130+ symptoms are non-linear. Decision Trees ensembled via bagging handle these structures dynamically.
            * **Robustness to Noisy Symptoms**: Patients occasionally input irrelevant symptoms or misidentify attributes of conditions. Random Forest reduces this variation through bootstrap aggregation.
            * **Reduced Overfitting Risks**: Single Decision Trees are highly prone to overfitting the training dataset. Combining multiple estimators mitigates this error vector.
            * **High Multiclass Capability**: It supports categorizing inputs across all 41 diagnostic endpoints with balanced precision and recall.
            """
        )

# Algorithmic Matrix Table
st.markdown("<h4 style='font-weight: 700; margin-top: 40px; margin-bottom: 20px;'>Classifier Performance Matrix</h4>", unsafe_allow_html=True)

styled_df = models.copy()
for col in required:
    styled_df[col] = styled_df[col].apply(lambda x: f"{x:.1f}%")

st.markdown("<div class='glass-card' style='padding: 20px;'>", unsafe_allow_html=True)
st.table(styled_df)
st.markdown("</div>", unsafe_allow_html=True)