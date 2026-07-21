import streamlit as st
from styles.theme import get_theme_css

st.set_page_config(
    page_title="About | MediSense AI",
    page_icon="ℹ️",
    layout="wide"
)

# Theme
if "theme" not in st.session_state: st.session_state.theme = "light"
with open("styles/custom.css") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)


st.markdown(
    """
    <div class='hero-banner' style='text-align: center;'>
        <h1 style='color: white !important; font-size: 3rem;'>About MediSense AI System</h1>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.1rem; max-width: 600px; margin: 0 auto;'>A cutting-edge thesis platform merging machine learning with clinical diagnostics to provide accessible healthcare intelligence.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 Platform Details", "🏗️ Architecture", "👨‍💻 Developer"])

with tab1:
    st.markdown("<h3 style='margin-bottom: 20px;'>Project Ecosystem</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(
            """
            <div class='glass-card'>
                <h4 style='color: #2563EB;'>Core Mission</h4>
                <p style='color: var(--text-muted); font-size: 0.95rem;'>To demystify symptom analysis and provide a rapid, AI-driven first line of diagnostic insight for individuals and clinicians alike.</p>
            </div>
            """, unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            """
            <div class='glass-card'>
                <h4 style='color: #10B981;'>Clinical Value</h4>
                <p style='color: var(--text-muted); font-size: 0.95rem;'>Reduced preliminary assessment times, extensive database spanning 41 conditions, and hospital-grade PDF export capabilities.</p>
            </div>
            """, unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            """
            <div class='glass-card'>
                <h4 style='color: #F59E0B;'>Future Scope</h4>
                <p style='color: var(--text-muted); font-size: 0.95rem;'>Integration with IoT wearables, deep neural networks for medical imaging, and cloud-native scalable deployment.</p>
            </div>
            """, unsafe_allow_html=True
        )

with tab2:
    st.markdown("<h3 style='margin-bottom: 20px;'>System Architecture</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='glass-card' style='text-align: center; padding: 40px;'>
            <code style='font-size: 1.1rem; color: #2563EB; background: rgba(37,99,235,0.1); padding: 20px; border-radius: 12px; display: inline-block; text-align: left; line-height: 2;'>
                [Patient Input] ➔ [Streamlit State UI] ➔ [Symptom Vectorization]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                [Healthcare Dashboards] ⬅ [ReportLab AI PDF] ⬅ [Scikit-Learn Random Forest]<br>
            </code>
        </div>
        """, unsafe_allow_html=True
    )

with tab3:
    st.markdown("<h3 style='margin-bottom: 20px;'>Developer Profile</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='glass-card' style='max-width: 600px;'>
            <h4>Senior Tech Architect</h4>
            <p style='color: var(--text-muted);'>This platform was engineered as an advanced demonstration of modern web application development, machine learning pipeline integration, and premium UX/UI design within the healthcare domain.</p>
            <hr style='border: none; border-top: 1px solid var(--border-color); margin: 20px 0;'>
            <p style='margin: 0;'><strong>Stack:</strong> Python, Streamlit, Pandas, Scikit-Learn, Plotly, ReportLab, Vanilla Custom CSS.</p>
        </div>
        """, unsafe_allow_html=True
    )