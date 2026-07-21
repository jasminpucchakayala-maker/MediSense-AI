import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from styles.theme import get_theme_css

st.set_page_config(
    page_title="PDF Reports | MediSense AI",
    page_icon="📄",
    layout="wide"
)

# Theme
if "theme" not in st.session_state: st.session_state.theme = "light"
with open("styles/custom.css") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

st.markdown(
    
    """
    <div style='margin-bottom: 40px;' class='animate-fade-in'>
        <h1 style='font-size: 2.8rem; font-weight: 800;'>Medical Report Generator</h1>
        <p style='color: var(--text-muted); font-size: 1.1rem;'>Synthesize professional, hospital-grade PDF diagnostic documentation.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
history_file = os.path.join(BASE_DIR, "data", "prediction_history.csv")

if not os.path.exists(history_file):
   
    st.stop()

df = pd.read_csv(history_file)
if df.empty:
    st.warning("No records available to generate reports.")
    st.stop()

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

# Reorder so latest is first
df = df.iloc[::-1].reset_index(drop=True)

st.markdown("<h4 style='font-weight: 700;'>Select Clinical Record</h4>", unsafe_allow_html=True)
c1, c2 = st.columns([1, 2])
with c1:
    selected_index = st.selectbox(
        "Choose a case study to generate documentation",
        range(len(df)),
        format_func=lambda x: f"{df.iloc[x]['Date']} | {df.iloc[x]['Disease']}"
    )

record = df.iloc[selected_index]

st.markdown("<hr style='border-color: var(--border-color); margin: 30px 0;'>", unsafe_allow_html=True)

st.markdown("<h4 style='font-weight: 700;'>Hospital Report Preview</h4>", unsafe_allow_html=True)

preview_col, action_col = st.columns([2, 1])

with preview_col:
    components.html(
        f"""
        <div style='background: white; color: black; padding: 40px; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 10px solid #2563EB;'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #E5E7EB; padding-bottom: 20px; margin-bottom: 20px;'>
                <div>
                    <h2 style='margin: 0; color: #1E293B;'>MediSense AI Hospital</h2>
                    <p style='margin: 5px 0 0 0; color: #64748B; font-size: 0.9rem;'>Digital automated diagnosis lab</p>
                </div>
                <div style='text-align: right;'>
                    <p style='margin: 0; font-weight: bold;'>CONFIDENTIAL</p>
                    <p style='margin: 0; color: #64748B;'>Date: {record['Date']}</p>
                </div>
            </div>  
            <h3 style='text-align: center; color: #2563EB; margin: 30px 0;'>Automated Patient Diagnostics Report</h3>
           <table style="width:100%; border-collapse:collapse; margin-bottom:30px;">
    <tr>
        <td style="padding:10px; border:1px solid #E5E7EB; background:#F8FAFC; width:30%;"><strong>Primary Finding</strong></td>
        <td style="padding:10px; border:1px solid #E5E7EB; font-size:1.1rem; font-weight:bold; color:black;">
            {record["Disease"]}
        </td>
    </tr>

    <tr>
        <td style="padding:10px; border:1px solid #E5E7EB; background:#F8FAFC; color:black;"><strong>AI Confidence</strong></td>
        <td style="padding:10px; border:1px solid #E5E7EB; color:black;">
            {record.get("Confidence", "N/A")}%
        </td>
    </tr>

    <tr>
        <td style="padding:10px; border:1px solid #E5E7EB; background:#F8FAFC; color:black;"><strong>Risk Level</strong></td>
        <td style="padding:10px; border:1px solid #E5E7EB; color:black;">
            {record.get("Risk Level", "N/A")}
        </td>
    </tr>

    <tr>
        <td style="padding:10px; border:1px solid #E5E7EB; background:#F8FAFC; color:black;"><strong>Reported Symptoms</strong></td>
        <td style="padding:10px; border:1px solid #E5E7EB; color:black;">
            {str(record["Symptoms"]).replace("_", " ").title()}
        </td>
    </tr>
</table>

<p style="margin-bottom:5px; font-weight:bold; color:black;">
    Clinical Notice:
</p>

<p style="color:#64748B; font-size:0.9rem;">
    This report is structurally generated via MediSense AI machine learning
    models. It requires human clinician review for final sign-off.
</p>

</div>
""",
        height=560,
        scrolling=True,
    )
    
    
def generate_pdf():
    pdf_path = os.path.join(BASE_DIR, "MediSense_Clinical_Report.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(name='CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor("#2563EB"), spaceAfter=30, alignment=1)
    header_style = ParagraphStyle(name='Header', parent=styles['Normal'], fontSize=10, textColor=colors.gray)
    sub_head = ParagraphStyle(name='Sub', parent=styles['Heading2'], spaceBefore=20, spaceAfter=10, textColor=colors.HexColor("#1E293B"))
    
    elements = []
    
    # Header
    elements.append(Paragraph("<b>MediSense AI Healthcare Systems</b>", title_style))
    elements.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  <b>Confidentiality:</b> High", header_style))
    elements.append(Spacer(1, 30))
    
    elements.append(Paragraph("Clinical Diagnostic Evaluation", sub_head))
    
    # Data Table
    data = [
        ["Date of Assessment", record['Date']],
        ["Time", record.get('Time', 'N/A')],
        ["Primary AI Diagnosis", record['Disease']],
        ["System Confidence", f"{record.get('Confidence', 'N/A')}%"],
        ["Assessed Risk Level", record.get('Risk Level', 'N/A')]
    ]
    
    t = Table(data, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F8FAFC")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#1E293B")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#E5E7EB"))
    ]))
    elements.append(t)
    
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Patient Symptoms", sub_head))
    symptoms_text = str(record['Symptoms']).replace("_", " ").title()
    elements.append(Paragraph(symptoms_text, styles['Normal']))
    
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("<b>Disclaimer:</b> This document does not constitute a definitive medical diagnosis. Please consult a registered medical practitioner.", styles['Italic']))
    
    doc.build(elements)
    return pdf_path


with action_col:
    st.markdown(
        """
        <div class='glass-card'>
            <h4 style='margin-bottom: 20px;'>Generate PDF</h4>
            <p style='font-size: 0.9rem; color: var(--text-muted); margin-bottom: 20px;'>Click below to compile the official diagnostic document for this case.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("📄 Compile Hospital Report", type="primary", use_container_width=True):
        with st.spinner("Compiling PDF document..."):
            pdf_file = generate_pdf()
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="⬇️ Download Official PDF",
                    data=f,
                    file_name=f"MediSense_Report_{record['Date']}.pdf",
                    mime="application/pdf"
                )
            st.success("Compilation Success! Document ready for download.")