import streamlit as st
import pandas as pd
import os
from styles.theme import get_theme_css

st.set_page_config(
    page_title="EMR Prediction History | MediSense AI",
    page_icon="📜",
    layout="wide"
)

# Load theme
if "theme" not in st.session_state:
    st.session_state.theme = "light"
with open("styles/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

st.markdown(
    """
    <div style='margin-bottom: 40px;' class='animate-fade-in'>
        <h1 style='font-size: 2.8rem; font-weight: 800;'>Electronic Medical Records</h1>
        <p style='color: var(--text-muted); font-size: 1.1rem;'>Secure clinical history of all AI-driven diagnostic prediction events.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

history_file = "data/prediction_history.csv"

def get_badge(val, type="risk"):
    if type == "risk":
        return f"🟢 {val}" if val == "Low" else f"🟡 {val}" if val == "Medium" else f"🔴 {val}"
    elif type == "conf":
        return f"✨ {val}%"

# Load history
if os.path.exists(history_file):
    df = pd.read_csv(history_file)
    
    # Ensure missing columns exist for older records
    if "Confidence" not in df.columns:
        df["Confidence"] = 85.0
    else:
        df["Confidence"] = df["Confidence"].fillna(85.0)

    if "Risk Level" not in df.columns:
        df["Risk Level"] = "Medium"
    else:
        df["Risk Level"] = df["Risk Level"].fillna("Medium")
        
    if "Time" not in df.columns:
        df["Time"] = "12:00 PM"
    else:
        df["Time"] = df["Time"].fillna("12:00 PM")
else:
    df = pd.DataFrame(columns=["Date", "Time", "Disease", "Symptoms", "Confidence", "Risk Level"])

if df.empty:
    st.info("No clinical prediction history available in the system.")
    st.stop()

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

# Top EMR Summary
st.markdown("<h4 style='font-weight: 700;'>Database Overview</h4>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='glass-card'><h4>Total Records</h4><h2 style='color:#2563EB;'>{len(df)}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='glass-card'><h4>Unique Diagnoses</h4><h2 style='color:#10B981;'>{df['Disease'].nunique()}</h2></div>", unsafe_allow_html=True)
with col3:
    latest = df.iloc[-1]['Disease'] if not df.empty else "N/A"
    st.markdown(f"<div class='glass-card'><h4>Latest Finding</h4><h2 style='color:#F59E0B;'>{latest}</h2></div>", unsafe_allow_html=True)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# Advanced Search & Filter Layer
st.markdown("<div style='background: var(--card-bg); padding: 20px; border-radius: 16px; border: 1px solid var(--border-color);'>", unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns([2, 1.5, 1.5, 1])
with f1:
    search_term = st.text_input("🔍 Global Search (Symptoms, Disease)", placeholder="e.g. fever or Malaria")
with f2:
    dis_filter = st.selectbox("Disease Filter", ["All"] + sorted(list(df["Disease"].unique())))
with f3:
    risk_filter = st.selectbox("Risk Badge Filter", ["All", "Low", "Medium", "High", "Severe"])
with f4:
    sort_ord = st.selectbox("Sort By", ["Newest First", "Oldest First", "Highest Confidence"])
st.markdown("</div>", unsafe_allow_html=True)

# Apply filters
filtered_df = df.copy()

if search_term:
    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
    filtered_df = filtered_df[mask]

if dis_filter != "All":
    filtered_df = filtered_df[filtered_df["Disease"] == dis_filter]

if risk_filter != "All":
    filtered_df = filtered_df[filtered_df["Risk Level"] == risk_filter]

if sort_ord == "Newest First": filtered_df = filtered_df.sort_values(by="Date", ascending=False)
elif sort_ord == "Oldest First": filtered_df = filtered_df.sort_values(by="Date", ascending=True)
elif sort_ord == "Highest Confidence": filtered_df = filtered_df.sort_values(by="Confidence", ascending=False)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Fancy Table Presentation
display_df = filtered_df.copy()
display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
if "Risk Level" in display_df.columns:
    display_df["Risk Level"] = display_df["Risk Level"].apply(lambda x: get_badge(x, "risk"))
if "Confidence" in display_df.columns:
    display_df["Confidence"] = display_df["Confidence"].apply(lambda x: get_badge(x, "conf"))

# Rename for clean output
display_df = display_df.rename(columns={"Risk Level": "Risk Badge", "Confidence": "Confidence Score"})

st.markdown("<h4 style='font-weight: 700;'>Medical History Ledger</h4>", unsafe_allow_html=True)
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=400
)

# Export
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
csv_data = filtered_df.to_csv(index=False)
st.download_button(
    label="💾 Export Clinical Data (CSV)",
    data=csv_data,
    file_name="medisense_emr_export.csv",
    mime="text/csv",
    type="secondary"
)