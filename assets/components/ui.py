import streamlit as st


# ===========================================
# Page Header
# ===========================================
def page_header(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="card">
            <div class="title">{title}</div>
            <div class="subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================
# Hero Section
# ===========================================
def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero">
            <h1 style="
                color:white;
                font-size:48px;
                font-weight:800;
                margin-bottom:10px;
            ">
                {title}
            </h1>

            <p style="
                color:white;
                font-size:18px;
                line-height:1.8;
                opacity:.95;
            ">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================
# Metric Card
# ===========================================
def metric_card(title: str, value: str, icon: str = "📊"):
    st.markdown(
        f"""
        <div class="metric">
            <div style="font-size:38px;">{icon}</div>

            <h2 style="
                margin-top:10px;
                color:#2563EB;
                font-weight:700;
            ">
                {value}
            </h2>

            <p style="
                color:#64748B;
                margin-top:5px;
            ">
                {title}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================
# Feature Card
# ===========================================
def feature_card(icon: str, title: str, description: str):
    st.markdown(
        f"""
        <div class="feature">

            <div style="
                font-size:45px;
                margin-bottom:15px;
            ">
                {icon}
            </div>

            <h3 style="
                color:#0F172A;
                font-weight:700;
            ">
                {title}
            </h3>

            <p style="
                color:#64748B;
                line-height:1.7;
            ">
                {description}
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================
# Result Card
# ===========================================
def result_card(disease, confidence="High Confidence"):
    st.markdown(
        f"""
        <div class="result">

            <h2 style="
                color:#2563EB;
                font-weight:700;
            ">
                🩺 {disease}
            </h2>

            <hr>

            <h4>Confidence</h4>

            <span style="
                background:#2563EB;
                color:white;
                padding:8px 18px;
                border-radius:20px;
                font-weight:600;
            ">
                {confidence}
            </span>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================
# Information Box
# ===========================================
def info_box(title, text):
    st.markdown(
        f"""
        <div class="card">

        <h3 style="
            color:#2563EB;
            margin-bottom:10px;
        ">
            {title}
        </h3>

        <p style="
            color:#475569;
            line-height:1.8;
        ">
            {text}
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================
# Section Divider
# ===========================================
def section(title):
    st.markdown(
        f"""
        <h2 style="
            margin-top:30px;
            margin-bottom:20px;
            color:#0F172A;
        ">
            {title}
        </h2>
        """,
        unsafe_allow_html=True,
    )


# ===========================================
# Footer
# ===========================================
def footer():
    st.markdown(
        """
        <hr>

        <center>

        <p style="color:#94A3B8">

        🩺 MediSense AI <br>

        AI-Powered Disease Prediction System

        </p>

        </center>
        """,
        unsafe_allow_html=True,
    )