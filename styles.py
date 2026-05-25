def apply_styles():
    import streamlit as st
    import base64

    # Load background
    with open("bg.jpg", "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    /* ================= HIDE STREAMLIT UI ================= */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}

    /* ================= BACKGROUND ================= */
    .stApp {{
        background: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* ================= CENTER CONTAINER ================= */
    .block-container {{
        padding-top: 4rem !important;
        display: flex !important;
        justify-content: center !important;
    }}

    [data-testid="stVerticalBlock"] {{
        margin: auto !important;
        width: 100% !important;
        max-width: 850px !important;
        text-align: center;
    }}

    /* ================= SHINING NEON TITLE ================= */
    .main-title-text {{
        font-size: 20px !important; 
        font-weight: 800 !important;
        color: #1A365D !important; /* Deep Navy Text */
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 40px !important;
        text-align: center;
        /* THE SHINE: Lighter cyan glow behind dark text */
        text-shadow: 0 0 10px #00E5FF, 0 0 20px rgba(0, 229, 255, 0.4);
    }}

    /* ================= SUBHEADINGS ================= */
    h1, h2, h3, .stTitle {{
        color: #1A365D !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        text-shadow: 0 0 8px rgba(0, 229, 255, 0.3);
    }}

    /* ================= LABELS ================= */
    [data-testid="stWidgetLabel"] p, 
    .stMarkdown p, 
    label, 
    [data-testid="stRadio"] label p {{
        color: #1A365D !important;
        font-weight: 700 !important;
        font-size: 20px !important;
    }}

    /* ================= SHINING INPUT FIELDS ================= */
    div[data-baseweb="input"], 
    div[data-baseweb="input"] > div {{
        background-color: transparent !important;
    }}

    div[data-baseweb="input"] input {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #1A365D !important;
        border: 2px solid #00E5FF !important; /* Bright border */
        border-radius: 10px !important;
        /* Outer shining glow */
        box-shadow: 0 0 8px rgba(0, 229, 255, 0.2);
    }}

    div[data-baseweb="input"] input:focus {{
        border: 2px solid #00E5FF !important;
        box-shadow: 0 0 15px #00E5FF !important;
        outline: none !important;
    }}

    /* ================= SHINING BUTTON ================= */
    .stButton>button {{
        background-color: #1A365D ;
        color: #00E5FF ; /* Cyan text on Navy button */
        border: 1px solid #00E5FF ;
        border-radius: 10px ;
        font-weight: 700 ;
        width: 100px ;
        transition: all 0.3s ease;
        /* Shining shadow */
        box-shadow: 0 0 12px rgba(0, 229, 255, 0.4);
    }}

    .stButton>button:hover {{
        background-color: #00E5FF ;
        color: #1A365D ;
        box-shadow: 0 0 25px #00E5FF ;
        transform: translateY(-2px);
    }}

    /* Radio buttons */
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {{
        border-color: #00E5FF !important;
        box-shadow: 0 0 5px #00E5FF;
    }}
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child > div {{
        background-color: #00E5FF !important;
    }}

    </style>

    <div class="main-title-text">
        AI-Based Brain Tumor Detection and Classification System
    </div>
    """, unsafe_allow_html=True)