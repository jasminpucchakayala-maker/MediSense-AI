def get_theme_css(theme="light"):
    if theme == "dark":
        # Dark Theme Palette (Teal + Emerald)
        bg_color = "#0F172A"
        sidebar_bg = "#111827"
        card_bg = "#1E293B"
        border_color = "#334155"
        text_color = "#F8FAFC"
        text_muted = "#CBD5E1"
        input_bg = "#1E293B"
        hero_start = "#115E59"
        hero_end = "#0F766E"
        metric_value = "#5EEAD4"
    else:
        # Light Theme Palette (Teal + Emerald)
        bg_color = "#F8FAFC"
        sidebar_bg = "#F1F5F9"
        card_bg = "#FFFFFF"
        border_color = "#E5E7EB"
        text_color = "#111827"
        text_muted = "#4B5563"
        input_bg = "#FFFFFF"
        hero_start = "#0F766E"
        hero_end = "#14B8A6"
        metric_value = "#0F766E"

    return f"""
    <style>
    :root {{
        --background: {bg_color};
        --sidebar-bg: {sidebar_bg};
        --card-bg: {card_bg};
        --border-color: {border_color};
        --text-color: {text_color};
        --text-muted: {text_muted};
        --input-bg: {input_bg};
        --hero-start: {hero_start};
        --hero-end: {hero_end};
        --metric-value: {metric_value};
    }}

    /* Apply background globally */
    .stApp {{
        background-color: var(--background) !important;
        color: var(--text-color) !important;
    }}
    
    h1, h2, h3, h4, h5, h6, p, span, div, label {{
        color: var(--text-color) !important;
    }}
    
    .stMarkdown p {{
        color: var(--text-muted) !important;
    }}
    
    /* Ensure the metric cards use proper contrast variables */
    [data-testid="stMetricValue"] {{
        color: var(--metric-value) !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: var(--text-muted) !important;
    }}
    </style>
    """